#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

def main():
    print("=== 演算法公式比較與分析 ===")
    print()
    
    print("您照片中的公式就是指數距離演算法！")
    print()
    
    print("🎯 鄰近性演算法 (Proximity-Based):")
    print("   公式: reward = (old_distance - new_distance) × multiplier")
    print("   特徵: 線性關係，穩定獎勵")
    print()
    
    print("📈 指數距離演算法 (Exponential Distance):") 
    print("   公式: r = base_reward + amplitude × exp(-(|xi-xd|/x_scale + |yi-yd|/y_scale))")
    print("   特徵: 指數衰減，接近目標時獎勵急劇增加")
    print()
    
    print("=== 實際數值比較 (車輛距離目標不同距離時的獎勵) ===")
    print("距離   鄰近性獎勵   指數距離獎勵")
    print("----   ---------   -----------")
    
    # 設定參數
    base_reward = -1
    amplitude = 40
    x_scale = 1.5
    y_scale = 2.0
    
    for dist in [10, 7, 5, 3, 1, 0.5]:
        # 鄰近性演算法 (簡化版本)
        proximity_reward = 5 * (1 if dist > 0 else 10)  # 固定倍數
        
        # 指數距離演算法
        normalized_dist = dist / x_scale + dist / y_scale
        exp_reward = base_reward + amplitude * math.exp(-normalized_dist)
        
        print(f"{dist:4.1f}   {proximity_reward:9.1f}   {exp_reward:11.2f}")
    
    print()
    print("📊 關鍵差異:")
    print("1. 鄰近性演算法: 線性、穩定、適合一般導航")
    print("2. 指數距離演算法: 指數衰減、高敏感度、適合精確定位")
    print()
    print("您照片中的公式確實是指數距離演算法的數學表達式！")

if __name__ == "__main__":
    main()
