#!/usr/bin/env python3
"""
獎勵配置GUI功能展示腳本

這個腳本展示如何使用新的獎勵配置GUI功能來調整車輛行為。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from UI.simulation_controller import SimulationController
from algorithm.agent import QLearningAgent
from module.urban_grid import UrbanGrid
from algorithm.reward_config import RewardConfig

def main():
    """主函數 - 啟動獎勵配置GUI"""
    print("=== 獎勵配置GUI功能展示 ===")
    print()
    print("此程序將啟動一個帶有獎勵配置功能的模擬控制器。")
    print()
    print("功能特點:")
    print("1. 🎯 基本獎勵設定 - 調整步驟懲罰、目的地獎勵等")
    print("2. 🚫 移動懲罰設定 - 調整壅塞懲罰、後退懲罰等")
    print("3. ⚙️  進階設定 - 調整迴圈檢測、接近獎勵等")
    print("4. 📋 預設配置 - 快速載入積極型、謹慎型或平衡型配置")
    print("5. 💾 即時應用 - 立即將設定應用到模擬中")
    print()
    print("使用方法:")
    print("1. 啟動後會看到一個模擬控制器視窗")
    print("2. 找到「Reward Configuration」部分")
    print("3. 有三個標籤頁可以調整不同類型的獎勵")
    print("4. 修改數值後點擊「Apply Reward Config」")
    print("5. 可以使用「Load Preset」快速載入預設配置")
    print("6. 然後開始模擬來測試效果")
    print()
    
    try:
        # 創建基本組件
        print("🔧 初始化模擬環境...")
        grid = UrbanGrid(size=15)  # 使用中等大小的網格
        agent = QLearningAgent(grid)
        
        print("✅ 環境初始化完成")
        print("🚀 啟動GUI...")
        
        # 創建模擬控制器（這會自動包含獎勵配置GUI）
        controller = SimulationController(trained_agent=agent)
        
        print()
        print("📖 GUI使用提示:")
        print("   • 獎勵配置在主視窗的中間部分")
        print("   • 三個標籤頁分別對應不同類型的設定")
        print("   • 數值可以是正數（獎勵）或負數（懲罰）")
        print("   • 修改後記得點擊「Apply Reward Config」")
        print("   • 可以隨時「Reset to Defaults」回到預設值")
        print()
        print("🎮 開始使用GUI...")
        
        # 啟動GUI主循環
        controller.run()
        
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        print("請確保所有必要的模組都已正確安裝")
        return 1
    
    print("👋 程序結束")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
