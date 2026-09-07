# 📊 Raspberry Pi 5 單一模型獨立評測報告：`llama3.1:8b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 22:50:05


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`2.46` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`46.62` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`1.620` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`57.6` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`5.76` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **2.46** | 42.60 | 1.760s | +4.7°C |
| Coding & Algorithm | Two Sum Algorithm | **2.46** | 52.85 | 1.637s | +4.3°C |
| Quick Fact & Summary | ARM Architecture Summary | **2.47** | 44.41 | 1.462s | +4.9°C |

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
**Process vs Thread: A Key Concept in Operating Systems**
===========================================================

In operating systems, a process and a thread are two fundamental concepts that are often confused with each other. Understanding the difference between them is crucial for designing and developing efficient and secure software systems.

**Process**
-----------

A process is an independent program that is executed by the operating system. Each process has its own:

*   **Memory space**: Each process has its own virtual address space, which is a separate region of memory allocated by the operating system.
*   **Resources**: Each process has its own set of resources, such as open files, network connections, and system calls.
*   **Program counter**: Each process has its own program counter, which keeps track of the current instruction being executed.

**Thread**
---------

A thread is a lightweight process that shares the same memory space as its parent process. Threads are used to improve the responsiveness and efficiency of a program by allowing multiple tasks to run concurrently.

**Key differences**
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
**Two Sum Problem Solution**
================================

The Two Sum problem is a classic problem in algorithm design. Given an array of integers and a target sum, find two elements in the array that add up to the target sum.

**Solution**
------------

```python
from typing import List, Dict

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Returns the indices of the two elements in the array that add up to the target sum.

    Args:
        nums (List[int]): The input array of integers.
        target (int): The target sum.

    Returns:
        List[int]: The indices of the two elements that add up to the target sum.
    """
    num_dict: Dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return [num_dict[complement], i]
        num_dict[num] = i
    return []
``
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
Here are the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points:

• **Improved Out-of-Order Execution (OoOE)**: The Cortex-A76 introduces a more efficient OoOE engine, allowing for better instruction-level parallelism and improved performance in complex workloads.

• **Enhanced Branch Predictor**: The Cortex-A76 features a more accurate and efficient branch predictor, reducing misprediction penalties and improving overall performance in applications with complex branching patterns.

• **Increased L1 Cache Bandwidth**: The Cortex-A76 increases the L1 cache bandwidth by 50%, allowing for faster access to frequently accessed data and improving performance in memory-bound workloads.
```
