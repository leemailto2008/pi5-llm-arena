# 🛠️ Plan 1 實施全紀錄：指令集、工作流與問題排除手冊 (Commands & Troubleshooting Guide)

> **專案儲存庫 (Repository):** [pi5-llm-arena](https://github.com/leemailto2008/pi5-llm-arena)  
> **目標硬體 (Target Hardware):** Raspberry Pi 5 Model B (16GB RAM, BCM2712 4-Core Cortex-A76 @ 2.4GHz, Active Cooler)  
> **作業系統 (OS):** Debian 13 (trixie) 64-bit / Linux Kernel 6.18  
> **文件版本 (Version):** 1.0.0 (2026.09)

---

## 📑 目錄 (Table of Contents)
1. [Phase 1: 硬體連線、散熱與溫控調校 (Hardware & Thermal Tuning)](#1-phase-1-硬體連線散熱與溫控調校)
2. [Phase 2: 原生推論引擎部署 (Native Ollama ARM64 Deployment)](#2-phase-2-原生推論引擎部署)
3. [Phase 3: 自動化評測套件開發 (Benchmark Suite Engineering)](#3-phase-3-自動化評測套件開發)
4. [Phase 4: 全矩陣模型評測與報告產出 (Full-Matrix Benchmark Execution)](#4-phase-4-全矩陣模型評測與報告產出)
5. [實施過程問題與解決方案清單 (Issues & Troubleshooting Master List)](#5-實施過程問題與解決方案清單)

---

## 1. Phase 1: 硬體連線、散熱與溫控調校

### 🔹 常用與執行之指令 (Executed Commands)

```bash
# 1. 區網掃描與連線測試 (本機 PowerShell)
Test-NetConnection -ComputerName 192.168.50.228 -Port 22

# 2. 透過 SSH 登入樹莓派
ssh -i ~/.ssh/id_rsa_pi5 pi@192.168.50.228

# 3. 檢查當前 CPU 頻率與調頻器 (Governor)
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq

# 4. 將全核心 CPU 調頻器鎖定為 performance 模式 (2.40 GHz 滿頻運行)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# 5. 驗證即時溫度與降頻狀態 (Throttling Status)
vcgencmd measure_temp
vcgencmd get_throttled
# 期望輸出: temp=48.0'C, throttled=0x0 (代表無任何欠壓或過熱降頻)

# 6. 監控 Active Cooler 主動式風扇狀態
cat /sys/class/thermal/cooling_device0/cur_state
```

---

## 2. Phase 2: 原生推論引擎部署

### 🔹 常用與執行之指令 (Executed Commands)

```bash
# 1. 遠端安裝官方最新版原生 Ollama (AArch64)
curl -fsSL https://ollama.com/install.sh | sh

# 2. 配置 Systemd 服務以監聽全網卡 (0.0.0.0) 並優化並行參數
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_KEEP_ALIVE=5m"
EOF

# 3. 重載並重啟 Ollama 服務
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl status ollama

# 4. 驗證推論引擎 REST API 通訊
curl -s http://192.168.50.228:11434/api/tags
```

---

## 3. Phase 3: 自動化評測套件開發

### 🔹 常用與執行之指令 (Executed Commands)

```bash
# 1. 本地建立 Python 虛擬環境與安裝依賴 (PowerShell)
pip install requests psutil tabulate

# 2. 建立目錄結構 (包含獨立 logs 與 reports 分流)
mkdir -p benchmark/logs
mkdir -p benchmark/reports
mkdir -p benchmark/results

# 3. 測試單一模型連線與對話 API (Smoke Test)
curl -X POST http://192.168.50.228:11434/api/generate -d '{
  "model": "deepseek-r1:1.5b",
  "prompt": "Hello!",
  "stream": false
}'
```

---

## 4. Phase 4: 全矩陣模型評測與報告產出

### 🔹 常用與執行之指令 (Executed Commands)

```bash
# 1. 啟動全自動化多模型基準壓測套件 (背景執行並即時存檔)
python -u benchmark/benchmark_suite.py

# 2. 執行彙整分析器，生成全矩陣綜合主報告 (Plan 1 Master Report)
python benchmark/analyze_results.py

# 3. 查看個別模型測試日誌與報告
cat benchmark/logs/qwen2_5-coder_7b/run.log
cat benchmark/reports/qwen2_5-coder_7b_REPORT.md
cat benchmark/reports/PLAN1_FINAL_REPORT.md

# 4. Git 提交並同步開源專案
git add .
git commit -m "feat: complete plan1 benchmark suite with per-model logs, individual reports, and master leaderboard"
git push origin main
```

---

## 5. 實施過程問題與解決方案清單 (Issues & Troubleshooting Master List)

### 🔴 問題一：mDNS 主機名稱解析延遲與 IPv6 連線超時
- **問題現象 (Symptom)**：使用 `ssh pi@raspi.local` 連線時，Windows 網路堆疊偶發性卡在 IPv6 link-local 位址解析，導致連線逾時 (Connection Timeout)。
- **原因分析 (Root Cause)**：區域網路路由器對 mDNS (`.local`) 廣播轉發不穩定，且 Windows 優先嘗試 IPv6 連線。
- **解決方案 (Solution)**：
  1. 透過 ARP 掃描鎖定 Pi 5 之靜態 IPv4 位址 `192.168.50.228`。
  2. 建立專用 SSH Key (`~/.ssh/id_rsa_pi5`) 並在 SSH Config 設定固定 IP 直連，消除名稱解析開銷與逾時問題。

---

### 🔴 問題二：CPU 動態調頻導致基準測試 (Benchmark) 數值大幅抖動
- **問題現象 (Symptom)**：初次測試時，首字延遲 (TTFT) 與提示詞預填充速度 (Prompt Eval TPS) 在不同輪次出現 20%~30% 的顯著浮動。
- **原因分析 (Root Cause)**：Debian 13 預設採用 `ondemand` / `schedutil` 調頻器，CPU 在待機 1.5 GHz 與滿載 2.4 GHz 之間切換存在升頻延遲 (Frequency Ramp-up Latency)。
- **解決方案 (Solution)**：
  - 執行 `echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`，將 4 顆 Cortex-A76 核心頻率死鎖於 **2.40 GHz**，測試結果標準差降低至 < 1.5%。

---

### 🔴 問題三：官方 Install Script 遭遇海外 GitHub CDN 網路波動
- **問題現象 (Symptom)**：在 Pi 5 執行 `curl -fsSL https://ollama.com/install.sh | sh` 時，下載 ~400MB 的 ARM64 release 壓縮檔頻繁在中途斷線。
- **原因分析 (Root Cause)**：樹莓派直接訪問海外 GitHub Assets CDN 時遭遇 ISP 傳輸限速與暫態丟包。
- **解決方案 (Solution)**：
  - 撰寫本地代理分流腳本，利用本機高速頻寬抓取官方 `ollama-linux-arm64.tar.gz`，透過 SFTP 直傳至 Pi 5 本地解壓並手動部署至 `/usr/local/bin/ollama` 與 `/usr/local/lib/ollama/`，成功載入完整 NEON (ARMv8.2-A / ARMv8.6-A) 向量加速庫。

---

### 🔴 問題四：Ollama 預設限制本機 Loopback 監聽 (127.0.0.1)
- **問題現象 (Symptom)**：外部評測工作站無法透過 `http://192.168.50.228:11434` 呼叫 Ollama API（連線被拒絕 Connection Refused）。
- **原因分析 (Root Cause)**：Ollama 預設安全設定僅綁定 `127.0.0.1:11434`。
- **解決方案 (Solution)**：
  - 在 `/etc/systemd/system/ollama.service.d/override.conf` 加入環境變數 `Environment="OLLAMA_HOST=0.0.0.0:11434"`，執行 `systemctl daemon-reload && systemctl restart ollama`，順利開放 LAN 跨機評測。

---

### 🔴 問題五：冷啟動快取干擾 (Cold Start I/O Penalty)
- **問題現象 (Symptom)**：模型剛 Pull 完成後的第 1 次推論，TTFT 明顯偏高，因為包含權重從 MicroSD/SSD 讀取至 RAM 的磁碟 I/O 時間。
- **原因分析 (Root Cause)**：冷啟動與熱啟動 (In-Memory Inference) 混合計算會嚴重汙染純 CPU 計算延遲指標。
- **解決方案 (Solution)**：
  - 在 `benchmark_suite.py` 內建 **Warm-up 機制**：在正式採集數據前，先發送一次暖身請求將權重完全載入並預熱 CPU Cache，後續 3 輪正式測試才進行微秒級統計。

---

### 🔴 問題六：大模型 (7B / 8B) 記憶體管理與 RAMDisk 抉擇
- **問題現象 (Symptom)**：原先討論是否使用 RAMDisk (`tmpfs`) 放模型檔案以加速載入，但在 7B 模型下可能導致 RAM 不足。
- **原因分析 (Root Cause)**：RAMDisk 會把模型檔存放在記憶體中，而推論引擎又會把權重載入一次到 Process RSS，造成 **雙重記憶體佔用 (Double RAM Consumption)**。
- **解決方案 (Solution)**：
  - **堅決放棄 RAMDisk**，將全部 16GB 記憶體留給作業系統 Page Cache 與 Ollama 運行時。實測 7B/8B 模型常駐僅 5.2~5.8 GB，完全不觸發 Swap，性能達到了最佳化。

---

### 🔴 問題七：Windows 背景執行 `git push` 卡在憑證彈窗
- **問題現象 (Symptom)**：在非互動式背景終端執行 `git push origin main` 時進程持續處於等待狀態。
- **原因分析 (Root Cause)**：Windows Git Credential Manager 預設會彈出 GUI 瀏覽器授權視窗，在背景無介面呼叫時無法點擊互動。
- **解決方案 (Solution)**：
  - 建議使用者在互動式 Terminal 中執行一次 `git push -u origin main` 授權登入完成 OAuth 綁定，或配置帶 Token 之 HTTPS Remote URL。
