# 🚀 Raspberry Pi 5 (16GB) LLM Arena

> **A Comprehensive Benchmark & Architecture Arena for Edge LLM Inference on Raspberry Pi 5 (16GB RAM)**

[![Hardware](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%20(16GB)-C51A4A?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![OS](https://img.shields.io/badge/OS-Debian%2013%20(trixie)%2064--bit-A81D33?logo=debian&logoColor=white)](https://www.debian.org/)
[![Engine](https://img.shields.io/badge/Inference%20Engine-Native%20Ollama%20ARM64%20(v0.33.3)-000000?logo=ollama&logoColor=white)](https://ollama.com)
[![Status](https://img.shields.io/badge/Benchmark%20Status-Phase%203%20Completed-brightgreen)](#-基準測試排行榜-benchmark-leaderboard)

---

## 🏆 基準測試排行榜 (Benchmark Leaderboard)

以下為在 **Raspberry Pi 5 (BCM2712 4-Core Cortex-A76 @ 2.40 GHz, 16GB LPDDR4X)** 鎖頻效能模式下執行的標準化多維度實測結果：

| 排名 (Rank) | 評測模型 (Model) | 參數量 | 生成速度 (Gen TPS) | 提示詞速度 (Prompt TPS) | 首字延遲 (TTFT) | 峰值溫度 | 記憶體佔用 | 獨立評測報告 (Report) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 **冠軍** | `deepseek-r1:1.5b` | 1.5B | **11.54 tok/s** | 183.09 tok/s | **0.243s** | 56.5°C | 1.84 GB | [📄 1.5B 報告](./benchmark/reports/deepseek-r1_1_5b_REPORT.md) |
| 🥈 **亞軍** | `qwen2.5:3b` | 3B | **6.02 tok/s** | 178.39 tok/s | **0.661s** | 56.5°C | 2.87 GB | [📄 Qwen 3B 報告](./benchmark/reports/qwen2_5_3b_REPORT.md) |
| 🥉 **季軍** | `llama3.2:3b` | 3B | **5.92 tok/s** | 164.10 tok/s | **0.629s** | 56.5°C | 3.39 GB | [📄 Llama 3B 報告](./benchmark/reports/llama3_2_3b_REPORT.md) |
| **#4** | `qwen2.5-coder:7b` | 7B | **2.77 tok/s** | 80.20 tok/s | **1.744s** | 58.2°C | 5.23 GB | [📄 Coder 7B 報告](./benchmark/reports/qwen2_5-coder_7b_REPORT.md) |
| **#5** | `deepseek-r1:7b` | 7B | **2.53 tok/s** | 38.29 tok/s | **1.384s** | 57.1°C | 5.23 GB | [📄 R1 7B 報告](./benchmark/reports/deepseek-r1_7b_REPORT.md) |
| **#6** | `llama3.1:8b` | 8B | **2.46 tok/s** | 46.62 tok/s | **1.620s** | 57.6°C | 5.76 GB | [📄 Llama 8B 報告](./benchmark/reports/llama3_1_8b_REPORT.md) |

> 📊 **完整統整評測報告 (Master Report):** 詳見 [PLAN1_FINAL_REPORT.md](./benchmark/reports/PLAN1_FINAL_REPORT.md) 與 [plan1.md](./plan1.md)。

---

## ⚡ 核心發現與架構分析 (Architectural Insights)

### 1. 超輕量即時對話首選 (Sub-3B Tier)
- **`deepseek-r1:1.5b`**：達到 **11.54 tokens/sec** 的超高速生成，首字延遲僅 **0.243s**，具備完整思維鏈 (CoT) 推理能力，記憶體僅耗費 1.84 GB，是邊緣即時 Agent 的最佳首選。
- **`qwen2.5:3b` & `llama3.2:3b`**：穩定達到 **~6.0 tokens/sec** 實用區間，在繁體中文理解與通用語意問答上達到流暢可用標準。

### 2. 重度邏輯與編程首選 (7B~8B Tier)
- 16GB 實體記憶體徹底消除了 Swap 換頁延遲，7B 與 8B 模型常駐僅需 5.2 ~ 5.8 GB RAM。
- **`qwen2.5-coder:7b`** 與 **`deepseek-r1:7b`** 推論速率穩定落在 **2.5 ~ 2.8 tokens/sec**，適合批次後台代碼審查與深度推理任務。

### 3. 溫控與能效表現 (Thermal Dynamics)
- CPU 鎖定於 2.40 GHz (`performance` governor) 全核滿載推論下，搭配官方 Active Cooler，最高溫僅 **58.2°C**（距 80°C 降頻點有 >21°C 安全餘裕），完全無 Thermal Throttling (`throttled=0x0`)。

---

## 📂 專案結構 (Repository Structure)

```text
pi5-llm-arena/
├── README.md                           # 專案首頁與 Leaderboard
├── plan1.md                            # Plan 1 實施計畫書與評測報告彙整
├── plan1_cmd.md                        # Plan 1 完整指令集、工作流與問題排除手冊
├── plan2.md                            # Native Ollama vs Docker vs llama.cpp 深度架構分析
├── requirements.txt                    # Python 相依套件
├── benchmark/
│   ├── benchmark_suite.py              # 全自動評測套件 (自動測量 TTFT, TPS, 溫度, RAM)
│   ├── analyze_results.py              # 統計彙整分析器
│   ├── logs/                           # 各模型專屬原始 Log 與 JSON 指標
│   │   ├── deepseek-r1_1_5b/
│   │   ├── qwen2_5_3b/
│   │   ├── llama3_2_3b/
│   │   ├── qwen2_5-coder_7b/
│   │   ├── deepseek-r1_7b/
│   │   └── llama3_1_8b/
│   ├── reports/                        # 各模型獨立 Markdown 報告與主報告
│   │   ├── deepseek-r1_1_5b_REPORT.md
│   │   ├── qwen2_5_3b_REPORT.md
│   │   ├── llama3_2_3b_REPORT.md
│   │   ├── qwen2_5-coder_7b_REPORT.md
│   │   ├── deepseek-r1_7b_REPORT.md
│   │   ├── llama3_1_8b_REPORT.md
│   │   └── PLAN1_FINAL_REPORT.md
│   └── results/
│       └── master_benchmark_summary.json
```

---

## 🛠️ 重現評測步驟 (How to Reproduce)

1. **安裝依賴套件:**
   ```bash
   pip install -r requirements.txt
   ```
2. **執行評測套件:**
   ```bash
   python benchmark/benchmark_suite.py
   ```
3. **重新彙整報告:**
   ```bash
   python benchmark/analyze_results.py
   ```
