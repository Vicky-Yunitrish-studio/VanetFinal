# 獎勵配置系統 (Reward Configuration System)

## 概述

本項目現在包含一個獨立的獎勵配置系統，讓您可以輕鬆地調整車輛行為，而無需修改核心的 `Vehicle` 類別代碼。

## 主要文件

- `reward_config.py`: 包含 `RewardConfig` 類別的主要配置系統
- `vehicle.py`: 已修改為使用獎勵配置系統
- `reward_config_examples.py`: 使用範例和最佳實踐

## RewardConfig 類別

### 主要功能

1. **集中管理所有獎勵參數**
2. **運行時動態修改配置**
3. **預設配置和自定義配置**
4. **配置驗證和錯誤處理**

### 可配置的獎勵參數

#### 基本移動獎勵

- `step_penalty`: 每步的成本 (預設: -1)

#### A* 路徑跟隨獎勵

- `astar_follow_reward`: 完全跟隨 A* 路徑的獎勵 (預設: 10)
- `astar_on_path_reward`: 在最佳路徑上的獎勵 (預設: 5)

#### 距離相關獎勵

- `closer_to_destination_reward`: 靠近目的地的獎勵 (預設: 3)

#### 交通壅塞懲罰

- `high_congestion_threshold`: 高壅塞閾值 (預設: 0.5)
- `congestion_penalty_multiplier`: 壅塞懲罰倍數 (預設: 5)

#### 後退移動懲罰

- `immediate_backtrack_penalty`: 立即後退的懲罰 (預設: -30)
- `oscillation_penalty`: 振盪行為的懲罰 (預設: -40)
- `long_oscillation_penalty`: 長時間振盪的懲罰 (預設: -50)

#### 交通燈懲罰

- `red_light_wait_penalty`: 紅燈等待的懲罰 (預設: -5)

#### 目的地獎勵

- `destination_reached_reward`: 到達目的地的獎勵 (預設: 100)

#### 迴圈檢測和懲罰

- `loop_threshold_base`: 迴圈檢測的基礎閾值 (預設: 3)
- `loop_threshold_max`: 迴圈檢測的最大閾值 (預設: 5)
- `loop_penalty_base`: 每次迴圈的基礎懲罰 (預設: -20)
- `loop_penalty_max`: 最大迴圈懲罰 (預設: -100)

#### 接近獎勵參數

- `proximity_base_multiplier`: 基礎接近獎勵倍數 (預設: 5)
- `proximity_max_multiplier`: 額外接近獎勵倍數 (預設: 15)

#### A* 路徑距離獎勵參數

- `path_distance_base_reward`: 接近最佳路徑的基礎獎勵 (預設: 10)
- `path_distance_penalty_multiplier`: 遠離路徑的懲罰倍數 (預設: 2)

## 使用方法

### 1. 使用預設配置

```python
from vehicle import Vehicle
from reward_config import RewardConfig

# 使用預設配置
vehicle = Vehicle(urban_grid, agent)
```

### 2. 使用自定義配置

```python
from reward_config import RewardConfig

# 創建自定義配置
custom_config = RewardConfig()
custom_config.update_config(
    step_penalty=-2,
    destination_reached_reward=200,
    congestion_penalty_multiplier=10
)

# 使用自定義配置創建車輛
vehicle = Vehicle(urban_grid, agent, reward_config=custom_config)
```

### 3. 運行時修改配置

```python
# 運行時修改配置
vehicle.reward_config.update_config(
    step_penalty=-5,
    astar_follow_reward=15
)

# 重置為預設值
vehicle.reward_config.reset_to_defaults()
```

### 4. 獲取配置信息

```python
# 獲取所有配置
all_config = vehicle.reward_config.get_all_config()

# 獲取特定配置群組
astar_rewards = vehicle.reward_config.get_astar_rewards()
congestion_config = vehicle.reward_config.get_congestion_config()
```

## 預設行為配置範例

### 積極型配置 (快速、直接)

```python
aggressive_config = RewardConfig()
aggressive_config.update_config(
    step_penalty=-3,
    astar_follow_reward=20,
    destination_reached_reward=300,
    immediate_backtrack_penalty=-100,
    congestion_penalty_multiplier=15
)
```

### 謹慎型配置 (探索性強)

```python
cautious_config = RewardConfig()
cautious_config.update_config(
    step_penalty=-0.5,
    astar_follow_reward=5,
    destination_reached_reward=50,
    immediate_backtrack_penalty=-10,
    congestion_penalty_multiplier=2
)
```

## 最佳實踐

1. **實驗不同配置**: 使用不同的配置來測試車輛行為
2. **動態調整**: 根據環境條件動態調整獎勵參數
3. **保存配置**: 將成功的配置保存為 JSON 或其他格式
4. **文檔記錄**: 記錄不同配置的效果和使用場景

## 配置建議

### 提高路徑效率

- 增加 `astar_follow_reward`
- 增加 `step_penalty` (更負的值)
- 增加 `immediate_backtrack_penalty` (更負的值)

### 提高探索性

- 減少 `step_penalty` (較少負的值)
- 減少 `astar_follow_reward`
- 減少後退懲罰

### 避免交通壅塞

- 增加 `congestion_penalty_multiplier`
- 調低 `high_congestion_threshold`

### 加快收斂速度

- 增加 `destination_reached_reward`
- 增加 `closer_to_destination_reward`

## 故障排除

### 常見問題

1. **車輛移動太慢**: 減少 `step_penalty` 的絕對值
2. **車輛不跟隨最佳路徑**: 增加 `astar_follow_reward`
3. **車輛在迴圈中困住**: 檢查 `loop_threshold_base` 和 `loop_penalty_base`
4. **車輛避開壅塞區域不夠**: 增加 `congestion_penalty_multiplier`

### 調試技巧

```python
# 打印當前配置
print(vehicle.reward_config.get_all_config())

# 監控獎勵值變化
reward = vehicle.move()
print(f"Step reward: {reward}")
print(f"Total reward: {vehicle.total_reward}")
```

## 擴展性

該系統設計為易於擴展：

1. **添加新參數**: 在 `RewardConfig` 中添加新屬性
2. **添加新的獎勵函數**: 在 `vehicle.py` 中實現並使用配置參數
3. **創建配置模板**: 為特定場景創建預定義的配置類別

這個獎勵配置系統讓您可以輕鬆地實驗不同的車輛行為，而無需深入修改核心代碼，從而提高了代碼的可維護性和實驗的靈活性。
