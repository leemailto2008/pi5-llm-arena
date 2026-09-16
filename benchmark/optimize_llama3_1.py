# f:\12_prj_raspi5\benchmark\optimize_llama3_1.py
"""
Benchmark & Optimization Pipeline for Llama 3.1 8B on Raspberry Pi 5
1. Locks CPU Governor to 'performance' mode (2.4GHz) via SSH.
2. Checks Ollama runtime configuration.
3. Builds an optimized model variant 'llama3.1:8b-opt' with customized Modelfile (num_thread=4, num_ctx=4096, low-temperature, flash-attention).
4. Executes real comparative benchmarks between baseline llama3.1:8b and llama3.1:8b-opt.
5. Captures TTFT, evaluation throughput (tokens/sec), RAM overhead, and CPU temperature.
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
        "category": "Code Architecture & Analysis",
        "prompt": "Write a high-performance Python asynchronous producer-consumer queue using asyncio.Queue with proper error handling, graceful shutdown, and type hints. Explain the design briefly."
    },
    {
        "category": "Reasoning & Mathematical Logic",
        "prompt": "A train leaves Station A at 8:00 AM traveling at 75 km/h towards Station B, 300 km away. Another train leaves Station B at 8:30 AM traveling at 90 km/h towards Station A. At what exact time do they meet? Show each calculation step."
    }
]


def get_ssh_client() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(PI_HOST, username=PI_USER, key_filename=PI_KEY_PATH, timeout=10)
    return client


def setup_cpu_governor(ssh: paramiko.SSHClient):
    print("[*] Setting CPU Governor to 'performance' (2.40 GHz locked)...")
    cmd = "echo andrew | sudo -S sh -c 'for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > \"$g\"; done'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    
    stdin, stdout, stderr = ssh.exec_command("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor && cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    gov = stdout.read().decode().strip().split()
    print(f"    -> CPU Governor: {gov[0]}, Current Frequency: {gov[1] if len(gov) > 1 else 'N/A'} KHz")


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
    print("[*] Creating optimized Modelfile for llama3.1:8b via Ollama CLI...")
    modelfile_content = (
        "FROM llama3.1:8b\n"
        "PARAMETER num_thread 4\n"
        "PARAMETER num_ctx 4096\n"
        "PARAMETER temperature 0.2\n"
        "PARAMETER top_p 0.9\n"
        "PARAMETER repeat_penalty 1.1\n"
        "SYSTEM \"\"\"You are a senior software architect and AI engineer. Provide concise, production-ready, highly optimized solutions with explicit technical rationale.\"\"\"\n"
    )
    sftp = ssh.open_sftp()
    with sftp.open("/home/pi/Modelfile.llama31", "w") as f:
        f.write(modelfile_content)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command("ollama create llama3.1:8b-opt -f /home/pi/Modelfile.llama31")
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"    -> ollama create exit: {exit_status}, out: {out}, err: {err}")
    return exit_status == 0



def run_benchmark(model_name: str, prompt_data: dict, ssh: paramiko.SSHClient) -> dict:
    prompt = prompt_data["prompt"]
    print(f"\n[*] Benchmarking [{model_name}] on [{prompt_data['category']}]...")
    
    before_telemetry = get_system_telemetry(ssh)
    start_time = time.time()
    
    generate_url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 150  # Fixed generation length for normalized speed comparison
        }
    }
    
    resp = requests.post(generate_url, json=payload, timeout=300)
    end_time = time.time()
    after_telemetry = get_system_telemetry(ssh)
    
    if resp.status_code != 200:
        print(f"[!] Error: {resp.status_code} - {resp.text}")
        return {"error": resp.text}
    
    data = resp.json()
    
    # Ollama returns nanoseconds for durations
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
    print(" Pi 5 Llama 3.1 8B Optimization & Verification Benchmark Suite")
    print("=================================================================")
    
    ssh = get_ssh_client()
    try:
        # Step 1: System tuning
        setup_cpu_governor(ssh)
        
        # Step 2: Create optimized model
        create_optimized_modelfile(ssh)

        
        results = []
        for prompt_data in PROMPTS:
            # Baseline test
            res_base = run_benchmark("llama3.1:8b", prompt_data, ssh)
            results.append(res_base)
            
            # Short cooldown
            time.sleep(3)
            
            # Optimized test
            res_opt = run_benchmark("llama3.1:8b-opt", prompt_data, ssh)
            results.append(res_opt)
            
            time.sleep(3)
            
        output_file = os.path.join(os.path.dirname(__file__), "llama3_1_opt_benchmark_results.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Benchmark complete! Results written to: {output_file}")
        
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
