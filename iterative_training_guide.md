# 迭代訓練說明

這個文件說明如何使用自動迭代訓練功能來訓練 Q-Learning 交通模擬代理。

## 迭代訓練基本概念

迭代訓練允許您在多個連續的訓練階段中訓練代理，每個階段結束時可以儲存中間結果。這樣可以觀察代理的學習過程，並在需要時從特定階段繼續訓練，而不必從頭開始。

## 使用方法

### 執行多迭代訓練

```bash
# 執行 5 個迭代，每個迭代包含 100 個訓練回合，保存每個迭代的結果
python main.py --mode train --episodes 100 --iterations 5 --save-iterations
```

### 從特定迭代繼續訓練

```bash
# 先將某個迭代的結果設為當前代理
cp trained_agent_iter3.pkl trained_agent.pkl

# 然後繼續訓練
python main.py --mode train --episodes 100 --iterations 2 --continue
```

### 自動迭代訓練參數

以下是迭代訓練相關的命令行參數：

| 參數 | 說明 |
|-----|------|
| `--episodes N` | 每次迭代的訓練回合數 (默認: 200) |
| `--iterations N` | 要執行的訓練迭代次數 (默認: 1) |
| `--save-iterations` | 保存每個迭代後的中間代理 |
| `--continue` | 從現有的 `trained_agent.pkl` 繼續訓練 |
| `--no-save` | 不保存最終訓練的代理 |

## 輸出文件

迭代訓練會產生以下文件：

- `trained_agent_iter1.pkl`, `trained_agent_iter2.pkl`, ... : 每個迭代結束後保存的中間結果
- `trained_agent.pkl` : 最終訓練完成的代理

## 案例示例

### 場景 1: 初始訓練並觀察學習進度

```bash
# 執行 10 次迭代，每次 50 個回合，共 500 個回合的訓練
python main.py --mode train --episodes 50 --iterations 10 --save-iterations
```

這會產生 10 個中間保存點，讓您可以觀察不同階段的代理表現。

### 場景 2: 繼續之前的訓練，並提高學習質量

```bash
# 從之前的訓練繼續
python main.py --mode train --episodes 100 --iterations 5 --continue
```

這將從之前保存的 `trained_agent.pkl` 繼續訓練 5 個迭代，每個迭代 100 個回合。

### 場景 3: 訓練後立即進行模擬

```bash
# 訓練並立即模擬
python main.py --mode both --episodes 100 --iterations 3
```

這將執行 3 個迭代的訓練後啟動模擬控制器。

## 比較不同訓練階段的代理表現

您可以使用模擬控制器來比較不同階段的代理表現：

1. 啟動模擬控制器：`python main.py --mode simulate`
2. 點擊 "Load Agent" 按鈕
3. 選擇要測試的代理檔案 (例如 `trained_agent_iter3.pkl`)
4. 使用模擬控制器來評估代理在不同場景下的表現

利用這種方式，您可以系統地比較不同訓練階段的代理效能，選擇最適合您需求的版本。
