# f:\12_prj_raspi5\benchmark\sample_progress.py
import os
import sys
import json
import time
from datetime import datetime

TRACKER_FILE = r"f:\12_prj_raspi5\benchmark\backup_tracker.json"
LOCAL_MODELS = r"f:\12_prj_raspi5\raspi5_ollama_backup\models"
LOCAL_BLOBS = os.path.join(LOCAL_MODELS, "blobs")

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

def fmt_size(b: float) -> str:
    for u in ['B', 'KB', 'MB', 'GB']:
        if b < 1024.0:
            return f"{b:.2f} {u}"
        b /= 1024.0
    return f"{b:.2f} TB"

def sample_progress():
    now_ts = time.time()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_target = sum(s for _, s, _ in MODELS_CATALOG)
    total_downloaded = 0
    completed_count = 0
    active_model_info = None
    models_details = []

    for name, target, label in MODELS_CATALOG:
        p = os.path.join(LOCAL_BLOBS, name)
        sz = os.path.getsize(p) if os.path.exists(p) else 0
        total_downloaded += sz
        done = (sz >= target)
        if done:
            completed_count += 1
            status = "done"
        elif sz > 0:
            status = "downloading"
            if active_model_info is None:
                active_model_info = {
                    "name": label,
                    "current": sz,
                    "target": target,
                    "pct": (sz / target * 100) if target > 0 else 0
                }
        else:
            status = "pending"

        models_details.append({
            "name": label,
            "current_size": sz,
            "target_size": target,
            "percent": (sz / target * 100) if target > 0 else 0,
            "status": status
        })

    # Read previous tracker
    prev_data = {}
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
                prev_data = json.load(f)
        except Exception:
            pass

    prev_ts = prev_data.get("timestamp_epoch", now_ts)
    prev_bytes = prev_data.get("total_downloaded_bytes", total_downloaded)

    dt = now_ts - prev_ts
    d_bytes = total_downloaded - prev_bytes
    if dt > 0 and d_bytes >= 0:
        speed_bps = d_bytes / dt
    else:
        speed_bps = 0.0

    speed_mb_s = speed_bps / (1024 * 1024)
    speed_kb_s = speed_bps / 1024

    overall_pct = (total_downloaded / total_target * 100) if total_target > 0 else 0
    all_done = (completed_count == len(MODELS_CATALOG))

    result = {
        "timestamp": now_str,
        "timestamp_epoch": now_ts,
        "total_downloaded_bytes": total_downloaded,
        "total_target_bytes": total_target,
        "total_downloaded_str": fmt_size(total_downloaded),
        "total_target_str": fmt_size(total_target),
        "overall_percent": overall_pct,
        "speed_mb_s": speed_mb_s,
        "speed_kb_s": speed_kb_s,
        "completed_count": completed_count,
        "total_models": len(MODELS_CATALOG),
        "all_done": all_done,
        "active_model": active_model_info,
        "models": models_details
    }

    # Save to tracker
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result

if __name__ == "__main__":
    res = sample_progress()
    print(json.dumps(res, indent=2, ensure_ascii=False))
