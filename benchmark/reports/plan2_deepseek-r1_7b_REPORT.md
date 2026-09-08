# 📊 Plan 2: Native llama.cpp 基準測試報告 — `deepseek-r1:7b`

> **測試環境 (Test Environment):** Raspberry Pi 5 16GB (Cortex-A76 @ 2.4 GHz, LPDDR4X-4267)  
> **編譯參數 (Compiler Flags):** `-mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod -DGGML_CPU_AARCH64=ON`  
> **評測工具 (Tool):** Native `llama-bench` (Build 050dde5 / Release)  
> **測試時間 (Timestamp):** `2026-09-08T11:57:05.391477`

---

## 1. 核心效能指標摘要 (Executive Performance Metrics)

| 評測指標項目<br><sub>(Benchmark Metric)</sub> | 實測數值<br><sub>(Measured Value)</sub> | 單位 / 說明<br><sub>(Unit / Description)</sub> |
| :--- | :--- | :--- |
| **模型參數規模 (Model Parameters)** | **7.61B** | 官方發行架構規模 |
| **模型量化等級 (Quantization)** | **Q4_K_M** | 4-bit K-Quants Medium |
| **模型檔案大小 (Weight Size)** | **4.36 GB** | POSIX `mmap` 零副本載入 |
| **平均解碼生成速度 (Avg Generation TPS)** | **2.7 tokens/s** | 4 核心向量並行解碼速度 |
| **平均提示詞處理速度 (Avg Prompt Prefill)** | **11.27 tokens/s** | ARM NEON / DotProd 加速 Prefill |
| **實體記憶體佔用 (Peak RAM RSS)** | **0.44 GiB** | 含 Context KV Cache 與權重 |
| **SoC 核心峰值溫度 (Peak Temperature)** | **58.7 °C** | Active Cooler 散熱溫控狀態 |

---

## 2. 測試場景細部數據矩陣 (Detailed Micro-Benchmark Matrix)

| 測試場景與上下文配置<br><sub>(Scenario & Context Spec)</sub> | Prompt 長度<br><sub>(Prompt Tokens)</sub> | Gen 長度<br><sub>(Gen Tokens)</sub> | 提示詞處理速度<br><sub>(Prefill TPS)</sub> | Token 生成速度<br><sub>(Generation TPS)</sub> | 核心溫度<br><sub>(SoC Temp)</sub> |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Interaction (P512 / G128)** | 512 tokens | 128 tokens | **11.24 ± 0.03** t/s | **2.65 ± 0.0** t/s | 58.7 °C |
| **Long Context & Code Generation (P1024 / G256)** | 1024 tokens | 256 tokens | **11.3 ± 0.01** t/s | **2.75 ± 0.0** t/s | 57.6 °C |

---

## 3. 架構師效能與硬體分析 (Architectural Analysis)

1. **向量化算子收益 (NEON & DotProd Speedup):**
   - 透過 `-march=armv8.2-a+fp16+dotprod` 與 `-mcpu=cortex-a76` 原生編譯，Cortex-A76 的雙發射 (Dual-Issue) ASIMD 向量管線得到完整利用。
   - 在 Prompt Prefill 階段，Dot-Product 指令 (`SDOT`/`UDOT`) 大幅加速了量化矩陣乘法 (GEMM / GEMV)。

2. **記憶體頻寬利用率 (Memory Bandwidth Efficiency):**
   - 模型權重為 4.36 GB，實測 Token 生成速度為 **2.7 tokens/s**。
   - 實測有效讀取頻寬為：
     $$\text{Effective Bandwidth} = 4.36 \text{ GB} \times 2.7 \text{ t/s} \approx 11.77 \text{ GB/s}$$
   - 接近 Raspberry Pi 5 LPDDR4X 記憶體匯流排在 CPU 端點的實體天花板。

3. **溫控與能耗表現 (Thermal & Energy):**
   - 壓測全程溫度維持在 **58.7 °C**，Active Cooler 運作穩定，未觸發任何降頻標誌 (`throttled=0x0`)。
