# 獎勵配置GUI使用指南

## 概述

本系統新增了一個圖形化的獎勵配置界面，讓您可以在訓練前輕鬆調整車輛的獎勵函數參數，無需修改代碼。

## 如何啟動

### 方法1: 使用展示腳本

```bash
python demo_reward_config_gui.py
```

### 方法2: 直接使用控制器

```bash
python test_reward_config_gui.py
```

### 方法3: 集成到現有程序

```python
from simulation_controller import SimulationController
from agent import QLearningAgent
from urban_grid import UrbanGrid

# 創建環境
grid = UrbanGrid(size=15)
agent = QLearningAgent(grid)

# 啟動帶有獎勵配置的控制器
controller = SimulationController(trained_agent=agent)
controller.run()
```

## GUI界面說明

### 主要組件位置

獎勵配置部分位於模擬控制器主視窗的中間，標題為「Reward Configuration」。

### 三個配置標籤頁

#### 1. Basic Rewards (基本獎勵)

- **Step Penalty** - 每步移動的成本 (建議: -0.5 到 -5)
- **Destination Reward** - 到達目的地的獎勵 (建議: 50 到 500)
- **A* Follow Reward**- 完全跟隨A*路徑的獎勵 (建議: 5 到 50)
- **A* On Path Reward** - 在最佳路徑上的獎勵 (建議: 2 到 20)
- **Distance Reward** - 靠近目的地的獎勵 (建議: 1 到 10)

#### 2. Movement Penalties (移動懲罰)

- **Congestion Threshold** - 高壅塞閾值 (範圍: 0.0-1.0)
- **Congestion Penalty Multiplier** - 壅塞懲罰倍數 (建議: 1 到 20)
- **Backtrack Penalty** - 立即後退懲罰 (建議: -10 到 -100)
- **Oscillation Penalty** - 振盪行為懲罰 (建議: -15 到 -80)
- **Red Light Penalty** - 紅燈等待懲罰 (建議: -1 到 -10)

#### 3. Advanced Settings (進階設定)

- **Loop Threshold Base** - 迴圈檢測基礎閾值 (建議: 2 到 10)
- **Loop Penalty Base** - 迴圈基礎懲罰 (建議: -10 到 -50)
- **Proximity Base Multiplier** - 基礎接近獎勵倍數 (建議: 2 到 10)
- **Proximity Max Multiplier** - 最大接近獎勵倍數 (建議: 5 到 30)

### 控制按鈕

#### Apply Reward Config

點擊此按鈕將當前GUI中的設定應用到模擬系統中。

#### Reset to Defaults

將所有設定重置為預設值。

#### Load Preset

快速載入預定義的配置：

- **積極型** - 快速直接的路線規劃
- **謹慎型** - 探索性強的行為
- **平衡型** - 預設的均衡配置

## 預設配置詳細說明

### 積極型配置 (快速直接)

```
步驟懲罰: -3 (鼓勵快速移動)
A*跟隨獎勵: 20 (強烈鼓勵跟隨最佳路徑)
目的地獎勵: 300 (高目標導向)
後退懲罰: -100 (嚴格禁止後退)
壅塞懲罰倍數: 15 (強烈避免壅塞)
```

### 謹慎型配置 (探索性強)

```
步驟懲罰: -0.5 (允許更多探索)
A*跟隨獎勵: 5 (較低的路徑約束)
目的地獎勵: 50 (溫和的目標導向)
後退懲罰: -10 (溫和的後退限制)
壅塞懲罰倍數: 2 (較能容忍壅塞)
```

### 平衡型配置 (預設)

所有參數都使用系統預設值，適合大多數情況。

## 使用流程

1. **啟動程序** - 使用上述任一方法啟動GUI
2. **調整參數** - 在三個標籤頁中修改所需的參數
3. **應用設定** - 點擊「Apply Reward Config」
4. **測試效果** - 開始模擬觀察車輛行為變化
5. **迭代優化** - 根據結果繼續調整參數

## 調優建議

### 提高路徑效率

- 增加「A* Follow Reward」
- 增加「Step Penalty」(更負的值)
- 增加「Backtrack Penalty」(更負的值)

### 增強探索能力

- 減少「Step Penalty」(較少負的值)
- 減少「A* Follow Reward」
- 減少各種後退懲罰

### 避免交通壅塞

- 增加「Congestion Penalty Multiplier」
- 降低「Congestion Threshold」

### 加快收斂速度

- 增加「Destination Reward」
- 增加「Distance Reward」

## 故障排除

### 常見問題

1. **輸入錯誤**: 確保所有數值都是有效的數字
2. **沒有效果**: 記得點擊「Apply Reward Config」
3. **行為異常**: 嘗試「Reset to Defaults」然後重新設定

### 調試提示

- 在狀態視窗中查看配置更新訊息
- 觀察車輛移動模式的變化
- 比較不同配置下的性能指標

## 技術細節

該GUI系統基於以下技術：

- **Tkinter**: 用於創建圖形界面
- **Notebook Widget**: 提供標籤頁界面
- **RewardConfig類別**: 後端獎勵配置管理
- **即時更新**: 參數修改即時生效

這個獎勵配置GUI讓實驗不同的車輛行為變得簡單直觀，大大提高了系統的可用性和實驗效率。
