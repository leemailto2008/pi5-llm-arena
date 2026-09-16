# Raspberry Pi 5 本地 10 大 AI 模型技術論文研讀與選型指南 (AI Models Paper Compendium & Selection Guide)

本目錄收錄 Raspberry Pi 5 部署環境中，所有已安裝並支援之 **10 款開源大型語言與多模態模型 (LLMs & Vision-Language Models)** 的深入論文研讀、底層架構解析、注意力機制比較、以及在 ARM Cortex-A76 四核心 CPU 上的實測性能調優指引。

> [!TIP]
> - **全維度深度比較表專文**：橫跨「模型規格參數 / 創新機制 / 訓練管線與數據 / 特性剖析」之橫向對比大表，請參閱 [10_models_comparison_matrix.md](./10_models_comparison_matrix.md)。
> - **優化前後全維度量化對比表 (Before vs. After Matrix)**：查閱 10 款模型調優前後的輸入處理速度、生成吞吐、冷啟動縮減與可用 RAM 總對比，請參閱 [optimization_comparison_table.md](./optimization_comparison_table.md)。
> - **學術論文選題與高引文獻調研 (Research Paper Topics & Survey)**：聚焦系統頂會 (MLSys, MobiSys, DAC) 之四大原創架構題目與 10 篇全球頂級論文，請參閱 [surveyPaperTopic.md](./surveyPaperTopic.md)。
> - **邊緣模型極限優化指南**：五大工程調優手段 (投機解碼、iMatrix 量化、KV 快取壓縮、CPU 頻率鎖定、LoRA)，請參閱 [model_optimization_guide.md](./model_optimization_guide.md)。

> - **實測優化驗證報告 (Live Verification Reports)**：
>   - [01_optimization_report_llama3.1_8b.md](./01_optimization_report_llama3.1_8b.md) (Llama 3.1 8B 鎖頻 2.4GHz、4k 上下文約束、Prompt 處理提速 +8.2% 實測驗證)。
>   - [02_optimization_report_deepseek_r1_7b.md](./02_optimization_report_deepseek_r1_7b.md) (DeepSeek-R1 7B 長思考鏈參數調優、Prompt 處理提速 +13.9%、生成 2.78 tok/s 實測驗證)。
>   - [03_optimization_report_qwen2.5_coder_7b.md](./03_optimization_report_qwen2.5_coder_7b.md) (Qwen2.5-Coder 7B 代碼審查專用採樣對齊、初次載入時長縮短 -40.6%、Prompt 處理 13.05 tok/s 實測驗證)。
>   - [04_optimization_report_olmo3_7b.md](./04_optimization_report_olmo3_7b.md) (OLMo-3 7B 64k->4k 快取記憶體約束、生成吞吐提速 +7.4%、冷啟動縮短 -38.2% 實測驗證)。
>   - [05_optimization_report_olmo2_7b.md](./05_optimization_report_olmo2_7b.md) (OLMo 2 7B 科學驗證參數固化、Prompt 解析突破 14.55 tok/s 實測驗證)。
>   - [06_optimization_report_gemma4_e4b.md](./06_optimization_report_gemma4_e4b.md) (Gemma 4 E4B 多模態採樣固化、Prompt 解析達 22.76 tok/s、生成逼近 4 tok/s 實測驗證)。
>   - [07_optimization_report_llama3.2_3b.md](./07_optimization_report_llama3.2_3b.md) (Llama 3.2 3B 剪枝極速架構、Prompt 解析突破 35.16 tok/s、可用 RAM 12.8GB 實測驗證)。
>   - [08_optimization_report_qwen2.5_3b.md](./08_optimization_report_qwen2.5_3b.md) (Qwen2.5 3B 繁中系統工程對齊、GQA 8:1 記憶體極致壓縮、可用 RAM 13.27GB 實測驗證)。
>   - [09_optimization_report_gemma4_e2b.md](./09_optimization_report_gemma4_e2b.md) (Gemma 4 E2B 深度剪枝多模態、Prompt 狂飆 46.73 tok/s、生成 7.64 tok/s 實測驗證)。
>   - [10_optimization_report_deepseek_r1_1.5b.md](./10_optimization_report_deepseek_r1_1.5b.md) (DeepSeek-R1 1.5B 數理思考微模型、Prompt 飆破 74.47 tok/s、生成 12.08 tok/s 實測驗證)。













---

## 一、 10 大模型全景技術規格橫向對比表 (Architecture Comparison)

| 序號 | 模型名稱 (Model Tag) | 研發機構 (Org) | 發布時間 (Release) | 核心參數量 (Params) | Context 長度 | 特色架構 / 技術特徵 | 論文技術研讀檔案 (Technical Report) |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **01** | `gemma4:e4b` | Google DeepMind | 2026.04 | ~8.0B (Text 4.2B) | **128k** | PLE 層級嵌入、原生視覺/音訊多模態、Thinking Mode | [01_gemma4_e4b.md](./01_gemma4_e4b.md) |
| **02** | `gemma4:e2b` | Google DeepMind | 2026.04 | ~5.1B (Text 2.2B) | **128k** | PLE、極限端側剪枝、大模型蒸餾、低維度高效率 | [02_gemma4_e2b.md](./02_gemma4_e2b.md) |
| **03** | `olmo2:7b` | Allen AI (Ai2) | 2024.11 | 7.3B | 4k | 完全開源 (Fully-Open)、Dolma 2 數據集、Tulu 3 對齊 | [03_olmo2_7b.md](./03_olmo2_7b.md) |
| **04** | `olmo-3:7b` | Allen AI (Ai2) | 2025.11 | 7.3B | **64k** | 完全可溯源 (OLMoTrace)、Dolma 3 語料、Thinking 模式 | [04_olmo3_7b.md](./04_olmo3_7b.md) |
| **05** | `llama3.1:8b` | Meta AI | 2024.07 | 8.03B | **128k** | 15T Tokens 超飽和訓練、128k Vocab、GQA 4:1 | [05_llama3.1_8b.md](./05_llama3.1_8b.md) |
| **06** | `deepseek-r1:7b` | DeepSeek-AI | 2025.01 | 7.61B | 32k ~ 64k | 純強化學習 (GRPO)、R1 80萬思考鏈樣本蒸餾 | [06_deepseek_r1_7b.md](./06_deepseek_r1_7b.md) |
| **07** | `qwen2.5-coder:7b` | Alibaba Qwen | 2024.09 | 7.61B | **128k** | 5.5T 代碼預訓練、FIM 中間填空、軟體工程專精 | [07_qwen2.5_coder_7b.md](./07_qwen2.5_coder_7b.md) |
| **08** | `qwen2.5:3b` | Alibaba Qwen | 2024.09 | 3.09B | 32k | 18T 龐大語料、GQA 8:1 極致低快取、繁中最強 3B | [08_qwen2.5_3b.md](./08_qwen2.5_3b.md) |
| **09** | `llama3.2:3b` | Meta AI | 2024.09 | 3.21B | **128k** | 結構化剪枝 (Structured Pruning) + 雙軌蒸餾回補 | [09_llama3.2_3b.md](./09_llama3.2_3b.md) |
| **10** | `deepseek-r1:1.5b` | DeepSeek-AI | 2025.01 | 1.77B | 32k | 微型推理神經網路、Math-500 82.8%、極速端側思考 | [10_deepseek_r1_1.5b.md](./10_deepseek_r1_1.5b.md) |

---

## 二、 Raspberry Pi 5 邊緣運算選型決策指南 (Selection Matrix for Pi 5)

針對 Raspberry Pi 5 (16GB RAM, Broadcom BCM2712 四核 ARM Cortex-A76 @ 2.4GHz) 之物理硬體特徵，我們將 10 款模型依推論延遲與場景分類為三大戰術梯隊：

```
                             [ Raspberry Pi 5 推論延遲與能力光譜 ]

  極速即時對話 (<15s)                    平衡多模態 (20s~1m)                  深度專業推論 (2m~5m)
  ┌───────────────────────┐            ┌──────────────────────┐             ┌───────────────────────┐
  │ • llama3.2:3b         │            │ • gemma4:e2b         │             │ • qwen2.5-coder:7b    │
  │ • qwen2.5:3b          │            │ • gemma4:e4b         │             │ • deepseek-r1:7b      │
  │ • deepseek-r1:1.5b    │            │                      │             │ • llama3.1:8b         │
  │ (16 ~ 28 tok/s)       │            │ (5 ~ 15 tok/s)       │             │ • olmo2 / olmo3:7b    │
  └───────────────────────┘            └──────────────────────┘             │ (2.2 ~ 2.8 tok/s)     │
                                                                            └───────────────────────┘
```

### 1. 第一梯隊：秒級日常問答與即時互動 (Interactive Real-time)
- **推薦模型：** `llama3.2:3b`、`qwen2.5:3b`、`deepseek-r1:1.5b`
- **CPU 速度：** **16.0 ~ 28.5 tok/s** (單次 200 字回覆僅需 7 ~ 12 秒)
- **記憶體佔用：** 僅約 1.1 ~ 2.0 GB RAM。
- **最佳適用情境：** Web 聊天介面、語音助理、終端即時指令諮詢。

### 2. 第二梯隊：邊緣多模態與視覺巡檢 (Edge Vision & Multimodal)
- **推薦模型：** `gemma4:e2b`、`gemma4:e4b`
- **CPU 速度：** **4.5 ~ 15.0 tok/s**
- **記憶體佔用：** 約 3.1 ~ 4.8 GB RAM。
- **最佳適用情境：** 樹莓派外接 CSI 攝影機進行本地影像辨識、智慧家庭視覺問答、多模態物聯網 (IoT)。

### 3. 第三梯隊：非同步專業軟體工程與高深邏輯推理 (Async Expert Engine)
- **推薦模型：** `qwen2.5-coder:7b` (軟體代碼專用)、`deepseek-r1:7b` (高難度數學推理)
- **CPU 速度：** **2.3 ~ 2.7 tok/s** (單次 800 字生成需 4 ~ 5 分鐘)
- **記憶體佔用：** 約 4.7 ~ 5.0 GB RAM。
- **最佳適用情境：** 本專案之 **FastAPI + Redis Queue 非同步背景佇列**。透過 PC 端發送任務，在 Pi 5 後台默默完成資安漏洞檢驗、重構代碼撰寫，徹底避免 Client 端阻塞等待。

---

## 三、 本目錄檔案清單 (File Manifest)

- [01_gemma4_e4b.md](./01_gemma4_e4b.md): Google Gemma 4 E4B 邊緣多模態與高能效思考架構研讀報告
- [02_gemma4_e2b.md](./02_gemma4_e2b.md): Google Gemma 4 E2B 超羽量級邊緣多模態模型研讀報告
- [03_olmo2_7b.md](./03_olmo2_7b.md): Ai2 OLMo 2 7B 頂級完全開源模型架構研讀報告
- [04_olmo3_7b.md](./04_olmo3_7b.md): Ai2 OLMo 3 7B 支援長上下文與推理思考的完全開源模型研讀報告
- [05_llama3.1_8b.md](./05_llama3.1_8b.md): Meta Llama 3.1 8B 工業級開源語言模型基準研讀報告
- [06_deepseek_r1_7b.md](./06_deepseek_r1_7b.md): DeepSeek-R1-Distill-Qwen-7B 強化學習與思考鏈蒸餾模型研讀報告
- [07_qwen2.5_coder_7b.md](./07_qwen2.5_coder_7b.md): Qwen2.5-Coder 7B 專業程式碼與軟體工程大模型研讀報告
- [08_qwen2.5_3b.md](./08_qwen2.5_3b.md): Qwen2.5 3B 全能型輕量通用大模型研讀報告
- [09_llama3.2_3b.md](./09_llama3.2_3b.md): Meta Llama 3.2 3B 結構化剪枝與知識蒸餾之邊緣模型研讀報告
- [10_deepseek_r1_1.5b.md](./10_deepseek_r1_1.5b.md): DeepSeek-R1-Distill-Qwen-1.5B 極限輕量端側推理模型研讀報告
