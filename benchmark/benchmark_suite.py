"""
Raspberry Pi 5 LLM Arena - Automated Benchmark Suite
Tests inference speed (TTFT, TPS), peak memory consumption, and thermal dynamics across modern SLMs.
"""

import os
import sys
import time
import json
import socket
import argparse
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests

DEFAULT_MODELS = [
    "llama3.2:3b",
    "deepseek-r1:1.5b",
    "qwen2.5:3b",
    "qwen2.5-coder:7b",
    "deepseek-r1:7b",
    "llama3.1:8b",
]

BENCHMARK_PROMPTS = [
    {
        "category": "Reasoning & Logic",
        "prompt": "Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.",
        "max_tokens": 256
    },
    {
        "category": "Coding & Algorithm",
        "prompt": "Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.",
        "max_tokens": 256
    },
    {
        "category": "Quick Fact / Knowledge",
        "prompt": "Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.",
        "max_tokens": 150
    }
]

def get_cpu_temp() -> float:
    """Retrieve Pi 5 CPU temperature in Celsius."""
    try:
        res = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            # Output format: temp=42.3'C
            return float(res.stdout.strip().replace("temp=", "").replace("'C", ""))
    except Exception:
        pass
    
    # Fallback to sysfs
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000.0
    except Exception:
        return 0.0

def get_mem_info() -> Dict[str, float]:
    """Retrieve system memory stats in GiB."""
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip().split()[0]
                    mem[key] = int(val) / (1024 * 1024)  # in GiB
        return {
            "total_gib": mem.get("MemTotal", 0.0),
            "free_gib": mem.get("MemFree", 0.0),
            "available_gib": mem.get("MemAvailable", 0.0),
            "used_gib": mem.get("MemTotal", 0.0) - mem.get("MemAvailable", 0.0)
        }
    except Exception:
        return {"total_gib": 0.0, "free_gib": 0.0, "available_gib": 0.0, "used_gib": 0.0}

def pull_model(host: str, model_name: str) -> bool:
    """Pull model via Ollama REST API with streaming progress."""
    url = f"{host}/api/pull"
    print(f"\n[+] Ensuring model is present: {model_name}...")
    try:
        resp = requests.post(url, json={"name": model_name}, stream=True, timeout=1800)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                status = data.get("status", "")
                completed = data.get("completed", 0)
                total = data.get("total", 0)
                if total > 0:
                    pct = (completed / total) * 100
                    print(f"\r  -> {status}: {completed/(1024*1024):.1f}/{total/(1024*1024):.1f} MB ({pct:.1f}%)", end="", flush=True)
                else:
                    print(f"\r  -> {status}", end="", flush=True)
        print("\n[+] Model pulled successfully.")
        return True
    except Exception as e:
        print(f"\n[!] Failed to pull {model_name}: {e}")
        return False

def run_inference_benchmark(host: str, model_name: str, prompt_data: Dict[str, Any], runs: int = 3) -> Dict[str, Any]:
    """Execute benchmark runs for a single prompt and collect metrics."""
    url = f"{host}/api/generate"
    category = prompt_data["category"]
    prompt = prompt_data["prompt"]
    
    results = []
    
    print(f"\n  --- Benchmarking [{category}] (Runs: {runs}) ---")
    print(f"  Prompt: {prompt[:60]}...")
    
    for r in range(runs):
        start_temp = get_cpu_temp()
        mem_before = get_mem_info()
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": prompt_data.get("max_tokens", 256),
                "temperature": 0.0  # Greedy decoding for deterministic benchmarks
            }
        }
        
        t0 = time.perf_counter()
        resp = requests.post(url, json=payload, timeout=300)
        t1 = time.perf_counter()
        
        end_temp = get_cpu_temp()
        mem_after = get_mem_info()
        
        if resp.status_code != 200:
            print(f"  [Run {r+1}] FAILED with HTTP {resp.status_code}: {resp.text}")
            continue
            
        data = resp.json()
        
        # Parse Ollama timings (in nanoseconds)
        total_duration_s = data.get("total_duration", 0) / 1e9
        load_duration_s = data.get("load_duration", 0) / 1e9
        prompt_eval_count = data.get("prompt_eval_count", 0)
        prompt_eval_duration_s = data.get("prompt_eval_duration", 0) / 1e9
        eval_count = data.get("eval_count", 0)
        eval_duration_s = data.get("eval_duration", 0) / 1e9
        
        # Calculate metrics
        prompt_tps = (prompt_eval_count / prompt_eval_duration_s) if prompt_eval_duration_s > 0 else 0.0
        eval_tps = (eval_count / eval_duration_s) if eval_duration_s > 0 else 0.0
        ttft_s = prompt_eval_duration_s  # Time to first token
        
        metrics = {
            "run": r + 1,
            "eval_tokens": eval_count,
            "prompt_tokens": prompt_eval_count,
            "total_duration_s": round(total_duration_s, 3),
            "ttft_s": round(ttft_s, 3),
            "prompt_eval_tps": round(prompt_tps, 2),
            "eval_tps": round(eval_tps, 2),
            "start_temp_c": start_temp,
            "end_temp_c": end_temp,
            "delta_temp_c": round(end_temp - start_temp, 2),
            "mem_used_gib": round(mem_after["used_gib"], 2)
        }
        
        print(f"  [Run {r+1}] TPS: {eval_tps:.2f} tok/s | TTFT: {ttft_s:.2f}s | Gen: {eval_count} toks | Temp: {end_temp:.1f}°C | RAM: {mem_after['used_gib']:.2f} GiB")
        results.append(metrics)
        
        # Cool down pause
        time.sleep(2)
        
    return {
        "category": category,
        "runs": results,
        "avg_eval_tps": round(sum(x["eval_tps"] for x in results) / len(results), 2) if results else 0,
        "avg_prompt_tps": round(sum(x["prompt_eval_tps"] for x in results) / len(results), 2) if results else 0,
        "avg_ttft_s": round(sum(x["ttft_s"] for x in results) / len(results), 2) if results else 0,
        "max_temp_c": max([x["end_temp_c"] for x in results]) if results else 0,
    }

def unload_model(host: str, model_name: str):
    """Unload model from memory to ensure clean slate for next benchmark."""
    url = f"{host}/api/generate"
    try:
        requests.post(url, json={"model": model_name, "keep_alive": 0}, timeout=10)
        time.sleep(3)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Raspberry Pi 5 LLM Arena Benchmark Suite")
    parser.add_argument("--host", default="http://127.0.0.1:11434", help="Ollama API base URL")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="List of models to benchmark")
    parser.add_argument("--runs", type=int, default=3, help="Number of benchmark runs per prompt")
    parser.add_argument("--output-dir", default="benchmark/results", help="Directory to store benchmark JSON")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(args.output_dir, f"benchmark_{timestamp}.json")
    
    print("=================================================================")
    print(f"  Raspberry Pi 5 LLM Arena - Benchmark Execution")
    print(f"  Target Host: {args.host}")
    print(f"  Models: {args.models}")
    print(f"  Runs per Prompt: {args.runs}")
    print("=================================================================")
    
    all_results = {
        "timestamp": timestamp,
        "hardware": {
            "device": "Raspberry Pi 5 Model B",
            "soc": "BCM2712 4x Cortex-A76 @ 2.4GHz",
            "total_ram_gib": get_mem_info()["total_gib"],
            "governor": "performance"
        },
        "models": {}
    }
    
    for model in args.models:
        print(f"\n==================================================")
        print(f"  >>> Testing Model: {model}")
        print(f"==================================================")
        
        if not pull_model(args.host, model):
            print(f"[!] Skipping {model} due to pull error.")
            continue
            
        model_benchmark_data = []
        for prompt_data in BENCHMARK_PROMPTS:
            res = run_inference_benchmark(args.host, model, prompt_data, runs=args.runs)
            model_benchmark_data.append(res)
            
        # Summary for this model
        valid_cats = [c for c in model_benchmark_data if c["runs"]]
        overall_avg_tps = round(sum(c["avg_eval_tps"] for c in valid_cats) / len(valid_cats), 2) if valid_cats else 0
        overall_avg_ttft = round(sum(c["avg_ttft_s"] for c in valid_cats) / len(valid_cats), 2) if valid_cats else 0
        max_temp = max([c["max_temp_c"] for c in valid_cats]) if valid_cats else 0
        
        all_results["models"][model] = {
            "categories": model_benchmark_data,
            "overall_avg_eval_tps": overall_avg_tps,
            "overall_avg_ttft_s": overall_avg_ttft,
            "peak_temp_c": max_temp
        }
        
        print(f"\n[+] Summary for {model}: Avg TPS = {overall_avg_tps} tok/s | Avg TTFT = {overall_avg_ttft}s | Peak Temp = {max_temp}°C")
        
        # Unload model
        unload_model(args.host, model)
        
    # Save results
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
        
    print("\n=================================================================")
    print(f"  Benchmark Completed! Results saved to: {summary_file}")
    print("=================================================================")

if __name__ == "__main__":
    main()
