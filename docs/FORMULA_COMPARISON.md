# 演算法公式比較與分析

## 兩種獎勵演算法的核心差別

根據您提供的照片公式和程式碼實作，這兩種演算法的確有根本性的差別：

---

## 1. 🎯 **鄰近性演算法 (Proximity-Based Algorithm)**

### 核心公式

```
proximity_reward = old_distance - new_distance
scaled_reward = proximity_reward × proximity_multiplier
```

其中：

- `proximity_multiplier = base_multiplier + (max_multiplier × progress)`
- `progress = 1 - (distance_to_destination / max_possible_distance)`

### 特徵

- **線性關係**：獎勵與距離呈線性關係
- **步進式改善**：每次移動只看距離差異
- **漸進式獎勵**：越接近目標，乘數越大

---

## 2. 📈 **指數距離演算法 (Exponential Distance Algorithm)**

### 核心公式（您照片中的公式）

```
r = base_reward + amplitude × exp(-(|xi-xd|/x_scale + |yi-yd|/y_scale))
```

其中：

- `xi, yi` = 當前位置座標
- `xd, yd` = 目標位置座標  
- `x_scale, y_scale` = X和Y方向的縮放因子
- `amplitude` = 振幅參數
- `base_reward` = 基礎獎勵

### 特徵

- **指數衰減關係**：獎勵隨距離指數衰減
- **高靈敏度**：在接近目標時獎勵變化更劇烈
- **非線性響應**：距離變化對獎勵的影響非線性

---

## 主要差別總結

| 特徵 | 鄰近性演算法 | 指數距離演算法 |
|------|-------------|---------------|
| **數學關係** | 線性 | 指數衰減 |
| **獎勵敏感度** | 均勻分布 | 接近目標時高敏感 |
| **學習行為** | 穩定、漸進 | 激進、快速收斂 |
| **計算複雜度** | O(1) | O(1) + exp運算 |
| **適用場景** | 一般導航 | 精確定位 |

---

## 實際效果差異

### 鄰近性演算法

- 車輛會**穩定地**朝目標移動
- 學習過程**平穩**，較少振盪
- 適合**大範圍導航**

### 指數距離演算法

- 車輛在**接近目標時會更積極**
- 可能出現**更精確的最終定位**
- 適合需要**精確到達**的場景

您的照片公式正是指數距離演算法的數學表達式！
