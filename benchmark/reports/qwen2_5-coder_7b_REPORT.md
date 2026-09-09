# 📊 Raspberry Pi 5 單一模型獨立評測報告：`qwen2.5-coder:7b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 20:10:45


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`2.77` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`80.20` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`1.744` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`58.2` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`5.23` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **2.76** | 74.30 | 2.232s | +5.8°C |
| Coding & Algorithm | Two Sum Algorithm | **2.76** | 86.94 | 1.521s | +30.4°C |
| Quick Fact & Summary | ARM Architecture Summary | **2.79** | 79.36 | 1.482s | +29.6°C |

---

---

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
In an operating system, a process is a program in execution. It is a complete, independent unit of work that is managed by the operating system. Each process has its own memory space, which means that one process cannot directly access the memory of another process. This isolation is enforced by the operating system's memory management system.

A thread, on the other hand, is a lightweight sub-process within a process. Threads share the same memory space as other threads in the same process. This means that threads can access and modify the same data, which can lead to issues such as race conditions if not properly managed.

Here's a concrete example to illustrate the difference:

Suppose you have a program that needs to perform a complex calculation. This program can be designed as a single process with a single thread. However, if the calculation is too complex to be handled by a single thread, the program can be designed as a single process with multiple threads. Each thread can handle a different part of the calculation,
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
```python
from typing import List, Tuple

def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Finds two indices in the list 'nums' such that the numbers at those indices add up to 'target'.
    
    Args:
    nums (List[int]): A list of integers.
    target (int): The target sum to find within the list.
    
    Returns:
    Tuple[int, int]: A tuple containing the indices of the two numbers that add up to the target.
    
    Raises:
    ValueError: If no two numbers add up to the target.
    """
    # Dictionary to store the difference and its index
    num_dict = {}
    
    # Iterate over the list
    for i, num in enumerate(nums):
        # Calculate the difference needed to reach the target
        difference = target - num
        
        # Check if the difference is already in the dictionary
        if difference in num_dict:
            # If
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
- **Enhanced Performance**: The ARM Cortex-A76 microarchitecture introduces a 25% increase in performance compared to its predecessor, Cortex-A75, by optimizing the CPU core design for better efficiency and speed.
- **Improved Power Efficiency**: With a focus on power management, Cortex-A76 reduces power consumption by up to 40% under heavy workloads, making it ideal for battery-powered devices and extending device life.
- **Advanced Security Features**: The microarchitecture includes enhanced security features such as TrustZone, which provides a secure execution environment, protecting against unauthorized access and ensuring data integrity.
```
