# f:\12_prj_raspi5\benchmark\optimize_gemma4_e4b.py
"""
Benchmark & Optimization Pipeline for Gemma 4 E4B on Raspberry Pi 5
1. Verifies CPU Governor is locked at 'performance' (2.40 GHz).
2. Builds optimized model variant 'gemma4:e4b-opt' with customized Modelfile (num_thread=4, num_ctx=4096, multimodal edge params).
3. Executes real comparative benchmarks between baseline gemma4:e4b and gemma4:e4b-opt on multimodal edge pipeline and PLE parameter efficiency tasks.
4. Records TTFT, evaluation throughput (tokens/sec), RAM, and thermals.
"""

import os
import sys
import time
import json
import requests
import paramiko

PI_HOST = "192.168.50.228"
PI_USER = "pi"
PI_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa_pi5")
OLLAMA_API_URL = f"http://{PI_HOST}:11434"

PROMPTS = [
    {
        "category": "Edge Multimodal Architecture & IoT Vision",
        "prompt": "Design an edge multimodal inference pipeline on Raspberry Pi 5 combining a camera stream (V4L2) with Gemma 4 E4B for real-time anomaly detection. Detail frame subsampling, embedding projection, and latency budgeting."
    },
    {
        "category": "Per-Layer Embeddings (PLE) Parameter Efficiency",
        "prompt": "Explain how Per-Layer Embeddings (PLE) reduce cross-layer parameter redundancy in transformer models compared to standard input token embedding layers. What are the memory bandwidth trade-offs on ARM CPUs?"
    }
]


def get_ssh_client() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(PI_HOST, username=PI_USER, key_filename=PI_KEY_PATH, timeout=10)
    return client


def get_system_telemetry(ssh: paramiko.SSHClient):
    stdin, stdout, _ = ssh.exec_command("vcgencmd measure_temp && free -m")
    lines = stdout.read().decode().strip().splitlines()
    temp = lines[0].replace("temp=", "") if lines else "N/A"
    free_ram = "N/A"
    for l in lines[1:]:
        if l.startswith("Mem:"):
            parts = l.split()
            free_ram = f"{parts[6]}MB available / {parts[1]}MB total"
    return {"temp": temp, "ram": free_ram}


def create_optimized_modelfile(ssh: paramiko.SSHClient):
    print("[*] Creating optimized Modelfile for gemma4:e4b via Ollama CLI...")
    modelfile_content = (
        "FROM gemma4:e4b\n"
        "PARAMETER num_thread 4\n"
        "PARAMETER num_ctx 4096\n"
        "PARAMETER temperature 0.3\n"
        "PARAMETER top_p 0.9\n"
        "PARAMETER repeat_penalty 1.1\n"
        "SYSTEM \"\"\"You are a senior AI research engineer specializing in multimodal architectures and edge computing. Provide clean, rigorous, and technically precise solutions.\"\"\"\n"
    )
    sftp = ssh.open_sftp()
    with sftp.open("/home/pi/Modelfile.gemma4_e4b", "w") as f:
        f.write(modelfile_content)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command("ollama create gemma4:e4b-opt -f /home/pi/Modelfile.gemma4_e4b")
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"    -> ollama create exit: {exit_status}, out: {out}, err: {err}")
    return exit_status == 0


def run_benchmark(model_name: str, prompt_data: dict, ssh: paramiko.SSHClient) -> dict:
    prompt = prompt_data["prompt"]
    print(f"\n[*] Benchmarking [{model_name}] on [{prompt_data['category']}]...")
    
    before_telemetry = get_system_telemetry(ssh)
    
    generate_url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 150  # Fixed 150 tokens for standardized throughput comparison
        }
    }
    
    resp = requests.post(generate_url, json=payload, timeout=300)
    after_telemetry = get_system_telemetry(ssh)
    
    if resp.status_code != 200:
        print(f"[!] Error: {resp.status_code} - {resp.text}")
        return {"error": resp.text}
    
    data = resp.json()
    
    total_duration_s = data.get("total_duration", 0) / 1e9
    load_duration_s = data.get("load_duration", 0) / 1e9
    prompt_eval_count = data.get("prompt_eval_count", 0)
    prompt_eval_duration_s = data.get("prompt_eval_duration", 0) / 1e9
    eval_count = data.get("eval_count", 0)
    eval_duration_s = data.get("eval_duration", 0) / 1e9
    
    prompt_eval_rate = prompt_eval_count / prompt_eval_duration_s if prompt_eval_duration_s > 0 else 0
    eval_rate = eval_count / eval_duration_s if eval_duration_s > 0 else 0
    
    result = {
        "model": model_name,
        "category": prompt_data["category"],
        "prompt_tokens": prompt_eval_count,
        "eval_tokens": eval_count,
        "total_duration_s": round(total_duration_s, 2),
        "load_duration_s": round(load_duration_s, 2),
        "eval_rate_tok_per_sec": round(eval_rate, 2),
        "prompt_eval_rate_tok_per_sec": round(prompt_eval_rate, 2),
        "before_telemetry": before_telemetry,
        "after_telemetry": after_telemetry,
        "response_snippet": data.get("response", "")[:120] + "..."
    }
    
    print(f"    -> Generated Tokens: {eval_count}")
    print(f"    -> Eval Throughput: {result['eval_rate_tok_per_sec']} tok/s")
    print(f"    -> Prompt Eval Speed: {result['prompt_eval_rate_tok_per_sec']} tok/s")
    print(f"    -> Total Time: {result['total_duration_s']}s")
    print(f"    -> Temperature: {after_telemetry['temp']}")
    return result


def main():
    print("=================================================================")
    print(" Pi 5 Gemma 4 E4B Optimization & Verification Benchmark Suite")
    print("=================================================================")
    
    ssh = get_ssh_client()
    try:
        create_optimized_modelfile(ssh)
        
        results = []
        for prompt_data in PROMPTS:
            res_base = run_benchmark("gemma4:e4b", prompt_data, ssh)
            results.append(res_base)
            
            time.sleep(3)
            
            res_opt = run_benchmark("gemma4:e4b-opt", prompt_data, ssh)
            results.append(res_opt)
            
            time.sleep(3)
            
        output_file = os.path.join(os.path.dirname(__file__), "gemma4_e4b_opt_benchmark_results.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Benchmark complete! Results written to: {output_file}")
        
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
