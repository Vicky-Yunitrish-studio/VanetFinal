# Q-Learning 都市車聯網路徑選擇模擬系統 專案說明

## 一、專案整體架構

本專案模擬一個城市網格路網，使用 Q-Learning 強化學習演算法，讓多台車輛在動態交通環境下自主規劃路徑，避開擁塞與障礙，並支援互動式模擬與多種訓練模式。

### 主要流程
1. **環境建構**：建立城市網格 (`UrbanGrid`)，可隨機產生障礙與調整擁塞度。
2. **代理訓練**：每台車輛為一個 Q-Learning 代理 (`QLearningAgent`)，透過多回合訓練學習最佳路徑。
3. **模擬互動**：可視化模擬車輛移動、調整參數、即時觀察學習成果。
4. **模型儲存/載入**：支援代理模型的保存與載入，方便多階段訓練與比較。

---

## 二、各檔案功能說明

### 主要程式

- **main.py**  
  專案主入口，負責解析命令列參數，根據模式（訓練、模擬、兩者皆執行）調用對應流程。支援多種訓練與模擬參數設定。

- **urban_grid.py**  
  定義 `UrbanGrid` 類別，負責建立城市網格、管理道路擁塞度、障礙物、交通事故等環境狀態，並提供環境重置與視覺化支援。

- **agent.py**  
  定義 `QLearningAgent` 類別，實作 Q-Learning 強化學習邏輯，包括狀態空間設計、動作選擇（epsilon-greedy）、Q-table 更新、學習率與折扣因子設定等。

- **vehicle.py**  
  定義 `Vehicle` 類別，模擬單一車輛的行為，負責與 QLearningAgent 互動、移動決策、獎勵計算、路徑記錄等。

- **simulation.py**  
  負責訓練與測試流程的主控，包括環境初始化、多車輛管理、統計數據收集（獎勵、步數、成功率）、學習曲線繪製等。

- **simulation_controller.py**  
  提供互動式模擬控制器（GUI/CLI），支援開始、暫停、單步執行、重置、參數調整（車輛數、步數、延遲）、代理載入/儲存等功能。

- **visualizer.py**  
  負責城市網格、車輛移動、障礙物、擁塞度等視覺化顯示，支援學習過程與測試結果的圖形化。

- **astar.py**  
  提供 A* 演算法輔助路徑規劃（如用於 baseline 或障礙檢查）。

---

### 測試與驗證

- **test_all_features.py**  
  測試所有主要功能與模組整合，確保系統穩定性。

- **test_path_visualization.py**  
  專注於路徑規劃與視覺化功能的測試。

- **test_ui.py**  
  測試模擬控制器的互動界面與參數調整功能。

---

### 代理模型與數據

- **v1.pkl**  
  範例訓練完成的 Q-Learning 代理模型，可直接載入進行模擬。

---

### 其他

- **requirements.txt**  
  專案所需 Python 套件列表。

- **docs/**  
  說明文件資料夾，包含詳細的使用手冊、訓練指引、無限步數模式說明等。

- **IMPROVEMENTS_SUMMARY.md**  
  已完成功能與技術細節總結。

- **readme.md**  
  專案簡介、核心概念、設計說明、主要類別與函數、執行方式等。

---

## 三、使用方式

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 執行訓練
訓練一個新的 Q-Learning 代理（預設 200 回合）：
```bash
python main.py --mode train --episodes 200
```
可加上 `--iterations N` 進行多階段訓練，`--save-iterations` 會保存每個階段的代理。

### 3. 執行模擬
載入已訓練代理進行互動模擬：
```bash
python main.py --mode simulate
```
可於模擬控制器中調整車輛數、步數、障礙等參數。

### 4. 訓練+模擬（預設模式）
先訓練後自動進入模擬：
```bash
python main.py
# 或
python main.py --mode both
```

### 5. 無限步數模式
允許模擬直到所有車輛到達目的地：
```bash
python main.py --mode train --unlimited-steps
```
或於模擬控制器中勾選「無限步數」選項。

### 6. 代理模型儲存與載入
- 訓練過程會自動保存 `trained_agent.pkl` 或 `trained_agent_iterN.pkl`。
- 可於模擬控制器中載入指定代理檔案進行測試與比較。

---

## 四、參考文件

- [`readme.md`](VanetFinal/readme.md)：專案總覽、設計理念、主要類別與函數說明
- [`docs/simulation_readme.md`](VanetFinal/docs/simulation_readme.md)：模擬控制器詳細操作說明
- [`docs/iterative_training_guide.md`](VanetFinal/docs/iterative_training_guide.md)：多階段訓練與模型管理指引
- [`docs/unlimited_steps_guide.md`](VanetFinal/docs/unlimited_steps_guide.md)：無限步數模式說明
- [`IMPROVEMENTS_SUMMARY.md`](VanetFinal/IMPROVEMENTS_SUMMARY.md)：功能與技術細節總結

---

## 五、檔案結構總覽

```
VanetFinal/
├── agent.py
├── astar.py
├── main.py
├── simulation.py
├── simulation_controller.py
├── urban_grid.py
├── vehicle.py
├── visualizer.py
├── test_all_features.py
├── test_path_visualization.py
├── test_ui.py
├── v1.pkl
├── requirements.txt
├── readme.md
├── IMPROVEMENTS_SUMMARY.md
├── docs/
│   ├── simulation_readme.md
│   ├── iterative_training_guide.md
│   └── unlimited_steps_guide.md
└── ...
```

---

如需更細節的類別與函數說明，請參考 [`readme.md`](VanetFinal/readme.md) 及 `docs/` 內各說明