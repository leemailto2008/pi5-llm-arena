# OLMo 3 7B: 支援長上下文與推理思考的完全開源模型研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *OLMo 3: Open Reasoning and Long-Context Language Models*
- **研發機構 (Organization):** Allen Institute for AI (Ai2)
- **發布時間 (Release Date):** 2025 年 11 月
- **開源許可證 (License):** Apache 2.0 (全生命週期開源：含 Dolma 3 數據、訓練日誌、OLMoTrace)
- **模型系列 (Model Family):** OLMo 3 (提供 7B 與 32B 兩種尺寸；包含 Base, Instruct, Think 與 RL Zero 變形)

---

## 2. 核心架構與技術升級 (Architecture & Major Upgrades)

### 2.1 模型規格參數 (Specifications)
| 參數項目 (Metric) | 數值 / 配置 (Value) |
| :--- | :--- |
| **參數量 (Parameters)** | 7.3B |
| **上下文長度 (Context Window)** | **65,536 Tokens (64k)** (大幅超越 OLMo 2 的 4k) |
| **隱藏維度 (Hidden Size)** | 4096 |
| **注意力機制 (Attention)** | 滑動窗口注意力 (Sliding Window Attention, SWA) 結合 GQA |
| **長文本擴展機制** | YaRN (Yet another RoPE extensioN) 位置頻率插值 |
| **原生推理支援 (Thinking)** | 支援 `<think>...</think>` 推理輸出模式 |

### 2.2 核心突破點：Dolma 3 數據集與 OLMoTrace 可溯源技術
1. **Dolma 3 預訓練語料 (5.9T Tokens)**：
   - 相比前代，大幅增加科學論文 (arXiv / PubMed)、代碼儲存庫 (GitHub) 與數學題目（MATH / OlympiadBench）。
   - 採用多階段數據退火 (Data Annealing)，在預訓練後期注入高質量合成 Reasoning 語料。
2. **OLMoTrace 技術**：
   - 允許開發者與審計人員將模型的特定輸出或推論步驟，逆向追溯到訓練集中的具體文檔與權重梯度，是目前可解釋性 (Explainability) 最高的開源模型。

---

## 3. 推理思考模式 (Thinking Mode Mechanism)

- OLMo 3-Think 引入類似 DeepSeek-R1 的自我反思 (Self-Correction) 機制：
  - 在輸出最終答案前，模型會在 `<think>` 標籤中自發性地進行多方案推演、矛盾檢查與邏輯驗證。
  - 此機制顯著提升了其在 GSM8k 與競技編程 (Competitive Programming) 上的準確率，但相應地會增加生成的 Token 總數。

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **記憶體佔用 (RAM Usage):** 約 **4.6 GB** (若開啟長 Context 64k，KV 快取需預留額外約 1.5 ~ 2 GB RAM)
- **CPU 運算特性 (ARM Cortex-A76 4 核心):**
  - **常規模式推論速度:** 約 **2.5 ~ 2.7 tok/s**。
  - **Thinking 模式注意事項:** 因為模型會先輸出思考鏈，單次問答總生成 Tokens 往往超過 400 ~ 600，在 Pi 5 上需耗時 150 ~ 250 秒。
- **邊緣端部署結論:**
  - 適合需要「完全透明可解釋性、無產權爭議」的本地隱私資料審計系統。
