#!/usr/bin/env python3
"""
Algorithm Performance Comparison Test
比較兩種演算法的性能測試

This script runs automated tests to compare the Proximity-Based and Exponential Distance algorithms.
"""

import sys
import time
import numpy as np
from module.urban_grid import UrbanGrid
from algorithm.agent import QLearningAgent
from vehicle import Vehicle
from algorithm.reward_config import RewardConfig

def run_algorithm_test(algorithm_name, algorithm_type, num_episodes=50, max_steps=200):
    """
    Run performance test for a specific algorithm
    
    Args:
        algorithm_name: Display name of the algorithm
        algorithm_type: Technical name ('proximity_based' or 'exponential_distance')
        num_episodes: Number of test episodes
        max_steps: Maximum steps per episode
    
    Returns:
        Dictionary with performance metrics
    """
    print(f"\n{'='*60}")
    print(f"測試演算法: {algorithm_name}")
    print(f"Testing Algorithm: {algorithm_name}")
    print(f"{'='*60}")
    
    # Initialize environment
    grid_size = 15
    grid = UrbanGrid(size=grid_size)
    agent = QLearningAgent(grid)
    
    # Configure reward system
    reward_config = RewardConfig()
    reward_config.algorithm = algorithm_type
    
    # Performance metrics
    success_count = 0
    total_steps = []
    total_rewards = []
    computation_times = []
    path_efficiencies = []
    
    for episode in range(num_episodes):
        print(f"Episode {episode + 1}/{num_episodes}", end=" ")
        
        # Random start and destination
        start_pos = (np.random.randint(1, grid_size-1), np.random.randint(1, grid_size-1))
        dest_pos = (np.random.randint(1, grid_size-1), np.random.randint(1, grid_size-1))
        
        # Ensure start and destination are different
        while start_pos == dest_pos:
            dest_pos = (np.random.randint(1, grid_size-1), np.random.randint(1, grid_size-1))
        
        # Create vehicle with specific algorithm
        vehicle = Vehicle(grid, agent, position=start_pos, destination=dest_pos, reward_config=reward_config)
        
        episode_steps = 0
        episode_reward = 0
        start_time = time.time()
        
        # Run episode
        for step in range(max_steps):
            if vehicle.reached:
                success_count += 1
                break
                
            step_reward = vehicle.move()
            episode_reward += step_reward
            episode_steps += 1
        
        computation_time = time.time() - start_time
        
        # Calculate path efficiency (actual vs optimal)
        optimal_distance = abs(start_pos[0] - dest_pos[0]) + abs(start_pos[1] - dest_pos[1])
        if episode_steps > 0:
            efficiency = optimal_distance / episode_steps
        else:
            efficiency = 0
        
        total_steps.append(episode_steps)
        total_rewards.append(episode_reward)
        computation_times.append(computation_time)
        path_efficiencies.append(efficiency)
        
        # Progress indicator
        if vehicle.reached:
            print("✅ 成功 Success")
        else:
            print("❌ 失敗 Failed")
    
    # Calculate metrics
    success_rate = success_count / num_episodes
    avg_steps = np.mean(total_steps) if total_steps else 0
    avg_reward = np.mean(total_rewards) if total_rewards else 0
    avg_computation_time = np.mean(computation_times) if computation_times else 0
    avg_efficiency = np.mean(path_efficiencies) if path_efficiencies else 0
    
    return {
        'algorithm_name': algorithm_name,
        'algorithm_type': algorithm_type,
        'success_rate': success_rate,
        'avg_steps': avg_steps,
        'avg_reward': avg_reward,
        'avg_computation_time': avg_computation_time,
        'avg_efficiency': avg_efficiency,
        'total_episodes': num_episodes
    }

def print_comparison_results(proximity_results, exponential_results):
    """Print detailed comparison results"""
    print(f"\n{'='*80}")
    print("📊 演算法性能比較結果 (Algorithm Performance Comparison Results)")
    print(f"{'='*80}")
    
    # Results table
    print(f"\n{'指標 (Metric)':<25} {'基於鄰近性':<15} {'指數距離':<15} {'差異 (Diff)':<15}")
    print("-" * 75)
    
    # Success rate
    prox_success = proximity_results['success_rate'] * 100
    exp_success = exponential_results['success_rate'] * 100
    success_diff = exp_success - prox_success
    print(f"{'成功率 (Success Rate %)':<25} {prox_success:<15.1f} {exp_success:<15.1f} {success_diff:+.1f}")
    
    # Average steps
    prox_steps = proximity_results['avg_steps']
    exp_steps = exponential_results['avg_steps']
    steps_diff = exp_steps - prox_steps
    print(f"{'平均步數 (Avg Steps)':<25} {prox_steps:<15.1f} {exp_steps:<15.1f} {steps_diff:+.1f}")
    
    # Path efficiency
    prox_eff = proximity_results['avg_efficiency'] * 100
    exp_eff = exponential_results['avg_efficiency'] * 100
    eff_diff = exp_eff - prox_eff
    print(f"{'路徑效率 (Path Eff %)':<25} {prox_eff:<15.1f} {exp_eff:<15.1f} {eff_diff:+.1f}")
    
    # Computation time
    prox_time = proximity_results['avg_computation_time'] * 1000
    exp_time = exponential_results['avg_computation_time'] * 1000
    time_diff = exp_time - prox_time
    print(f"{'計算時間 (Comp Time ms)':<25} {prox_time:<15.1f} {exp_time:<15.1f} {time_diff:+.1f}")
    
    # Average reward
    prox_reward = proximity_results['avg_reward']
    exp_reward = exponential_results['avg_reward']
    reward_diff = exp_reward - prox_reward
    print(f"{'平均獎勵 (Avg Reward)':<25} {prox_reward:<15.1f} {exp_reward:<15.1f} {reward_diff:+.1f}")
    
    print("\n" + "="*80)
    print("📈 分析結果 (Analysis Results)")
    print("="*80)
    
    # Analysis
    print("\n🎯 基於鄰近性演算法 (Proximity-Based Algorithm):")
    if prox_success > exp_success:
        print("  ✅ 更高的成功率")
    if prox_steps < exp_steps:
        print("  ✅ 更少的平均步數")
    if prox_time < exp_time:
        print("  ✅ 更快的計算速度")
    if prox_eff > exp_eff:
        print("  ✅ 更高的路徑效率")
    
    print("\n📈 指數距離演算法 (Exponential Distance Algorithm):")
    if exp_success > prox_success:
        print("  ✅ 更高的成功率")
    if exp_steps < prox_steps:
        print("  ✅ 更少的平均步數")
    if exp_time < prox_time:
        print("  ✅ 更快的計算速度")
    if exp_eff > prox_eff:
        print("  ✅ 更高的路徑效率")
    
    print(f"\n💡 建議 (Recommendations):")
    
    if prox_success > exp_success and prox_time < exp_time:
        print("  • 對於一般應用，建議使用基於鄰近性的演算法")
        print("  • For general applications, recommend Proximity-Based Algorithm")
    elif exp_success > prox_success and exp_eff > prox_eff:
        print("  • 對於需要高精度的應用，建議使用指數距離演算法")
        print("  • For high-precision applications, recommend Exponential Distance Algorithm")
    else:
        print("  • 兩種演算法各有優勢，根據具體需求選擇")
        print("  • Both algorithms have advantages, choose based on specific requirements")

def main():
    """Main test function"""
    print("🚀 演算法性能比較測試 (Algorithm Performance Comparison Test)")
    print("=" * 80)
    
    # Test parameters
    num_episodes = 30  # Reduced for faster testing
    max_steps = 150
    
    print(f"測試參數 (Test Parameters):")
    print(f"  • 測試集數 Episodes: {num_episodes}")
    print(f"  • 最大步數 Max Steps: {max_steps}")
    print(f"  • 地圖大小 Grid Size: 15x15")
    
    try:
        # Test Proximity-Based Algorithm
        proximity_results = run_algorithm_test(
            "基於鄰近性演算法 (Proximity-Based)", 
            "proximity_based", 
            num_episodes, 
            max_steps
        )
        
        # Test Exponential Distance Algorithm  
        exponential_results = run_algorithm_test(
            "指數距離演算法 (Exponential Distance)", 
            "exponential_distance", 
            num_episodes, 
            max_steps
        )
        
        # Print comparison results
        print_comparison_results(proximity_results, exponential_results)
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤 (Error during testing): {str(e)}")
        return 1
    
    print(f"\n✅ 測試完成 (Testing Complete)")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
