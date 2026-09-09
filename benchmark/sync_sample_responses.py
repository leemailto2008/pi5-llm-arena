import os
import sys
import time
import json
import requests
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PI_HOST = "http://192.168.50.228:11434"

MODELS = [
    "deepseek-r1:1.5b",
    "gemma4:e2b",
    "llama3.2:3b",
    "qwen2.5:3b",
    "gemma4:e4b",
    "qwen2.5-coder:7b",
    "deepseek-r1:7b",
    "olmo2:7b",
    "olmo-3:7b",
    "llama3.1:8b",
]

PROMPTS = [
    {
        "category": "Reasoning & Logic",
        "name": "Process vs Thread",
        "prompt": "Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.",
        "max_tokens": 180
    },
    {
        "category": "Coding & Algorithm",
        "name": "Two Sum Algorithm",
        "prompt": "Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.",
        "max_tokens": 180
    },
    {
        "category": "Quick Fact & Summary",
        "name": "ARM Architecture Summary",
        "prompt": "Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.",
        "max_tokens": 120
    }
]

def sanitize_model_name(name: str) -> str:
    return name.replace(":", "_").replace("/", "_").replace(".", "_")

def update_model_report(model_name: str, model_data: dict):
    safe_name = sanitize_model_name(model_name)
    report_path = os.path.join("benchmark", "reports", f"{safe_name}_REPORT.md")
    if not os.path.exists(report_path):
        return

    with open(report_path, "r", encoding="utf-8") as f:
        old_content = f.read()

    split_marker = "## 💬 測試生成範例輸出 (Sample Generated Outputs)"
    if split_marker in old_content:
        header_part = old_content.split(split_marker)[0]
    else:
        header_part = old_content + "\n"

    md = []
    md.append(header_part.strip())
    md.append("\n---\n")
    md.append("## 💬 測試生成範例輸出 (Sample Generated Outputs)\n")

    for cat in model_data.get("categories", []):
        cat_name = cat.get("category", "")
        prompt_text = cat.get("prompt", "")
        sample_resp = cat.get("sample_response", "")
        md.append(f"### 🔹 [{cat_name}] {cat.get('name', '')}\n")
        md.append(f"**輸入 Prompt:**\n> {prompt_text}\n\n")
        md.append(f"**模型輸出 Response:**\n```text\n{sample_resp.strip()}\n```\n")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"[✓] Updated report: {report_path}", flush=True)

def main():
    # 1. Download existing Pi sample responses
    scp_cmd = [
        r"C:\Windows\System32\OpenSSH\scp.exe",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=NUL",
        "-i", r"C:\Users\Andrew\.ssh\id_rsa_pi5",
        "pi@192.168.50.228:/home/pi/sample_responses.json",
        "scratch/pi_sample_responses.json"
    ]
    subprocess.run(scp_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    pi_samples = {}
    if os.path.exists("scratch/pi_sample_responses.json"):
        try:
            with open("scratch/pi_sample_responses.json", "r", encoding="utf-8") as f:
                pi_samples = json.load(f)
        except Exception:
            pass

    for model in MODELS:
        safe_name = sanitize_model_name(model)
        json_path = os.path.join("benchmark", "logs", safe_name, "raw_metrics.json")
        if not os.path.exists(json_path):
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            model_data = json.load(f)

        print(f"\n[+] Processing: {model}...", flush=True)
        changed = False

        for cat in model_data.get("categories", []):
            cat_name = cat.get("category", "")
            current_resp = cat.get("sample_response", "").strip()

            # Check if pi_samples has it
            if not current_resp and model in pi_samples:
                if cat_name in pi_samples[model] and len(pi_samples[model][cat_name].strip()) > 20:
                    current_resp = pi_samples[model][cat_name].strip()
                    cat["sample_response"] = current_resp
                    changed = True
                    print(f"  [✓] Loaded from Pi cache: {cat_name} ({len(current_resp)} chars)", flush=True)

            # If still empty, query Ollama with thinking support (/api/chat handles gemma4 thinking properly)
            if len(current_resp) < 20:
                print(f"  [*] Querying Ollama for: {cat_name}...", flush=True)
                prompt_text = cat.get("prompt", "")
                for p in PROMPTS:
                    if p["category"] == cat_name:
                        prompt_text = p["prompt"]
                        max_tok = p["max_tokens"]
                        break
                else:
                    max_tok = 180

                # Use /api/chat for universal thinking support across deepseek and gemma4
                chat_payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt_text}],
                    "stream": False,
                    "options": {
                        "temperature": 0.0,
                        "num_predict": max_tok
                    }
                }
                for retry in range(2):
                    try:
                        r = requests.post(f"{PI_HOST}/api/chat", json=chat_payload, timeout=240)
                        if r.status_code == 200:
                            d = r.json()
                            msg = d.get("message", {})
                            resp = msg.get("content", "").strip()
                            think = msg.get("thinking", "").strip()
                            
                            # Fallback to top-level if any
                            if not resp and not think:
                                resp = d.get("response", "").strip()
                                think = d.get("thinking", "").strip()

                            if think and resp:
                                final_out = f"<think>\n{think}\n</think>\n\n{resp}"
                            elif think:
                                final_out = f"<think>\n{think}\n</think>"
                            else:
                                final_out = resp

                            if len(final_out.strip()) > 0:
                                cat["sample_response"] = final_out
                                changed = True
                                print(f"  [+] Success! Captured {len(final_out)} chars (Think: {len(think)}, Resp: {len(resp)})", flush=True)
                                break
                    except Exception as e:
                        print(f"  [-] Retry {retry+1}: {e}", flush=True)
                        time.sleep(2)

        if changed:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(model_data, f, indent=2, ensure_ascii=False)

        update_model_report(model, model_data)

    print("\n[🎉] Complete sample output synchronization finished!", flush=True)

if __name__ == "__main__":
    main()
