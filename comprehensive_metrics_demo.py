#!/usr/bin/env python3
"""
完整的五個核心性能指標計算和分析演示
Comprehensive Five Core Performance Metrics Calculation and Analysis Demo

這個腳本展示如何計算和分析導航系統的五個核心評估指標：
1. 成功率 (Success Rate)
2. 平均步數 (Average Steps)  
3. 路徑效率 (Path Efficiency)
4. 計算時間 (Computation Time)
5. 平均獎勵 (Average Reward)
"""

import time
import random
import numpy as np
from typing import Dict, List, Tuple, NamedTuple
import matplotlib.pyplot as plt
import sys
import os

# 添加專案路徑以便導入模組
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class NavigationResult(NamedTuple):
    """導航結果數據結構"""
    success: bool
    steps: int
    total_reward: float
    path: List[Tuple[int, int]]
    start: Tuple[int, int]
    end: Tuple[int, int]
    computation_time: float  # 毫秒

class MetricsCalculator:
    """五個核心指標的計算器"""
    
    def __init__(self):
        self.results: List[NavigationResult] = []
    
    def add_result(self, result: NavigationResult):
        """添加一次導航結果"""
        self.results.append(result)
    
    def calculate_astar_optimal_steps(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        """計算A*演算法的理論最短步數（曼哈頓距離）"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    def get_metrics(self) -> Dict[str, float]:
        """計算所有五個核心指標"""
        if not self.results:
            return {
                'success_rate': 0.0,
                'avg_steps': 0.0,
                'path_efficiency': 0.0,
                'avg_computation_time': 0.0,
                'avg_reward': 0.0
            }
        
        # 1. 成功率 (Success Rate)
        successful_results = [r for r in self.results if r.success]
        success_rate = len(successful_results) / len(self.results) * 100
        
        if not successful_results:
            return {
                'success_rate': success_rate,
                'avg_steps': 0.0,
                'path_efficiency': 0.0,
                'avg_computation_time': 0.0,
                'avg_reward': 0.0
            }
        
        # 2. 平均步數 (Average Steps) - 只計算成功的任務
        avg_steps = sum(r.steps for r in successful_results) / len(successful_results)
        
        # 3. 路徑效率 (Path Efficiency)
        path_efficiencies = []
        for result in successful_results:
            optimal_steps = self.calculate_astar_optimal_steps(result.start, result.end)
            efficiency = optimal_steps / result.steps if result.steps > 0 else 0
            path_efficiencies.append(efficiency)
        
        avg_path_efficiency = sum(path_efficiencies) / len(path_efficiencies) * 100 if path_efficiencies else 0
        
        # 4. 計算時間 (Computation Time)
        avg_computation_time = sum(r.computation_time for r in self.results) / len(self.results)
        
        # 5. 平均獎勵 (Average Reward) - 每步的平均獎勵
        total_reward = sum(r.total_reward for r in successful_results)
        total_steps = sum(r.steps for r in successful_results)
        avg_reward = total_reward / total_steps if total_steps > 0 else 0
        
        return {
            'success_rate': success_rate,
            'avg_steps': avg_steps,
            'path_efficiency': avg_path_efficiency,
            'avg_computation_time': avg_computation_time,
            'avg_reward': avg_reward
        }
    
    def get_detailed_analysis(self) -> Dict:
        """獲取詳細的分析報告"""
        metrics = self.get_metrics()
        successful_results = [r for r in self.results if r.success]
        
        analysis = {
            'basic_metrics': metrics,
            'test_summary': {
                'total_tests': len(self.results),
                'successful_tests': len(successful_results),
                'failed_tests': len(self.results) - len(successful_results)
            },
            'performance_evaluation': self._evaluate_performance(metrics),
            'detailed_stats': self._get_detailed_stats(successful_results)
        }
        
        return analysis
    
    def _evaluate_performance(self, metrics: Dict[str, float]) -> Dict[str, str]:
        """根據指標評估性能等級"""
        evaluation = {}
        
        # 成功率評估
        if metrics['success_rate'] >= 95:
            evaluation['success_rate'] = '優秀 (Excellent)'
        elif metrics['success_rate'] >= 85:
            evaluation['success_rate'] = '良好 (Good)'
        elif metrics['success_rate'] >= 70:
            evaluation['success_rate'] = '一般 (Fair)'
        else:
            evaluation['success_rate'] = '需改進 (Needs Improvement)'
        
        # 路徑效率評估
        if metrics['path_efficiency'] >= 80:
            evaluation['path_efficiency'] = '高效率 (High Efficiency)'
        elif metrics['path_efficiency'] >= 60:
            evaluation['path_efficiency'] = '中等效率 (Medium Efficiency)'
        else:
            evaluation['path_efficiency'] = '低效率 (Low Efficiency)'
        
        # 計算時間評估
        if metrics['avg_computation_time'] < 1:
            evaluation['computation_time'] = '優秀 (Excellent - Real-time)'
        elif metrics['avg_computation_time'] < 5:
            evaluation['computation_time'] = '良好 (Good - Fast)'
        elif metrics['avg_computation_time'] < 20:
            evaluation['computation_time'] = '一般 (Fair - Acceptable)'
        else:
            evaluation['computation_time'] = '需改進 (Needs Improvement)'
        
        # 平均獎勵評估
        if metrics['avg_reward'] > 5:
            evaluation['avg_reward'] = '優秀 (Excellent)'
        elif metrics['avg_reward'] > 2:
            evaluation['avg_reward'] = '良好 (Good)'
        elif metrics['avg_reward'] > 0:
            evaluation['avg_reward'] = '一般 (Fair)'
        else:
            evaluation['avg_reward'] = '需改進 (Needs Improvement)'
        
        return evaluation
    
    def _get_detailed_stats(self, successful_results: List[NavigationResult]) -> Dict:
        """獲取詳細統計信息"""
        if not successful_results:
            return {}
        
        steps = [r.steps for r in successful_results]
        rewards = [r.total_reward for r in successful_results]
        computation_times = [r.computation_time for r in self.results]
        
        return {
            'steps_stats': {
                'min': min(steps),
                'max': max(steps),
                'std': np.std(steps),
                'median': np.median(steps)
            },
            'reward_stats': {
                'min': min(rewards),
                'max': max(rewards),
                'std': np.std(rewards),
                'median': np.median(rewards)
            },
            'computation_time_stats': {
                'min': min(computation_times),
                'max': max(computation_times),
                'std': np.std(computation_times),
                'median': np.median(computation_times)
            }
        }

def simulate_navigation_algorithm(algorithm_name: str, start: Tuple[int, int], 
                                end: Tuple[int, int]) -> NavigationResult:
    """模擬導航演算法執行"""
    start_time = time.time()
    
    # 模擬不同演算法的特性
    if algorithm_name == "proximity":
        # 鄰近性演算法：較穩定但可能步數較多
        success_prob = 0.95
        base_steps = abs(start[0] - end[0]) + abs(start[1] - end[1])  # 曼哈頓距離
        steps_multiplier = random.uniform(1.2, 1.8)  # 比最優路徑多20%-80%
        reward_per_step = random.uniform(3, 6)  # 穩定的獎勵
        computation_delay = random.uniform(0.3, 0.8)  # 快速計算
        
    elif algorithm_name == "exponential":
        # 指數距離演算法：更精確但計算較慢
        success_prob = 0.88
        base_steps = abs(start[0] - end[0]) + abs(start[1] - end[1])
        steps_multiplier = random.uniform(1.1, 1.5)  # 比最優路徑多10%-50%
        reward_per_step = random.uniform(-1, 8)  # 變化較大的獎勵
        computation_delay = random.uniform(0.8, 2.5)  # 較慢的計算
        
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    # 模擬計算時間
    time.sleep(computation_delay / 1000)  # 轉換為秒
    end_time = time.time()
    computation_time = (end_time - start_time) * 1000  # 轉換為毫秒
    
    # 決定是否成功
    success = random.random() < success_prob
    
    if success:
        steps = int(base_steps * steps_multiplier)
        total_reward = steps * reward_per_step + random.uniform(50, 100)  # 額外的到達獎勵
        # 生成簡化的路徑
        path = [(start[0] + i, start[1]) for i in range(steps//2)] + \
               [(end[0], start[1] + i) for i in range(steps//2)]
    else:
        steps = 0
        total_reward = -50  # 失敗懲罰
        path = []
    
    return NavigationResult(
        success=success,
        steps=steps,
        total_reward=total_reward,
        path=path,
        start=start,
        end=end,
        computation_time=computation_time
    )

def run_comprehensive_evaluation():
    """執行完整的五個指標評估"""
    print("🚗 導航系統五個核心指標評估演示")
    print("=" * 60)
    
    # 測試兩種演算法
    algorithms = ["proximity", "exponential"]
    test_cases = 50  # 每個演算法測試50次
    
    results = {}
    
    for algorithm in algorithms:
        print(f"\n📊 評估演算法: {algorithm.upper()}")
        print("-" * 40)
        
        calculator = MetricsCalculator()
        
        # 執行多次測試
        for i in range(test_cases):
            # 隨機生成起點和終點
            start = (random.randint(0, 10), random.randint(0, 10))
            end = (random.randint(0, 10), random.randint(0, 10))
            
            # 確保起點和終點不同
            while start == end:
                end = (random.randint(0, 10), random.randint(0, 10))
            
            # 執行導航模擬
            result = simulate_navigation_algorithm(algorithm, start, end)
            calculator.add_result(result)
            
            # 顯示進度
            if (i + 1) % 10 == 0:
                print(f"  已完成 {i + 1}/{test_cases} 次測試...")
        
        # 計算並顯示結果
        analysis = calculator.get_detailed_analysis()
        results[algorithm] = analysis
        
        print("\n📈 核心指標結果:")
        metrics = analysis['basic_metrics']
        evaluation = analysis['performance_evaluation']
        
        print(f"  1️⃣  成功率: {metrics['success_rate']:.1f}% - {evaluation['success_rate']}")
        print(f"  2️⃣  平均步數: {metrics['avg_steps']:.1f} 步")
        print(f"  3️⃣  路徑效率: {metrics['path_efficiency']:.1f}% - {evaluation['path_efficiency']}")
        print(f"  4️⃣  計算時間: {metrics['avg_computation_time']:.2f} ms - {evaluation['computation_time']}")
        print(f"  5️⃣  平均獎勵: {metrics['avg_reward']:.2f} 分/步 - {evaluation['avg_reward']}")
        
        # 顯示測試統計
        test_summary = analysis['test_summary']
        print(f"\n📋 測試統計:")
        print(f"  總測試次數: {test_summary['total_tests']}")
        print(f"  成功次數: {test_summary['successful_tests']}")
        print(f"  失敗次數: {test_summary['failed_tests']}")
    
    # 演算法比較
    print("\n🔄 演算法比較分析")
    print("=" * 60)
    
    proximity_metrics = results['proximity']['basic_metrics']
    exponential_metrics = results['exponential']['basic_metrics']
    
    print(f"{'指標':<15} {'鄰近性演算法':<15} {'指數距離演算法':<15} {'較優者':<10}")
    print("-" * 65)
    
    comparisons = [
        ('成功率 (%)', 'success_rate', True),
        ('平均步數', 'avg_steps', False),
        ('路徑效率 (%)', 'path_efficiency', True),
        ('計算時間 (ms)', 'avg_computation_time', False),
        ('平均獎勵', 'avg_reward', True)
    ]
    
    for name, key, higher_is_better in comparisons:
        prox_val = proximity_metrics[key]
        exp_val = exponential_metrics[key]
        
        if higher_is_better:
            winner = "鄰近性" if prox_val > exp_val else "指數距離"
        else:
            winner = "鄰近性" if prox_val < exp_val else "指數距離"
        
        print(f"{name:<15} {prox_val:<15.2f} {exp_val:<15.2f} {winner:<10}")
    
    # 綜合評分
    print("\n🏆 綜合評分")
    print("-" * 30)
    
    def calculate_comprehensive_score(metrics):
        """計算綜合評分"""
        # 正規化各指標
        success_rate_norm = metrics['success_rate'] / 100
        path_efficiency_norm = metrics['path_efficiency'] / 100
        steps_efficiency = min(1.0, 10 / max(metrics['avg_steps'], 1))
        time_efficiency = min(1.0, 1.0 / max(metrics['avg_computation_time'], 0.1))
        reward_efficiency = min(1.0, max(0, metrics['avg_reward'] / 8.0))
        
        # 加權計算
        score = (success_rate_norm * 0.35 + 
                path_efficiency_norm * 0.25 + 
                steps_efficiency * 0.20 + 
                time_efficiency * 0.10 + 
                reward_efficiency * 0.10)
        
        return score * 100
    
    prox_score = calculate_comprehensive_score(proximity_metrics)
    exp_score = calculate_comprehensive_score(exponential_metrics)
    
    print(f"鄰近性演算法綜合得分: {prox_score:.1f}分")
    print(f"指數距離演算法綜合得分: {exp_score:.1f}分")
    
    winner = "鄰近性演算法" if prox_score > exp_score else "指數距離演算法"
    print(f"\n🥇 總體優勝者: {winner}")
    
    print("\n💡 指標分析建議:")
    print("=" * 40)
    print("• 成功率: 反映演算法的可靠性，越高越好")
    print("• 平均步數: 反映路徑長度，越少越好")
    print("• 路徑效率: 反映路徑優化程度，越高越好")
    print("• 計算時間: 反映實時性能，越短越好")
    print("• 平均獎勵: 反映行為品質，越高越好")
    print("\n🎯 選擇演算法時需要根據具體應用場景考慮各指標的重要性！")

if __name__ == "__main__":
    run_comprehensive_evaluation()
