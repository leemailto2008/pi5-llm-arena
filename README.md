# 🚀 Raspberry Pi 5 (16GB) LLM Arena

> **A Comprehensive Benchmark & Architecture Arena for Edge LLM Inference on Raspberry Pi 5 (16GB RAM)**

[![Hardware](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%20(16GB)-C51A4A?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![OS](https://img.shields.io/badge/OS-Debian%2013%20(trixie)%2064--bit-A81D33?logo=debian&logoColor=white)](https://www.debian.org/)
[![Engines](https://img.shields.io/badge/Engines-Native%20llama.cpp%20%7C%20Native%20Ollama-000000?logo=ollama&logoColor=white)](#-三大推論架構深度對比-architecture-comparison)
[![Status](https://img.shields.io/badge/Benchmark%20Status-Plan%201%20%26%20Plan%202%20Completed-brightgreen)](#-基準測試排行榜-benchmark-leaderboard)

---

## 🏆 基準測試排行榜 (Benchmark Leaderboard)

### 🥇 Plan 1: Native Ollama (ARM64 REST API 標準化評測)
透過 Native Ollama HTTP REST API 進行全自動真實對話多輪提示詞基準測試：

| 排名<br><sub>(Rank)</sub> | 評測模型<br><sub>(Model)</sub> | 參數量<br><sub>(Params)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞速度<br><sub>(Prompt TPS)</sub> | 首字延遲<br><sub>(TTFT)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 記憶體<br><sub>(RAM)</sub> | 獨立報告<br><sub>(Report)</sub> |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 **冠軍** | `deepseek-r1:1.5b` | 1.5B | **11.54 tok/s** | 183.09 tok/s | **0.243s** | 56.5°C | 1.84 GB | [📄 1.5B 報告](./benchmark/reports/deepseek-r1_1_5b_REPORT.md) |
| 🥈 **亞軍** | `gemma4:e2b` | 2.6B | **7.61 tok/s** | 99.16 tok/s | **0.585s** | 58.2°C | 8.55 GB | [📄 Gemma4 2B 報告](./benchmark/reports/gemma4_e2b_REPORT.md) |
| 🥉 **季軍** | `qwen2.5:3b` | 3B | **6.02 tok/s** | 178.39 tok/s | **0.661s** | 56.5°C | 2.87 GB | [📄 Qwen 3B 報告](./benchmark/reports/qwen2_5_3b_REPORT.md) |
| **#4** | `llama3.2:3b` | 3B | **5.92 tok/s** | 164.10 tok/s | **0.629s** | 56.5°C | 3.39 GB | [📄 Llama 3B 報告](./benchmark/reports/llama3_2_3b_REPORT.md) |
| **#5** | `gemma4:e4b` | 4.3B | **3.71 tok/s** | 47.74 tok/s | **1.243s** | 57.1°C | 10.25 GB | [📄 Gemma4 4B 報告](./benchmark/reports/gemma4_e4b_REPORT.md) |
| **#6** | `qwen2.5-coder:7b` | 7B | **2.77 tok/s** | 80.20 tok/s | **1.744s** | 58.2°C | 5.23 GB | [📄 Coder 7B 報告](./benchmark/reports/qwen2_5-coder_7b_REPORT.md) |
| **#7** | `olmo2:7b` | 7B | **2.73 tok/s** | 94.08 tok/s | **1.549s** | 57.6°C | 12.37 GB | [📄 OLMo2 7B 報告](./benchmark/reports/olmo2_7b_REPORT.md) |
| **#8** | `olmo-3:7b` | 7B | **2.56 tok/s** | 51.90 tok/s | **3.436s** | 56.5°C | 13.05 GB | [📄 OLMo-3 7B 報告](./benchmark/reports/olmo-3_7b_REPORT.md) |
| **#9** | `deepseek-r1:7b` | 7B | **2.53 tok/s** | 38.29 tok/s | **1.384s** | 57.1°C | 5.23 GB | [📄 R1 7B 報告](./benchmark/reports/deepseek-r1_7b_REPORT.md) |
| **#10** | `llama3.1:8b` | 8B | **2.46 tok/s** | 46.62 tok/s | **1.620s** | 57.6°C | 5.76 GB | [📄 Llama 8B 報告](./benchmark/reports/llama3_1_8b_REPORT.md) |

> 📊 **Plan 1 完整統整評測報告 (Master Report):** 詳見 [PLAN1_FINAL_REPORT.md](./benchmark/reports/PLAN1_FINAL_REPORT.md) 與 [plan1.md](./plan1.md)。

---

### 🥈 Plan 2: Native llama.cpp (ARMv8.2-a DotProd / FP16 向量加速)
在 **Raspberry Pi 5 (BCM2712 4-Core Cortex-A76 @ 2.40 GHz, 16GB LPDDR4X)** 上啟用 `-mcpu=cortex-a76 -march=armv8.2-a+fp16+dotprod` 原生極限微基準壓測 (`llama-bench`)：

| 排名<br><sub>(Rank)</sub> | 評測模型<br><sub>(Model Tag)</sub> | 參數量 / 檔案<br><sub>(Params / Size)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞處理<br><sub>(Prefill TPS)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 實體記憶體<br><sub>(Peak RAM)</sub> | 獨立報告<br><sub>(Report)</sub> |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 **冠軍** | `deepseek-r1:1.5b` | 1.78B (1.04 GB) | **12.02 tok/s** | **60.66 tok/s** | 57.1°C | **0.59 GiB** | [📄 1.5B 報告](./benchmark/reports/plan2_deepseek-r1_1_5b_REPORT.md) |
| 🥈 **亞軍** | `gemma4:e2b` | 2.6B (6.67 GB) | **7.04 tok/s** | **45.44 tok/s** | 58.2°C | **3.20 GiB** | [📄 Gemma4 2B 報告](./benchmark/reports/plan2_gemma4_e2b_REPORT.md) |
| 🥉 **季軍** | `qwen2.5:3b` | 3.09B (1.80 GB) | **6.01 tok/s** | **28.89 tok/s** | 56.5°C | **0.60 GiB** | [📄 Qwen 3B 報告](./benchmark/reports/plan2_qwen2_5_3b_REPORT.md) |
| **#4** | `llama3.2:3b` | 3.21B (1.88 GB) | **5.71 tok/s** | **27.23 tok/s** | 57.6°C | **0.62 GiB** | [📄 Llama 3B 報告](./benchmark/reports/plan2_llama3_2_3b_REPORT.md) |
| **#5** | `gemma4:e4b` | 4.3B (8.95 GB) | **3.68 tok/s** | **22.50 tok/s** | 62.1°C | **5.80 GiB** | [📄 Gemma4 4B 報告](./benchmark/reports/plan2_gemma4_e4b_REPORT.md) |
| **#6** | `qwen2.5-coder:7b` | 7.61B (4.36 GB) | **2.76 tok/s** | **11.59 tok/s** | 58.2°C | **0.46 GiB** | [📄 Coder 7B 報告](./benchmark/reports/plan2_qwen2_5-coder_7b_REPORT.md) |
| **#7** | `deepseek-r1:7b` | 7.61B (4.36 GB) | **2.70 tok/s** | **11.30 tok/s** | 58.7°C | **0.44 GiB** | [📄 R1 7B 報告](./benchmark/reports/plan2_deepseek-r1_7b_REPORT.md) |
| **#8** | `olmo2:7b` | 7.05B (4.16 GB) | **2.59 tok/s** | **11.59 tok/s** | 58.7°C | **6.37 GiB** | [📄 OLMo2 報告](./benchmark/reports/PLAN2_FINAL_REPORT.md) |
| **#9** | `llama3.1:8b` | 8.03B (4.58 GB) | **2.46 tok/s** | **10.69 tok/s** | 57.6°C | **0.43 GiB** | [📄 Llama 8B 報告](./benchmark/reports/plan2_llama3_1_8b_REPORT.md) |
| **#10** | `olmo-3:7b` | 6.95B (4.16 GB) | **2.37 tok/s** | **13.90 tok/s** | 65.3°C | **8.90 GiB** | [📄 OLMo-3 報告](./benchmark/reports/plan2_olmo-3_7b_REPORT.md) |

> 📊 **Plan 2 完整統整評測報告 (Master Report):** 詳見 [PLAN2_FINAL_REPORT.md](./benchmark/reports/PLAN2_FINAL_REPORT.md) 與 [plan2.md](./plan2.md)。

---

## ⚡ 核心發現與三大架構對比 (Architecture Comparison)

```mermaid
graph TD
    subgraph Architecture 1: Native llama.cpp
        A1[Native CLI / llama-bench] -->|ARM NEON / DotProd ASM| B1[Linux Kernel & CPU Registers]
    end

    subgraph Architecture 2: Native Ollama
        A2[REST API :11434] -->|Go Daemon / IPC| B2[llama.cpp Runner]
        B2 -->|ARM NEON Vector Ops| C2[Linux Kernel & CPU Registers]
    end

    subgraph Architecture 3: Dockerized Ollama
        A3[Port Forwarding :11434] -->|OverlayFS / cgroups| B3[Ollama Container]
        B3 -->|IPC| C3[llama.cpp Runner]
        C3 -->|Virtualization Overhead| D3[Linux Kernel & CPU Registers]
    end
```

| 評估維度<br><sub>(Dimension)</sub> | Native llama.cpp<br><sub>(DotProd Accelerated)</sub> | Native Ollama<br><sub>(Host Service)</sub> | Dockerized Ollama<br><sub>(Container)</sub> |
| :--- | :--- | :--- | :--- |
| **推論生成吞吐量 (TPS)** | **極致最高 (100% 物理極限)** | **極高 (~95% - 98%)** | 中高 (~88% - 93%) |
| **記憶體額外開銷 (RAM Overhead)** | **0 MB (純 POSIX mmap 映射)** | ~30 MB (Go Runtime) | ~200 MB (Containerd + OverlayFS) |
| **模型管理便利度 (DX)** | 手動下載 / 需指定 Blob 路徑 | **一鍵 `ollama pull`** | 一鍵 `ollama pull` |
| **硬體感測器整合 (Telemetry)** | **原生完全支援 (`vcgencmd`)** | **原生完全支援 (`vcgencmd`)** | 需高風險 `--privileged` 提權 |
| **長文本 Prefill 運算加速** | **ARMv8.2-a DotProd 向量極致** | 依賴動態載入動態函式庫 | 依賴動態載入動態函式庫 |

---

## 📂 專案結構 (Repository Structure)

```text
pi5-llm-arena/
├── README.md                           # 專案首頁與雙階段 Leaderboard
├── plan1.md                            # Plan 1 實施計畫書與評測報告彙整
├── plan1_cmd.md                        # Plan 1 完整指令集、工作流與問題排除手冊
├── plan2.md                            # Plan 2 實施計畫書與三大架構深度剖析
├── plan2_cmd.md                        # Plan 2 原生編譯 llama.cpp 與 DotProd 壓測手冊
├── requirements.txt                    # Python 相依套件
├── benchmark/
│   ├── benchmark_suite.py              # Plan 1 全自動評測套件 (測量 TTFT, TPS, 溫度, RAM)
│   ├── analyze_results.py              # Plan 1 統計彙整分析器
│   ├── plan2_benchmark_suite.py        # Plan 2 遠端調度微基準測試套件
│   ├── pi5_plan2_local_runner.py       # Plan 2 Pi 5 本地守護壓測進程 (Zero-Jitter)
│   ├── plan2_analyze_results.py        # Plan 2 雙引擎交叉對比報告產生器
│   ├── logs/                           # Plan 1 原始對話 Log 與指標
│   ├── logs_plan2/                     # Plan 2 llama-bench 原始微基準 Log
│   ├── reports/                        # Markdown 評測報告集散庫
│   │   ├── deepseek-r1_1_5b_REPORT.md
│   │   ├── plan2_deepseek-r1_1_5b_REPORT.md
│   │   ├── ...
│   │   ├── PLAN1_FINAL_REPORT.md       # Plan 1 最終主報告
│   │   └── PLAN2_FINAL_REPORT.md       # Plan 2 最終主報告
│   └── results/
│       ├── master_benchmark_summary.json
│       └── plan2_benchmark_summary.json
```

---

## 🛠️ 重現評測步驟 (How to Reproduce)

### 1. 執行 Plan 1 (Native Ollama 評測)
```bash
python benchmark/benchmark_suite.py
python benchmark/analyze_results.py
```

### 2. 執行 Plan 2 (Native llama.cpp 評測)
```bash
# 在 Pi 5 上編譯 Native llama.cpp
cmake -B build -G Ninja -DGGML_CPU_AARCH64=ON -DCMAKE_C_FLAGS="-mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod"
cmake --build build --config Release -j4 --target llama-bench

# 執行本地基準壓測並產出報告
python3 benchmark/pi5_plan2_local_runner.py
python3 benchmark/plan2_analyze_results.py
```
