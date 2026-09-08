# 📊 Raspberry Pi 5 單一模型獨立評測報告：`olmo2:7b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-08 23:30:11


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`2.73` tok/s** | 🟡 稍慢 (Slow <5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`94.08` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`1.549` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`57.6` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`12.37` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **2.70** | 85.44 | 2.203s | +5.5°C |
| Coding & Algorithm | Two Sum Algorithm | **2.70** | 103.27 | 1.302s | +4.7°C |
| Quick Fact & Summary | ARM Architecture Summary | **2.79** | 93.53 | 1.143s | +3.9°C |

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
In operating systems, a **process** is an instance of a computer program in execution. It includes all the data and code needed to perform a specific task and represents a functional unit that can be independently managed by the operating system. A process has a unique process ID (PID), and it can have multiple threads. Each thread is a separate path of execution within the process. Threads share the same memory space and resources of the process they belong to, which allows for efficient communication and synchronization between them.

On the other hand, a **thread** is a lightweight subprocess within a process. It represents a sequence of instructions that can be executed independently within the same process. Threads are more resource-efficient than processes because they share the same memory space and resources of the parent process. This sharing allows for lower overhead and faster context switching compared to processes.

**Example:**

Imagine you are working on a document in a word processor. The **process** is the entire instance of the word processor application running on your
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
```python
def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """
    Finds two numbers in the list that sum up to the target.

    Args:
        nums (list): A list of integers.
        target (int): The target sum.

    Returns:
        tuple: A tuple containing two numbers (num1, num2) such that num1 + num2 == target.
    """
    nums_dict = {num: i for i, num in enumerate(nums)}
    result = None

    for key, value in nums_dict.items():
        complement = target - value
        if complement in nums_dict:
            result = (value, nums_dict[complement])
            break

    return result
```

This function first creates a dictionary `nums_dict` where the keys are the indices of the elements in `nums`, and the values are the elements themselves. Then, it iterates through the dictionary to find a key `value
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
- Enhanced single-thread performance through improved out-of-order execution and larger 64-entry decode window.
- Improved power efficiency with a more dynamic voltage scaling and clocking mechanism, including a new 6-stage pipeline.
- Increased instruction throughput with a larger 128-bit wide integer and floating-point execution units.
```
