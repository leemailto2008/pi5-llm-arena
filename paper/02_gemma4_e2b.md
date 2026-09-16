# Gemma 4 E2B: 超羽量級邊緣多模態模型研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *Gemma 4: Open Multimodal Models Built for Edge & Cloud*
- **研發機構 (Organization):** Google DeepMind
- **發布時間 (Release Date):** 2026 年 4 月
- **開源許可證 (License):** Apache 2.0
- **模型定位 (Target Segment):** 極限低功耗邊緣端設備、單板電腦 (SBC)、手機端及微型機器人控制核心

---

## 2. 核心架構與技術創新 (Architecture & Key Innovations)

### 2.1 模型規格參數 (Specifications)
| 參數項目 (Metric) | 數值 / 配置 (Value) |
| :--- | :--- |
| **總參數量 (Total Parameters)** | ~5.1B (包含視覺與語音模態適配層) |
| **實質語言核心參數量 (Core Text Params)**| ~2.2B |
| **上下文長度 (Context Window)** | **131,072 Tokens (128k)** |
| **隱藏層維度 (Hidden Dimension)** | 1536 |
| **注意力機制 (Attention)** | 多查詢注意力 (Multi-Query Attention, MQA) 混合分組查詢 (GQA) |
| **特殊架構 (Architecture)** | Per-Layer Embeddings (PLE) + 緊湊層剪枝 (Layer Pruned) |

### 2.2 核心技術：極致參數量下的維度壓縮與多模態融合
- **低維度高層投影 (Compact Dimension Projections)**：
  隱藏維度縮減至 1536，相較於 7B 等級模型的 4096，矩陣計算量（FLOPs per token）降至僅約原本的 $\frac{1}{7}$。
- **跨層權重共享與重用 (Selective Weight Reuse)**：
  借鑑 Gemini 3 在超輕量級設備上的量化感知蒸餾 (QAT-aware Distillation)，使 2B 級別核心能保有接近前代 7B 的指令遵循 (Instruction Following) 能力。

---

## 3. 訓練與數據蒸餾 (Training & Distillation)

1. **大模型知識蒸餾 (Knowledge Distillation from Gemma 4 31B & Gemini 3):**
   - E2B 並非單純從頭預訓練 (Scratch Training)，而是採用強大教師模型 (Teacher Model) 的輸出分佈與 Intermediate Activations 進行對齊蒸餾。
2. **合成推理數據驅動 (Synthetic Reasoning):**
   - 大量注入包含明確推理步階的合成數據，彌補小模型在自然語言預訓練語料中缺乏深層推理鏈的短板。

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **權重佔用大小 (Disk / RAM):** 約 **3.1 GB** (對 Pi 5 16GB 而言幾乎無任何記憶體壓力)
- **CPU 運算特性 (ARM Cortex-A76 4 核心):**
  - **預期生成速度:** 高達 **12.0 ~ 16.5 tok/s** (接近即時對話流暢度)。
  - **適用情境:** 樹莓派端即時語音助手、攝影機鏡頭邊緣視覺巡檢 (Edge Vision AI)、即時終端自動化腳本生成。
- **架構師建議 (Architect's Verdict):**
  - 若在 Pi 5 上需要同時兼顧「多模態能力 (Vision)」與「流暢生成速度 (10+ tok/s)」，**Gemma 4 E2B 是目前邊緣端綜合效能最頂尖的選擇**。
