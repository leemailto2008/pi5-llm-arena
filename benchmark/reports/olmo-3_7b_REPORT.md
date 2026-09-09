# 📊 Raspberry Pi 5 單一模型獨立評測報告：`olmo-3:7b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-08 23:23:07


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`2.56` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`51.90` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`3.436` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`56.5` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`13.05` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **2.54** | 53.44 | 3.336s | +6.3°C |
| Coding & Algorithm | Two Sum Algorithm | **2.55** | 51.22 | 3.584s | +3.3°C |
| Quick Fact & Summary | ARM Architecture Summary | **2.59** | 51.05 | 3.389s | +3.5°C |

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
Okay, so I need to explain the difference between processes and threads in operating systems. Hmm, let me start by recalling what I know. 

First, processes. I think a process is like an instance of a program running on the system. Like, if you have multiple applications open, each one is a process. They have their own memory space, right? So each process gets its own address space, which means they can't directly access each other's memory. That's probably memory isolation for processes.

Then threads. A thread is a flow of control within a single process. So one process can have multiple threads, each executing different parts of the same program. For example, a web browser might have a main thread handling the UI and then separate threads for loading images or handling clicks. Threads share the same memory space as their parent process, so they can communicate more easily but might not have
</think>
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
<think>
Okay, I need to write an efficient Python function for the Two Sum problem that runs in O(N) time using a dictionary. Let me think about how the Two Sum problem works. The task is to find two numbers in an array that add up to a target and return their indices. The brute force approach is O(N^2), which is too slow. So the optimal way is to use a hash map or dictionary to store the values and their indices as we iterate through the list. That way, for each element, we can check if the complement (target - current element) exists in the dictionary in constant time.

Hmm, right. So the plan is: loop through each element in the array. For each element, calculate the complement (target - num). Then check if the complement is already in the dictionary. If it is, return the current index and the stored index of the
</think>
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
<think>
Okay, I need to summarize the key architectural improvements of the ARM Cortex-A76 microarchitecture in three concise bullet points. Let me start by recalling what I know about the Cortex-A series. The A76 is part of the ARMv8-A family, right? It's an evolution from previous cores like the A72 or A75. 

First, I remember that performance is often a big focus in new CPU designs. Maybe the A76 has improved performance through better instruction decoding or execution units. Wait, I think it introduced a new superscalar architecture. Superscalar means multiple instructions can be
</think>
```
