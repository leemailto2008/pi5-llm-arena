# 📊 Raspberry Pi 5 單一模型獨立評測報告：`gemma4:e4b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-08 23:39:46


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`3.71` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`47.74` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`1.243` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`57.1` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`10.25` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **3.68** | 44.09 | 1.157s | +5.5°C |
| Coding & Algorithm | Two Sum Algorithm | **3.71** | 53.53 | 1.341s | +4.4°C |
| Quick Fact & Summary | ARM Architecture Summary | **3.73** | 45.61 | 1.230s | +3.9°C |

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
The concepts of **process** and **thread** are fundamental to understanding how modern operating systems manage and execute programs. While both are mechanisms for achieving concurrency, they differ significantly in terms of resource ownership, isolation, and overhead.

Here is a detailed explanation of the differences, followed by a concrete example and a comparison of memory isolation.

---

## 🧠 Core Concepts

### 1. Process (The Container)

A **process** is an independent instance of a running program. It is the operating system's primary unit of resource allocation. When you double-click an application icon, the OS typically creates a new process for that application.

*   **What it owns:** A process owns a dedicated, isolated set of resources, including its own memory address space, file descriptors, and system resources.
*   **Isolation:** Processes are heavily isolated from one another. If one process crashes, it generally does not affect other processes running on the system.
*   **
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
