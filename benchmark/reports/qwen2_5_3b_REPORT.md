# 📊 Raspberry Pi 5 單一模型獨立評測報告：`qwen2.5:3b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 18:54:37


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`6.02` tok/s** | 🟢 實用流暢 (Usable >5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`178.39` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`0.661` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`56.5` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`2.87` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **6.01** | 157.62 | 0.842s | +-21.1°C |
| Coding & Algorithm | Two Sum Algorithm | **6.02** | 197.44 | 0.585s | +5.0°C |
| Quick Fact & Summary | ARM Architecture Summary | **6.04** | 180.10 | 0.555s | +4.7°C |

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
In an operating system, a process and a thread are both units of execution, but they differ in several aspects, including their isolation, memory management, and the way they interact with the operating system.

### Process
A process is the basic unit of execution in an operating system. It is an instance of a program that is being executed. Each process has its own memory space, which includes its own stack, heap, and code segment. Processes are isolated from each other in terms of memory, meaning that one process cannot directly access another process's memory. This isolation is enforced by the operating system, which manages memory allocation and ensures that each process has its own private memory space.

### Thread
A thread is a lighter-weight unit of execution within a process. It is a sequence of instructions that can be scheduled for execution. Threads share the same memory space as the process they belong to, which means that threads within the same process can directly access each other's memory. Threads are often used to improve
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
Certainly! Below is a Python function that solves the Two Sum problem in O(N) time complexity using a dictionary. The function is efficient and includes type hints and docstrings for clarity.

```python
from typing import List, Dict

def two_sum(numbers: List[int], target: int) -> List[int]:
    """
    Finds two numbers in the given list 'numbers' that add up to the 'target'.
    The function uses a dictionary to achieve O(N) time complexity.

    Parameters:
    numbers (List[int]): A list of integers where we need to find the two numbers.
    target (int): The target sum we are looking for.

    Returns:
    List[int]: A list containing the indices of the two numbers that add up to the target.
               If no such pair exists, returns [-1, -1].

    Example:
    >>> two_sum([2, 7, 11, 15], 9)
    [0, 1
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
1. Enhanced Performance: ARM Cortex-A76 incorporates a more advanced out-of-order execution engine, which allows for more efficient and concurrent processing of instructions, leading to improved performance.

2. Increased Efficiency: The microarchitecture includes optimizations for energy efficiency, such as a more efficient branch prediction mechanism and a smaller, more efficient instruction set, which helps in reducing power consumption without compromising performance.

3. Advanced Memory Management: Cortex-A76 features an improved memory management unit (MMU) that supports larger virtual address spaces, enabling more efficient memory management and better support for modern memory technologies like LPDDR5.
```
