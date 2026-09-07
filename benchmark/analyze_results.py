"""
Raspberry Pi 5 LLM Arena - Benchmark Result Analyzer
Parses benchmark JSON files and formats Markdown leaderboard and comparative tables for README.md.
"""

import os
import sys
import glob
import json
from typing import Dict, Any, List

def analyze_latest(results_dir: str = "benchmark/results") -> str:
    files = glob.glob(os.path.join(results_dir, "benchmark_*.json"))
    if not files:
        print(f"[!] No benchmark results found in {results_dir}")
        return ""
        
    latest_file = max(files, key=os.path.getctime)
    print(f"[+] Analyzing latest benchmark: {latest_file}")
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    models = data.get("models", {})
    if not models:
        print("[!] No model data found in file.")
        return ""
        
    # Sort models by overall avg eval TPS descending
    sorted_models = sorted(
        models.items(),
        key=lambda x: x[1].get("overall_avg_eval_tps", 0.0),
        reverse=True
    )
    
    md = []
    md.append("## 🏆 Raspberry Pi 5 (16GB) LLM Inference Leaderboard\n")
    md.append(f"> **Hardware Environment:** Raspberry Pi 5 (BCM2712 4-Core A76 @ 2.4GHz, 16GB LPDDR4X, Active Fan Cooler, Performance Governor)\n")
    md.append(f"> **Benchmark Date:** {data.get('timestamp')}\n\n")
    
    # Leaderboard Table
    md.append("| Rank | Model | Generation Speed (tok/s) | TTFT (Prompt Latency) | Peak Temp (°C) | Status |")
    md.append("| :---: | :--- | :---: | :---: | :---: | :---: |")
    
    for idx, (model_name, mdata) in enumerate(sorted_models, 1):
        tps = mdata.get("overall_avg_eval_tps", 0.0)
        ttft = mdata.get("overall_avg_ttft_s", 0.0)
        temp = mdata.get("peak_temp_c", 0.0)
        
        status = "⚡ Real-time Capable (>10 tps)" if tps >= 10.0 else ("🟢 Usable (>5 tps)" if tps >= 5.0 else "🟡 Slow (<5 tps)")
        badge = f"🥇" if idx == 1 else (f"🥈" if idx == 2 else (f"🥉" if idx == 3 else f"#{idx}"))
        
        md.append(f"| {badge} | `{model_name}` | **{tps:.2f}** | {ttft:.2f}s | {temp:.1f}°C | {status} |")
        
    md.append("\n### 📊 Detailed Breakdown by Prompt Category\n")
    
    for model_name, mdata in sorted_models:
        md.append(f"#### 🔹 `{model_name}`")
        md.append("| Category | Avg Generation TPS | Avg TTFT (s) | Prompt Eval TPS | Peak Temp (°C) |")
        md.append("| :--- | :---: | :---: | :---: | :---: |")
        for cat in mdata.get("categories", []):
            md.append(f"| {cat['category']} | {cat['avg_eval_tps']:.2f} | {cat['avg_ttft_s']:.2f} | {cat['avg_prompt_tps']:.2f} | {cat['max_temp_c']:.1f}°C |")
        md.append("")
        
    markdown_output = "\n".join(md)
    print("\n" + markdown_output)
    
    # Output to markdown file
    out_md_path = os.path.join(results_dir, "LATEST_LEADERBOARD.md")
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"\n[+] Saved leaderboard Markdown to: {out_md_path}")
    return markdown_output

if __name__ == "__main__":
    analyze_latest()
