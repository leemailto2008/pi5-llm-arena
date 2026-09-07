# 📊 Raspberry Pi 5 單一模型獨立評測報告：`deepseek-r1:7b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 21:30:48


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`2.53` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`38.29` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`1.384` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`57.1` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`5.23` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **2.52** | 33.97 | 1.217s | +4.7°C |
| Coding & Algorithm | Two Sum Algorithm | **2.52** | 44.22 | 1.490s | +3.9°C |
| Quick Fact & Summary | ARM Architecture Summary | **2.53** | 36.69 | 1.444s | +4.4°C |

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text

```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text

```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text

```
