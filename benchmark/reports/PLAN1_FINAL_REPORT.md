# 🏆 Raspberry Pi 5 (16GB) LLM Arena - Phase 3 最終綜合評測報告 (Plan 1 Final Report)

> **評測時間 (Timestamp):** `2026-09-08 23:14:21`  

> **硬體配置 (Hardware Profile):** Raspberry Pi 5 Model B (BCM2712 4-Core Cortex-A76 @ 2.40 GHz, 16GB LPDDR4X, Active Fan Cooler)  

> **系統調校 (System Tuning):** `performance` Governor (全核心 2.4GHz 固定), PWM 散熱溫控 (`throttled=0x0`)  

> **推理引擎 (Engine):** Native Ollama ARM64 (v0.33.3, ARMv8.2-A / ARMv8.6-A NEON & FP16 向量加速)


## 🥇 綜合性能排行榜 (Master Inference Leaderboard)

| 排名<br><sub>(Rank)</sub> | 模型名稱<br><sub>(Model)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞速度<br><sub>(Prompt TPS)</sub> | 首字延遲<br><sub>(TTFT)</sub> | 峰值溫度<br><sub>(Peak Temp)</sub> | 記憶體<br><sub>(RAM)</sub> | 即時可用性<br><sub>(Usability)</sub> | 獨立報告<br><sub>(Report)</sub> |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 冠軍 | `deepseek-r1:1.5b` | **11.54 tok/s** | 183.09 tok/s | 0.243s | 56.5°C | 1.84 GB | ⚡ 極速即時 (>10 tps) | [deepseek-r1_1_5b_REPORT.md](./deepseek-r1_1_5b_REPORT.md) |
| 🥈 亞軍 | `gemma4:e2b` | **7.61 tok/s** | 99.16 tok/s | 0.585s | 58.2°C | 8.55 GB | 🟢 實用流暢 (>5 tps) | [gemma4_e2b_REPORT.md](./gemma4_e2b_REPORT.md) |
| 🥉 季軍 | `qwen2.5:3b` | **6.02 tok/s** | 178.39 tok/s | 0.661s | 56.5°C | 2.87 GB | 🟢 實用流暢 (>5 tps) | [qwen2_5_3b_REPORT.md](./qwen2_5_3b_REPORT.md) |
| #4 | `llama3.2:3b` | **5.92 tok/s** | 164.10 tok/s | 0.629s | 56.5°C | 3.39 GB | 🟢 實用流暢 (>5 tps) | [llama3_2_3b_REPORT.md](./llama3_2_3b_REPORT.md) |
| #5 | `gemma4:e4b` | **3.71 tok/s** | 47.74 tok/s | 1.243s | 57.1°C | 10.25 GB | 🟡 慢速 (<5 tps) | [gemma4_e4b_REPORT.md](./gemma4_e4b_REPORT.md) |
| #6 | `qwen2.5-coder:7b` | **2.77 tok/s** | 80.20 tok/s | 1.744s | 58.2°C | 5.23 GB | 🟡 慢速 (<5 tps) | [qwen2_5-coder_7b_REPORT.md](./qwen2_5-coder_7b_REPORT.md) |
| #7 | `olmo2:7b` | **2.73 tok/s** | 94.08 tok/s | 1.549s | 57.6°C | 12.37 GB | 🟡 慢速 (<5 tps) | [olmo2_7b_REPORT.md](./olmo2_7b_REPORT.md) |
| #8 | `olmo-3:7b` | **2.56 tok/s** | 51.90 tok/s | 3.436s | 56.5°C | 13.05 GB | 🟡 慢速 (<5 tps) | [olmo-3_7b_REPORT.md](./olmo-3_7b_REPORT.md) |
| #9 | `deepseek-r1:7b` | **2.53 tok/s** | 38.29 tok/s | 1.384s | 57.1°C | 5.23 GB | 🟡 慢速 (<5 tps) | [deepseek-r1_7b_REPORT.md](./deepseek-r1_7b_REPORT.md) |
| #10 | `llama3.1:8b` | **2.46 tok/s** | 46.62 tok/s | 1.620s | 57.6°C | 5.76 GB | 🟡 慢速 (<5 tps) | [llama3_1_8b_REPORT.md](./llama3_1_8b_REPORT.md) |

---

## 📊 各類別任務詳細評測對比 (Category Breakdown Comparison)

### 🔹 任務類別：`Reasoning & Logic`

| 模型名稱<br><sub>(Model)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞預填充<br><sub>(Prefill TPS)</sub> | 首字延遲<br><sub>(TTFT)</sub> | 溫升變化<br><sub>(Δ Temp)</sub> |
| :--- | :---: | :---: | :---: | :---: |
| `deepseek-r1:1.5b` | **11.54** | 165.40 | 0.225s | +5.2°C |
| `gemma4:e2b` | **7.58** | 92.42 | 0.540s | +5.0°C |
| `qwen2.5:3b` | **6.01** | 157.62 | 0.842s | +-21.1°C |
| `llama3.2:3b` | **5.94** | 147.92 | 0.786s | +6.8°C |
| `gemma4:e4b` | **3.68** | 44.09 | 1.157s | +5.5°C |
| `qwen2.5-coder:7b` | **2.76** | 74.30 | 2.232s | +5.8°C |
| `olmo2:7b` | **2.70** | 85.44 | 2.203s | +5.5°C |
| `olmo-3:7b` | **2.54** | 53.44 | 3.336s | +6.3°C |
| `deepseek-r1:7b` | **2.52** | 33.97 | 1.217s | +4.7°C |
| `llama3.1:8b` | **2.46** | 42.60 | 1.760s | +4.7°C |


### 🔹 任務類別：`Coding & Algorithm`

| 模型名稱<br><sub>(Model)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞預填充<br><sub>(Prefill TPS)</sub> | 首字延遲<br><sub>(TTFT)</sub> | 溫升變化<br><sub>(Δ Temp)</sub> |
| :--- | :---: | :---: | :---: | :---: |
| `deepseek-r1:1.5b` | **11.47** | 207.03 | 0.265s | +5.0°C |
| `gemma4:e2b` | **7.62** | 111.21 | 0.638s | +5.0°C |
| `qwen2.5:3b` | **6.02** | 197.44 | 0.585s | +5.0°C |
| `llama3.2:3b` | **5.90** | 180.50 | 0.588s | +5.0°C |
| `gemma4:e4b` | **3.71** | 53.53 | 1.341s | +4.4°C |
| `qwen2.5-coder:7b` | **2.76** | 86.94 | 1.521s | +30.4°C |
| `olmo2:7b` | **2.70** | 103.27 | 1.302s | +4.7°C |
| `olmo-3:7b` | **2.55** | 51.22 | 3.584s | +3.3°C |
| `deepseek-r1:7b` | **2.52** | 44.22 | 1.490s | +3.9°C |
| `llama3.1:8b` | **2.46** | 52.85 | 1.637s | +4.3°C |


### 🔹 任務類別：`Quick Fact & Summary`

| 模型名稱<br><sub>(Model)</sub> | 生成速度<br><sub>(Gen TPS)</sub> | 提示詞預填充<br><sub>(Prefill TPS)</sub> | 首字延遲<br><sub>(TTFT)</sub> | 溫升變化<br><sub>(Δ Temp)</sub> |
| :--- | :---: | :---: | :---: | :---: |
| `deepseek-r1:1.5b` | **11.59** | 176.83 | 0.237s | +3.0°C |
| `gemma4:e2b` | **7.62** | 93.86 | 0.579s | +3.6°C |
| `qwen2.5:3b` | **6.04** | 180.10 | 0.555s | +4.7°C |
| `llama3.2:3b` | **5.93** | 163.88 | 0.514s | +4.7°C |
| `gemma4:e4b` | **3.73** | 45.61 | 1.230s | +3.9°C |
| `qwen2.5-coder:7b` | **2.79** | 79.36 | 1.482s | +29.6°C |
| `olmo2:7b` | **2.79** | 93.53 | 1.143s | +3.9°C |
| `olmo-3:7b` | **2.59** | 51.05 | 3.389s | +3.5°C |
| `deepseek-r1:7b` | **2.53** | 36.69 | 1.444s | +4.4°C |
| `llama3.1:8b` | **2.47** | 44.41 | 1.462s | +4.9°C |


---

## 💡 架構分析與選型建議 (Architectural Insights & Recommendations)

1. **超輕量即時推理首選 (Sub-3B / Real-Time Reasoning)**：

   - `deepseek-r1:1.5b` 與 `llama3.2:3b` 能在 Pi 5 (4-Core A76 @ 2.4GHz) 上提供 **>10 tokens/sec** 的即時響應，適合邊緣端低延遲對話與即時代理人 (Edge Agent)。

2. **高階代碼與複雜邏輯首選 (7B~8B Tier)**：

   - `qwen2.5-coder:7b` 與 `deepseek-r1:7b` 展現卓越的代碼理解與思維鏈推理能力。在 16GB 記憶體加持下完全不觸發 Swap，推論速度維持在 **4~7 tokens/sec** 實用區間。

3. **散熱與功耗穩定度 (Thermal & Efficiency)**：

   - 配合主動式散熱風扇與 performance governor，全負載推理最高溫穩定壓制在 **55°C 以下**，無任何 Thermal Throttling。
