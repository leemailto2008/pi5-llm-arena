# 🚀 Raspberry Pi 5 (16GB) LLM 邊緣推論競技場 (LLM Arena)

> **樹莓派 5 邊緣大型語言模型推論之綜合基準評測與架構競技場 (A Comprehensive Benchmark & Architecture Arena for Edge LLM Inference on Raspberry Pi 5 16GB RAM)**

[![硬體規格 (Hardware)](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%20(16GB)-C51A4A?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![作業系統 (OS)](https://img.shields.io/badge/OS-Debian%2013%20(trixie)%2064--bit-A81D33?logo=debian&logoColor=white)](https://www.debian.org/)
[![推論引擎 (Inference Engines)](https://img.shields.io/badge/Engines-Native%20llama.cpp%20%7C%20Native%20Ollama-000000?logo=ollama&logoColor=white)](#-三大推論架構深度對比-architecture-comparison)
[![評測狀態 (Benchmark Status)](https://img.shields.io/badge/Benchmark%20Status-Plan%201%2C%202%20%26%203%20Completed-brightgreen)](#-基準測試排行榜-benchmark-leaderboard)

---

## 🏆 基準測試排行榜 (Benchmark Leaderboard)

### 🥇 Plan 1: 原生 Ollama 服務 (Native Ollama: ARM64 REST API 標準化評測)
透過原生 Ollama (Native Ollama) HTTP 表現層狀態轉換應用程式介面 (REST API) 進行全自動真實對話多輪提示詞基準測試 (Automated Multi-turn Prompt Benchmark)：

| 排名<br><sub>(Rank)</sub> | 評測模型<br><sub>(Model Tag)</sub> | 參數量<br><sub>(Parameters)</sub> | 生成速度<br><sub>(Generation TPS)</sub> | 提示詞速度<br><sub>(Prompt TPS)</sub> | 首字延遲<br><sub>(Time To First Token, TTFT)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 實體記憶體<br><sub>(RAM Usage)</sub> | 獨立驗證報告<br><sub>(Report)</sub> |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 **冠軍 (Champion)** | `deepseek-r1:1.5b` | 1.5B | **11.54 tok/s** | 183.09 tok/s | **0.243s** | 56.5°C | 1.84 GB | [📄 1.5B 報告](./benchmark/reports/deepseek-r1_1_5b_REPORT.md) |
| 🥈 **亞軍 (Runner-up)** | `gemma4:e2b` | 2.6B | **7.61 tok/s** | 99.16 tok/s | **0.585s** | 58.2°C | 8.55 GB | [📄 Gemma4 2B 報告](./benchmark/reports/gemma4_e2b_REPORT.md) |
| 🥉 **季軍 (Third Place)** | `qwen2.5:3b` | 3B | **6.02 tok/s** | 178.39 tok/s | **0.661s** | 56.5°C | 2.87 GB | [📄 Qwen 3B 報告](./benchmark/reports/qwen2_5_3b_REPORT.md) |
| **#4** | `llama3.2:3b` | 3B | **5.92 tok/s** | 164.10 tok/s | **0.629s** | 56.5°C | 3.39 GB | [📄 Llama 3B 報告](./benchmark/reports/llama3_2_3b_REPORT.md) |
| **#5** | `gemma4:e4b` | 4.3B | **3.71 tok/s** | 47.74 tok/s | **1.243s** | 57.1°C | 10.25 GB | [📄 Gemma4 4B 報告](./benchmark/reports/gemma4_e4b_REPORT.md) |
| **#6** | `qwen2.5-coder:7b` | 7B | **2.77 tok/s** | 80.20 tok/s | **1.744s** | 58.2°C | 5.23 GB | [📄 Coder 7B 報告](./benchmark/reports/qwen2_5-coder_7b_REPORT.md) |
| **#7** | `olmo2:7b` | 7B | **2.73 tok/s** | 94.08 tok/s | **1.549s** | 57.6°C | 12.37 GB | [📄 OLMo2 7B 報告](./benchmark/reports/olmo2_7b_REPORT.md) |
| **#8** | `olmo-3:7b` | 7B | **2.56 tok/s** | 51.90 tok/s | **3.436s** | 56.5°C | 13.05 GB | [📄 OLMo-3 7B 報告](./benchmark/reports/olmo-3_7b_REPORT.md) |
| **#9** | `deepseek-r1:7b` | 7B | **2.53 tok/s** | 38.29 tok/s | **1.384s** | 57.1°C | 5.23 GB | [📄 R1 7B 報告](./benchmark/reports/deepseek-r1_7b_REPORT.md) |
| **#10** | `llama3.1:8b` | 8B | **2.46 tok/s** | 46.62 tok/s | **1.620s** | 57.6°C | 5.76 GB | [📄 Llama 8B 報告](./benchmark/reports/llama3_1_8b_REPORT.md) |

> 📊 **Plan 1 完整統整評測報告 (Master Report):** 詳見 [PLAN1_FINAL_REPORT.md](./benchmark/reports/PLAN1_FINAL_REPORT.md) 與 [plan1.md](./plan1.md)。

---

### 🥈 Plan 2: 原生 llama.cpp (Native llama.cpp: ARMv8.2-a 點積向量加速 / 半精度浮點 DotProd & FP16)
在 **樹莓派 5 (Raspberry Pi 5: BCM2712 四核心 ARM Cortex-A76 @ 2.40 GHz, 16GB LPDDR4X 記憶體)** 上啟用編譯優化參數 `-mcpu=cortex-a76 -march=armv8.2-a+fp16+dotprod` 執行硬體極限微基準壓測 (Micro-benchmarking via `llama-bench`)：

| 排名<br><sub>(Rank)</sub> | 評測模型<br><sub>(Model Tag)</sub> | 參數量 / 檔案大小<br><sub>(Params / Size)</sub> | 生成吞吐率<br><sub>(Generation TPS)</sub> | 提示詞預填速度<br><sub>(Prefill TPS)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 實體記憶體佔用<br><sub>(Peak RAM)</sub> | 獨立驗證報告<br><sub>(Report)</sub> |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 **冠軍 (Champion)** | `deepseek-r1:1.5b` | 1.78B (1.04 GB) | **12.02 tok/s** | **60.66 tok/s** | 57.1°C | **0.59 GiB** | [📄 1.5B 報告](./benchmark/reports/plan2_deepseek-r1_1_5b_REPORT.md) |
| 🥈 **亞軍 (Runner-up)** | `gemma4:e2b` | 2.6B (6.67 GB) | **7.04 tok/s** | **45.44 tok/s** | 58.2°C | **3.20 GiB** | [📄 Gemma4 2B 報告](./benchmark/reports/plan2_gemma4_e2b_REPORT.md) |
| 🥉 **季軍 (Third Place)** | `qwen2.5:3b` | 3.09B (1.80 GB) | **6.01 tok/s** | **28.89 tok/s** | 56.5°C | **0.60 GiB** | [📄 Qwen 3B 報告](./benchmark/reports/plan2_qwen2_5_3b_REPORT.md) |
| **#4** | `llama3.2:3b` | 3.21B (1.88 GB) | **5.71 tok/s** | **27.23 tok/s** | 57.6°C | **0.62 GiB** | [📄 Llama 3B 報告](./benchmark/reports/plan2_llama3_2_3b_REPORT.md) |
| **#5** | `gemma4:e4b` | 4.3B (8.95 GB) | **3.68 tok/s** | **22.50 tok/s** | 62.1°C | **5.80 GiB** | [📄 Gemma4 4B 報告](./benchmark/reports/plan2_gemma4_e4b_REPORT.md) |
| **#6** | `qwen2.5-coder:7b` | 7.61B (4.36 GB) | **2.76 tok/s** | **11.59 tok/s** | 58.2°C | **0.46 GiB** | [📄 Coder 7B 報告](./benchmark/reports/plan2_qwen2_5-coder_7b_REPORT.md) |
| **#7** | `deepseek-r1:7b` | 7.61B (4.36 GB) | **2.70 tok/s** | **11.30 tok/s** | 58.7°C | **0.44 GiB** | [📄 R1 7B 報告](./benchmark/reports/plan2_deepseek-r1_7b_REPORT.md) |
| **#8** | `olmo2:7b` | 7.05B (4.16 GB) | **2.59 tok/s** | **11.59 tok/s** | 58.7°C | **6.37 GiB** | [📄 OLMo2 報告](./benchmark/reports/PLAN2_FINAL_REPORT.md) |
| **#9** | `llama3.1:8b` | 8.03B (4.58 GB) | **2.46 tok/s** | **10.69 tok/s** | 57.6°C | **0.43 GiB** | [📄 Llama 8B 報告](./benchmark/reports/plan2_llama3_1_8b_REPORT.md) |
| **#10** | `olmo-3:7b` | 6.95B (4.16 GB) | **2.37 tok/s** | **13.90 tok/s** | 65.3°C | **8.90 GiB** | [📄 OLMo-3 報告](./benchmark/reports/plan2_olmo-3_7b_REPORT.md) |

> 📊 **Plan 2 完整統整評測報告 (Master Report):** 詳見 [PLAN2_FINAL_REPORT.md](./benchmark/reports/PLAN2_FINAL_REPORT.md) 與 [plan2.md](./plan2.md)。

---

### 🥉 Plan 3: 10 大模型邊緣極限優化與調優前後實測 (Edge Extreme Optimization & Before-vs-After Benchmark)
針對 ARM Cortex-A76 四核心處理器進行 **處理器調節器效能鎖頻 (CPU Performance Governor Lock) 2.40 GHz**、**模型檔案上下文記憶體邊界約束 (Modelfile Context Bounding to 4k)**、**執行緒物理核心綁定 (4-Thread Core Pinning)** 及 **任務專項採樣超參數對齊 (Task-Specific Sampling Hyperparameters Alignment)** 前後的真實量化基準對比（單次生成標準化 150 個權杖 Tokens）：

#### 📊 優化前後核心性能全景對比總表 (Comprehensive Performance Matrix)

| 序號<br><sub>(No.)</sub> | 模型名稱<br><sub>(Model Tag)</sub> | 參數量<br><sub>(Params)</sub> | 輸入解析速度 (Prompt tok/s)<br><sub>優化前 $\to$ **優化後 (增幅 Gain)**</sub> | 生成吞吐量 (Eval tok/s)<br><sub>優化前 $\to$ **優化後 (增幅 Gain)**</sub> | 首次冷啟動時長 (Cold Load)<br><sub>優化前 $\to$ **優化後 (減幅 Reduction)**</sub> | 實體可用記憶體<br><sub>(Free RAM)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 獨立評測報告<br><sub>(Report)</sub> |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **01** | **`deepseek-r1:1.5b-opt`** | 1.77B | 69.50 $\to$ **73.44 (+5.7%)** | 11.96 $\to$ **12.08 tok/s** | 30.9s $\to$ **17.1s (-44.7%)** | **14.28 GB** | 57.1°C | [📄 1.5B 報告](./paper/10_optimization_report_deepseek_r1_1.5b.md) |
| **02** | **`gemma4:e2b-opt`** | 2.2B Text | 44.01 $\to$ **46.73 tok/s** | 7.24 $\to$ **7.64 tok/s (+5.5%)** | 60.6s $\to$ **28.8s (-52.5%)** | 12.65 GB | 55.4°C | [📄 Gemma4 2B 報告](./paper/09_optimization_report_gemma4_e2b.md) |
| **03** | **`qwen2.5:3b-opt`** | 3.09B | 34.78 $\to$ **35.27 tok/s (繁中對齊)** | 5.79 $\to$ **6.01 tok/s (+3.8%)** | 60.6s $\to$ **35.1s (-42.1%)** | **13.27 GB** | 51.0°C | [📄 Qwen 3B 報告](./paper/08_optimization_report_qwen2.5_3b.md) |
| **04** | **`llama3.2:3b-opt`** | 3.21B | 33.58 $\to$ **35.16 tok/s (英文極速)** | 5.94 $\to$ **5.94 tok/s** | 59.8s $\to$ **34.5s (-42.3%)** | 12.81 GB | 57.1°C | [📄 Llama 3B 報告](./paper/07_optimization_report_llama3.2_3b.md) |
| **05** | **`gemma4:e4b-opt`** | ~4.2B | 20.95 $\to$ **22.76 tok/s (+8.6%)** | 3.86 $\to$ **3.90 tok/s** | 103.2s $\to$ **53.5s (-48.2%)** | 10.92 GB | 54.9°C | [📄 Gemma4 4B 報告](./paper/06_optimization_report_gemma4_e4b.md) |
| **06** | **`deepseek-r1:7b-opt`** | 7.61B | 11.44 $\to$ **13.22 tok/s (+15.6%)** | 2.64 $\to$ **2.78 tok/s (+5.3%)** | 125.3s $\to$ **72.7s (-42.0%)** | 10.82 GB | 56.5°C | [📄 R1 7B 報告](./paper/02_optimization_report_deepseek_r1_7b.md) |
| **07** | **`qwen2.5-coder:7b-opt`**| 7.61B | 11.36 $\to$ **13.05 tok/s (+14.9%)** | 2.65 $\to$ **2.78 tok/s (+4.9%)** | 129.3s $\to$ **76.8s (-40.6%)** | 10.81 GB | 57.1°C | [📄 Coder 7B 報告](./paper/03_optimization_report_qwen2.5_coder_7b.md) |
| **08** | **`olmo2:7b-opt`** | 7.03B | 13.77 $\to$ **14.55 tok/s (+5.7%)** | 2.64 $\to$ **2.76 tok/s (+4.5%)** | 130.2s $\to$ **78.5s (-39.7%)** | 9.21 GB | 54.3°C | [📄 OLMo2 7B 報告](./paper/05_optimization_report_olmo2_7b.md) |
| **09** | **`olmo-3:7b-opt`** | 7.20B | 12.69 $\to$ **13.69 tok/s (+7.9%)** | 2.56 $\to$ **2.75 tok/s (+7.4%)** | 134.8s $\to$ **83.3s (-38.2%)** | 9.18 GB | 57.6°C | [📄 OLMo-3 7B 報告](./paper/04_optimization_report_olmo3_7b.md) |
| **10** | **`llama3.1:8b-opt`** | 8.03B | 11.28 $\to$ **12.21 tok/s (+8.2%)** | 2.40 $\to$ **2.61 tok/s (+8.8%)** | 4k 上下文防抖 (Jitter-Free) | 10.29 GB | 55.4°C | [📄 Llama 8B 報告](./paper/01_optimization_report_llama3.1_8b.md) |

#### 📈 四大維度優化量化收益深度剖析 (Deep-Dive Gains Analysis)
1. **輸入處理速度 (Prompt Evaluation Speed / TTFT) 提速顯著：**
   - 平均提速達 **+5% ~ +15.6%**。`deepseek-r1:7b` 躍升至 **13.22 tok/s**，`deepseek-r1:1.5b` 達到驚人的 **73.44 tok/s**，大幅消除前端對話的首字等待延遲 (Time-To-First-Token, TTFT)。
2. **初次冷啟動載入時長 (Cold-Start Load Latency) 腰斬 (-38% ~ -52.5%)：**
   - 原始模型預設分配高達 32k ~ 131k 超長預留視窗，造成龐大鍵值快取 (Key-Value Cache, KV Cache) 記憶體映射初始化耗時。
   - 透過模型檔案 (Modelfile) 約束 **4096 (4k) 上下文視窗 (Context Window)** 後，7B 模型冷啟動耗時自 130s 大幅降至 **72s ~ 83s (淨省 50 秒以上)**；2.2B 模型自 60s 降至 **28.8s (-52.5%)**。
3. **穩定生成吞吐率 (Generation Throughput) 逼近硬體物理極限：**
   - 7B/8B 旗艦模型全數穩定運行於 **2.60 ~ 2.78 tok/s**（逼近樹莓派 5 雙通道 LPDDR4X 17 GB/s 記憶體頻寬極限 Memory Bandwidth Wall）。
   - 3B 模型達到 **5.90 ~ 6.01 tok/s**（實現即時流式交談 Streaming Chat 流暢體驗）。
   - 1.5B/2.2B 模型達到 **7.64 ~ 12.08 tok/s**（達成邊緣秒級推理 Edge Instant Inference）。
4. **實體記憶體餘裕 (Physical RAM Margin) 與散熱穩定性 (Thermal Stability)：**
   - 運行 7B/8B 時系統實體剩餘記憶體 (Free RAM) 仍高達 **9.2 ~ 10.8 GB**；運行 3B 時剩餘 **12.8 ~ 13.2 GB**；運行 1.5B 時剩餘高達 **14.28 GB**。
   - 鎖頻 2.40 GHz 高負載連續矩陣乘法推論下，最高溫僅 **51.0°C ~ 57.6°C**，降頻暫存器 (`vcgencmd get_throttled`) 全程為 `0x0`（零降頻 Zero Throttling、零電壓不穩 Zero Undervoltage）。

```
                        [ Raspberry Pi 5 邊緣模型推論生成吞吐率 (Tokens/Sec) ]

  1.5B 微型思考模型   [==================================================] 12.08 tok/s  (deepseek-r1:1.5b-opt)
  2.2B 剪枝多模態     [===============================] 7.64 tok/s                     (gemma4:e2b-opt)
  3.1B 繁中旗艦       [========================] 6.01 tok/s                            (qwen2.5:3b-opt)
  3.2B 英文剪枝       [========================] 5.94 tok/s                            (llama3.2:3b-opt)
  4.2B 原生多模態     [================] 3.90 tok/s                                    (gemma4:e4b-opt)
  7.6B 代碼旗艦       [===========] 2.78 tok/s                                         (qwen2.5-coder:7b-opt)
  7.6B 深度推理       [===========] 2.78 tok/s                                         (deepseek-r1:7b-opt)
  7.0B 完全開放       [===========] 2.76 tok/s                                         (olmo2:7b-opt)
  7.2B 溯源推理       [===========] 2.75 tok/s                                         (olmo-3:7b-opt)
  8.0B 旗艦基底       [==========] 2.61 tok/s                                          (llama3.1:8b-opt)
                      0         2         4         6         8         10        12 (tok/s)
```

> 📊 **優化前後全維度量化深度對比總表 (Master Comparison):** 詳見 [optimization_comparison_table.md](./paper/optimization_comparison_table.md)。  
> 📑 **10 大模型論文研讀與選型指南專區 (Paper Compendium):** 詳見 [paper/README.md](./paper/README.md) 與 [10_models_comparison_matrix.md](./paper/10_models_comparison_matrix.md)。  
> 🎓 **學術論文選題與頂級文獻調研 (Research Topics & Survey):** 詳見 [surveyPaperTopic.md](./paper/surveyPaperTopic.md)。  
> 🛠️ **模型極限調優工程手冊 (Optimization Guide):** 詳見 [model_optimization_guide.md](./paper/model_optimization_guide.md)。


---

## ⚡ 核心發現與三大推論架構深度對比 (Three Major Inference Architectures Comparison)

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

| 評估維度<br><sub>(Dimension)</sub> | 原生編譯 llama.cpp<br><sub>(Native llama.cpp: DotProd Accelerated)</sub> | 原生系統服務 Ollama<br><sub>(Native Ollama: Host Daemon Service)</sub> | 容器化 Ollama<br><sub>(Dockerized Ollama: Container Service)</sub> |
| :--- | :--- | :--- | :--- |
| **推論生成吞吐量<br><sub>(Generation Throughput, TPS)</sub>** | **極致最高 (100% 物理極限 Physical Limit)** | **極高 (~95% - 98%)** | 中高 (~88% - 93%) |
| **記憶體額外開銷<br><sub>(Memory Overhead)</sub>** | **0 MB (純 POSIX 記憶體映射 Memory Mapping, mmap)** | ~30 MB (Go 語言執行時期 Go Runtime) | ~200 MB (容器守護行程 Containerd + 疊加檔案系統 OverlayFS) |
| **模型管理便利度<br><sub>(Developer Experience, DX)</sub>** | 手動下載 / 需指定大型二進位物件 (Binary Large Object, Blob) 路徑 | **一鍵指令快速拉取 (`ollama pull`)** | 一鍵指令快速拉取 (`ollama pull`) |
| **硬體感測器遙測整合<br><sub>(Hardware Telemetry Integration)</sub>** | **原生底層完整支援 (`vcgencmd`)** | **原生底層完整支援 (`vcgencmd`)** | 需高安全風險之特權模式提權 (`--privileged`) |
| **長文本前向預填加速<br><sub>(Long-Context Prefill Acceleration)</sub>** | **ARMv8.2-a 點積運算單指令多資料流極致向量加速 (DotProd SIMD)** | 依賴動態載入動態共享函式庫 (Dynamic Shared Libraries, .so) | 依賴容器內部動態共享函式庫 |

---

## 📂 專案檔案結構樹 (Repository Directory Structure)

```text
pi5-llm-arena/
├── README.md                           # 專案首頁與三階段極限評測排行榜 (Benchmark Leaderboard)
├── plan1.md                            # Plan 1 原生 Ollama 實施計畫書與評測報告彙整
├── plan1_cmd.md                        # Plan 1 完整指令集、工作流與問題排除手冊 (Troubleshooting Guide)
├── plan2.md                            # Plan 2 原生 llama.cpp 實施計畫書與三大架構深度剖析
├── plan2_cmd.md                        # Plan 2 原生編譯 llama.cpp 與 DotProd 壓測操作手冊
├── requirements.txt                    # Python 相依套件清單 (Dependencies)
├── paper/                              # 📚 10 大模型技術論文研讀、調優對比大表與實測報告庫
│   ├── README.md                       # 論文研讀專區與邊緣選型決策指南總覽 (Selection Guide)
│   ├── surveyPaperTopic.md             # 🎓 頂會級論文題目深度調研與 10 篇高引文獻綜述 (Academic Survey)
│   ├── 10_models_comparison_matrix.md  # 規格/機制/數據/特性 四維深度橫向技術比較矩陣
│   ├── optimization_comparison_table.md# ⚡ 調優前後全維度量化實測對比大表 (Optimization Comparison)
│   ├── model_optimization_guide.md     # 五大工程極限調優手段指南手冊 (Optimization Guide)
│   ├── 01_gemma4_e4b.md ~ 10_...       # 10 份個別模型技術論文深度剖析文件 (Technical Papers)
│   └── 01_optimization_report_...      # 10 份調優前後實測評測量化報告 (Benchmark Reports)
├── code_dispatcher/                    # 🚀 FastAPI + Redis Queue (RQ) 非同步任務調度閘道伺服器
│   ├── main.py                         # RESTful API 路由與硬體感測器遙測端點 (Telemetry Endpoints)
│   ├── tasks.py                        # Redis Queue 背景推論工作者任務 (Background Worker Tasks)
│   └── ui.html                         # 即時網頁聊天與代碼審查使用者介面 (Web UI & Code Reviewer)
├── benchmark/                          # 基準測試自動化工具庫 (Automated Benchmark Suites)
│   ├── benchmark_suite.py              # Plan 1 全自動評測套件 (測量 TTFT, TPS, 核心溫度, 記憶體)
│   ├── analyze_results.py              # Plan 1 統計數據彙整分析器 (Statistical Analyzer)
│   ├── plan2_benchmark_suite.py        # Plan 2 遠端調度微基準測試套件 (Remote Orchestrator)
│   ├── pi5_plan2_local_runner.py       # Plan 2 樹莓派本地零抖動守護壓測進程 (Zero-Jitter Runner)
│   ├── plan2_analyze_results.py        # Plan 2 雙引擎交叉對比報告產生器 (Cross-Engine Analyzer)
│   ├── logs/                           # Plan 1 原始推論對話日誌與指標 (Raw Logs)
│   ├── logs_plan2/                     # Plan 2 llama-bench 原始微基準測試日誌 (Micro-benchmark Logs)
│   ├── reports/                        # Markdown 評測報告集散庫 (Markdown Benchmark Reports)
│   │   ├── deepseek-r1_1_5b_REPORT.md
│   │   ├── plan2_deepseek-r1_1_5b_REPORT.md
│   │   ├── ...
│   │   ├── PLAN1_FINAL_REPORT.md       # Plan 1 最終統整主報告 (Master Report)
│   │   └── PLAN2_FINAL_REPORT.md       # Plan 2 最終統整主報告 (Master Report)
│   └── results/                        # JSON 格式評測結果數據庫 (Benchmark Results Database)
│       ├── master_benchmark_summary.json
│       └── plan2_benchmark_summary.json
```

---

## 🛠️ 重現評測步驟指南 (How to Reproduce the Benchmarks)

### 1. 執行 Plan 1 (原生 Ollama API 評測 / Native Ollama Benchmark)
```bash
python benchmark/benchmark_suite.py
python benchmark/analyze_results.py
```

### 2. 執行 Plan 2 (原生編譯 llama.cpp 向量加速評測 / Native llama.cpp Benchmark)
```bash
# 在樹莓派 5 上編譯含 ARM Cortex-A76 向量擴充指令之原生 llama.cpp
cmake -B build -G Ninja -DGGML_CPU_AARCH64=ON -DCMAKE_C_FLAGS="-mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod"
cmake --build build --config Release -j4 --target llama-bench

# 執行本地守護壓測進程並產生雙引擎交叉對比報告
python3 benchmark/pi5_plan2_local_runner.py
python3 benchmark/plan2_analyze_results.py
```
