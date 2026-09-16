# DeepSeek-R1-Distill-Qwen-7B: 強化學習與思考鏈蒸餾模型研讀報告 (Technical Paper Review)

## 1. 論文基本資訊 (Paper Metadata)
- **論文題目 (Title):** *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*
- **研發機構 (Organization):** DeepSeek-AI
- **發布時間 (Release Date):** 2025 年 1 月
- **論文連結 (arXiv):** [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
- **開源許可證 (License):** MIT (完全無限制開源與商用)
- **模型實體:** `deepseek-r1:7b` (以 Qwen2.5-Math-7B / Qwen2.5-7B 為基底，蒸餾 DeepSeek-R1 80 萬條優質思考鏈樣本)

---

## 2. 核心技術突破與理論機制 (Core Theoretical Breakthroughs)

### 2.1 論文革命性里程碑：DeepSeek-R1-Zero 與 純強化學習 (Pure RL)
DeepSeek 在該論文中首次證實：
- **無需人類監督微調 (Zero SFT)**：僅透過基於規則的獎勵函數 (Rule-based Rewards: 答案正確性與格式規範性)，利用 **GRPO (Group Relative Policy Optimization)** 演算法，模型即可自發學會：
  1. 長思考鏈推演 (Long Chain-of-Thought, CoT)。
  2. 自我質疑與自我反思 (Self-Reflection / Self-Correction)。
  3. 發現新的解題途徑（著名的「Aha Moment」顿悟現象）。

### 2.2 GRPO (Group Relative Policy Optimization)
傳統 PPO 算法需要訓練一個獨立的 Critic 模型來預測價值基線 (Baseline)，在 671B 等級模型上顯存與計算開銷巨大。
GRPO 的創新在於：
- 對同一個 Prompt 取樣一組（Group）輸出序列 $\{o_1, o_2, ..., o_G\}$。
- 計算該組回傳的平均分數與標準差，以群體相對表現作為優勢函數 (Advantage) 計算依據：
  $$A_i = \frac{r_i - \text{mean}(r)}{\text{std}(r)}$$
- 徹底省去了龐大的 Critic 神經網路，訓練效率成倍提升。

### 2.3 知識蒸餾 (Distillation to Dense Models)
DeepSeek-R1 利用 671B 大模型產生的 80 萬條高質量推理樣本（包含完整思考過程與最終答案），直接對 Qwen2.5-7B 進行監督微調蒸餾。
- **論文重要發現**：直接蒸餾強大 R1 模型的思考鏈數據，比讓小型 7B 模型自己做 RL 強化學習的效果顯著更好，徹底打破了「小模型不具備高階推理能力」的迷思。

---

## 3. 實測推理特性 (Reasoning Characteristics)

- **思考標籤標註**：輸出會嚴格包裝在 `<think>...</think>` 中，顯示探索、假設、排除矛盾的完整內心獨白，隨後給出精準解答。
- **數學與競程表現**：在 AIME 2024 (美國數學邀請賽) 與 MATH-500 基準上，7B 蒸餾模型的表現媲美 OpenAI o1-mini！

---

## 4. Raspberry Pi 5 實測特性剖析 (Pi 5 Hardware Profiling)

- **量化格式 (Quantization):** `Q4_K_M`
- **RAM 佔用:** 約 **4.7 GB**
- **推論速度:** 約 **2.3 ~ 2.6 tok/s**
- **邊緣端使用核心注意事項 (Critical Latency Reality):**
  - 因為 R1-7B 的思考鏈極其詳細，單次問題生成的總 Token 數常達 **500 ~ 1200 Tokens**。
  - 在 Pi 5 上推論一個邏輯題，總耗時通常在 **3 ~ 7 分鐘**。
  - **建議配置:** 在 Web UI 或 API 端點呼叫時，需適當設定較長的 HTTP Timeout (例如 600s 以上)，防止客戶端逾時。
