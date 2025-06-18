"""
測試獎勵配置GUI功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation_controller import SimulationController
from agent import QLearningAgent
from urban_grid import UrbanGrid

def test_reward_config_gui():
    """測試獎勵配置GUI"""
    print("開始測試獎勵配置GUI...")
    
    # 創建基本組件
    grid = UrbanGrid(size=10)
    agent = QLearningAgent(grid)
    
    # 創建模擬控制器
    controller = SimulationController(trained_agent=agent)
    
    print("獎勵配置GUI已創建，可以進行測試")
    print("請在GUI中:")
    print("1. 檢查獎勵配置標籤頁")
    print("2. 測試修改數值")
    print("3. 測試預設配置")
    print("4. 測試應用配置")
    
    # 啟動GUI
    controller.run()

if __name__ == "__main__":
    test_reward_config_gui()
