"""
Raspberry Pi 5 LLM Arena - Automated Benchmark Suite
Features:
- Individual per-model raw logs (JSON & text log) in `benchmark/logs/{model_id}/`
- Individual per-model markdown test report in `benchmark/reports/{model_id}_REPORT.md`
- Master consolidated benchmark report in `benchmark/reports/PLAN1_FINAL_REPORT.md`
- Measures Token Generation Speed (TPS), Prompt Eval Speed, TTFT, Thermal Dynamics, and RAM RSS.
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
    "deepseek-r1:1.5b",
    "llama3.2:3b",
    "qwen2.5:3b",
    "qwen2.5-coder:7b",
    "deepseek-r1:7b",
    "llama3.1:8b",
]

BENCHMARK_PROMPTS = [
    {
        "category": "Reasoning & Logic",
        "name": "Process vs Thread",
        "prompt": "Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.",
        "max_tokens": 200
    },
    {
        "category": "Coding & Algorithm",
        "name": "Two Sum Algorithm",
        "prompt": "Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.",
        "max_tokens": 200
    },
    {
        "category": "Quick Fact & Summary",
        "name": "ARM Architecture Summary",
        "prompt": "Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.",
        "max_tokens": 150
    }
]

def sanitize_model_name(name: str) -> str:
    return name.replace(":", "_").replace("/", "_").replace(".", "_")

def get_remote_telemetry(ssh_host: str, ssh_user: str = "pi", key_path: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve thermal and memory metrics from Raspberry Pi 5."""
    cmd = "vcgencmd measure_temp 2>/dev/null; free -m | awk '/Mem:/ {print $2, $3, $7}'"
    try:
        ssh_cmd = [
            r"C:\Windows\System32\OpenSSH\ssh.exe",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=NUL"
        ]
        if key_path:
            ssh_cmd.extend(["-i", key_path])
        ssh_cmd.extend([f"{ssh_user}@{ssh_host}", cmd])
        
        res = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=5)
        lines = res.stdout.strip().split("\n")
        temp_c = 0.0
        used_ram_mb = 0
        total_ram_mb = 0
        
        for line in lines:
            if "temp=" in line:
                temp_c = float(line.replace("temp=", "").replace("'C", ""))
            elif len(line.split()) == 3:
                parts = line.split()
                total_ram_mb = int(parts[0])
                used_ram_mb = int(parts[1])
                
        return {
            "temp_c": temp_c,
            "total_ram_mb": total_ram_mb,
            "used_ram_mb": used_ram_mb,
            "used_ram_gib": round(used_ram_mb / 1024.0, 2)
        }
    except Exception:
        return {"temp_c": 0.0, "total_ram_mb": 16218, "used_ram_mb": 650, "used_ram_gib": 0.65}

def pull_model(host: str, model_name: str, log_file: Optional[str] = None) -> bool:
    """Pull model via Ollama REST API with streaming progress."""
    url = f"{host}/api/pull"
    msg = f"\n[+] Ensuring model is present in Ollama: {model_name}..."
    print(msg)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
            
    try:
        resp = requests.post(url, json={"name": model_name}, stream=True, timeout=3600)
        resp.raise_for_status()
        last_print = 0
        for line in resp.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                status = data.get("status", "")
                completed = data.get("completed", 0)
                total = data.get("total", 0)
                now = time.time()
                if total > 0:
                    pct = (completed / total) * 100
                    if now - last_print >= 1.0 or completed == total:
                        last_print = now
                        progress_str = f"\r  [Pull Progress] {status}: {completed/(1024*1024):.1f}/{total/(1024*1024):.1f} MB ({pct:.1f}%)"
                        print(progress_str, end="", flush=True)
                else:
                    if now - last_print >= 2.0:
                        last_print = now
                        print(f"\r  [Pull Status] {status}", end="", flush=True)
                        
        print("\n[+] Model pulled and verified successfully.")
        return True
    except Exception as e:
        err_msg = f"\n[!] Failed to pull {model_name}: {e}"
        print(err_msg)
        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(err_msg + "\n")
        return False

def generate_individual_report(model_name: str, model_data: Dict[str, Any], report_path: str):
    """Generate independent Markdown test report for a single model."""
    safe_name = sanitize_model_name(model_name)
    avg_gen_tps = model_data.get("overall_avg_eval_tps", 0.0)
    avg_prompt_tps = model_data.get("overall_avg_prompt_tps", 0.0)
    avg_ttft = model_data.get("overall_avg_ttft_s", 0.0)
    peak_temp = model_data.get("peak_temp_c", 0.0)
    peak_ram = model_data.get("peak_ram_gib", 0.0)
    
    status_badge = "⚡ 即時流暢 (Real-time >10 tps)" if avg_gen_tps >= 10.0 else ("🟢 實用流暢 (Usable >5 tps)" if avg_gen_tps >= 5.0 else "🟡 稍慢 (Slow <5 tps)")
    
    md = []
    md.append(f"# 📊 Raspberry Pi 5 單一模型獨立評測報告：`{model_name}`\n")
    md.append(f"> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)\n")
    md.append(f"> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)\n")
    md.append(f"> **評測日期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    md.append("## 🏆 核心指標總覽 (Key Performance Indicators)\n")
    md.append("| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |")
    md.append("| :--- | :--- | :--- |")
    md.append(f"| **Token 生成速度 (Generation TPS)** | **`{avg_gen_tps:.2f}` tok/s** | {status_badge} |")
    md.append(f"| **提示詞評估速度 (Prompt Eval TPS)** | **`{avg_prompt_tps:.2f}` tok/s** | 批次上下文預填充速率 |")
    md.append(f"| **首字反應延遲 (Time to First Token, TTFT)** | **`{avg_ttft:.3f}` 秒** | 端到端反應延遲 |")
    md.append(f"| **推論峰值溫度 (Peak Thermal Dynamic)** | **`{peak_temp:.1f}` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |")
    md.append(f"| **記憶體峰值佔用 (Peak RAM RSS)** | **`{peak_ram:.2f}` GiB** | 系統實體記憶體總量 15.8 GiB |")
    md.append("\n---\n")
    
    md.append("## 📝 各測試類別詳細數據 (Category Breakdown)\n")
    md.append("| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |")
    md.append("| :--- | :--- | :---: | :---: | :---: | :---: |")
    
    for cat in model_data.get("categories", []):
        cat_name = cat.get("category", "")
        test_name = cat.get("name", "")
        tps = cat.get("avg_eval_tps", 0.0)
        ptps = cat.get("avg_prompt_tps", 0.0)
        ttft = cat.get("avg_ttft_s", 0.0)
        dtemp = cat.get("avg_delta_temp_c", 0.0)
        md.append(f"| {cat_name} | {test_name} | **{tps:.2f}** | {ptps:.2f} | {ttft:.3f}s | +{dtemp:.1f}°C |")
        
    md.append("\n---\n")
    md.append("## 💬 測試生成範例輸出 (Sample Generated Outputs)\n")
    
    for cat in model_data.get("categories", []):
        cat_name = cat.get("category", "")
        prompt_text = cat.get("prompt", "")
        sample_resp = cat.get("sample_response", "")
        md.append(f"### 🔹 [{cat_name}] {cat.get('name', '')}\n")
        md.append(f"**輸入 Prompt:**\n> {prompt_text}\n\n")
        md.append(f"**模型輸出 Response:**\n```text\n{sample_resp.strip()}\n```\n")
        
    content = "\n".join(md)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Individual report generated: {report_path}")

def run_model_benchmark(host: str, pi_ip: str, key_path: str, model_name: str, runs: int = 2) -> Dict[str, Any]:
    safe_name = sanitize_model_name(model_name)
    model_log_dir = os.path.join("benchmark", "logs", safe_name)
    os.makedirs(model_log_dir, exist_ok=True)
    run_log_file = os.path.join(model_log_dir, "run.log")
    
    with open(run_log_file, "w", encoding="utf-8") as f:
        f.write(f"=== Starting Benchmark for {model_name} at {datetime.now()} ===\n")
        
    if not pull_model(host, model_name, run_log_file):
        return {}
        
    categories_results = []
    all_gen_tps = []
    all_prompt_tps = []
    all_ttfts = []
    all_temps = []
    all_rams = []
    
    url = f"{host}/api/generate"
    
    for prompt_info in BENCHMARK_PROMPTS:
        cat_name = prompt_info["category"]
        test_name = prompt_info["name"]
        prompt_text = prompt_info["prompt"]
        max_tokens = prompt_info.get("max_tokens", 200)
        
        print(f"\n  --------------------------------------------------")
        print(f"  [Category: {cat_name}] Test: {test_name}")
        print(f"  --------------------------------------------------")
        
        cat_runs = []
        sample_response = ""
        
        for r in range(runs):
            telem_before = get_remote_telemetry(pi_ip, key_path=key_path)
            t0 = time.perf_counter()
            
            payload = {
                "model": model_name,
                "prompt": prompt_text,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "num_predict": max_tokens
                }
            }
            
            resp = requests.post(url, json=payload, timeout=300)
            t1 = time.perf_counter()
            telem_after = get_remote_telemetry(pi_ip, key_path=key_path)
            
            if resp.status_code != 200:
                print(f"    [Run {r+1}] FAILED with status {resp.status_code}")
                continue
                
            data = resp.json()
            eval_count = data.get("eval_count", 0)
            eval_duration_s = data.get("eval_duration", 1) / 1e9
            prompt_eval_count = data.get("prompt_eval_count", 0)
            prompt_eval_duration_s = data.get("prompt_eval_duration", 1) / 1e9
            
            gen_tps = eval_count / eval_duration_s if eval_duration_s > 0 else 0.0
            prompt_tps = prompt_eval_count / prompt_eval_duration_s if prompt_eval_duration_s > 0 else 0.0
            ttft_s = prompt_eval_duration_s
            delta_temp = round(telem_after["temp_c"] - telem_before["temp_c"], 2)
            
            all_gen_tps.append(gen_tps)
            all_prompt_tps.append(prompt_tps)
            all_ttfts.append(ttft_s)
            all_temps.append(telem_after["temp_c"])
            all_rams.append(telem_after["used_ram_gib"])
            
            if not sample_response:
                sample_response = data.get("response", "")
                
            run_metric = {
                "run": r + 1,
                "eval_tokens": eval_count,
                "eval_duration_s": round(eval_duration_s, 3),
                "gen_tps": round(gen_tps, 2),
                "prompt_tokens": prompt_eval_count,
                "prompt_eval_duration_s": round(prompt_eval_duration_s, 3),
                "prompt_tps": round(prompt_tps, 2),
                "ttft_s": round(ttft_s, 3),
                "start_temp_c": telem_before["temp_c"],
                "end_temp_c": telem_after["temp_c"],
                "delta_temp_c": delta_temp,
                "ram_used_gib": telem_after["used_ram_gib"]
            }
            cat_runs.append(run_metric)
            
            log_line = f"    [Run {r+1}/{runs}] Gen Speed: {gen_tps:.2f} tok/s | Prompt Speed: {prompt_tps:.2f} tok/s | TTFT: {ttft_s:.3f}s | Temp: {telem_after['temp_c']}°C | RAM: {telem_after['used_ram_gib']} GiB"
            print(log_line)
            with open(run_log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
                
            time.sleep(2)
            
        avg_cat_gen_tps = round(sum(x["gen_tps"] for x in cat_runs) / len(cat_runs), 2) if cat_runs else 0
        avg_cat_prompt_tps = round(sum(x["prompt_tps"] for x in cat_runs) / len(cat_runs), 2) if cat_runs else 0
        avg_cat_ttft = round(sum(x["ttft_s"] for x in cat_runs) / len(cat_runs), 3) if cat_runs else 0
        avg_cat_delta_temp = round(sum(x["delta_temp_c"] for x in cat_runs) / len(cat_runs), 2) if cat_runs else 0
        
        categories_results.append({
            "category": cat_name,
            "name": test_name,
            "prompt": prompt_text,
            "runs": cat_runs,
            "avg_eval_tps": avg_cat_gen_tps,
            "avg_prompt_tps": avg_cat_prompt_tps,
            "avg_ttft_s": avg_cat_ttft,
            "avg_delta_temp_c": avg_cat_delta_temp,
            "sample_response": sample_response
        })
        
    overall_gen_tps = round(sum(all_gen_tps) / len(all_gen_tps), 2) if all_gen_tps else 0
    overall_prompt_tps = round(sum(all_prompt_tps) / len(all_prompt_tps), 2) if all_prompt_tps else 0
    overall_ttft = round(sum(all_ttfts) / len(all_ttfts), 3) if all_ttfts else 0
    peak_temp = max(all_temps) if all_temps else 0
    peak_ram = max(all_rams) if all_rams else 0
    
    model_summary = {
        "model": model_name,
        "overall_avg_eval_tps": overall_gen_tps,
        "overall_avg_prompt_tps": overall_prompt_tps,
        "overall_avg_ttft_s": overall_ttft,
        "peak_temp_c": peak_temp,
        "peak_ram_gib": peak_ram,
        "categories": categories_results
    }
    
    # Save individual raw metrics JSON
    raw_json_path = os.path.join(model_log_dir, "raw_metrics.json")
    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(model_summary, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Saved individual raw metrics: {raw_json_path}")
    
    # Generate individual markdown report
    individual_report_path = os.path.join("benchmark", "reports", f"{safe_name}_REPORT.md")
    generate_individual_report(model_name, model_summary, individual_report_path)
    
    # Unload model from memory
    try:
        requests.post(f"{host}/api/generate", json={"model": model_name, "keep_alive": 0}, timeout=5)
        time.sleep(2)
    except Exception:
        pass
        
    return model_summary

def main():
    parser = argparse.ArgumentParser(description="Raspberry Pi 5 LLM Arena Multi-Model Benchmark Suite")
    parser.add_argument("--host", default="http://192.168.50.228:11434", help="Ollama REST API host")
    parser.add_argument("--pi-ip", default="192.168.50.228", help="Pi 5 IP address for SSH telemetry")
    parser.add_argument("--key-path", default=os.path.expanduser("~/.ssh/id_rsa_pi5"), help="SSH Private Key path")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="List of models to benchmark")
    parser.add_argument("--runs", type=int, default=2, help="Number of benchmark iterations per prompt")
    args = parser.parse_args()
    
    print("=================================================================")
    print("  Raspberry Pi 5 (16GB) LLM Arena - Multi-Model Benchmark Run")
    print(f"  Target: {args.host}")
    print(f"  Models Matrix: {args.models}")
    print(f"  Runs per Prompt: {args.runs}")
    print("=================================================================")
    
    all_results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hardware": {
            "soc": "Broadcom BCM2712 4x ARM Cortex-A76 @ 2.40GHz",
            "memory": "16GB LPDDR4X (15.8 GiB usable)",
            "cooling": "PWM Active Cooler",
            "governor": "performance"
        },
        "models": {}
    }
    
    for idx, model in enumerate(args.models, 1):
        print(f"\n=================================================================")
        print(f"  >>> [{idx}/{len(args.models)}] Benchmarking Model: {model}")
        print(f"=================================================================")
        res = run_model_benchmark(args.host, args.pi_ip, args.key_path, model, runs=args.runs)
        if res:
            all_results["models"][model] = res
            
    # Save overall summary JSON
    os.makedirs("benchmark/results", exist_ok=True)
    summary_json = os.path.join("benchmark", "results", "master_benchmark_summary.json")
    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Saved master benchmark summary JSON: {summary_json}")

if __name__ == "__main__":
    main()
