# 📊 Plan 2: Native llama.cpp 基準測試報告 — olmo-3:7b

> **測試環境 (Test Environment):** Raspberry Pi 5 16GB (Cortex-A76 @ 2.4 GHz, LPDDR4X-4267)  
> **編譯參數 (Compiler Flags):** -mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod -DGGML_CPU_AARCH64=ON  
> **評測工具 (Tool):** Native llama-server (Ollama 官方相容修補引擎 / ARMv8.2 DotProd)  
> **測試時間 (Timestamp):** 2026-09-09T09:57:30.274232

---

## 1. 核心效能指標摘要 (Executive Performance Metrics)

| 評測指標項目<br><sub>(Benchmark Metric)</sub> | 實測數值<br><sub>(Measured Value)</sub> | 單位 / 說明<br><sub>(Unit / Description)</sub> |
| :--- | :--- | :--- |
| **模型參數規模 (Model Parameters)** | **6.95B** | OLMo-3 架構規模 |
| **模型量化等級 (Quantization)** | **Q4_K_M** | 4-bit K-Quants Medium |
| **模型檔案大小 (Weight Size)** | **4.16 GB** | POSIX mmap 載入 |
| **平均解碼生成速度 (Avg Generation TPS)** | **2.37 tokens/s** | 4 核心並行解碼速度 |
| **平均提示詞處理速度 (Avg Prompt Prefill)** | **13.90 tokens/s** | ARM NEON / DotProd 加速 Prefill |
| **實體記憶體佔用 (Peak RAM RSS)** | **8.90 GiB** | 含 Context KV Cache 與權重 |
| **SoC 核心峰值溫度 (Peak Temperature)** | **65.3 °C** | Active Cooler 散熱溫控狀態 |

---

## 2. 測試場景細部數據矩陣 (Detailed Micro-Benchmark Matrix)

| 測試場景與上下文配置<br><sub>(Scenario & Context Spec)</sub> | Prompt 長度<br><sub>(Prompt Tokens)</sub> | Gen 長度<br><sub>(Gen Tokens)</sub> | 提示詞處理速度<br><sub>(Prefill TPS)</sub> | Token 生成速度<br><sub>(Generation TPS)</sub> | 核心溫度<br><sub>(SoC Temp)</sub> |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Interaction (P512 / G128)** | 512 tokens | 128 tokens | **13.90** t/s | **2.37** t/s | 65.3 °C |

---

## 3. 架構師效能與硬體分析 (Architectural Analysis)

1. **相容層解析 (Compatibility Layer):**
   - 透過官方相容模組解決 upstream llama.cpp 尚未支援 LLM_ARCH_OLMO3 之問題，成功在 Native 環境完整執行推論。
2. **頻寬利用率 (Bandwidth Utilization):**
   - 4.16 GB 權重以 2.37 t/s 解碼，讀取頻寬達 ~9.86 GB/s，充分利用 Pi 5 記憶體匯流排。
