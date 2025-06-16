# DQN & SARSA 演算法公式總整理

## 📋 快速對比表

| 演算法 | 更新公式 | 特點 | 適用場景 |
|--------|----------|------|----------|
| **Q-Learning** | `Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]` | 離策略、最優解 | 您目前的系統 ✅ |
| **SARSA** | `Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]` | 在策略、保守學習 | 安全導航 |
| **DQN** | `L(θ) = E[(r + γ max Q(s',a';θ⁻) - Q(s,a;θ))²]` | 深度網絡、大狀態空間 | 複雜環境 |

---

## 🧠 Q-Learning（您當前使用的）

### 核心公式

```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
                            a'
```

### 關鍵概念

- **離策略 (Off-policy)**：學習最優策略，不管當前執行什麼策略
- **貝爾曼方程**：使用下一狀態的最大Q值更新
- **收斂性**：保證收斂到最優Q*函數

### 您系統中的實現

```python
# 來自 agent.py
def update_q_table(self, state, action, reward, next_state):
    best_next_action = np.argmax(self.q_table[next_state])
    self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                 self.learning_rate * (reward + self.discount_factor * 
                                                     self.q_table[next_state][best_next_action])
```

---

## 🎯 SARSA 演算法

### 核心公式

```
Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]
```

### 與Q-Learning的差異

| Q-Learning | SARSA |
|------------|-------|
| `max Q(s',a')` | `Q(s',a')` |
| 使用最優動作 | 使用實際選擇的動作 |
| 離策略學習 | 在策略學習 |

### 完整演算法流程

```
1. 初始化 Q(s,a)
2. 觀察狀態 s，選擇動作 a
3. 執行動作 a，得到 r, s'
4. 在 s' 選擇動作 a'
5. 更新 Q(s,a) ← Q(s,a) + α[r + γ Q(s',a') - Q(s,a)]
6. s ← s', a ← a'
7. 重複步驟 3-6
```

### 適合車輛導航的原因

- **安全學習**：不會學習危險的探索動作
- **保守策略**：避免在學習過程中冒險
- **實際可行**：學習當前策略下的最佳表現

### 實現範例

```python
class SARSAAgent(QLearningAgent):
    def update_q_table(self, state, action, reward, next_state, next_action):
        """SARSA更新：使用實際選擇的next_action"""
        if next_action is not None:
            target = reward + self.discount_factor * self.q_table[next_state][next_action]
        else:
            target = reward  # 終端狀態
            
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                     self.learning_rate * target
```

---

## 🔮 Deep Q-Network (DQN)

### 核心概念

DQN = Q-Learning + 深度神經網絡

### 損失函數

```
L(θ) = E[(y - Q(s,a;θ))²]

其中: y = r + γ max Q(s',a';θ⁻)
                a'
```

### 關鍵技術

#### 1. 神經網絡結構

```
輸入層: 狀態特徵
隱藏層: 全連接層 (64-128 神經元)
輸出層: 4個動作的Q值 [上,右,下,左]
```

#### 2. 經驗回放 (Experience Replay)

```python
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
```

#### 3. 目標網絡 (Target Network)

```python
# 每N步更新目標網絡
if step % target_update_freq == 0:
    target_network.load_state_dict(main_network.state_dict())
```

### 車輛導航中的應用

#### 狀態表示

```python
def get_state_representation(vehicle_pos, destination, congestion_map):
    state = [
        vehicle_pos[0] / grid_size,      # 正規化x座標
        vehicle_pos[1] / grid_size,      # 正規化y座標
        destination[0] / grid_size,      # 正規化目標x
        destination[1] / grid_size,      # 正規化目標y
        *congestion_map.flatten()        # 擁塞地圖
    ]
    return np.array(state)
```

#### 網絡架構範例

```python
class DQNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
```

---

## ⚖️ 三種演算法實用比較

### 在您的車輛導航系統中的選擇建議

#### 🎯 Q-Learning（當前）

**何時使用：**

- ✅ 20x20 網格環境（小狀態空間）
- ✅ 快速原型和測試
- ✅ 需要透明的決策過程
- ✅ 計算資源有限

**優勢：**

- 實現簡單，易於調試
- 收斂有理論保證
- 可直接查看Q表了解學習結果

#### 🛡️ SARSA（建議擴展）

**何時使用：**

- 🚗 安全關鍵的車輛導航
- 🔒 不能承受探索風險
- 📈 在線學習環境
- 🎯 需要保守策略

**實現建議：**

```python
# 在您的系統中添加SARSA選項
def create_agent(algorithm_type="qlearning"):
    if algorithm_type == "sarsa":
        return SARSAAgent(urban_grid)
    else:
        return QLearningAgent(urban_grid)
```

#### 🔮 DQN（未來擴展）

**何時使用：**

- 🗺️ 更大的地圖（100x100+）
- 🖼️ 需要處理圖像輸入
- 🧠 複雜的狀態特徵
- 💪 有充足計算資源

**準備工作：**

- 需要GPU支援
- 需要大量訓練數據
- 需要更複雜的超參數調優

---

## 🔧 實際整合建議

### 1. 擴展您的agent.py

```python
class QLearningAgent:
    def __init__(self, urban_grid, algorithm="qlearning", ...):
        self.algorithm = algorithm
        # ... 其他初始化
    
    def update_q_table(self, state, action, reward, next_state, next_action=None):
        if self.algorithm == "sarsa" and next_action is not None:
            # SARSA更新
            target = reward + self.discount_factor * self.q_table[next_state][next_action]
        else:
            # Q-Learning更新
            target = reward + self.discount_factor * np.max(self.q_table[next_state])
        
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                     self.learning_rate * target
```

### 2. 在GUI中添加演算法選擇

```python
# 在simulation_controller.py中
algorithms = ["Q-Learning", "SARSA", "DQN"]
self.algorithm_combo = ttk.Combobox(parent, values=algorithms)
```

### 3. 性能比較框架

```python
def compare_algorithms():
    results = {}
    for algo in ["qlearning", "sarsa"]:
        agent = create_agent(algo)
        metrics = run_evaluation(agent, episodes=100)
        results[algo] = metrics
    return results
```

這樣您就有了完整的演算法公式參考和實際整合建議！每個演算法都有其適用的場景，可以根據具體需求選擇最合適的方法。
