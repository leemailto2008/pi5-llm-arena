# 📊 Raspberry Pi 5 單一模型獨立評測報告：`gemma4:e2b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-08 23:33:31


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`7.61` tok/s** | 🟢 實用流暢 (Usable >5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`99.16` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`0.585` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`58.2` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`8.55` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **7.58** | 92.42 | 0.540s | +5.0°C |
| Coding & Algorithm | Two Sum Algorithm | **7.62** | 111.21 | 0.638s | +5.0°C |
| Quick Fact & Summary | ARM Architecture Summary | **7.62** | 93.86 | 0.579s | +3.6°C |

---

---

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
<think>
Here's a thinking process to structure the explanation:

1.  **Deconstruct the Request:**
    *   Explain the difference between **process** and **thread** in operating systems.
    *   Provide a **concrete example**.
    *   Compare **memory isolation**.

2.  **Define Process vs. Thread (The Core Concepts):**
    *   *Process:* An independent execution environment. It owns resources (memory space, files, etc.). It's heavy.
    *   *Thread:* A path of execution *within* a process. It's a unit of CPU utilization. Threads share the process's resources. It's lightweight.

3.  **Analogy/Relationship (Setting the Stage):**
    *   A good analogy is crucial. (Process = House/Application; Thread = Person
</think>
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
<think>
Thinking Process:

1.  **Understand the Goal:** The request is to solve the "Two Sum" problem efficiently (O(N) time complexity) using a dictionary (hash map).
2.  **Understand Two Sum:** Given an array of integers (`nums`) and a target sum (`target`), find the indices of the two numbers that add up to the target.
3.  **Determine the Strategy (O(N) with Dictionary):**
    *   If we iterate through the array, for each number `x`, we need to quickly check if the required complement (`target - x`) exists in the array.
    *   A dictionary (hash map) allows O(1) average time lookup.
    *   *The core idea:* Iterate through the array once. For each element `nums[i]`, calculate the `complement
</think>
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
<think>
1.  **Analyze the Request:** The user wants a summary of the *key architectural improvements* of the ARM Cortex-A76 microarchitecture, presented in *3 concise bullet points*.

2.  **Identify the Subject (Cortex-A76):** The A76 is a high-performance, high-efficiency CPU core, typically found in server and high-end mobile applications. It belongs to the "big.LITTLE" or high-performance segment.

3.  **Recall/Research Key Architectural Improvements (A76 vs. predecessors
</think>
```
