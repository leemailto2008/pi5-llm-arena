# Gemma 4 E4B: 邊緣多模態與高能效思考架構研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *Gemma 4: Open Multimodal Models Built for Edge & Cloud*
- **研發機構 (Organization):** Google DeepMind
- **發布時間 (Release Date):** 2026 年 4 月
- **開源許可證 (License):** Apache 2.0 (完全開放權重與商業許可)
- **模型定位 (Target Segment):** 端側高階邊緣設備 (Edge AI)、具備視覺與音訊輸入能力的多模態推理微模型 (Multimodal Edge LLM)

---

## 2. 核心架構與技術創新 (Architecture & Key Innovations)

### 2.1 模型規格參數 (Specifications)
| 參數項目 (Metric) | 數值 / 配置 (Value) |
| :--- | :--- |
| **總參數量 (Total Parameters)** | ~8.0B (含跨模態視覺/音訊投影層) |
| **有效文字參數量 (Active Text Params)** | ~4.2B |
| **上下文長度 (Context Window)** | **131,072 Tokens (128k)** |
| **隱藏層維度 (Hidden Dimension)** | 2560 |
| **注意力機制 (Attention)** | 分組查詢注意力 (Grouped-Query Attention, GQA) + 滑動窗口 (Sliding Window) |
| **位置編碼 (Positional Encoding)** | 旋轉位置編碼 (RoPE, 帶高頻頻率擴展) |
| **激活函式 (Activation Function)** | GeGLU / SwiGLU 變形架構 |

### 2.2 創新機制：層級嵌入 (Per-Layer Embeddings, PLE)
在傳統 Transformer 中，Token Embedding 僅作用於第一層輸入。Gemma 4 E4B 引入了由 Gemini 3 技術下放的 **PLE (Per-Layer Embeddings)** 機制：
- 在不同 Transformer Block 之間動態注入縮放後的層級語意投影向量。
- 此設計允許模型在極小的端側參數量下（4B 等級），維持高層語義概念的深度表徵，大幅改善小型模型在多步推理時「注意力散焦」與「長距離記憶喪失」的通病。

### 2.3 原生多模態與思考模式 (Native Multimodal & Thinking Mode)
- **Encoder-free 投影**：不同於以往需額外載入龐大的 ViT (Vision Transformer) 骨幹，E4B 採用輕量化視覺 Patch Tokenizer，圖像直接交錯投影至同一 Embedding 空間。
- **Thinking Mode (思考鏈)**：支援原生 `<thought>...</thought>` 推理標籤，透過內隱思考鏈 (Internal Chain-of-Thought) 在回答複雜邏輯前進行多步驗證。

---

## 3. 訓練管線與數據集 (Training Pipeline & Data)

1. **預訓練數據 (Pre-training):**
   - 採用超過 **8 兆 (8T) Tokens** 的多語言多模態數據集進行訓練。
   - 包含高比例代碼 (Code)、STEM 科學論文、數學推導及高品質合成對話數據。
2. **後訓練與強化學習 (Post-Training & RL):**
   - 採用 **RLHF (Reinforcement Learning from Human Feedback)** 搭配基於自我博弈 (Self-Play) 的驗證機制。
   - 特別針對 Tool-use (函式呼叫 Function Calling) 與 Agentic 工作流進行專項微調。

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **權重佔用大小 (Disk / RAM):** 約 **4.8 GB** (載入至 16GB Pi 5 僅佔用不到 33% 實體記憶體)
- **CPU 運算特性 (ARM Cortex-A76 4 核心):**
  - **預期生成速度:** 約 **4.2 ~ 5.5 tok/s**。
  - **適用情境:** 邊緣多模態物聯網閘道 (IoT Gateway)、端側視覺物體辨識結合文字問答、輕量 Agent 自主決策。
- **優缺點評估 (Pros & Cons):**
  - **優點:** 具備 128k 超長上下文；支援原生多模態與思考標籤；由 DeepMind 官方 Apache 2.0 授權。
  - **缺點:** 因包含視覺投影層，單純文字生成速度略慢於純文字微模型（如 3B 模型）。
