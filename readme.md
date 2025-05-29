# Q-Learning 模擬車聯網的路徑選擇（Path Planning in Urban Grid）

## 核心概念

模擬一個城市路網（例如 10x10 的交叉口），每台車用 Q-Learning 決定在每個路口往哪邊走，避開壅塞區域、繞路事故。

## 模擬場景

- 車輛從起點走到終點，路網為固定 grid
- 每條道路都有一個擁擠程度（模擬成 congestion level）
- 可模擬交通事件（例如某些路段不可通行）

## Q-learning 設計

### 狀態

- 當前座標（可 hash 成一個 state）
- 附近擁擠程度（例如平均 3x3 grid congestion）

### 行動

- 向上、下、左、右移動

### 獎勵

- 抵達目的地：+100
- 經過高壅塞道路：-5
- 每多耗一格移動：-1

## 程式碼架構

### 主要類別

1. **UrbanGrid** - 模擬城市道路網格系統
   - 管理城市地圖的基本結構
   - 處理交通擁塞度的更新和計算
   - 模擬交通事故/障礙物
   - 視覺化城市狀態和車輛移動

2. **QLearningAgent** - 實現 Q-Learning 演算法
   - 定義狀態空間（位置 + 擁塞程度）
   - 實現 epsilon-greedy 策略選擇動作
   - 避開障礙物和邊界
   - 更新 Q-table 和學習過程

3. **Vehicle** - 模擬車輛
   - 透過 Q-Learning 做決策移動
   - 處理起點/終點設置
   - 計算並接收獎勵
   - 記錄行駛路徑

### 主要函數

1. **run_simulation** - 執行完整模擬
   - 設置環境和障礙物
   - 創建和運行多輛車輛
   - 追踪統計數據（獎勵、步數、成功率）
   - 繪製學習曲線

2. **test_incident_response** - 測試學習結果
   - 在特定場景下測試學習到的策略
   - 模擬道路中間的障礙物
   - 驗證車輛是否能成功避開障礙

### 控制參數

- **show_plots** - 控制是否顯示視覺化圖表
  - 可設置為 False 以加速模擬過程
  - 影響所有視覺化元素（移動過程、學習曲線等）

## 執行方式

```python
if __name__ == "__main__":
    # 設定是否顯示圖表
    show_plots = False  # 將此變數設為 False 可暫時關閉所有圖表顯示
    
    # 訓練智能體
    trained_agent = run_simulation(episodes=200, visualize_interval=50, show_plots=show_plots)
    
    # 測試智能體在特定場景下的表現
    test_incident_response(trained_agent, show_plot=show_plots)
```