# f:\12_prj_raspi5\code_dispatcher\main.py
"""
Raspberry Pi 5 Code Dispatcher & Task Gateway (FastAPI)
Exposes REST endpoints for pushing code analysis tasks to Redis Queue.
"""

import os
import sys
import subprocess
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
from redis import Redis
from rq import Queue
from rq.job import Job

# Ensure task functions can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tasks import analyze_code_task

QUEUE_NAME = "code_review_queue"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

app = FastAPI(
    title="Pi 5 LLM Code Dispatcher API",
    description="High-performance asynchronous code review and inference queue powered by FastAPI & Redis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
task_queue = Queue(QUEUE_NAME, connection=redis_conn)

HTML_UI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui.html")


class CodeTaskRequest(BaseModel):
    code: Optional[str] = Field(default="", description="Source code snippet or file content to review")
    prompt: Optional[str] = Field(
        default="Perform a thorough code review, identifying potential bugs, security vulnerabilities, edge cases, and performance optimizations.",
        description="Custom instruction or review focus"
    )
    model: Optional[str] = Field(default="qwen2.5-coder:7b", description="Ollama model to use")
    language: Optional[str] = Field(default="python", description="Programming language of the code")
    filename: Optional[str] = Field(default="snippet.py", description="Source filename")
    temperature: Optional[float] = Field(default=0.2, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=1500, ge=50, le=4096, description="Max generated tokens")


@app.get("/", response_class=HTMLResponse, tags=["Web UI"])
def get_web_ui():
    """Serve the sleek Web Chat & Code Review user interface."""
    if os.path.exists(HTML_UI_PATH):
        with open(HTML_UI_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Pi 5 LLM Arena Gateway</h1><p>ui.html not found.</p>"


class TaskEnqueueResponse(BaseModel):
    task_id: str
    status: str
    queue_name: str
    position_in_queue: int
    model: str
    filename: str
    submitted_at: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/health", tags=["Monitoring"])
def get_system_health() -> Dict[str, Any]:
    """Retrieve Pi 5 hardware telemetry and services health."""
    redis_ok = False
    try:
        redis_ok = redis_conn.ping()
    except Exception:
        pass

    ollama_ok = False
    active_models: List[str] = []
    try:
        resp = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            ollama_ok = True
            active_models = [m.get("name") for m in resp.json().get("models", [])]
    except Exception:
        pass

    temp_c = 0.0
    try:
        res = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True, timeout=2)
        temp_c = float(res.stdout.strip().replace("temp=", "").replace("'C", ""))
    except Exception:
        pass

    free_ram_mb = 0
    total_ram_mb = 0
    try:
        res = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=2)
        for line in res.stdout.splitlines():
            if line.startswith("Mem:"):
                parts = line.split()
                total_ram_mb = int(parts[1])
                free_ram_mb = int(parts[6])  # available RAM
    except Exception:
        pass

    return {
        "status": "healthy" if (redis_ok and ollama_ok) else "degraded",
        "redis_connected": redis_ok,
        "ollama_running": ollama_ok,
        "available_models_count": len(active_models),
        "cpu_temperature_c": temp_c,
        "ram_available_mb": free_ram_mb,
        "ram_total_mb": total_ram_mb,
        "queue_length": len(task_queue),
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/api/models", tags=["Models"])
def list_models() -> Dict[str, Any]:
    """List available LLM models in local Ollama instance."""
    try:
        resp = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to query Ollama models: {str(e)}"
        )


@app.post("/api/tasks", response_model=TaskEnqueueResponse, status_code=status.HTTP_202_ACCEPTED, tags=["Tasks"])
def create_task(req: CodeTaskRequest) -> TaskEnqueueResponse:
    """Submit a new code review task to the Redis Queue."""
    task_payload = req.model_dump()
    job = task_queue.enqueue(
        analyze_code_task,
        task_payload,
        job_timeout=600,
        result_ttl=86400  # Keep result in Redis for 24 hours
    )

    return TaskEnqueueResponse(
        task_id=job.id,
        status=job.get_status() or "queued",
        queue_name=QUEUE_NAME,
        position_in_queue=len(task_queue),
        model=req.model,
        filename=req.filename,
        submitted_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.get("/api/tasks/{task_id}", response_model=TaskStatusResponse, tags=["Tasks"])
def get_task_status(task_id: str) -> TaskStatusResponse:
    """Retrieve execution status and generated results of a submitted task."""
    try:
        job = Job.fetch(task_id, connection=redis_conn)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task ID '{task_id}' not found in Redis."
        )

    job_status = job.get_status()
    created_at = job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else None
    started_at = job.started_at.strftime("%Y-%m-%d %H:%M:%S") if job.started_at else None
    ended_at = job.ended_at.strftime("%Y-%m-%d %H:%M:%S") if job.ended_at else None

    return TaskStatusResponse(
        task_id=task_id,
        status=job_status,
        created_at=created_at,
        started_at=started_at,
        ended_at=ended_at,
        result=job.result if job.is_finished else None,
        error=str(job.exc_info) if job.is_failed else None
    )


@app.get("/api/queue", tags=["Monitoring"])
def get_queue_status() -> Dict[str, Any]:
    """Inspect queue depth and active jobs."""
    return {
        "queue_name": QUEUE_NAME,
        "queued_jobs_count": len(task_queue),
        "started_jobs_count": task_queue.started_job_registry.count,
        "finished_jobs_count": task_queue.finished_job_registry.count,
        "failed_jobs_count": task_queue.failed_job_registry.count
    }
