# 📊 Raspberry Pi 5 單一模型獨立評測報告：`deepseek-r1:1.5b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 17:48:18


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`11.54` tok/s** | ⚡ 即時流暢 (Real-time >10 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`183.09` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`0.243` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`56.5` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`1.84` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **11.54** | 165.40 | 0.225s | +5.2°C |
| Coding & Algorithm | Two Sum Algorithm | **11.47** | 207.03 | 0.265s | +5.0°C |
| Quick Fact & Summary | ARM Architecture Summary | **11.59** | 176.83 | 0.237s | +3.0°C |

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
Okay, so I need to explain the difference between process and thread in operating systems, give a concrete example, and compare memory isolation. Hmm, I remember that both processes and threads are related to how tasks are managed, but I'm a bit fuzzy on the details. Let me try to break this down.

First, I think processes are like the main tasks that the OS runs. They handle everything, right? So when I open a browser, the browser is a process. It runs the web server and the browser's application. But wait, what about the actual browser itself? Is that a process or a thread? I'm not sure. Maybe the browser is a process because it's a single task, but the user interface is a thread. That makes sense because the UI is a smaller part that runs in parallel.

Then there are threads. I believe threads are smaller units of
</think>
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
<think>
Okay, I need to write a Python function to solve the Two Sum problem with O(N) time complexity using a dictionary. Let me think about how to approach this.

First, the Two Sum problem is about finding two distinct elements in an array that add up to a target value. The goal is to return their indices. The user wants the solution to be efficient, specifically O(N) time complexity, which suggests that using a dictionary to store seen elements and their indices is the way to go.

So, the plan is: iterate through each element in the array, for each element, check if the complement (target - current element) exists in the dictionary of seen elements. If it does, return the indices of the two elements. If not, add the current element and its index to the dictionary.

Wait, but the user also mentioned including type hints and a docstring. So
</think>
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
<think>
Okay, so I need to summarize the key architectural improvements of the ARM Cortex-A76 microarchitecture in three concise bullet points. I'm not super familiar with the details, but I know it's an improvement over the previous Cortex-A5, which was a big deal. Let me think through this step by step.

First, I remember that the Cortex-A5 had a lot of features, but it was a bit limited. The Cortex-A76 is supposed to be more advanced. I think it introduced some new features that made it better for certain tasks. Maybe it's faster or
</think>
```
