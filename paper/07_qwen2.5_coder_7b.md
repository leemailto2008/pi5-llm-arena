# Qwen2.5-Coder 7B: 專業程式碼與軟體工程大模型研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *Qwen2.5-Coder Technical Report: Code You Can Count On*
- **研發機構 (Organization):** Alibaba Cloud Qwen Team
- **主要作者 (Authors):** Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, et al.
- **發布時間 (Release Date):** 2024 年 9 月 (並於 11 月全面開源 0.5B ~ 32B 全矩陣)
- **論文連結 (arXiv):** [arXiv:2409.12186](https://arxiv.org/abs/2409.12186)
- **開源許可證 (License):** Apache 2.0 (完全開放權重、商用無限制)

---

## 2. 核心架構與預訓練數據工程 (Architecture & Training)

### 2.1 模型規格參數 (Specifications)
| 參數項目 (Metric) | 數值 / 配置 (Value) |
| :--- | :--- |
| **參數量 (Parameters)** | 7.61B |
| **詞彙表大小 (Vocabulary Size)** | 151,936 (152k，代碼符號壓縮率極高) |
| **隱藏維度 (Hidden Size)** | 3584 (共 28 層) |
| **注意力頭數 (Attention Heads)** | 28 Query Heads / 4 KV Heads (GQA 7:1) |
| **上下文長度 (Context Window)** | **131,072 Tokens (128k)** (原生支援超長倉庫級代碼庫理解) |
| **前饋層擴展 (Intermediate Size)** | 18944 (SwiGLU) |

### 2.2 程式碼專精技術突破
1. **高達 5.5 兆 (5.5 Trillion) Tokens 的代碼預訓練語料**：
   - 涵蓋 92 種主流程式語言（Python, C/C++, Java, Go, Rust, TypeScript, Bash, SQL, Verilog 等）。
   - 深度結合合成代碼 (Synthetic Code)、單元測試生成與程式執行反饋過濾 (Execution-Guided Filtering)。
2. **中間填空補全機制 (Fill-in-the-Middle, FIM)**：
   - 訓練階段以高比例混合 `<fim_prefix>`, `<fim_suffix>`, `<fim_middle>` 格式，賦予模型在代碼中間補全、即時 Copilot 內嵌推薦的超強能力。
3. **長上下文代碼推理 (Repo-Level Reasoning)**：
   - 支援 128k 窗口，能一口氣吞入整個 Git Repository 的架構定義與相依函式庫，精準完成跨檔案呼叫分析 (Cross-File Reference Resolution)。

---

## 3. 業界評測成就 (Benchmark Achievements)

- 在國際知名權威代碼基準測試中：
  - **HumanEval (Python)** 達 **88.4%**。
  - **EvalPlus (嚴格單元測試)** 超越同量級甚至 34B 的前代模型。
  - **SWE-bench / Aider (真實軟體工程除錯修復)** 達到開源 7B 模型的歷史最高分，甚至媲美 GPT-4o-mini。

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **權重佔用 (Disk / RAM):** 約 **4.7 GB**
- **CPU 運算速度 (ARM Cortex-A76 4 核心):**
  - **推論速度:** 穩定在 **2.5 ~ 2.7 tok/s**。
  - **散熱與功耗:** 在 Pi 5 主動散熱片下，持續生成溫度穩定於 57 ~ 59°C。
- **最佳適用場景:**
  - **非同步代碼審查與重構 (Asynchronous Code Review)**：如本專案設計之 Redis Queue Worker，在背景自動審查 SQL 注入、時間複雜度缺陷與交易回滾。
  - **本地離線代碼助手**：保護專有代碼資產不流出本機內網。
