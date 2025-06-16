# 多演算法支援功能完成總結

## ✅ 已完成的功能

### 1. 新增指數距離演算法

基於圖片中的公式實現：

```
r = -1 + 40 × exp(-(|xi-xd|/1.5 + |yi-yd|/2.0))
```

**特點：**

- 使用指數衰減函數計算距離獎勵
- 支援 x 和 y 方向的不同縮放因子
- 更精細的目標接近獎勵機制

### 2. 演算法選擇系統

- ✅ **Proximity Based** - 原始的距離基礎獎勵系統
- ✅ **Exponential Distance** - 新的指數距離獎勵系統
- ✅ GUI 下拉選單讓用戶選擇演算法
- ✅ 即時演算法切換功能

### 3. 獎勵配置擴展

**新增參數：**

- `algorithm` - 演算法選擇 ("proximity_based" 或 "exponential_distance")
- `exp_base_reward` - 指數演算法基礎獎勵 (預設: -1)
- `exp_amplitude` - 指數函數振幅 (預設: 40)
- `exp_x_scale` - X方向縮放因子 (預設: 1.5)
- `exp_y_scale` - Y方向縮放因子 (預設: 2.0)

### 4. GUI 界面增強

- ✅ 在獎勵配置區域新增演算法選擇下拉選單
- ✅ 在進階設定標籤頁新增指數演算法參數
- ✅ 新增指數距離演算法預設配置
- ✅ 支援即時參數調整和應用

## 🎯 兩種演算法比較

### Proximity Based (原始演算法)

**優點：**

- 線性距離獎勵，行為可預測
- 適合一般路徑規劃
- 計算簡單，性能好

**適用場景：**

- 需要穩定路徑規劃的情況
- 大規模模擬
- 基礎訓練

### Exponential Distance (新演算法)

**優點：**

- 非線性獎勵，更細緻的目標接近行為
- 可調整的方向性權重 (x_scale, y_scale)
- 更強的目標導向性

**適用場景：**

- 需要精確目標接近的情況
- 特殊環境布局 (如長寬比例不同的地圖)
- 研究不同獎勵函數的影響

## 🚀 使用方法

### 1. 啟動演算法選擇GUI

```bash
python test_algorithm_selection.py
```

### 2. 在GUI中切換演算法

1. 找到 "Reward Configuration" 區域
2. 在 "Algorithm:" 下拉選單中選擇演算法
3. 調整對應的參數
4. 點擊 "Apply Reward Config"
5. 開始模擬觀察差異

### 3. 預設配置

- **Aggressive** - 使用 proximity_based，快速直接
- **Cautious** - 使用 proximity_based，探索性強
- **Exponential Distance** - 使用指數演算法的最佳參數
- **Balanced** - 預設的平衡配置

## ⚙️ 指數演算法參數調整指南

### Base Reward (基礎獎勵)

- **建議值**: -1 到 -5
- **作用**: 每步的基本成本

### Amplitude (振幅)

- **建議值**: 20 到 100
- **作用**: 控制距離獎勵的強度

### X/Y Scale Factor (縮放因子)

- **建議值**: 0.5 到 5.0
- **作用**: 控制各方向的敏感度
- **較小值**: 該方向更敏感
- **較大值**: 該方向較不敏感

## 📊 實驗建議

### 比較實驗

1. 使用相同環境設定
2. 分別測試兩種演算法
3. 記錄到達時間、路徑效率
4. 觀察行為差異

### 參數調優

1. 從預設值開始
2. 逐步調整單一參數
3. 觀察行為變化
4. 記錄最佳組合

## 🔧 技術實現

### 核心類別修改

- **RewardConfig**: 新增演算法參數支援
- **Vehicle**: 實現兩套獎勵計算邏輯
- **SimulationController**: GUI 演算法選擇界面

### 演算法切換邏輯

```python
if self.reward_config.algorithm == "exponential_distance":
    reward = self.calculate_exponential_distance_reward(new_position)
else:
    reward = self.calculate_proximity_based_reward(new_position)
```

## ✨ 主要優勢

### 1. 靈活性

- 即時切換演算法
- 無需重新編譯或重啟
- 保持所有其他功能不變

### 2. 可比性

- 相同環境下測試不同演算法
- 客觀評估演算法性能
- 研究獎勵函數設計的影響

### 3. 擴展性

- 易於新增更多演算法
- 模組化設計
- 向後兼容

這個多演算法支援系統讓您可以在運行時輕鬆比較不同的獎勵策略，為車輛行為研究提供了強大的實驗工具！🚗💨
