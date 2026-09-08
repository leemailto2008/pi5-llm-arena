# Raspberry Pi 5 原生編譯 llama.cpp (ARM NEON / DotProd 加速) 實作與極限壓測操作手冊

> **專案 (Project):** `pi5-llm-arena`  
> **目標硬體 (Hardware):** Raspberry Pi 5 16GB (Broadcom BCM2712, 4-Core ARM Cortex-A76 @ 2.4 GHz, LPDDR4X-4267)  
> **文件代號 (Doc ID):** `plan2_cmd.md`  
> **技術核心 (Core Tech):** Native `llama.cpp` 原生最佳化編譯、ARMv8.2-a DotProd / FP16 向量加速、`llama-bench` 底層微基準測試 (Micro-Benchmarking)

---

## 1. 系統環境準備與依賴套件安裝 (Prerequisites Installation)

在 Raspberry Pi OS (Debian 12 Bookworm, 64-bit ARM64) 上安裝最新編譯工具鏈：

```bash
# 1. 更新系統套件庫清單 (Update Package Index)
sudo apt update && sudo apt upgrade -y

# 2. 安裝核心建置工具鏈 (Build Essentials & Compiler)
sudo apt install -y \
  build-essential \
  cmake \
  ninja-build \
  gcc \
  g++ \
  git \
  pkg-config \
  curl \
  libomp-dev \
  wireless-tools \
  iw
```

驗證編譯器與硬體架構：
```bash
gcc --version        # 建議 GCC 12.2.0 或 14.2.0+
cmake --version      # 建議 CMake 3.25+
lscpu | grep "Model name\|Flags"  # 確認支援 fp16, asimd, asimddp, crc32 等指令集
```

---

## 2. 下載 llama.cpp 原始碼與原生硬體最佳化編譯 (Native Compilation)

針對 Raspberry Pi 5 的 **Broadcom BCM2712 (ARM Cortex-A76)** 晶片特性，啟用專屬 CPU 微架構參數與 ARMv8.2-a 擴展指令集 (`fp16` 半精度浮點運算、`dotprod` 點積加速向量計算)：

```bash
# 1. 取得 llama.cpp 最新原始碼
cd /home/pi
git clone https://github.com/ggerganov/llama.cpp.git
cd /home/pi/llama.cpp

# 2. 建立專屬建置目錄並透過 CMake 配置最佳化編譯參數 (ARMv8.2-a + DotProd + FP16)
cmake -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CPU_AARCH64=ON \
  -DCMAKE_C_FLAGS="-mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod" \
  -DCMAKE_CXX_FLAGS="-mcpu=cortex-a76 -O3 -march=armv8.2-a+fp16+dotprod"

# 3. 執行平行編譯 (4 核心全開)
cmake --build build --config Release -j4 --target llama-bench llama-cli
```

### 編譯成果驗證 (Build Verification)
確認產生之執行檔已成功嵌入 ARM Cortex-A76 向量指令：
```bash
./build/bin/llama-bench --help
./build/bin/llama-cli --version
```
輸出確認：
- `ARM_NEON = 1`
- `ARM_FMA = 1`
- `ARM_FP16_VECTOR_ARITHMETIC = 1`
- `DOTPROD = 1`

---

## 3. Ollama GGUF 權重解析 (Zero-Copy Evaluation)

為了在 Native `llama.cpp` 中直接評測現有的 6 款模型，無需重複從 Hugging Face 下載數十 GB 的 GGUF 權重，我們直接讀取 Ollama 本地儲存的 Blobs：

```bash
# Ollama 模型 Blobs 儲存目錄
ls -lh ~/.ollama/models/blobs/
```

### 模型對應表 (Model Blob Mapping)
| 模型名稱<br><sub>(Model Name)</sub> | 參數量<br><sub>(Parameters)</sub> | 磁碟大小<br><sub>(File Size)</sub> | GGUF Blob 路徑<br><sub>(Ollama Blob Path)</sub> |
| :--- | :--- | :--- | :--- |
| `deepseek-r1:1.5b` | 1.5B | 1.04 GB | `~/.ollama/models/blobs/sha256-aabd4debf0c8f08881923f2c25fc0fdeed24435271c2b3e92c4af36704040dbc` |
| `llama3.2:3b` | 3B | 1.88 GB | `~/.ollama/models/blobs/sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff` |
| `qwen2.5:3b` | 3B | 1.80 GB | `~/.ollama/models/blobs/sha256-5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6` |
| `qwen2.5-coder:7b` | 7B | 4.36 GB | `~/.ollama/models/blobs/sha256-60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463` |
| `deepseek-r1:7b` | 7B | 4.36 GB | `~/.ollama/models/blobs/sha256-96c415656d377afbff962f6cdb2394ab092ccbcbaab4b82525bc4ca800fe8a49` |
| `llama3.1:8b` | 8B | 4.58 GB | `~/.ollama/models/blobs/sha256-667b0c1932bc6ffc593ed1d03f895bf2dc8dc6df21db3042284a6f4416b06a29` |

---

## 4. 系統層調優與穩定度防護 (System Tuning & Stability)

在 Raspberry Pi 5 上以 4 核心 100% 滿載進行 7B/8B 模型矩陣計算時，極易因 CPU 資源與記憶體頻寬飽和導致 SSH 連線被飢餓斷開 (`client_loop: send disconnect`)。透過以下設定進行系統層隔離防護：

```bash
# 1. 將 CPU 調頻器設為效能模式 (Performance Governor)
sudo cpupower frequency-set -g performance || sudo bash -c 'for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $g; done'

# 2. 停用 Wi-Fi 省電休眠模式 (Disable Wi-Fi Power Saving)
sudo /usr/sbin/iw dev wlan0 set power_save off

# 3. 配置 SSH 服務端的心跳保持 (Keepalive)
sudo bash -c 'cat >> /etc/ssh/sshd_config.d/keepalive.conf << EOF
ClientAliveInterval 30
ClientAliveCountMax 10
EOF'
sudo systemctl restart ssh
```

---

## 5. 基準壓測指令 (Benchmarking Commands)

### (A) 單一模型快速壓測指令 (Single Model Micro-Benchmark)
以 `llama3.2:3b` 為例：
```bash
# 測試 Standard Interaction (P512 / G128)
/home/pi/llama.cpp/build/bin/llama-bench \
  -m /home/pi/.ollama/models/blobs/sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff \
  -t 4 \
  -p 512 \
  -n 128 \
  -r 2 \
  -o json
```

### (B) 完整全矩陣自動化壓測套件 (Full Matrix Runner)
透過自建之非同步守護進程腳本 `pi5_plan2_local_runner.py`，以 `nice -n 10` 低優先級執行以確保系統排程平衡：

```bash
# 啟動背景全矩陣自動壓測
nohup nice -n 10 python3 -u /home/pi/pi5_plan2_local_runner.py > /home/pi/plan2_bench.log 2>&1 &

# 即時追蹤壓測進度與硬體遙測日誌
tail -f /home/pi/plan2_bench.log
```

---

## 6. 結果數據分析與報告生成 (Analysis & Reporting)

壓測完成後，自動計算平均吞吐量、標準差、相較於 Native Ollama 與 Docker 之效能增益，並產出分析報告：

```bash
# 執行結果彙整與跨架構三方對比程式
python3 benchmark/plan2_analyze_results.py
```

產出物路徑清單：
- 全矩陣最終總體報告：`benchmark/reports/PLAN2_FINAL_REPORT.md`
- 各模型獨立報告：`benchmark/reports/plan2_{model}_REPORT.md`
- 原始 JSON 數據：`benchmark/results/plan2_benchmark_summary.json`
- 底層 Raw Log：`benchmark/logs_plan2/{model}/`

---

## 7. 疑難排解與實務經驗手冊 (Troubleshooting Guide)

### 問題 1: 執行 7B/8B 模型壓測時 SSH 連線中斷 (`client_loop: send disconnect`)
- **根本原因 (Root Cause):** `llama-bench` 啟動 4 執行緒執行 GEMM 運算時 100% 佔用 4 個 Cortex-A76 核心，導致 Linux Scheduler 無法及時分配 CPU 週期給 `sshd` 與網路中斷處理程式，TCP 連線因心跳逾時而中斷。
- **標準解法 (Solution):** 
  1. 不透過互動式 SSH Shell 直接前台運行，改用本地 Python 腳本 `pi5_plan2_local_runner.py` 搭配 `nohup nice -n 10` 在背景運行。
  2. 執行 `sudo /usr/sbin/iw dev wlan0 set power_save off` 避免 Wi-Fi 網卡進入省電狀態。

### 問題 2: CMake 找不到 Cortex-A76 專屬優化或報錯未知參數
- **根本原因 (Root Cause):** 舊版 GCC (如 GCC 10 或更早版本) 未完整支援 ARMv8.2-a DotProd 編譯標誌。
- **標準解法 (Solution):** 升級至 Debian Bookworm 官方 GCC 12.2+ 或 14.2+，並指定 `-mcpu=cortex-a76 -march=armv8.2-a+fp16+dotprod`。

### 問題 3: Ollama Blob GGUF 魔術標頭不匹配
- **根本原因 (Root Cause):** 部分早期下載的模型 Blob 可能含有自訂 Modelfile 封裝或非 GGUF 格式。
- **標準解法 (Solution):** 透過 `head -c 4 <blob_file>` 驗證前 4 位元組是否為 `GGUF` (Hex: `47 47 55 46`)，若為標準 GGUF 即可直接傳入 `llama-bench` 進行測試。
