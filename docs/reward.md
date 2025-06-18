# QLearningAgent.update_q_table 呼叫紀錄與使用方式

## 1. simulation.py

### 使用方式
在訓練過程中，每當車輛採取動作並獲得獎勵後，會呼叫 `agent.update_q_table(state, action, reward, next_state)` 來更新 Q-table。

### 計算方式
- 取得當前狀態 `state`、採取的動作 `action`、獲得的即時獎勵 `reward`、以及下個狀態 `next_state`
- 呼叫方式範例：
  ```python
  agent.update_q_table(state, action, reward, next_state)
  ```
- 依據 Q-learning 更新公式：
  ```
  Q(s,a) ← (1-α)Q(s,a) + α [r + γ max_a' Q(s',a')]
  ```
  其中 α 為學習率，γ 為折扣因子，r 為 reward。

---

## 2. vehicle.py

### 使用方式
每當車輛移動並獲得獎勵時，會呼叫 `agent.update_q_table` 更新該狀態-動作對的 Q 值。

### 計算方式
- 取得車輛當前狀態、動作、獎勵與下個狀態
- 呼叫方式範例：
  ```python
  self.agent.update_q_table(state, action, reward, next_state)
  ```
- 計算方式同上，依 Q-learning 標準公式進行。

---

## 3. 其他檔案

目前根據專案結構與說明，主要呼叫點集中於 `simulation.py` 與 `vehicle.py`，如有其他檔案呼叫，請依實際程式碼補充。

---

## Q-table 更新公式說明

```python
# agent.py
def update_q_table(self, state, action, reward, next_state):
    best_next_action = np.argmax(self.q_table[next_state])
    self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                 self.learning_rate * (reward + self.discount_factor * 
                                                     self.q_table[next_state][best_next_action])
```
- 其中 `self.learning_rate` 為 α，`self.discount_factor` 為 γ。
- `np.argmax(self.q_table[next_state])` 取得下個狀態的最大 Q 值。

---