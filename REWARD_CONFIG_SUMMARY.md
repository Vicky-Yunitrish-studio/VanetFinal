# 獎勵函數設定功能分離完成

## 完成的工作

✅ **已成功將獎勵函數設定功能分離**

### 新增的文件

1. **`reward_config.py`** - 主要的獎勵配置類別
   - 包含所有可調整的獎勵參數
   - 提供便捷的設定和獲取方法
   - 支持運行時動態修改配置

2. **`reward_config_examples.py`** - 使用範例
   - 展示如何使用不同的配置
   - 包含積極型、謹慎型等預設配置
   - 示範動態修改配置的方法

3. **`test_reward_config.py`** - 簡單測試文件
   - 驗證獎勵配置系統是否正常工作

4. **`docs/reward_config_guide.md`** - 詳細使用指南
   - 完整的參數說明
   - 使用方法和最佳實踐

### 修改的文件

1. **`vehicle.py`** - 已修改為使用獎勵配置系統
   - 增加 `reward_config` 參數到建構函數
   - 所有硬編碼的獎勵數值都改為從配置讀取

## 主要功能

### 1. 獨立的獎勵配置

- 所有獎勵相關的常數都集中在 `RewardConfig` 類別中
- 其他類別可以輕鬆載入和修改這些數值

### 2. 靈活的配置方式

```python
# 使用預設配置
vehicle = Vehicle(urban_grid, agent)

# 使用自定義配置
custom_config = RewardConfig()
custom_config.update_config(step_penalty=-2, destination_reached_reward=200)
vehicle = Vehicle(urban_grid, agent, reward_config=custom_config)
```

### 3. 運行時動態修改

```python
# 修改配置
vehicle.reward_config.update_config(step_penalty=-5)

# 重置為預設值
vehicle.reward_config.reset_to_defaults()
```

### 4. 多種配置模板

- 積極型配置（快速、直接路線）
- 謹慎型配置（探索性強）
- 自定義配置（完全客製化）

## 可配置的參數（19個）

- 基本移動獎勵 (1個)
- A* 路徑跟隨獎勵 (2個)
- 距離相關獎勵 (1個)
- 交通壅塞懲罰 (2個)
- 後退移動懲罰 (3個)
- 交通燈懲罰 (1個)
- 目的地獎勵 (1個)
- 迴圈檢測和懲罰 (4個)
- 接近獎勵參數 (2個)
- A* 路徑距離獎勵參數 (2個)

## 優點

1. **代碼可維護性**: 獎勵邏輯與核心車輛邏輯分離
2. **實驗便利性**: 可以輕鬆測試不同的獎勵策略
3. **配置管理**: 集中管理所有獎勵參數
4. **向後兼容**: 不提供配置時自動使用預設值
5. **擴展性**: 容易添加新的獎勵參數

## 測試結果

✅ 所有測試通過，系統運作正常

現在您可以在其他類別中輕鬆載入和修改獎勵函數的數值，無需直接修改 `Vehicle` 類別的核心代碼。
