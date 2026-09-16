# 10 大邊緣 AI 模型全維度深度橫向比較矩陣 (10 AI Models Comprehensive Comparison Matrix)

本文件針對部署於 **Raspberry Pi 5 (8GB/16GB, ARM Cortex-A76)** 之 10 款主流開源大語言與多模態模型，提供資深主任工程師 (Senior Staff Engineer & Architect) 視角的全維度技術對比。

---

## 一、模型規格參數橫向對比表 (Model Specifications & Architecture)

| 模型名稱 (Model Tag) | 參數量 (Parameters) | 注意力機制 (Attention) | 隱藏維度 / 層數 (Hidden / Layers) | 詞表大小 (Vocab Size) | 上下文長度 (Context Window) | 獨立分析報告 (Report Link) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E4B** | 9.6B Total (~4B Text) | PLE + Multi-Head (MHA) | 2560 / 28 層 | 256,000 | 131,072 (128k) | [01_gemma4_e4b.md](file:///f:/12_prj_raspi5/paper/01_gemma4_e4b.md) |
| **Gemma 4 E2B** | 5.1B Total (~2.2B Text) | PLE + Depth-Pruned | 2048 / 24 層 | 256,000 | 131,072 (128k) | [02_gemma4_e2b.md](file:///f:/12_prj_raspi5/paper/02_gemma4_e2b.md) |
| **OLMo 2 7B** | 7.03B | GQA 4:1 (32 Q / 8 KV) | 4096 / 28 層 | 100,288 | 4,096 (4k) | [03_olmo2_7b.md](file:///f:/12_prj_raspi5/paper/03_olmo2_7b.md) |
| **OLMo 3 7B** | 7.20B | GQA 4:1 + SWA 4k 窗口 | 4096 / 32 層 | 100,288 | 65,536 (64k) | [04_olmo3_7b.md](file:///f:/12_prj_raspi5/paper/04_olmo3_7b.md) |
| **Llama 3.1 8B** | 8.03B | GQA 4:1 (32 Q / 8 KV) | 4096 / 32 層 | 128,256 | 131,072 (128k) | [05_llama3.1_8b.md](file:///f:/12_prj_raspi5/paper/05_llama3.1_8b.md) |
| **DeepSeek-R1 7B** | 7.61B | GQA 4:1 (28 Q / 4 KV) | 3584 / 28 層 | 152,064 | 131,072 (128k) | [06_deepseek_r1_7b.md](file:///f:/12_prj_raspi5/paper/06_deepseek_r1_7b.md) |
| **Qwen2.5-Coder 7B**| 7.61B | GQA 4:1 (28 Q / 4 KV) | 3584 / 28 層 | 152,064 | 131,072 (128k) | [07_qwen2.5_coder_7b.md](file:///f:/12_prj_raspi5/paper/07_qwen2.5_coder_7b.md) |
| **Qwen2.5 3B** | 3.09B | GQA 8:1 (16 Q / 2 KV) | 2048 / 36 層 | 151,936 | 32,768 (32k) | [08_qwen2.5_3b.md](file:///f:/12_prj_raspi5/paper/08_qwen2.5_3b.md) |
| **Llama 3.2 3B** | 3.21B | GQA 3:1 (24 Q / 8 KV) | 3072 / 28 層 | 128,256 | 131,072 (128k) | [09_llama3.2_3b.md](file:///f:/12_prj_raspi5/paper/09_llama3.2_3b.md) |
| **DeepSeek-R1 1.5B**| 1.77B | GQA 6:1 (12 Q / 2 KV) | 1536 / 28 層 | 151,936 | 131,072 (128k) | [10_deepseek_r1_1.5b.md](file:///f:/12_prj_raspi5/paper/10_deepseek_r1_1.5b.md) |

---

## 二、核心創新機制橫向對比表 (Core Innovations & Novel Mechanisms)

| 模型名稱 (Model Tag) | 核心創新機制 (Key Architectural Innovations) | 結構化壓縮與推理優化技術 (Optimization & Inference Techniques) |
| :--- | :--- | :--- |
| **Gemma 4 E4B** | - **層級嵌入 (Per-Layer Embeddings, PLE)**：各層共享跨層表示，大幅降低冗餘參數。<br>- **原生視覺/音訊對齊**：多模態特徵投影直通主幹。<br>- **內建思考標籤 (Thinking Tag)**：支援端側推理解析步驟。 | - 模態投影矩陣動態量化。<br>- 128k 長序列 Flash-Attention 優化。 |
| **Gemma 4 E2B** | - **深度剪枝 (Depth Pruning) + 跨層權重共享**。<br>- 超輕量視覺 Token 壓縮編碼器。 | - 針對物聯網邊緣推論硬體極限壓縮。<br>- ARM NEON 4-bit 權重載入加速。 |
| **OLMo 2 7B** | - **全開放架構 (2 Overt 2 Furious)**：開放權重、訓練日誌、中繼檢查點。<br>- **QK-Norm**：注意力層前後引入 LayerNorm，防止半精度下注意力值溢位。 | - SwiGLU 激活函數與 RoPE 旋轉位置編碼。<br>- 權重分佈對齊 IEEE-754 數值穩定性。 |
| **OLMo 3 7B** | - **OLMoTrace 全流程可溯源機制**：可逆向查詢生成依據。<br>- **滑動窗口注意力 (Sliding Window Attention, SWA)**：局部窗口與全局 RoPE 混合。 | - 64k 上下文透過 SWA 降低記憶體複雜度至 $O(N \times W)$。<br>- 長短思考鏈可動態切換。 |
| **Llama 3.1 8B** | - **128k Tiktoken 超大詞表**：多語言分詞壓縮比大幅提昇。<br>- **8-Head KV 分組注意力 (GQA)**：將推論時 KV Cache 壓縮 4 倍。 | - RoPE 頻率縮放 (Frequency Scaling)，支援穩定外推至 128k。<br>- 深度矩陣正交化預防退化。 |
| **DeepSeek-R1 7B** | - **GRPO (Group Relative Policy Optimization)**：捨棄傳統價值模型 (Critic)，直接透過分組採樣相對評分優化。<br>- **深度思考鏈蒸餾 (CoT Distillation)**：自 671B 旗艦模型提煉長思考步驟。 | - 推理思考鏈 (Thinking Tokens) 與最終回應分離輸出架構。<br>- 針對數學與邏輯邊界條件之驗證器強化。 |
| **Qwen2.5-Coder 7B**| - **代碼中間填空 (Fill-in-the-Middle, FIM)**：支援光標處上下文預測。<br>- **倉庫級代碼庫推理 (Repo-level Reasoning)**：128k 全文件夾符號相依圖解析。 | - 語法樹引導 (AST-guided) 數據加權。<br>- 編程特定 Tokenizer 擴充。 |
| **Qwen2.5 3B** | - **極致 GQA (8:1)**：2 個 KV 頭服務 16 個 Query 頭，KV 記憶體佔用極低。<br>- **深窄架構 (Deep-and-Narrow)**：36 層深度，提供超越同級 3B 的非線性表達能力。 | - 專注邊緣端高並發低顯存佔用。<br>- 支援雙 RoPE 頻率切換 (32k / 128k)。 |
| **Llama 3.2 3B** | - **結構化剪枝 (Structured Pruning)**：自 8B 骨幹移除 4 層並縮減隱藏維度至 3072。<br>- **雙軌知識蒸餾 (Two-Stage Distillation)**：採用 KL 散度損失對齊 logits 與層級隱藏態。 | - 剪枝後保留 8B 大部分注意力注意力頭結構。<br>- 邊緣設備低延遲秒級啟動。 |
| **DeepSeek-R1 1.5B**| - **端側極限思考模型**：基於 Qwen2.5-Math-1.5B，融入 R1 80 萬高質量推理思考數據。<br>- **純策略優化蒸餾**：讓 1.77B 參數發揮高階符號運算能力。 | - 最小記憶體代價換取 AIME/MATH 頂級表現。<br>- 單線程高效解題。 |

---

## 三、訓練管線與數據集橫向對比表 (Training Pipeline & Datasets)

| 模型名稱 (Model Tag) | 預訓練語料規模 (Tokens) | 預訓練語料特色 (Pre-training Data Highlights) | 後訓練與對齊方法 (Post-Training & Alignment) |
| :--- | :--- | :--- | :--- |
| **Gemma 4 E4B** | **8 兆 (8T)** | 多語言多模態、大量 STEM 與代碼、Google 內部高品質合成語料。 | RLHF + 基於自我博弈 (Self-Play) 的 Tool-use / Agentic 微調。 |
| **Gemma 4 E2B** | **5 兆 (5T)** | 經 E4B 蒸餾篩選之精煉多模態數據流與簡化視覺對齊資料。 | 跨模型知識蒸餾 (KD) + 輕量級 DPO 指令微調。 |
| **OLMo 2 7B** | **4 兆 (4T)** | **Dolma 2 語料庫**：完全公開的網頁、Reddit、學術論文、原始代碼。 | **Tulu 3 管線**：SFT (精選提示詞) + DPO (直接偏好優化)。 |
| **OLMo 3 7B** | **6 兆 (6T)** | **Dolma 3 語料庫**：包含全流程代碼演進、長文獻以及合成思考數據。 | 在線強化學習 (Online RL) + 動態思考鏈 (Thinking CoT) SFT。 |
| **Llama 3.1 8B** | **15 兆 (15T)** | 超飽和語料 (Over-training)、50% 以上高質量代碼、30+ 語言。 | 多輪 RLHF + DPO + 迭代式拒絕採樣 (Rejection Sampling)。 |
| **DeepSeek-R1 7B** | **18T (Qwen 骨幹)** | Qwen2.5 預訓練海量基礎語料。 | **蒸餾自 DeepSeek-R1**：80 萬條純 RL 生成之長思考鏈數據 SFT。 |
| **Qwen2.5-Coder 7B**| **5.5 兆 (5.5T)** | **純代碼與數學專項語料**：覆蓋 92 種程式語言、GitHub 開源倉庫。 | 代碼執行反饋 (Compiler Feedback) + 多輪代碼修復強化學習。 |
| **Qwen2.5 3B** | **18 兆 (18T)** | 海量多語言多領域數據，中文、英文及亞洲語系比重極高。 | 系統化安全對齊、多階 SFT 與高階數學/指令 DPO。 |
| **Llama 3.2 3B** | **9 兆 (9T) 恢復訓練** | 自 8B 剪枝後，投入 9T 高質量多語言數據進行持續恢復預訓練。 | 與 Llama 3.1 70B/405B 進行 Logits 級知識蒸餾 + DPO。 |
| **DeepSeek-R1 1.5B**| **18T (Math 骨幹)** | Qwen2.5-Math 基礎數學運算與邏輯推理語料。 | **蒸餾自 DeepSeek-R1**：專注複雜數學、競賽題與邏輯推理之 CoT SFT。 |

---

## 四、邊緣設備硬體適配與特性剖析 (Pi 5 Hardware Profiling & Edge Viability)

> 基準環境：Raspberry Pi 5 (8GB/16GB), Broadcom BCM2712 4-Core ARM Cortex-A76 @ 2.4GHz, 採用 `Q4_K_M` 量化與 Ollama 引擎。

| 模型名稱 (Model Tag) | 量化後實體記憶體佔用 (RAM) | 邊緣推論速度 (Tokens/Sec) | 核心優勢 (Pros) | 局限性與缺點 (Cons) | 邊緣推薦定位 (Tier & Role) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E4B** | 約 4.8 GB | **4.2 ~ 5.5** | 原生視覺/音訊多模態、128k 上下文、Apache 2.0 商業授權友好。 | 多模態投影矩陣使單純文字生成較 3B 慢。 | **Tier 2: 邊緣物聯網視覺/多模態 Gateway** |
| **Gemma 4 E2B** | 約 2.6 GB | **12 ~ 16** | 極限輕量、快速流式輸出、具備邊緣影像理解能力。 | 複雜代碼推理與嚴謹邏輯能力略低於 7B/8B。 | **Tier 1: 即時邊緣端多模態流式助理** |
| **OLMo 2 7B** | 約 4.3 GB | **2.4 ~ 3.0** | 100% 透明可驗證、無學術倫理黑盒、穩健規範。 | 4k 上下文長度在現代模型中偏短。 | **Tier 3: 開源研究/訓練審計/RQ 佇列批處理** |
| **OLMo 3 7B** | 約 4.5 GB | **2.2 ~ 2.8** | 64k SWA 長上下文、OLMoTrace 數據溯源、具備思考模式。 | 啟動思考鏈時總生成 Token 數暴增，需佇列等待。 | **Tier 3: 深度可溯源文檔推理 (非同步)** |
| **Llama 3.1 8B** | 約 4.9 GB | **2.0 ~ 2.5** | 15T 訓練基底無比紮實、指令遵循頂級、生態相容度第一。 | Pi 5 記憶體頻寬吃緊，長上下文時首字延遲 (TTFT) 較高。 | **Tier 3: 旗艦級文本分析與架構設計 (非同步)** |
| **DeepSeek-R1 7B** | 約 4.7 GB | **2.1 ~ 2.6** | 具備自主反思與修復之長思考鏈 (CoT)、數學與演算法能力頂尖。 | 回應前需長達 1000+ tokens 思考，不適合即時 Web 聊天。 | **Tier 3: 困難演算法/競賽題/深度邏輯 (RQ 佇列)** |
| **Qwen2.5-Coder 7B**| 約 4.7 GB | **2.2 ~ 2.7** | 代碼生成與 Bug 修復無可匹敵、128k 代碼庫推理、FIM 補全。 | 生成長代碼耗時長，必須透過非同步佇列解耦。 | **Tier 3: 代碼審查/自動重構 Gateway 專用** |
| **Qwen2.5 3B** | 約 1.9 GB | **16 ~ 20** | 記憶體佔用極低 (<2GB)、繁中與常識理解頂尖、秒級流式回覆。 | 超長複雜多步推導有幻覺風險。 | **Tier 1: 網頁互動/高頻對話/Edge 首選** |
| **Llama 3.2 3B** | 約 2.0 GB | **18 ~ 22.5** | 推論速度極快、128k 上下文、英文指令遵循與摘要極強。 | 繁體中文理解力相較 Qwen 略顯平淡。 | **Tier 1: 快速英文摘要/即時邊緣端 API 路由器** |
| **DeepSeek-R1 1.5B**| 約 1.1 GB | **22 ~ 28.5** | 僅佔 1.1GB RAM、推論逼近 30 tok/s、數學推理顯著超越普通 3B。 | 一般人文對話、多輪閒聊與格式化 JSON 能力較弱。 | **Tier 1: 邊緣即時數理運算/輕量代碼單元測試** |

---

## 五、Raspberry Pi 5 邊緣部署決策架構矩陣 (Edge Deployment Strategy)

```mermaid
graph TD
    UserReq[使用者推播代碼/查詢請求] --> Dispatcher{任務類型判斷}
    
    Dispatcher -->|即時對話 / 快速摘要| Tier1[Tier 1: 即時秒級回應 (15~28 tok/s)]
    Dispatcher -->|邊緣影像 / 視覺物體問答| Tier2[Tier 2: 端側多模態 (4~16 tok/s)]
    Dispatcher -->|深度代碼審查 / 複雜推導 / 長文分析| Tier3[Tier 3: Redis Queue 非同步佇列 (2~3 tok/s)]

    Tier1 --> T1A[Qwen2.5 3B: 中文與常識]
    Tier1 --> T1B[Llama 3.2 3B: 英文與長文摘要]
    Tier1 --> T1C[DeepSeek-R1 1.5B: 快速數學邏輯]

    Tier2 --> T2A[Gemma 4 E2B: 輕量即時多模態]
    Tier2 --> T2B[Gemma 4 E4B: 128k 高品質多模態]

    Tier3 --> T3A[Qwen2.5-Coder 7B: 倉庫級 Code Review]
    Tier3 --> T3B[DeepSeek-R1 7B: 深度推理 CoT]
    Tier3 --> T3C[Llama 3.1 8B: 綜合旗艦生成]
    Tier3 --> T3D[OLMo 2/3 7B: 開放審計與溯源]
```

### 總結架構師建議 (Architect's Verdict)
1. **網頁即時互動 (Web Interactive UI)**：一律優先路由至 **Qwen2.5:3b**、**Llama 3.2:3b** 或 **DeepSeek-R1:1.5b**，可在 1~2 秒內完成流式輸出。
2. **多模態邊緣網關 (Edge Vision IoT)**：使用 **Gemma 4 E2B/E4B** 兼顧視覺輸入與 128k 上下文。
3. **高負載專業運算 (Heavy-duty Code/Math Review)**：**Qwen2.5-Coder:7b**、**DeepSeek-R1:7b** 與 **Llama 3.1:8b** 一律推入 **Redis Queue (RQ)**，由背景 Worker 逐步消耗，避免阻塞 Web 介面。
