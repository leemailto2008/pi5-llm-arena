#!/usr/bin/env python3
import subprocess
import time
import requests
import json
import sys

MODEL_BLOB = "/home/pi/.ollama/models/blobs/sha256-4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448"
PORT = 9999
HOST = "127.0.0.1"

print("[*] Starting llama-server for gemma4:e2b...")
subprocess.run(["pkill", "-9", "-f", "llama-server"])
time.sleep(1)

cmd = [
    "/usr/local/lib/ollama/llama-server",
    "-m", MODEL_BLOB,
    "-c", "2048",
    "-t", "4",
    "--port", str(PORT),
    "--host", HOST
]
env = {"LD_LIBRARY_PATH": "/usr/local/lib/ollama", "PATH": "/usr/local/bin:/usr/bin:/bin"}

proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

ready = False
for i in range(40):
    try:
        r = requests.get(f"http://{HOST}:{PORT}/health", timeout=2)
        if r.status_code == 200:
            print(f"[+] Server ready in {i*2}s! Response: {r.text}")
            ready = True
            break
        else:
            print(f"[-] Status {r.status_code}: {r.text.strip()}")
    except Exception as e:
        print(f"[-] Waiting for server... ({e})")
    time.sleep(2)

if not ready:
    print("[!] Failed to get ready state within 80s")
    proc.terminate()
    sys.exit(1)

prompt_512 = "The quick brown fox jumps over the lazy dog. " * 50
print("[*] Testing P512 / G128...")
payload = {
    "prompt": prompt_512,
    "n_predict": 128,
    "temperature": 0.0,
    "stream": False
}
t0 = time.time()
r = requests.post(f"http://{HOST}:{PORT}/completion", json=payload, timeout=300)
dur = time.time() - t0
print(f"[+] Request finished in {dur:.2f}s, HTTP {r.status_code}")

if r.status_code == 200:
    data = r.json()
    timings = data.get("timings", {})
    print(json.dumps(timings, indent=2))

proc.terminate()
proc.wait()
print("[DONE]")
