# 無限步數模式使用說明

無限步數模式是交通模擬系統的一個功能，它允許模擬運行直到所有車輛都到達目的地，而不受最大步數限制。這對於完整評估 Q-Learning 代理的性能特別有用，尤其是在複雜場景中。

## 命令行參數

在命令行中，您可以使用以下參數來控制無限步數功能：

```bash
# 啟用無限步數模式，確保所有車輛都到達目的地
python main.py --mode train --unlimited-steps

# 設置自定義最大步數 (僅在不使用無限步數時有效)
python main.py --mode train --max-steps 1000

# 這兩個參數可以組合使用
python main.py --mode train --iterations 3 --save-iterations --unlimited-steps
```

## 在模擬控制器中使用

在模擬控制器的圖形界面中，無限步數模式可以通過以下方式使用：

1. 啟動模擬控制器：
   ```bash
   python main.py --mode simulate
   ```

2. 在控制面板中，您會看到一個「無限步數 (直到所有車輛到達)」的選項。

3. 勾選此選項可啟用無限步數模式，取消勾選則使用滑塊設定的最大步數。

## 使用場景

無限步數模式適用於以下場景：

1. **評估代理完成率**：確定代理是否總能找到從起點到終點的路徑，而不論需要多少步。

2. **複雜環境下的測試**：在有大量障礙物或高擁堵的情況下，可能需要更多步數才能到達目的地。

3. **訓練穩定性評估**：觀察代理是否能在不同的訓練階段都能完成任務。

4. **最優路徑分析**：不受步數限制的情況下，分析代理最終選擇的路徑。

## 注意事項

1. 使用無限步數模式時，如果代理無法找到從起點到終點的路徑（例如被完全封鎖），模擬可能會無限運行。在這種情況下，您可以通過「暫停」按鈕來中止模擬。

2. 如果只有少數車輛無法到達目的地，可能會導致模擬運行時間過長。這種情況下，可以考慮調整障礙物位置或改用有限步數模式。

3. 在訓練過程中使用無限步數可能會延長總訓練時間，但可能會提高代理的路徑規劃能力。
