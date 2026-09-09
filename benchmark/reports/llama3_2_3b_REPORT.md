# 📊 Raspberry Pi 5 單一模型獨立評測報告：`llama3.2:3b`

> **硬體環境:** Raspberry Pi 5 Model B (BCM2712 4x Cortex-A76 @ 2.40GHz, 16GB LPDDR4X, Active Cooler)

> **執行引擎:** Native Ollama ARM64 (v0.33.3, Linux AArch64, Performance Governor)

> **評測日期:** 2026-09-07 18:22:42


## 🏆 核心指標總覽 (Key Performance Indicators)

| 效能指標 (Metric) | 評測數值 (Value) | 備註說明 (Notes) |
| :--- | :--- | :--- |
| **Token 生成速度 (Generation TPS)** | **`5.92` tok/s** | 🟢 實用流暢 (Usable >5 tps) |
| **提示詞評估速度 (Prompt Eval TPS)** | **`164.10` tok/s** | 批次上下文預填充速率 |
| **首字反應延遲 (Time to First Token, TTFT)** | **`0.629` 秒** | 端到端反應延遲 |
| **推論峰值溫度 (Peak Thermal Dynamic)** | **`56.5` °C** | 安全溫度 (距離 80°C 降頻點餘裕充足) |
| **記憶體峰值佔用 (Peak RAM RSS)** | **`3.39` GiB** | 系統實體記憶體總量 15.8 GiB |

---

## 📝 各測試類別詳細數據 (Category Breakdown)

| 測試類別 (Category) | 測試題目 (Test Name) | 生成速度 (TPS) | 提示詞速度 (TPS) | 首字延遲 (TTFT) | 溫升變化 (Δ Temp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Reasoning & Logic | Process vs Thread | **5.94** | 147.92 | 0.786s | +6.8°C |
| Coding & Algorithm | Two Sum Algorithm | **5.90** | 180.50 | 0.588s | +5.0°C |
| Quick Fact & Summary | ARM Architecture Summary | **5.93** | 163.88 | 0.514s | +4.7°C |

---

---

---

## 💬 測試生成範例輸出 (Sample Generated Outputs)

### 🔹 [Reasoning & Logic] Process vs Thread

**輸入 Prompt:**
> Explain the difference between process and thread in operating systems. Provide a concrete example and compare memory isolation.


**模型輸出 Response:**
```text
In operating systems, both processes and threads are used to execute multiple tasks concurrently, but they differ in their approach, characteristics, and usage.

**Process**

A process is an independent unit of execution that runs in its own memory space. Each process has its own program counter, stack, and memory space. When a process is created, the operating system allocates a separate memory space for it, which is known as a process image. The process image includes the program code, data, and stack.

Here's an example:

Imagine you're working on a project that involves writing a report. You open a word processing application, and the operating system creates a new process for the application. This process has its own memory space, where the word processing application can store its data, such as the report text. When you save the report, the operating system saves the entire process image, including the memory space, to disk.

**Thread**

A thread is a lightweight process that shares the same memory space as
```

### 🔹 [Coding & Algorithm] Two Sum Algorithm

**輸入 Prompt:**
> Write an efficient Python function to solve the Two Sum problem in O(N) time complexity using a dictionary. Include type hints and docstrings.


**模型輸出 Response:**
```text
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Returns the indices of the two numbers in the list that add up to the target.

    Args:
    - nums (list[int]): A list of integers.
    - target (int): The target sum.

    Returns:
    - list[int]: A list containing the indices of the two numbers that add up to the target.
    """
    num_dict = {}  # Initialize an empty dictionary to store the numbers and their indices.
    
    for i, num in enumerate(nums):  # Iterate over the list with the index and value.
        complement = target - num  # Calculate the complement of the current number.
        
        if complement in num_dict:  # Check if the complement is already in the dictionary.
            return [num_dict[complement], i]  # If it is, return the indices of the complement and the current number.
        
        num_dict[num] = i
```

### 🔹 [Quick Fact & Summary] ARM Architecture Summary

**輸入 Prompt:**
> Summarize the key architectural improvements of ARM Cortex-A76 microarchitecture in 3 concise bullet points.


**模型輸出 Response:**
```text
Here are three concise bullet points summarizing the key architectural improvements of ARM Cortex-A76 microarchitecture:

• **Increased Cores and Threads**: The Cortex-A76 features up to 8 cores and 8 threads, providing improved multithreading capabilities and increased processing power.

• **Improved Power Management**: The Cortex-A76 introduces a new power management system, which includes a more efficient clock gating mechanism and a dynamic voltage and frequency scaling (DVFS) system, allowing for better power efficiency and reduced heat generation.

• **Enhanced Security Features**: The Cortex-A76 includes enhanced security features, such as a secure boot mechanism, a secure storage mechanism, and a hardware-based implementation of the ARM TrustZone, providing improved protection against malware and other security threats
```
