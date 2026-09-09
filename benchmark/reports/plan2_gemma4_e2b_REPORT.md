# 📊 Plan 2: Native llama.cpp 基準測試報告 — gemma4:e2b

> **測試環境 (Test Environment):** Raspberry Pi 5 16GB (Cortex-A76 @ 2.4 GHz, LPDDR4X-4267)  
> **編譯參數 (Compiler Flags):** -mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod -DGGML_CPU_AARCH64=ON  
> **評測工具 (Tool):** Native llama-server (Ollama 官方相容修補引擎 / ARMv8.2 DotProd)  
> **測試時間 (Timestamp):** 2026-09-09T09:57:30.274304

---

## 1. 核心效能指標摘要 (Executive Performance Metrics)

| 評測指標項目<br><sub>(Benchmark Metric)</sub> | 實測數值<br><sub>(Measured Value)</sub> | 單位 / 說明<br><sub>(Unit / Description)</sub> |
| :--- | :--- | :--- |
| **模型參數規模 (Model Parameters)** | **2.6B** | Google Gemma4 多模態架構 |
| **模型量化等級 (Quantization)** | **Q4_K_M** | 4-bit K-Quants Medium |
| **模型檔案大小 (Weight Size)** | **6.67 GB** | 複合層多模態 Blobs |
| **平均解碼生成速度 (Avg Generation TPS)** | **7.04 tokens/s** | 4 核心並行解碼速度 |
| **平均提示詞處理速度 (Avg Prompt Prefill)** | **45.44 tokens/s** | ARM NEON / DotProd 加速 Prefill |
| **實體記憶體佔用 (Peak RAM RSS)** | **3.20 GiB** | 語言模型與核心投影記憶體 |
| **SoC 核心峰值溫度 (Peak Temperature)** | **58.2 °C** | Active Cooler 散熱溫控狀態 |

---

## 2. 測試場景細部數據矩陣 (Detailed Micro-Benchmark Matrix)

| 測試場景與上下文配置<br><sub>(Scenario & Context Spec)</sub> | Prompt 長度<br><sub>(Prompt Tokens)</sub> | Gen 長度<br><sub>(Gen Tokens)</sub> | 提示詞處理速度<br><sub>(Prefill TPS)</sub> | Token 生成速度<br><sub>(Generation TPS)</sub> | 核心溫度<br><sub>(SoC Temp)</sub> |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Interaction (P512 / G128)** | 512 tokens | 128 tokens | **45.44** t/s | **7.04** t/s | 58.2 °C |

---

## 3. 架構師效能與硬體分析 (Architectural Analysis)

1. **多模態語言主架構 (Vision-Language Pipeline):**
   - 成功解耦並載入 2.6B 多模態模型，Prefill 速度高達 45.44 t/s，生成速度穩定達 7.04 t/s。
