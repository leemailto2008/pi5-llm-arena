# Llama 3.1 8B: 工業級開源語言模型基準研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *The Llama 3 Herd of Models*
- **研發機構 (Organization):** Meta AI
- **主要作者 (Authors):** Abhimanyu Dubey, Junteng Jia, Derek Liu, et al. (超過數百位研究員)
- **發布時間 (Release Date):** 2024 年 7 月
- **論文連結 (arXiv):** [arXiv:2407.21783](https://arxiv.org/abs/2407.21783)
- **開源許可證 (License):** Llama 3.1 Community License (開放研究與每月活躍用戶 7 億以下免費商用)

---

## 2. 核心架構與工程設計 (Architecture & Engineering)

### 2.1 模型規格參數 (Specifications)
| 參數項目 (Metric) | 數值 / 配置 (Value) |
| :--- | :--- |
| **總參數量 (Parameters)** | 8.03B (80 億參數) |
| **詞彙表大小 (Vocabulary Size)** | **128,256 (128k Tiktoken)** |
| **隱藏層維度 (Hidden Dimension)** | 4096 (共 32 層 Transformer) |
| **注意力頭數 (Attention Heads)** | 32 Query Heads, 8 Key-Value Heads (GQA 4:1) |
| **上下文長度 (Context Length)** | **131,072 Tokens (128k)** |
| **位置編碼 (Positional Encoding)** | RoPE (Base Frequency 調整至 500,000 以原生支援超長 Context) |
| **前饋網路 (FFN)** | SwiGLU (Intermediate Size = 14336) |

### 2.2 論文關鍵亮點與技術貢獻
1. **龐大的高質量預訓練語料 (15 Trillion Tokens)**：
   - 相比 Llama 2 的 2T Tokens，資料量激增 7.5 倍，遠超 Chinchilla Optimal 預測的收斂點，實現顯著的「過度訓練 (Over-training)」，使 8B 尺寸在邊緣端能發揮出遠超參數量級別的泛化潛力。
2. **多語言與代碼混合佔比**：
   - 包含超過 5% 的非英語多語言數據（支援 30 種以上主要語言）以及 4 倍以上的代碼數據。
3. **後訓練循環對齊 (Iterative Post-Training)**：
   - 結合 SFT (Supervised Fine-Tuning)、Rejection Sampling、以及 DPO (Direct Preference Optimization) 多輪迭代，消除幻覺並強化遵循複雜指令 (Complex Instruction Following) 的能力。

---

## 3. 邊緣運算優化特徵 (Edge Adaptation)

- **GQA (Grouped-Query Attention) 帶來的低 KV 快取開銷**：
  在 8B 模型上，KV 記憶體佔用僅有純 MHA (Multi-Head Attention) 的 $\frac{1}{4}$。即使在 Pi 5 上處理 8k ~ 16k 長度文本，KV Cache 也不會撐爆 16GB 實體記憶體。
- **高密度詞彙表 (128k Vocab)**：
  大幅提升中文與程式碼的 Token 壓縮率（Compression Ratio），降低生成同樣語義所需運算的總 Token 數量。

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **磁碟與 RAM 佔用:** 約 **4.9 GB**
- **CPU 運算速度 (ARM Cortex-A76 4 核心):**
  - **推論速度:** 約 **2.2 ~ 2.5 tok/s**。
  - **溫度與發熱:** 滿載推論時約 58 ~ 61°C。
- **結論與推薦定位:**
  - Llama 3.1 8B 是目前業界生態最完善、工具支援最廣泛的 8B 模型。適合用作高精度總結、多語言翻譯與基準比對。
