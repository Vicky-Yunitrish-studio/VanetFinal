### 🔢 **指數距離演算法的數學公式**

#### D. **指數距離獎勵機制**

**程式碼實現**：

```python
def calculate_reward_exponential_distance(self, new_position, dx, dy):
    """Calculate reward using the exponential distance algorithm
    Formula: r = base_reward + multiplier × exp(-(|xi-xd|/x_scale + |yi-yd|/y_scale))
    """
    import math
    
    exp_config = self.reward_config.get_exponential_distance_config()
    
    # Calculate distance components
    x_dist = abs(new_position[0] - self.destination[0])
    y_dist = abs(new_position[1] - self.destination[1])
    
    # Calculate normalized distance
    normalized_dist = x_dist / exp_config['x_scale'] + y_dist / exp_config['y_scale']
    
    # Calculate exponential reward
    exp_reward = exp_config['multiplier'] * math.exp(-normalized_dist)
    reward = exp_config['base_reward'] + exp_reward
    
    return reward
```

**數學公式版本**：

##### 📊 指數距離獎勵函數

**歸一化距離**：

$
d_{norm}(s, g) = |x_s - x_g|/σ_x + |y_s - y_g|/σ_y
$

**指數獎勵函數**：

$
R_{exponential}(s) = β_{exp} + λ_{exp} × {exp}(-d_{norm}(s, g))
$

**完整指數距離獎勵**：

$
R_{\text{exp-total}} = β_{exp} + λ_{exp} × exp(-[|x_s - x_g|/σ_x + |y_s - y_g|/σ_y])
$

**參數說明**：

- $β_{exp} = 指數獎勵基礎值$
- $λ_{exp}= 指數獎勵乘數$
- $σ_x= X方向縮放因子$
- $σ_y= Y方向縮放因子$
- $(x_s, y_s)= 當前位置$
- $(x_g, y_g)= 目標位置$

##### 📈 指數函數特性分析

**獎勵衰減特性**：

$
lim_{d_{norm} → 0}*R_{exponential} = β_{exp} + λ_{exp}     (在目標位置) \\
lim_{d_{norm} → ∞}*R_{exponential} = β_{exp}             (距離目標極遠)
$

**梯度特性**：

$
∂×R_{exponential}/∂x = -λ_{exp} × exp(-d_{norm}) × sign(x_s - x_g)/σ_x \\
∂×R_{exponential}/∂y = -λ_{exp} × exp(-d_{norm}) × sign(y_s - y_g)/σ_y
$

**距離敏感度**：

- 在目標附近：獎勵變化劇烈，梯度大
- 距離目標較遠：獎勵變化平緩，梯度小
- 具有**非線性衰減**特性，比線性距離更精確