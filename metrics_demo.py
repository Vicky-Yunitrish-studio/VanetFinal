#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能指標演示程式
實際展示成功率、平均步數、路徑效率的計算過程
"""

import random
import math

def manhattan_distance(pos1, pos2):
    """計算曼哈頓距離"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def simulate_navigation_task(start, destination, max_steps=100):
    """
    模擬一次導航任務
    返回是否成功、使用的步數、實際路徑
    """
    current_pos = start
    steps = 0
    path = [current_pos]
    
    while steps < max_steps and current_pos != destination:
        # 簡化的移動策略：有80%機率朝目標移動，20%隨機探索
        if random.random() < 0.8:
            # 朝目標移動
            dx = 1 if destination[0] > current_pos[0] else (-1 if destination[0] < current_pos[0] else 0)
            dy = 1 if destination[1] > current_pos[1] else (-1 if destination[1] < current_pos[1] else 0)
        else:
            # 隨機探索
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        
        new_pos = (current_pos[0] + dx, current_pos[1] + dy)
        current_pos = new_pos
        path.append(current_pos)
        steps += 1
    
    success = (current_pos == destination)
    return success, steps, path

def calculate_metrics(test_results):
    """計算三個核心指標"""
    total_tests = len(test_results)
    successful_tests = [result for result in test_results if result['success']]
    
    # 1. 成功率
    success_rate = len(successful_tests) / total_tests
    
    # 2. 平均步數（只計算成功的任務）
    if successful_tests:
        avg_steps = sum(result['steps'] for result in successful_tests) / len(successful_tests)
    else:
        avg_steps = 0
    
    # 3. 路徑效率（只計算成功的任務）
    efficiencies = []
    for result in successful_tests:
        optimal_steps = result['optimal_steps']
        actual_steps = result['steps']
        efficiency = optimal_steps / actual_steps if actual_steps > 0 else 0
        efficiencies.append(efficiency)
    
    avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
    
    return {
        'success_rate': success_rate,
        'avg_steps': avg_steps,
        'path_efficiency': avg_efficiency,
        'total_tests': total_tests,
        'successful_tests': len(successful_tests)
    }

def main():
    print("=== 性能評估指標演示 ===")
    print()
    
    # 測試設定
    test_cases = 20
    max_steps = 50
    
    print(f"📋 測試設定：")
    print(f"   測試次數：{test_cases}")
    print(f"   最大步數限制：{max_steps}")
    print(f"   地圖範圍：10x10")
    print()
    
    # 收集測試結果
    results = []
    
    print("🔄 執行測試...")
    for i in range(test_cases):
        # 隨機生成起點和終點
        start = (random.randint(0, 9), random.randint(0, 9))
        destination = (random.randint(0, 9), random.randint(0, 9))
        
        # 確保起點和終點不同
        while start == destination:
            destination = (random.randint(0, 9), random.randint(0, 9))
        
        # 計算理論最短步數
        optimal_steps = manhattan_distance(start, destination)
        
        # 執行導航模擬
        success, steps, path = simulate_navigation_task(start, destination, max_steps)
        
        result = {
            'test_id': i + 1,
            'start': start,
            'destination': destination,
            'success': success,
            'steps': steps,
            'optimal_steps': optimal_steps,
            'path': path
        }
        results.append(result)
        
        # 顯示進度
        status = "✅ 成功" if success else "❌ 失敗"
        efficiency = f"{optimal_steps/steps*100:.1f}%" if success and steps > 0 else "N/A"
        print(f"   測試 {i+1:2d}: {start} → {destination} | {status} | 步數: {steps:2d} | 效率: {efficiency}")
    
    print()
    print("=" * 60)
    print("📊 性能指標計算結果")
    print("=" * 60)
    
    # 計算指標
    metrics = calculate_metrics(results)
    
    # 顯示結果
    print(f"\n🎯 1. 成功率 (Success Rate)")
    print(f"   公式: 成功次數 / 總測試次數")
    print(f"   計算: {metrics['successful_tests']} / {metrics['total_tests']}")
    print(f"   結果: {metrics['success_rate']*100:.1f}%")
    
    if metrics['success_rate'] >= 0.9:
        print(f"   評價: 🌟 優秀")
    elif metrics['success_rate'] >= 0.7:
        print(f"   評價: 👍 良好")
    else:
        print(f"   評價: ⚠️  需改進")
    
    print(f"\n🚶 2. 平均步數 (Average Steps)")
    print(f"   公式: 所有成功任務的總步數 / 成功任務數")
    if metrics['successful_tests'] > 0:
        total_steps = sum(result['steps'] for result in results if result['success'])
        print(f"   計算: {total_steps} / {metrics['successful_tests']}")
        print(f"   結果: {metrics['avg_steps']:.1f} 步")
        
        # 計算平均理論最短步數作為比較
        avg_optimal = sum(result['optimal_steps'] for result in results if result['success']) / metrics['successful_tests']
        step_efficiency = avg_optimal / metrics['avg_steps'] if metrics['avg_steps'] > 0 else 0
        print(f"   理論平均: {avg_optimal:.1f} 步")
        print(f"   步數效率: {step_efficiency*100:.1f}%")
    else:
        print(f"   結果: 無成功案例")
    
    print(f"\n📏 3. 路徑效率 (Path Efficiency)")
    print(f"   公式: 理論最短路徑 / 實際路徑長度")
    if metrics['successful_tests'] > 0:
        print(f"   平均效率: {metrics['path_efficiency']*100:.1f}%")
        
        if metrics['path_efficiency'] >= 0.8:
            print(f"   評價: 🌟 高效率")
        elif metrics['path_efficiency'] >= 0.6:
            print(f"   評價: 🔄 中等效率")
        else:
            print(f"   評價: ⚠️  低效率")
    else:
        print(f"   結果: 無成功案例")
    
    # 綜合評分
    if metrics['successful_tests'] > 0:
        comprehensive_score = (
            metrics['success_rate'] * 0.4 +
            metrics['path_efficiency'] * 0.4 +
            (avg_optimal / metrics['avg_steps'] if metrics['avg_steps'] > 0 else 0) * 0.2
        ) * 100
        
        print(f"\n🏆 綜合評分")
        print(f"   公式: 成功率×0.4 + 路徑效率×0.4 + 步數效率×0.2")
        print(f"   得分: {comprehensive_score:.1f}/100")
        
        if comprehensive_score >= 80:
            print(f"   等級: 🌟 優秀")
        elif comprehensive_score >= 65:
            print(f"   等級: 👍 良好")
        elif comprehensive_score >= 50:
            print(f"   等級: 🔄 一般")
        else:
            print(f"   等級: ⚠️  需改進")
    
    print(f"\n💡 指標解釋:")
    print(f"   • 成功率: 衡量演算法的穩定性和可靠性")
    print(f"   • 平均步數: 衡量到達目標的速度")
    print(f"   • 路徑效率: 衡量路徑的最優化程度")
    print(f"   • 三者結合可全面評估導航演算法性能")

if __name__ == "__main__":
    main()
