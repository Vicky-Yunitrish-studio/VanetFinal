# 強化學習演算法參數詳解 (RL Algorithm Parameters Guide)

## 📋 參數來源對照表

| 參數符號 | 英文名稱 | 中文名稱 | 來源位置 | 預設值 | 意義 |
|---------|---------|---------|----------|--------|------|
| `α` | learning_rate | 學習率 | `agent.py` | 0.2 | 控制學習速度 |
| `γ` | discount_factor | 折扣因子 | `agent.py` | 0.95 | 未來獎勵的重要性 |
| `ε` | epsilon | 探索率 | `agent.py` | 0.2 | 探索vs利用平衡 |
| `s` | state | 狀態 | `vehicle.move()` | 動態計算 | 車輛當前環境狀態 |
| `a` | action | 動作 | `agent.choose_action()` | 0-3 | 車輛移動方向 |
| `r` | reward | 獎勵 | `vehicle.calculate_reward()` | 動態計算 | 行為評價分數 |
| `s'` | next_state | 下一狀態 | `vehicle.move()` | 動態計算 | 執行動作後的狀態 |
| `θ` | network_params | 網絡參數 | DQN模型 | 隨機初始化 | 神經網絡權重 |

---

## 🎯 **Q-Learning 參數詳解**

### 核心公式回顧

```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

### 參數來源和計算

#### 1. **學習率 (α - Alpha)**

```python
# 來源：agent.py 第8行
self.learning_rate = learning_rate  # 預設 0.2

# 意義：控制每次更新Q值的幅度
# 範圍：(0, 1]
# 高值：學習快速但可能不穩定
# 低值：學習穩定但速度慢
```

**在您的系統中設定：**

- GUI設定：模擬控制器中的"Learning Rate"輸入框
- 程式設定：`QLearningAgent(urban_grid, learning_rate=0.3)`
- 動態調整：`agent.learning_rate = 0.15`

#### 2. **折扣因子 (γ - Gamma)**

```python
# 來源：agent.py 第9行
self.discount_factor = discount_factor  # 預設 0.95

# 意義：未來獎勵相對於即時獎勵的重要性
# 範圍：[0, 1]
# 接近1：重視長期回報
# 接近0：只關心即時獎勵
```

**實際影響：**

```python
# γ = 0.95 時，10步後的獎勵權重 ≈ 0.60
# γ = 0.90 時，10步後的獎勵權重 ≈ 0.35
# γ = 0.99 時，10步後的獎勵權重 ≈ 0.90
```

#### 3. **探索率 (ε - Epsilon)**

```python
# 來源：agent.py 第10行
self.epsilon = epsilon  # 預設 0.2

# 意義：隨機探索vs利用最佳策略的平衡
# 範圍：[0, 1]
# 高值：更多探索，學習更多可能性
# 低值：更多利用，使用已學到的最佳策略
```

**ε-greedy 策略實現：**

```python
# 來源：agent.py choose_action() 方法
if random.random() < self.epsilon:
    # 探索：隨機選擇動作
    return random.choice(valid_actions)
else:
    # 利用：選擇Q值最高的動作
    return best_action
```

#### 4. **狀態 (s - State)**

```python
# 來源：vehicle.py move() 方法第84行
congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
state = self.agent.get_state_key(self.position, congestion_level)

# 狀態組成：
# - 車輛位置 (x, y)
# - 周圍擁塞程度（3x3窗口平均值）
# - 目標位置信息（隱含在agent中）
```

**狀態表示範例：**

```python
# 實際狀態Key格式
state = f"{position[0]}_{position[1]}_{congestion_level:.2f}"
# 例如：'10_15_0.25' 表示位置(10,15)，擁塞度0.25
```

#### 5. **動作 (a - Action)**

```python
# 來源：agent.py 第12行
self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left

# 動作編碼：
# 0: 向上 (0, 1)
# 1: 向右 (1, 0)  
# 2: 向下 (0, -1)
# 3: 向左 (-1, 0)
```

**動作選擇過程：**

```python
# 來源：vehicle.py move() 方法第87行
action_idx = self.agent.choose_action(state, self.position)
dx, dy = self.agent.actions[action_idx]
new_position = (self.position[0] + dx, self.position[1] + dy)
```

#### 6. **獎勵 (r - Reward)**

```python
# 來源：vehicle.py move() 方法第91行
reward = self.calculate_reward(new_position, dx, dy)

# 獎勵計算來源：reward_config.py
# 包含多種獎勵類型：
```

**獎勵組成詳解：**

| 獎勵類型 | 來源參數 | 預設值 | 觸發條件 |
|---------|----------|--------|----------|
| 步數懲罰 | `step_penalty` | -1 | 每次移動 |
| 到達獎勵 | `destination_reached_reward` | 100 | 到達目標 |
| A*跟隨獎勵 | `astar_follow_reward` | 10 | 跟隨最優路徑 |
| 距離改善獎勵 | `closer_to_destination_reward` | 3 | 靠近目標 |
| 擁塞懲罰 | `congestion_penalty_multiplier` | 5 | 進入擁塞區域 |

#### 7. **下一狀態 (s' - Next State)**

```python
# 在Q值更新時計算
# 來源：vehicle.py move() 方法末尾
new_congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
new_state = self.agent.get_state_key(self.position, new_congestion_level)

# 用於Q表更新：
self.agent.update_q_table(state, action_idx, reward, new_state)
```

---

## 🎯 **SARSA 額外參數**

### 核心差異

```
SARSA: Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]
Q-Learning: Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

#### **下一動作 (a' - Next Action)**

```python
# SARSA需要實際選擇的下一動作，而非最優動作
# 實現建議：
def sarsa_update(self, state, action, reward, next_state):
    # 在下一狀態實際選擇動作（使用相同的ε-greedy策略）
    next_action = self.choose_action(next_state, next_position)
    
    # 使用實際選擇的動作進行更新
    target = reward + self.discount_factor * self.q_table[next_state][next_action]
    self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                 self.learning_rate * target
```

---

## 🔮 **DQN 參數詳解**

### 神經網絡參數 (θ - Theta)

#### 1. **網絡結構參數**

```python
# 輸入層大小：狀態特徵數量
state_size = position_features + congestion_features + destination_features
# 例如：2(位置) + 9(3x3擁塞) + 2(目標) = 13

# 隱藏層：
hidden_layer_1 = 64  # 第一隱藏層神經元數
hidden_layer_2 = 64  # 第二隱藏層神經元數

# 輸出層：動作數量
action_size = 4  # 上下左右四個動作
```

#### 2. **學習參數**

```python
# 學習率（用於神經網絡優化）
learning_rate = 0.001  # 通常比Q-Learning更小

# 批次大小
batch_size = 32  # 每次訓練的樣本數

# 目標網絡更新頻率
target_update_freq = 100  # 每100步更新一次目標網絡
```

#### 3. **經驗回放參數**

```python
# 經驗緩衝區大小
buffer_size = 10000  # 儲存的經驗數量

# 經驗樣本格式
experience = (state, action, reward, next_state, done)
# state: 當前狀態（陣列）
# action: 動作索引（0-3）
# reward: 即時獎勵（浮點數）
# next_state: 下一狀態（陣列）
# done: 是否結束（布林值）
```

---

## 📊 **參數調優指南**

### 在您的系統中調整參數

#### 1. **通過GUI調整**

```python
# 在simulation_controller.py中
# Q-learning參數輸入框：
self.learning_rate = tk.StringVar(value="0.2")
self.discount_factor = tk.StringVar(value="0.95") 
self.epsilon = tk.StringVar(value="0.2")

# 獎勵參數在"Reward Configuration"標籤中調整
```

#### 2. **通過程式碼調整**

```python
# 創建Agent時指定參數
agent = QLearningAgent(
    urban_grid=grid,
    learning_rate=0.15,      # 降低學習率提高穩定性
    discount_factor=0.99,    # 提高折扣因子重視長期回報  
    epsilon=0.1              # 降低探索率專注利用
)

# 動態調整
agent.epsilon = max(0.01, agent.epsilon * 0.995)  # 探索率衰減
```

#### 3. **獎勵參數調整**

```python
# 修改reward_config.py或使用RewardConfig
reward_config = RewardConfig()
reward_config.update_config(
    step_penalty=-0.5,              # 減少步數懲罰
    destination_reached_reward=200,  # 增加到達獎勵
    astar_follow_reward=15          # 增加路徑跟隨獎勵
)
```

### 參數調優建議

#### **學習率 (α) 調整**

```
問題：學習不穩定
解決：降低α至0.1-0.15

問題：學習太慢
解決：提高α至0.3-0.5

問題：振盪不收斂
解決：使用衰減學習率 α = α₀ × decay^episode
```

#### **探索率 (ε) 調整**

```
訓練初期：ε = 0.8-1.0 (高探索)
訓練中期：ε = 0.2-0.5 (平衡探索利用)
訓練後期：ε = 0.05-0.1 (主要利用)

實現：ε = max(0.01, ε × 0.995)
```

#### **折扣因子 (γ) 調整**

```
短距離任務：γ = 0.8-0.9
長距離任務：γ = 0.95-0.99
即時反應：γ = 0.5-0.7
```

---

## 🔧 **參數監控和調試**

### 在您的系統中添加參數監控

```python
# 在simulation_controller.py中添加參數顯示
def update_parameter_display(self):
    """顯示當前參數狀態"""
    if self.agent:
        param_info = f"LR:{self.agent.learning_rate:.3f} " \
                    f"DF:{self.agent.discount_factor:.3f} " \
                    f"EPS:{self.agent.epsilon:.3f}"
        self.update_status(param_info)

# 在vehicle.py中添加獎勵詳情記錄
def calculate_reward_detailed(self, new_position, dx, dy):
    """計算獎勵並記錄詳細信息"""
    reward_breakdown = {
        'step_penalty': self.reward_config.step_penalty,
        'astar_reward': 0,
        'distance_reward': 0,
        'congestion_penalty': 0,
        'total': 0
    }
    
    # ... 獎勵計算邏輯 ...
    
    return reward_breakdown['total'], reward_breakdown
```

這樣您就能清楚了解每個參數的來源、意義和調整方法，並且可以在實際使用中進行有效的參數調優！
