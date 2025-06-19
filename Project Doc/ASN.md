# A*演算法+鄰近演算法

## 本系統

### 1. 鄰近性概念在系統中的體現

#### A. **動作選擇的鄰近性**

```python
def get_valid_actions(self, position):
    """Get valid actions at current position (avoiding grid boundaries and obstacles)"""
    valid_actions = []
    for i, (dx, dy) in enumerate(self.actions):  # [(0,1), (1,0), (0,-1), (-1,0)]
        new_x = position[0] + dx
        new_y = position[1] + dy
        # 只考慮相鄰的四個位置 - 這就是鄰近性概念！
```

**鄰近性體現**：

- 您的系統只考慮當前位置的**直接相鄰位置**（上下左右四個方向）
- 這正是鄰近演算法的核心：**局部搜索**，只考慮附近的選項

#### B. **基於距離的獎勵機制**

**程式碼實現**：

```python
def calculate_reward_proximity_based(self, new_position, dx, dy):
    # --- Proximity reward: the closer to the destination, the higher the reward ---
    old_dist = manhattan_dist(self.position, self.destination)
    new_dist = manhattan_dist(new_position, self.destination)
    proximity_reward = old_dist - new_dist  # 越近獎勵越高
    
    # 距離越近，獎勵倍數越高
    progress = 1 - (new_dist / max_possible_dist)
    proximity_multiplier = base_multiplier + (max_multiplier * progress)
    reward += proximity_reward * proximity_multiplier
```

**數學公式版本**：

##### 📐 基礎鄰近獎勵函數

**曼哈頓距離**：

$d(p₁, p₂) = |x₁ - x₂| + |y₁ - y₂|$

**鄰近性獎勵**：

$R_{proximity} = d(s_t, g) - d(s_{t+1}, g)$

其中：

- $s_t = 當前位置 (current position)$
- $s_{t+1} = 下一個位置 (next position)$  
- $g = 目標位置 (goal position)$
- $d(x,y) = 曼哈頓距離函數$

##### 📊 動態倍數獎勵函數

**進度計算**：

$progress = 1 - d(s_{t+1}, g) / d_{max}$

**鄰近倍數**：

$M_{proximity} = α_{base} + α_{max} × progress$

**最終鄰近獎勵**：

$R_{proximity  final} = R_{proximity} × M_{proximity}$

##### 🎯 完整獎勵函數

**總獎勵函數**：

$R_{total} = R_{step} + R_{proximity final} + R_{astar} + R_{congestion} + R_{loop}$

展開為：

$R_{total} = β_{step} + [d(s_t,g) - d(s_{t+1},g)] × [α_{base} + α_{max} × (1 - d(s_{t+1},g)/d_{max})] + R_{astar} + R_{congestion} + R_{loop}$

**參數說明**：

- $β_{step} = 基礎步數懲罰 (通常為負值)$
- $α_{base} = 基礎鄰近倍數$
- $α_{max} = 最大鄰近倍數$
- $d_{max} = 網格最大可能距離 = 2 × grid size$
- $R_{asta} = \text{A*路徑跟隨獎勵}$
- $R_{congestion} = 擁塞懲罰$
- $R_{loop} = 迴路懲罰$

##### 🔢 典型參數值

- $β_{step} = -1          \quad\text {每步基礎懲罰}$
- $α_{base} = 1.0         \quad\text { 基礎倍數}$
- $α_{max} = 3.0          \quad\text { 最大倍數}$
- $d_{max} = 40           \quad\text { 對於20×20網格}$

##### 📈 獎勵函數性質分析

**距離獎勵特性**：

- 當 $d(s_{t+1}, g) < d(s_t, g)$ 時，$R_{proximity} > 0$ (靠近目標)
- 當 $d(s_{t+1}, g) > d(s_t, g)$ 時，$R_{proximity} < 0$ (遠離目標)
- 當 $d(s_{t+1}, g) = d(s_t, g)$ 時，$R_{proximity} = 0$ (距離不變)

**倍數效應**：

- 距離目標越近，倍數越大，獎勵放大效果越強
- 在目標附近：$M_{proximity} ≈ α_{base} + α_{max} ≈ 4.0$
- 在起始位置：$M_{proximity} ≈ α_{base} ≈ 1.0$

#### C. **狀態表示中的方向感知**

```python
def get_state_key(self, position, congestion_level):
    # Get direction to destination (discretized to 8 directions)
    if hasattr(self, 'current_destination'):
        dx = self.current_destination[0] - position[0]
        dy = self.current_destination[1] - position[1]
        angle = np.arctan2(dy, dx)
        direction = int(((angle + np.pi) * 4 / np.pi + 0.5) % 8)
```

**鄰近性體現**：

- 狀態表示包含了**朝向目標的方向**
- 這幫助智能體優先選擇朝向目標的相鄰位置

### 2. 我們的系統 vs 純鄰近演算法

| 特性 | 純鄰近演算法 | A*+Q-learning+鄰近演算法 |
|------|-------------|------------------|
| **搜索範圍** | 只考慮相鄰位置 | ✅ 也只考慮相鄰位置 |
| **距離偏好** | 選擇距離目標最近的相鄰位置 | ✅ 獎勵靠近目標的移動 |
| **決策機制** | 貪婪選擇 | 🔄 結合學習的貪婪選擇 |
| **全局規劃** | ❌ 無 | ✅ 有（A*指導） |
| **學習能力** | ❌ 無 | ✅ 有（Q-learning） |

### 3. 創新之處

#### A. **多層次的鄰近性**

**程式碼實現**：

```python
# 1. 即時鄰近性（傳統鄰近演算法）
proximity_reward = old_dist - new_dist

# 2. 路徑鄰近性（A*指導的鄰近）
if new_position == next_optimal:
    reward += astar_rewards['follow']  # 獎勵跟隨A*路徑

# 3. 歷史鄰近性（避免重複訪問）
if new_position in self.position_history:
    # 懲罰重複訪問相同位置
```

**數學公式版本**：

##### 🎯 A*路徑跟隨獎勵

**路徑距離函數**：

$d_{path}(s, P) = \text{min }{d(s, p_i) | p_i ∈ P}$

其中 $P = \{p₁, p₂, ..., p_n\}$ 是A*最優路徑

**路徑跟隨獎勵**：

$R_{a star} = \begin{cases}
    γ_{\text{ follow }},     \text { if } s_{t+1} = p_{next} \\
    γ_{\text{ on path }},    \text { if } s_{t+1} ∈ P \\
    0,            \text { otherwise }
\end{cases}$

**路徑進度獎勵**：

$R_{\text{ path progress}} = γ_{\text{base}} × max(0, 1 - d_{path}(s_{t+1}, P)/σ_{path}) × (i/|P|)$

參數說明：

- $γ_{follow} = 直接跟隨A*路徑的高獎勵$
- $γ_{\text{on path}} = 在A*路徑上的中等獎勵$
- $γ_{base} = 路徑距離基礎獎勵$
- $σ_{path} = 路徑距離懲罰係數$
- $i= 在路徑中的位置索引$
- $|P|= 路徑總長度$

##### 🔄 迴路懲罰函數

**位置訪問頻率**：

$freq(s) = |\{t | s_t = s, t ≤ \text{current time}\}|$

**迴路懲罰**：

$
R_{loop} = \begin{cases}
    λ_{loop} × (freq(s_{t+1}) - θ_{loop}),  \quad \text{if  } freq(s_{t+1}) > θ_loop \\
    0,\quad \text{otherwise}
\end{cases}
$

參數說明：

- $λ_{loop} = 迴路懲罰係數 (負值)$
- $θ_{loop} = 迴路檢測閾值$

##### 🚦 擁塞懲罰函數

**擁塞懲罰**：

$
R_{congestion} = \begin{cases}
    μ_{congestion} × C(s_{t+1}), \quad \text{if  }C(s_{t+1}) > θ_{congestion} \\
    0, \quad \text{otherwise}
\end{cases}
$

其中：

- $C(s) = 位置s的擁塞程度 ∈ [0,1]$
- $μ_{congestion} = 擁塞懲罰係數 (負值)$
- $θ_{congestion} = 擁塞懲罰閾值$

##### 🎲 完整多層次獎勵函數

**綜合獎勵函數**：

$R_{total}(s_t, a_t, s_{t+1}) = R_{base} + R_{proximity} + R_{astar} + R_{congestion} + R_{loop}$

展開為：

$
$R_{total} = β_{step} + [d(s_t,g) - d(s_{t+1},g)] × M_{proximity} + R_{astar}(s_{t+1}, P) + R_{congestion}(s_{t+1}) + R_{loop}(s_{t+1})$

##### 📊 典型參數配置

- $β_{step} = -1.0           \qquad\text{基礎步數懲罰}$
- $α_{base} = 1.0            \qquad\text{鄰近基礎倍數}$
- $α_{max} = 3.0             \qquad\text{鄰近最大倍數}$
- $γ_{follow} = 3.0          \qquad\text{A*跟隨獎勵}$
- $γ_{on_path} = 1.0         \qquad\text{A*路徑獎勵}$
- $γ_{base} = 2.0            \qquad\text{路徑距離基礎獎勵}$
- $σ_{path} = 2.0            \qquad\text{路徑距離係數}$
- $λ_{loop} = -20.0          \qquad\text{迴路懲罰係數}$
- $θ_{loop} = 3              \qquad\text{迴路閾值}$
- $μ_{congestion} = -10.0    \qquad\text{擁塞懲罰係數}$
- $θ_{congestion} = 0.5      \qquad\text{擁塞閾值}$

##### 🎯 獎勵函數最佳化特性

**梯度特性**：

- 距離梯度：引導智能體朝目標移動
- 路徑梯度：引導智能體跟隨最優路徑
- 懲罰梯度：避免不良行為（迴路、擁塞）

**收斂性**：

- 在無擁塞、無障礙的理想環境中，該獎勵函數保證收斂到最優解
- 多層次設計確保在複雜環境中也能找到近似最優解

#### B. **智能化的鄰近選擇**

**程式碼實現**：

```python
def choose_action(self, state, position):
    if random.random() < self.epsilon:
        return random.choice(valid_actions)  # 探索
    else:
        # 在相鄰位置中選擇Q值最高的（學習過的最優鄰近選擇）
        q_values = [self.q_table[state][a] for a in valid_actions]
        max_q = max(q_values)
```

**數學公式版本**：

##### 🧠 Q-learning動作選擇

**ε-貪婪策略**：

$
π(a|s) = \begin{cases}
    1 - ε + ε/|A(s)|,  if a = argmax*Q(s,a') \\
    ε/|A(s)|, \quad\text{otherwise} \\
\end{cases}
$

**動作選擇函數**：

$
a_t = \begin{cases}
    random(A(s_t)), \quad\text{with probability ε} \\
    argmax_{a∈A(s_t)} Q(s_t,a), \quad\text{with probability 1 - ε} \\
\end{cases}
$

其中：

- $A(s) = 狀態s下的有效動作集合(相鄰位置)$
- $ε = 探索率$
- $Q(s,a)= 狀態-動作價值函數$

##### 🎯 Q值更新函數

**Q-learning更新規則**：

$Q(s_t, a_t) ← Q(s_t, a_t) + α[r_{t+1} + γ*max_{a'} Q(s_{t+1}, a') - Q(s_t, a_t)]$

**時間差分誤差**：

$δ_t = r_{t+1} + γ*max_{a'} Q(s_{t+1}, a') - Q(s_t, a_t)$

**簡化更新形式**：

$Q(s_t, a_t) ← (1-α)Q(s_t, a_t) + α[r_{t+1} + γ max_{a'} Q(s_{t+1}, a')]$

參數說明：

- $α = 學習率 ∈ [0,1] $
- $γ = 折扣因子 ∈ [0,1]$
- $r_{t+1} = 即時獎勵(使用前面定義的獎勵函數)$

##### 🗺️ 狀態表示函數

**狀態編碼**：

$s = (x, y, c_{discrete}, θ_{direction})$

**擁塞離散化**：

$c_{discrete} = ⌊C(x,y) × 5⌋ ∈ {0,1,2,3,4}$

**方向離散化**：

$θ_{direction} = ⌊(arctan2(g_y - y, g_x - x) + π) × 4/π + 0.5⌋ mod\quad8$

其中$(g_x, g_y)$是目標位置。

### 4. 演算法分類

您的系統可以被分類為：

```graph
A*+Q-learning混合演算法
├── 🎯 全局規劃層：A*演算法
│   └── 提供最優路徑指導
├── 🧠 學習層：Q-learning
│   └── 從經驗中學習最佳鄰近選擇
└── 📍 執行層：增強鄰近演算法
    ├── 基礎鄰近性（距離導向）
    ├── 路徑鄰近性（A*導向）
    └── 學習鄰近性（Q值導向）
```


---

## 📐 **數學模型總結**

### 🎯 完整的A*+Q-learning混合演算法數學框架

#### 馬可夫決策過程定義

**狀態空間**：

$
S = \{(x, y, c, θ) | x,y ∈ [0, \text{grid-size}-1], c ∈ [0,4], θ ∈ [0,7]\}
$

**動作空間**：

$
A = \{North, East, South, West\} = \{(0,1), (1,0), (0,-1), (-1,0)\}
$

**轉移函數**：

$
P(s'|s,a) = \begin{cases}
    1,  \text{if }s' = (x+dx, y+dy, c', θ')\text{ and action }a = (dx,dy) \\
    0,  otherwise
\end{cases}
$

**獎勵函數**：

$
R(s,a,s') = R_{distance}(s,s') + R_{astar}(s') + R_{congestion}(s') + R_{loop}(s')
$

其中距離獎勵可選擇：

- **鄰近性算法**：$R_{distance} = [d(s,g) - d(s',g)] × M_{proximity}$
- **指數距離算法**：$R_{distance} = β_{exp} + λ_{exp} × exp(-d_{norm}(s',g))$

#### 完整獎勵函数展開

**鄰近性版本**：

$
R_{total} = -1 + [d(s,g) - d(s',g)] × [α_{base} + α_{max} × (1 - d(s',g)/d_{max})] \\
        + γ_{astar}(s', P) + μ_{congestion} × C(s') + λ_{loop} × freq(s')
$

**指數距離版本**：

$
R_{total} = β_{exp} + λ_{exp} × exp(-[|x_s' - x_g|/σ_x + |y_s' - y_g|/σ_y])
        + γ_{astar}(s', P) + μ_{congestion} × C(s') + λ_{loop} × freq(s')
$

#### Q-learning價值迭代

**狀態價值函數**：

$
V'(s) = max_a Q'(s,a)
$

**最優Q函數**：

$
Q'(s,a) = E[R(s,a,s') + γ*V'(s')]
$

**迭代更新**：

$
Q_{k+1}(s,a) = Q_k(s,a) + α[r + γ*max_{a'} Q_k(s',a') - Q_k(s,a)]
$

#### A*路徑規劃整合

**啟發式函數**：

$
h(s,g) = |x_s - x_g| + |y_s - y_g| + w_{congestion} × C(s)
$

**A*評估函數**：

$
f(s) = g(s) + h(s,goal)
$

其中$g(s)$是從起點到s的實際代價。

#### 策略函數

**最優策略**：

$
π*(s) = argmax_a Q*(s,a)
$

**ε-貪婪探索策略**：

$
π_ε(s) = \begin{cases}
    π*(s),           \text{with probability } 1-ε \\
    random(A(s)),    \text{with probability } ε
\end{cases}
$

### 🎲 典型參數配置總表

| 參數 | 符號 | 數值範圍 | 建議值 | 說明 |
|------|------|----------|--------|------|
| 學習率 | α | (0,1] | 0.2 | Q值更新速度 |
| 折扣因子 | γ | [0,1] | 0.95 | 未來獎勵重要性 |
| 探索率 | ε | [0,1] | 0.2 | 隨機探索概率 |
| 步數懲罰 | β_step | (-∞,0] | -1.0 | 鼓勵短路徑 |
| 鄰近基礎倍數 | α_base | [0,∞) | 1.0 | 基礎鄰近獎勵 |
| 鄰近最大倍數 | α_max | [0,∞) | 3.0 | 接近目標時的獎勵倍數 |
| A*跟隨獎勵 | γ_follow | [0,∞) | 3.0 | 直接跟隨A*路徑 |
| A*路徑獎勵 | γ_on_path | [0,∞) | 1.0 | 在A*路徑上 |
| 迴路懲罰係數 | λ_loop | (-∞,0] | -20.0 | 避免無限迴路 |
| 擁塞懲罰係數 | μ_congestion | (-∞,0] | -10.0 | 避免擁塞區域 |

