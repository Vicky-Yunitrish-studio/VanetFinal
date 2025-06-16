# 強化學習演算法公式總整理 (Reinforcement Learning Algorithms Formulas)

## 📚 三大核心演算法概覽

本文檔整理了在車輛導航系統中常用的三個主要強化學習演算法：Q-Learning、SARSA 和 Deep Q-Network (DQN)。

---

## 🧠 **Q-Learning 演算法**

### 演算法概述

Q-Learning 是一種無模型 (model-free) 的離策略 (off-policy) 時間差分學習演算法，用於學習最優動作-價值函數。

### 核心公式

#### Q值更新公式

```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
                                   a'
```

**公式解釋：**

- `Q(s,a)`: 在狀態 s 下執行動作 a 的 Q 值
- `α`: 學習率 (learning rate)，範圍 [0,1]
- `r`: 即時獎勵 (immediate reward)
- `γ`: 折扣因子 (discount factor)，範圍 [0,1]
- `s'`: 下一個狀態 (next state)
- `max Q(s',a')`: 下一狀態所有可能動作的最大 Q 值
     a'

#### 動作選擇策略 (ε-greedy)

```
π(s) = {
  argmax Q(s,a)     with probability (1-ε)
     a
  random action     with probability ε
}
```

### 在您的系統中的實現

根據 `agent.py` 中的實現：

```python
def update_q_table(self, state, action, reward, next_state):
    """Q-Learning 更新規則"""
    best_next_action = np.argmax(self.q_table[next_state])
    self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                 self.learning_rate * (reward + self.discount_factor * 
                                                     self.q_table[next_state][best_next_action])
```

### 特點

- ✅ **離策略學習**：可以從任何策略生成的數據中學習
- ✅ **收斂保證**：在滿足一定條件下保證收斂到最優解
- ✅ **簡單實現**：使用表格形式存儲 Q 值
- ⚠️ **維度限制**：狀態空間過大時表格會過於龐大

---

## 🎯 **SARSA 演算法 (State-Action-Reward-State-Action)**

### 演算法概述

SARSA 是一種在策略 (on-policy) 時間差分學習演算法，學習當前遵循策略的動作-價值函數。

### 核心公式

#### Q值更新公式

```
Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]
```

**公式解釋：**

- 與 Q-Learning 的主要差別：使用實際執行的動作 `a'` 而非最優動作
- `a'`: 在下一狀態 s' 實際選擇的動作（而非最優動作）

#### 完整演算法流程

```
1. 初始化 Q(s,a) 任意值
2. 選擇初始狀態 s，使用策略選擇動作 a
3. 重複以下步驟：
   - 執行動作 a，觀察獎勵 r 和新狀態 s'
   - 在 s' 使用策略選擇動作 a'
   - 更新 Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]
   - s ← s', a ← a'
```

### 與 Q-Learning 的比較

| 特性 | Q-Learning | SARSA |
|------|------------|-------|
| 策略類型 | 離策略 (Off-policy) | 在策略 (On-policy) |
| 更新目標 | max Q(s',a') | Q(s',a') |
| 學習內容 | 最優策略 | 當前策略 |
| 收斂性 | 收斂到最優解 | 收斂到當前策略的解 |
| 探索風險 | 較積極 | 較保守 |

### 適用場景

- 🚗 **安全關鍵應用**：車輛導航中需要保守策略
- 🎮 **在線學習**：需要邊學習邊執行的環境
- 🛡️ **風險敏感**：不能承受探索過程中的高風險

---

## 🔮 **Deep Q-Network (DQN) 演算法**

### 演算法概述

DQN 結合深度神經網絡和 Q-Learning，能夠處理高維狀態空間，是深度強化學習的突破性進展。

### 核心公式

#### 損失函數 (Loss Function)

```
L(θ) = E[(y - Q(s,a;θ))²]
```

其中目標值：

```
y = r + γ max Q(s',a';θ⁻)
              a'
```

**公式解釋：**

- `θ`: 神經網絡參數
- `θ⁻`: 目標網絡參數（定期從主網絡複製）
- `Q(s,a;θ)`: 主網絡的 Q 值預測
- `Q(s',a';θ⁻)`: 目標網絡的 Q 值預測

#### 梯度更新

```
θ ← θ - α ∇θ L(θ)
```

### 關鍵技術

#### 1. 經驗回放 (Experience Replay)

```
Buffer: (s, a, r, s') 的轉換樣本
隨機採樣批次進行訓練，打破數據相關性
```

#### 2. 目標網絡 (Target Network)

```
θ⁻ ← θ    (每 C 步更新一次)
```

#### 3. 網絡結構（車輛導航系統適用）

```
輸入層：狀態表示 (位置、擁塞度、目標等)
    ↓
隱藏層：全連接或卷積層
    ↓
輸出層：4個動作的 Q 值 (上、下、左、右)
```

### DQN 演算法偽代碼

```python
def dqn_algorithm():
    # 初始化經驗回放緩衝區和神經網絡
    replay_buffer = ReplayBuffer()
    main_network = QNetwork()
    target_network = copy(main_network)
    
    for episode in range(num_episodes):
        state = env.reset()
        for step in range(max_steps):
            # ε-greedy 動作選擇
            action = select_action(state, main_network, epsilon)
            
            # 執行動作
            next_state, reward, done = env.step(action)
            
            # 存儲經驗
            replay_buffer.store(state, action, reward, next_state, done)
            
            # 從緩衝區採樣並訓練
            if len(replay_buffer) > batch_size:
                batch = replay_buffer.sample(batch_size)
                loss = compute_loss(batch, main_network, target_network)
                update_network(main_network, loss)
            
            # 定期更新目標網絡
            if step % target_update_freq == 0:
                target_network = copy(main_network)
                
            state = next_state
```

### 在車輛導航中的應用

#### 狀態空間設計

```python
state = [
    vehicle_x,           # 車輛 x 座標
    vehicle_y,           # 車輛 y 座標
    destination_x,       # 目標 x 座標
    destination_y,       # 目標 y 座標
    congestion_map,      # 周圍擁塞度矩陣
    traffic_lights,      # 交通燈狀態
    distance_to_goal     # 到目標的距離
]
```

#### 動作空間

```python
actions = [
    0: 向上移動
    1: 向右移動
    2: 向下移動
    3: 向左移動
]
```

#### 獎勵函數（可結合您現有的設計）

```python
def calculate_reward(state, action, next_state):
    reward = 0
    
    # 基本步數懲罰
    reward += step_penalty
    
    # 到達目標獎勵
    if reached_destination(next_state):
        reward += destination_reward
    
    # 距離改善獎勵
    if distance_improved(state, next_state):
        reward += distance_reward
    
    # 擁塞懲罰
    if in_congested_area(next_state):
        reward += congestion_penalty
    
    return reward
```

---

## 📊 **三種演算法比較分析**

### 性能對比表

| 評估指標 | Q-Learning | SARSA | DQN |
|---------|------------|-------|-----|
| **狀態空間適用性** | 小型離散 | 小型離散 | 大型連續/離散 |
| **學習速度** | 中等 | 中等 | 較慢（需要大量數據） |
| **內存需求** | 低 | 低 | 高 |
| **實現複雜度** | 簡單 | 簡單 | 複雜 |
| **收斂穩定性** | 好 | 好 | 需要技巧 |
| **泛化能力** | 差 | 差 | 強 |

### 適用場景建議

#### 🎯 使用 Q-Learning 當

- 狀態空間較小（如20x20網格）
- 需要快速原型開發
- 要求演算法透明度高
- 計算資源有限

#### 🛡️ 使用 SARSA 當

- 安全性要求高（避免危險探索）
- 在線學習環境
- 需要保守的學習策略
- 環境中存在懲罰性陷阱

#### 🔮 使用 DQN 當

- 狀態空間很大或連續
- 有充足的計算資源
- 需要處理原始感知輸入（圖像等）
- 要求高泛化能力

---

## 💡 **在您的車輛導航系統中的應用建議**

### 當前系統分析

您的系統目前實現了 **Q-Learning** 演算法，具有以下特點：

- 20x20 網格環境 ✅ 適合 Q-Learning
- 離散狀態和動作空間 ✅
- 表格型 Q 值存儲 ✅
- ε-greedy 探索策略 ✅

### 擴展建議

#### 1. 添加 SARSA 支持

```python
class SARSAAgent(QLearningAgent):
    def update_q_table(self, state, action, reward, next_state, next_action):
        """SARSA 更新規則 - 使用實際選擇的下一動作"""
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                     self.learning_rate * (reward + self.discount_factor * 
                                                         self.q_table[next_state][next_action])
```

#### 2. 添加 DQN 支持（進階）

```python
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        
    def _build_model(self):
        # 構建神經網絡
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model
```

### 選擇建議

基於您現有的系統規模和複雜度，建議：

1. **保持 Q-Learning 作為主要演算法** - 適合當前 20x20 網格
2. **考慮添加 SARSA** - 提供更安全的學習選項
3. **DQN 作為未來擴展** - 當需要處理更大狀態空間時

這樣您就有了完整的強化學習演算法工具箱，可以根據不同需求選擇最適合的方法！

---

## 🔧 **實際實現參考代碼**

### Q-Learning 核心循環

```python
def q_learning_episode(agent, env):
    state = env.reset()
    total_reward = 0
    
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        
        # Q-Learning 更新（使用最優動作）
        agent.update_q_table(state, action, reward, next_state)
        
        state = next_state
        total_reward += reward
    
    return total_reward
```

### SARSA 核心循環

```python
def sarsa_episode(agent, env):
    state = env.reset()
    action = agent.choose_action(state)
    total_reward = 0
    
    while not done:
        next_state, reward, done = env.step(action)
        next_action = agent.choose_action(next_state) if not done else None
        
        # SARSA 更新（使用實際選擇的動作）
        agent.update_q_table(state, action, reward, next_state, next_action)
        
        state = next_state
        action = next_action
        total_reward += reward
    
    return total_reward
```

這份文檔提供了三種演算法的完整公式和實現指導，可以幫助您理解和擴展現有的車輛導航系統！
