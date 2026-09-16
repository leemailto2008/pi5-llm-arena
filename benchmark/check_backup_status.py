import os
import sys
import json
import time
from datetime import datetime

# Local paths
LOCAL_MODELS = r"f:\12_prj_raspi5\raspi5_ollama_backup\models"
LOCAL_BLOBS = os.path.join(LOCAL_MODELS, "blobs")
LOCAL_MANIFESTS = os.path.join(LOCAL_MODELS, "manifests")

# Target models and sizes (GGUF weights)
MODELS_CATALOG = [
    ("sha256-aabd4debf0c8f08881923f2c25fc0fdeed24435271c2b3e92c4af36704040dbc", 1117320512, "deepseek-r1:1.5b"),
    ("sha256-5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6", 1929903008, "qwen2.5:3b"),
    ("sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff", 2019377376, "llama3.2:3b"),
    ("sha256-3b6b58718a439291ffc1953067c4cc16587a23a88b00492c491c3d0787fb206c", 4471999712, "olmo2:7b"),
    ("sha256-ea89e3927d5ef671159a1359a22cdd418856c4baa2098e665f1c6eed59973968", 4472020256, "olmo-3:7b"),
    ("sha256-96c415656d377afbff962f6cdb2394ab092ccbcbaab4b82525bc4ca800fe8a49", 4683073184, "deepseek-r1:7b"),
    ("sha256-60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463", 4683074048, "qwen2.5-coder:7b"),
    ("sha256-667b0c1932bc6ffc593ed1d03f895bf2dc8dc6df21db3042284a6f4416b06a29", 4920738944, "llama3.1:8b"),
    ("sha256-4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448", 7162394016, "gemma4:e2b"),
    ("sha256-4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a", 9608338848, "gemma4:e4b"),
]

def fmt(b):
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f"{b:.2f} {u}"
        b /= 1024
    return f"{b:.2f} TB"

def get_stats():
    total_target_bytes = sum(s for _, s, _ in MODELS_CATALOG)
    total_downloaded_bytes = 0
    model_status = []
    completed_count = 0

    for name, target_sz, label in MODELS_CATALOG:
        path = os.path.join(LOCAL_BLOBS, name)
        cur_sz = os.path.getsize(path) if os.path.exists(path) else 0
        total_downloaded_bytes += cur_sz
        is_done = cur_sz >= target_sz
        if is_done:
            completed_count += 1
        pct = (cur_sz / target_sz * 100) if target_sz > 0 else 0
        model_status.append({
            "name": label,
            "current_size": cur_sz,
            "target_size": target_sz,
            "percent": pct,
            "done": is_done
        })

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_count": completed_count,
        "total_models": len(MODELS_CATALOG),
        "total_downloaded_bytes": total_downloaded_bytes,
        "total_target_bytes": total_target_bytes,
        "overall_percent": (total_downloaded_bytes / total_target_bytes * 100),
        "models": model_status,
        "all_done": (completed_count == len(MODELS_CATALOG))
    }

if __name__ == "__main__":
    data = get_stats()
    print(json.dumps(data, indent=2, ensure_ascii=False))
