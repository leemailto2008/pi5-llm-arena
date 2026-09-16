# Raspberry Pi 5 邊緣 AI 模型極限優化指南與可行性評估矩陣 (Edge AI Optimization Guide & Evaluation Matrix)

本文件針對部署於 **Raspberry Pi 5 (Broadcom BCM2712, 4-Core ARM Cortex-A76 @ 2.4GHz, 16GB LPDDR4X)** 的 10 款 AI 模型，從**硬體底層、推論引擎、量化工藝、投機解碼與架構調優**五大工程維度，提供系統性可落地的優化改良方案與量化評估矩陣。

---

## 一、邊緣推論瓶頸分析：為什麼需要優化？ (Bottleneck Analysis)

在 ARM Cortex-A76 架構上運行大語言模型 (LLM)，其運算特徵為：
1. **記憶體頻寬受限 (Memory-Bandwidth Bound)**：
   - Pi 5 採用 LPDDR4X-4267 雙通道記憶體，理論峰值頻寬約 **17.06 GB/s**。
   - 7B 模型 (Q4 量化約 4.5 GB) 每次生成 1 個 Token 必須從記憶體讀取全部 4.5 GB 權重，理論極限速度即為 $17.06 \div 4.5 \approx 3.79\text{ tok/s}$。實務上加上 CPU 開銷約 2.2 ~ 2.8 tok/s。
   - **結論**：提升速度最直接有效的手段是**壓縮模型位元組大小 (Model Weight Footprint)** 或**減少解碼記憶體搬移次數**。
2. **運算單元限制 (Compute Limitation)**：
   - 無獨立 NPU，完全依賴 4 核心 ARM NEON 128-bit SIMD 向量運算指令集。
   - 無法執行 BF16/FP16 高密度矩陣乘法，必須採用 `int8` / `int4` 整數點積指令 (`SDOT` / `UDOT`)。

---

## 二、五大核心優化改良維度 (5 Core Optimization Dimensions)

### 1. 投機解碼 (Speculative Decoding / Draft-Target Pipeline) ★★★★★
- **技術原理**：
  以超微型草稿模型 (Draft Model，如 `deepseek-r1:1.5b` 或 `qwen2.5:0.5b`，速度 25~40 tok/s) 連續快速推測 $K$ 個候選 Tokens，再由主幹目標模型 (Target Model，如 `qwen2.5-coder:7b` 或 `llama3.1:8b`) 於**單次前向傳播 (Single Forward Pass)** 中並行批次驗證。
- **優勢**：
  在保持 7B/8B 旗艦模型 100% 相同輸出分佈與精度的前提下，將生成速度提昇 **1.8x ~ 2.5x** (可將 7B 速度推至 4.5 ~ 6.0 tok/s)。

### 2. 重要性矩陣極限感知量化 (Importance Matrix Quantization: i-Matrix & IQ3/IQ4) ★★★★☆
- **技術原理**：
  捨棄標準的傳統 `Q4_K_M`，改採 llama.cpp 的 **iMatrix (Importance Matrix)** 離線校準量化。針對特定驗證集計算各權重張量對 Loss 的敏感度，敏感矩陣分配 4-bit/5-bit，非敏感矩陣降至 2-bit/3-bit (`IQ3_M` 或 `IQ3_S`)。
- **效益**：
  - 7B 模型大小自 4.7 GB 降至 **3.2 GB** (~32% 記憶體縮減)。
  - 記憶體頻寬需求大減，推論速度直接由 2.4 tok/s 提昇至 **3.4 ~ 3.8 tok/s**，且困惑度 (Perplexity) 幾乎無感增加 (<0.15)。

### 3. KV Cache 量化與上下文快取複用 (KV Cache Quantization & Context Pinning) ★★★★☆
- **技術原理**：
  預設情況下，注意力快取 (KV Cache) 以 FP16 精度儲存於 RAM 中。在 128k 或 32k 長文本對話下，KV Cache 往往暴增至 2GB ~ 6GB。
- **改良手段**：
  - 開啟 `--cache-type-k q8_0 --cache-type-v q8_0` (甚至 `q4_0`)，將 KV 快取空間壓縮至 25% ~ 50%。
  - **Prompt Caching (提示詞預熱固化)**：針對固定 System Prompt (例如代碼審查標準指引) 預先固化計算好的 KV Cache，消除首字延遲 (TTFT)。

### 4. 執行緒親和性與 Linux 核心排程調優 (CPU Thread Affinity & Core Optimization) ★★★☆☆
- **技術原理**：
  Linux 預設的 CFS (Completely Fair Scheduler) 會頻繁在 4 個 Cortex-A76 核心間遷移線程，引發 L1/L2 Cache 頻繁失效 (Cache Thrashing)。
- **改良手段**：
  - 使用 `taskset -c 0,1,2,3` 明確綁定 4 核心。
  - 將 CPU 調速器 (Governor) 鎖定為 `performance` 模式 (`cpufreq-set -g performance`)。
  - 關閉 Swap/ZRAM 換頁抖動，啟用 Transparent Huge Pages (THP)。

### 5. 邊緣微調：特定領域 LoRA 轉接器 (Domain-Specific LoRA Adapters) ★★★☆☆
- **技術原理**：
  直接在雲端微調好特定領域 (如繁體中文軟體工程規範、台灣在地問答、物聯網感測器 JSON 轉換) 的 LoRA 轉接器權重 (僅 10MB ~ 50MB)，並在 Pi 5 邊緣直接熱插拔掛載至 3B 基礎模型。
- **效益**：以 3B 模型的速度 (20 tok/s) 獲取超越通用 7B 的垂直領域精確度。

---

## 三、模型優化方案綜合評估表 (Optimization Feasibility & Evaluation Matrix)

| 優化技術方案 (Technique) | 實施層級 (Layer) | 預期加速比 (Speedup) | 記憶體節省比 (RAM Saved) | 精度損耗 (Accuracy Loss) | 實施複雜度 (Complexity) | 推薦優先級 (Priority) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **投機解碼 (Speculative Decoding)** | 推論執行時 (Runtime) | **+80% ~ +150% (1.8x~2.5x)** | 無節省 (需額外加載 1.5B 草稿模型約 1GB) | **0% (完全無損)** | 中 (需配置草稿/目標雙模型) | **P0 (極力推薦)** |
| **IQ3_M / IQ4_XS iMatrix 量化** | 權重編譯 (Compiler) | **+25% ~ +45%** | **節省 25% ~ 35%** | 極微小 (PPL +0.08 ~ +0.15) | 中 (需透過 llama.cpp 離線轉檔) | **P0 (性價比最高)** |
| **KV Cache 量化 (Q8_0 / Q4_0)** | 記憶體引擎 (Engine) | 長序列下 **+15% ~ +30%** | **長文本快取節省 50%~75%** | 幾乎無感 (PPL +0.02) | 低 (啟動參數直接指定) | **P0 (必開設定)** |
| **CPU 核心鎖定 + Performance 模式** | OS / 系統底層 (Kernel) | **+8% ~ +15%** | 0% | 0% (完全無損) | 極低 (Linux 指令直接生效) | **P1 (即刻實施)** |
| **主板 Active Cooler 超頻 (2.8GHz)** | 硬體設施 (Hardware) | **+15% ~ +20% (線性)** | 0% | 0% (完全無損) | 低 (需編輯 `config.txt`) | **P1 (硬體許可時推薦)** |
| **Prompt 預計算固化 (Context Cache)**| 應用架構 (App Architecture) | **TTFT 首字縮短 70%~90%** | 0% | 0% (完全無損) | 中 (需適配 API 固化參數) | **P1 (大幅改善體感)** |
| **LoRA 轉接器外掛 (LoRA Adapter)** | 模型算法 (Algorithm) | 0% (速度不變) | 0% (微增 20MB) | **精度大幅提升 (+15%~30%)** | 高 (需前期雲端微調訓練) | **P2 (依業務需求選用)** |

---

## 四、針對目前 10 款模型的專屬優化配方針對錶 (Per-Model Optimization Recipes)

| 模型標籤 (Model Tag) | 目前實測現況 | 最佳優化組合配方 (Recommended Recipe) | 優化後預期指標 (Post-Optimization) |
| :--- | :--- | :--- | :--- |
| **01. gemma4:e4b** | 4.5 tok/s, 4.8GB | 開啟 Flash-Attention + 影像投影層動態剪枝 + Q8_0 KV Cache | **6.5 ~ 7.2 tok/s**, RAM 降至 4.1GB |
| **02. gemma4:e2b** | 14 tok/s, 2.6GB | 綁定 4-Core CPU + CPU 2.8GHz 超頻 + INT8 視覺 Token 快取 | **18 ~ 22 tok/s**, 達成超即時視覺回饋 |
| **03. olmo2:7b** | 2.6 tok/s, 4.3GB | 採用 **IQ3_M** 重新量化 (自 4.3GB 壓至 3.1GB) + Q8_0 KV | **3.8 ~ 4.2 tok/s** (提昇 ~50%) |
| **04. olmo-3:7b** | 2.4 tok/s, 4.5GB | SWA 4k 滑動窗口鎖定 + 思考標籤提早停止策略 (Early-stopping) | 避免無效思考迴圈，整體任務時長縮短 40% |
| **05. llama3.1:8b** | 2.2 tok/s, 4.9GB | **Speculative Decoding** (以 Llama 3.2 1B/3B 為草稿模型驗證) | **4.2 ~ 5.5 tok/s** (接近翻倍體驗) |
| **06. deepseek-r1:7b** | 2.3 tok/s, 4.7GB | **Speculative Decoding** (以 DeepSeek-R1-1.5B 作為 Draft Model) | **4.5 ~ 5.8 tok/s**，且保留完整思維鏈深度 |
| **07. qwen2.5-coder:7b**| 2.4 tok/s, 4.7GB | **Speculative Decoding** (搭配 Qwen2.5-Coder-1.5B) + FIM 提示詞固化 | **4.8 ~ 6.0 tok/s**，代碼審查等待時間腰斬 |
| **08. qwen2.5:3b** | 18 tok/s, 1.9GB | 啟用 `cpufreq performance` + Q4_0 KV Cache + 繁中專項 LoRA | **22 ~ 26 tok/s**，媲美雲端 API 流式響應 |
| **09. llama3.2:3b** | 20 tok/s, 2.0GB | 綁定核心 Affinity + 128k 上下文 Q8_0 KV Cache | **24 ~ 28 tok/s**，長文摘要無痛秒回 |
| **10. deepseek-r1:1.5b**| 25 tok/s, 1.1GB | CPU NEON 向量化全開 + 作為 7B 模型的草稿協處理器 (Co-processor) | **30 ~ 35 tok/s** 極限吞吐 |

---

## 五、第一階段推薦落地工程指令 (Quick Win Actions)

### 步驟 1：啟用 Linux 效能模式與 CPU 頻率鎖定
在 Pi 5 終端機執行下列指令（立即可見 8~12% 推論加速）：
```bash
# 安裝 CPU 頻率工具
sudo apt-get install -y cpufrequtils

# 將 4 個 Cortex-A76 核心鎖定於最高頻率 2.4GHz
sudo cpufreq-set -r -g performance

# 驗證當前核心頻率
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
```

### 步驟 2：設定 Ollama / 推論引擎最佳環境變數
在 Pi 5 的 `/etc/systemd/system/ollama.service.d/override.conf` (或啟動腳本) 注入：
```ini
[Service]
# 限制並行任務為 1，避免多模型搶佔 RAM 與 L2 Cache
Environment="OLLAMA_NUM_PARALLEL=1"
# 鎖定 4 個實體核心
Environment="OLLAMA_NUM_THREADS=4"
# 允許記憶體預先保留
Environment="OLLAMA_FLASH_ATTENTION=1"
# 啟用 KV Cache 壓縮
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
```

### 步驟 3：部署投機解碼 (Speculative Decoding Pipeline)
針對代碼審查閘道 (Code Dispatcher)，可在背景排程中建立協同腳本：
1. 先由 `deepseek-r1:1.5b` (或 `qwen2.5-coder:1.5b`) 產出草稿 (Draft)。
2. 再由 `qwen2.5-coder:7b` 進行核驗。
3. 可在 FastAPI 閘道中以非同步流水線無縫完成，將使用者的平均等待時間由 3 分鐘縮短至 1 分 15 秒以內。
