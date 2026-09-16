# f:\12_prj_raspi5\client\push_task.py
"""
PC Developer Client for Pi 5 LLM Code Dispatcher
Dispatches local code to Raspberry Pi 5 Redis Queue for asynchronous inference.
"""

import sys
import os
import time
import json
import argparse
from typing import Optional, Dict, Any
import requests

DEFAULT_PI5_HOST = "http://192.168.50.228:8000"


# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def print_banner():
    print("=" * 70)
    print("  [Pi 5 LLM Code Dispatcher Client]")
    print("=" * 70)


def check_health(host: str) -> None:
    try:
        resp = requests.get(f"{host}/health", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(f"\n[+] Pi 5 System Health Status:")
        print(f"    - Status: {data.get('status', 'unknown')}")
        print(f"    - Redis Connected: {data.get('redis_connected')}")
        print(f"    - Ollama Running: {data.get('ollama_running')} ({data.get('available_models_count')} models available)")
        print(f"    - CPU Temperature: {data.get('cpu_temperature_c')} °C")
        print(f"    - Free RAM: {data.get('ram_available_mb')} MB / {data.get('ram_total_mb')} MB")
        print(f"    - Queued Jobs: {data.get('queue_length')}")
    except Exception as e:
        print(f"[-] Failed to reach Pi 5 at {host}: {e}")


def check_queue(host: str) -> None:
    try:
        resp = requests.get(f"{host}/api/queue", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(f"\n[+] Queue Telemetry ({data.get('queue_name')}):")
        print(f"    - Queued (Waiting): {data.get('queued_jobs_count')}")
        print(f"    - Running (Active): {data.get('started_jobs_count')}")
        print(f"    - Finished Jobs:    {data.get('finished_jobs_count')}")
        print(f"    - Failed Jobs:      {data.get('failed_jobs_count')}")
    except Exception as e:
        print(f"[-] Failed to query queue: {e}")


def check_status(host: str, task_id: str, verbose: bool = True) -> Optional[Dict[str, Any]]:
    try:
        resp = requests.get(f"{host}/api/tasks/{task_id}", timeout=10)
        if resp.status_code == 404:
            print(f"[-] Task ID '{task_id}' not found.")
            return None
        resp.raise_for_status()
        data = resp.json()
        if verbose:
            print(f"\n[+] Task Status: {task_id}")
            print(f"    - State: {data.get('status')}")
            print(f"    - Created: {data.get('created_at')}")
            print(f"    - Started: {data.get('started_at')}")
            print(f"    - Ended:   {data.get('ended_at')}")
        return data
    except Exception as e:
        print(f"[-] Error querying task {task_id}: {e}")
        return None


def submit_task(
    host: str,
    code: str,
    prompt: str,
    model: str,
    filename: str,
    language: str,
    wait: bool = True,
    poll_interval: float = 3.0,
    output_file: Optional[str] = None
) -> Optional[str]:
    payload = {
        "code": code,
        "prompt": prompt,
        "model": model,
        "filename": filename,
        "language": language
    }

    print(f"\n[*] Enqueuing code review task to Pi 5 ({host})...")
    print(f"    - Target File: {filename} ({len(code.splitlines())} lines, {len(code)} bytes)")
    print(f"    - Model: {model}")

    try:
        resp = requests.post(f"{host}/api/tasks", json=payload, timeout=10)
        resp.raise_for_status()
        enqueued = resp.json()
        task_id = enqueued.get("task_id")
        position = enqueued.get("position_in_queue", 1)
        print(f"[+] Task successfully queued! Task ID: {task_id}")
        print(f"    - Queue Position: #{position} (Execution is serialized, Concurrency = 1)")

        if not wait:
            print(f"\n[i] Non-blocking mode. To query status later, run:")
            print(f"    python client/push_task.py --status {task_id}\n")
            return task_id

        print("\n[*] Waiting for Pi 5 Worker to process task...")
        start_wait = time.time()
        while True:
            status_data = check_status(host, task_id, verbose=False)
            if not status_data:
                time.sleep(poll_interval)
                continue

            current_status = status_data.get("status")
            elapsed = int(time.time() - start_wait)

            if current_status == "queued":
                print(f"\r    [*] Status: QUEUED (Waiting in line... {elapsed}s elapsed)", end="", flush=True)
            elif current_status == "started":
                print(f"\r    [>] Status: PROCESSING on Pi 5 (Inference running... {elapsed}s elapsed)", end="", flush=True)
            elif current_status == "finished":
                print(f"\n\n[+] Task Completed successfully in {elapsed}s!")
                res = status_data.get("result", {})
                print("=" * 70)
                print(f"  AI CODE REVIEW REPORT ({res.get('model')})")
                print(f"  Speed: {res.get('eval_tps')} tok/s | Tokens: {res.get('total_tokens')} | Time: {res.get('eval_duration_s')}s")
                print("=" * 70)
                print(res.get("result", "").strip())
                print("=" * 70)

                if output_file:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(f"# AI Code Review: {filename}\n")
                        f.write(f"Model: {res.get('model')} | Speed: {res.get('eval_tps')} tok/s\n\n")
                        f.write(res.get("result", ""))
                    print(f"\n[+] Saved review report to: {output_file}")
                return task_id
            elif current_status == "failed":
                print(f"\n\n[-] Task execution failed on Pi 5!")
                print(f"Error Details: {status_data.get('error')}")
                return task_id

            time.sleep(poll_interval)

    except Exception as e:
        print(f"[-] Failed to enqueue task: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Push code tasks to Raspberry Pi 5 Inference Queue")
    parser.add_argument("--file", "-f", help="Path to source code file to analyze")
    parser.add_argument("--code", "-c", help="Direct inline code string to analyze")
    parser.add_argument("--prompt", "-p", default="Perform a comprehensive code review, identify potential bugs, security flaws, and performance optimizations.", help="Review instruction")
    parser.add_argument("--model", "-m", default="qwen2.5-coder:7b", help="Model name (e.g., qwen2.5-coder:7b, deepseek-r1:7b, llama3.1:8b)")
    parser.add_argument("--host", default=DEFAULT_PI5_HOST, help="Pi 5 FastAPI base URL")
    parser.add_argument("--no-wait", action="store_true", help="Do not wait for task completion")
    parser.add_argument("--status", "-s", help="Check status of a previously submitted task ID")
    parser.add_argument("--queue", "-q", action="store_true", help="Check queue length and worker status")
    parser.add_argument("--health", action="store_true", help="Check Pi 5 hardware & service health")
    parser.add_argument("--out", "-o", help="Save review output to a markdown/text file")

    args = parser.parse_args()
    print_banner()

    if args.health:
        check_health(args.host)
        return

    if args.queue:
        check_queue(args.host)
        return

    if args.status:
        res = check_status(args.host, args.status, verbose=True)
        if res and res.get("status") == "finished":
            print("\n--- Review Content ---")
            print(res.get("result", {}).get("result", "").strip())
        return

    code_content = ""
    filename = "snippet.py"
    language = "python"

    if args.file:
        if not os.path.exists(args.file):
            print(f"[-] File not found: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            code_content = f.read()
        filename = os.path.basename(args.file)
        ext = os.path.splitext(filename)[1].lstrip(".")
        if ext in ["py", "python"]:
            language = "python"
        elif ext in ["cpp", "c", "h", "hpp"]:
            language = "cpp"
        elif ext in ["js", "ts", "jsx", "tsx"]:
            language = "typescript"
        elif ext in ["go", "rs", "java", "sh"]:
            language = ext
    elif args.code:
        code_content = args.code
    else:
        print("[-] Please specify code to analyze using --file <path> or --code <string>.")
        print("    Example: python client/push_task.py --file app.py --model qwen2.5-coder:7b")
        return

    submit_task(
        host=args.host,
        code=code_content,
        prompt=args.prompt,
        model=args.model,
        filename=filename,
        language=language,
        wait=not args.no_wait,
        output_file=args.out
    )


if __name__ == "__main__":
    main()
