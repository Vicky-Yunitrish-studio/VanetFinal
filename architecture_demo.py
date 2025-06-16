#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系統架構層級演示
展示A*演算法與指數距離獎勵函數的不同層級關係
"""

def demonstrate_system_layers():
    print("=== 系統架構層級演示 ===")
    print()
    
    print("您的問題：照片公式與A*演算法是不同層級的嗎？")
    print("答案：是的！讓我們看看具體差異：")
    print()
    
    # 模擬一個簡單的場景
    start = (0, 0)
    destination = (5, 5)
    current_pos = (2, 3)
    
    print("🗺️  場景設定：")
    print(f"   起點：{start}")
    print(f"   目標：{destination}")
    print(f"   當前位置：{current_pos}")
    print()
    
    print("🏗️  第一層：A*路徑規劃演算法")
    print("   功能：計算最優路徑")
    astar_path = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5)]
    print(f"   A*計算的路徑：{astar_path}")
    print("   特點：靜態規劃，一次性計算完成")
    print()
    
    print("🧠  第二層：Q-Learning學習系統")
    print("   功能：結合A*指導進行動態學習")
    print("   當前狀態：車輛在(2,3)，A*建議走(3,3)")
    print("   Q-Learning考慮：跟隨A*路徑 vs 探索其他選項")
    print()
    
    print("⚡  第三層：獎勵函數設計（您的照片公式在這裡！）")
    print("   功能：評估每個動作的價值")
    print()
    
    # 計算不同獎勵
    import math
    
    # 模擬兩種獎勵計算
    def proximity_reward():
        old_dist = abs(2-5) + abs(3-5)  # 當前距離目標
        new_dist = abs(3-5) + abs(3-5)  # 移動到(3,3)後的距離
        return (old_dist - new_dist) * 5  # 線性獎勵
    
    def exponential_reward():
        # 您照片中的公式！
        base_reward = -1
        amplitude = 40
        x_scale = 1.5
        y_scale = 2.0
        
        x_dist = abs(3 - 5)  # 移動到(3,3)後與目標的X距離
        y_dist = abs(3 - 5)  # 移動到(3,3)後與目標的Y距離
        normalized_dist = x_dist / x_scale + y_dist / y_scale
        
        return base_reward + amplitude * math.exp(-normalized_dist)
    
    prox_reward = proximity_reward()
    exp_reward = exponential_reward()
    
    print(f"   選項A：鄰近性演算法獎勵 = {prox_reward:.2f}")
    print(f"   選項B：指數距離演算法獎勵 = {exp_reward:.2f}")
    print("           ↑ 這就是您照片中的公式！")
    print()
    
    print("🔧  系統整合：")
    print("   1. A*提供路徑指導")
    print("   2. Q-Learning決定是否跟隨或探索")
    print("   3. 獎勵函數塑造學習行為")
    print()
    
    print("💡  關鍵洞察：")
    print("   • A*演算法：解決'走哪條路'的問題")
    print("   • 指數距離公式：解決'如何評價每一步'的問題")
    print("   • 它們在不同層級上協同工作！")
    print()
    
    print("🎯  總結：")
    print("   您的照片公式是獎勵函數設計層級的工具，")
    print("   與A*路徑規劃演算法在不同層級上協同運作，")
    print("   共同構成了一個強大的混合智能導航系統！")

if __name__ == "__main__":
    demonstrate_system_layers()
