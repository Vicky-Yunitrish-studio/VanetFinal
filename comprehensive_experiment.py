#!/usr/bin/env python3
"""
大規模綜合實驗類
用於運行一萬次實驗的核心實驗類
"""

import time
import json
import numpy as np
from datetime import datetime
from algorithm.agent import QLearningAgent
from module.urban_grid import UrbanGrid
from vehicle import Vehicle
from algorithm.reward_config import RewardConfig


class ComprehensiveExperiment:
    """綜合實驗類，支持大規模實驗運行"""
    
    def __init__(self, grid_size=20):
        """初始化實驗環境
        
        Args:
            grid_size: 網格大小
        """
        self.grid_size = grid_size
        self.results = []
        
    def run_single_experiment(self, algorithm_type, obstacle_density, congestion_level, 
                            num_episodes=10000, max_steps=300):
        """運行單個實驗配置
        
        Args:
            algorithm_type: 演算法類型 ('proximity_based' 或 'exponential_distance')
            obstacle_density: 障礙物密度 (0.1, 0.25 等)
            congestion_level: 壅塞程度 ('low' 或 'high')
            num_episodes: 實驗回合數
            max_steps: 每回合最大步數
            
        Returns:
            實驗結果字典
        """
        print(f"🧪 開始實驗: {algorithm_type}, 密度{obstacle_density}, 壅塞{congestion_level}")
        print(f"📊 回合數: {num_episodes}, 最大步數: {max_steps}")
        
        # 設置獎勵配置
        reward_config = RewardConfig()
        reward_config.set_algorithm_type(algorithm_type)
        
        # 根據演算法類型調整參數
        if algorithm_type == "exponential_distance":
            reward_config.update_config(
                exp_base_reward=-1,
                exp_amplitude=40,
                exp_x_scale=1.5,
                exp_y_scale=2.0,
                step_penalty=0  # 由指數函數處理
            )
        
        # 創建環境
        urban_grid = UrbanGrid(size=self.grid_size)
        
        # 設置障礙物密度
        num_obstacles = int(obstacle_density * self.grid_size * self.grid_size)
        np.random.seed(42)  # 保證可重現性
        for _ in range(num_obstacles):
            x, y = np.random.randint(0, self.grid_size, 2)
            urban_grid.add_obstacle(x, y)
        
        # 設置壅塞程度
        if congestion_level == 'high':
            urban_grid.congestion = np.random.uniform(0.3, 0.8, size=(self.grid_size, self.grid_size))
        else:  # low
            urban_grid.congestion = np.random.uniform(0.0, 0.3, size=(self.grid_size, self.grid_size))
        
        # 創建代理
        agent = QLearningAgent(urban_grid, learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
        
        # 實驗統計
        success_count = 0
        total_steps = 0
        total_rewards = 0
        path_lengths = []
        computation_times = []
        
        # 進度顯示間隔
        progress_interval = max(1, num_episodes // 20)  # 每5%顯示一次
        
        start_time = time.time()
        
        for episode in range(num_episodes):
            # 隨機設置起點和終點
            start_pos = self._get_random_valid_position(urban_grid)
            end_pos = self._get_random_valid_position(urban_grid)
            
            # 確保起點和終點不同
            while start_pos == end_pos:
                end_pos = self._get_random_valid_position(urban_grid)
            
            # 創建車輛
            vehicle = Vehicle(urban_grid, agent, reward_config=reward_config)
            vehicle.position = start_pos
            vehicle.destination = end_pos
            vehicle.path = [start_pos]
            
            # 運行單回合
            episode_start_time = time.time()
            success, steps, total_reward = self._run_single_episode(
                vehicle, agent, urban_grid, max_steps
            )
            episode_time = time.time() - episode_start_time
            
            # 統計結果
            if success:
                success_count += 1
                path_lengths.append(steps)
            
            total_steps += steps
            total_rewards += total_reward
            computation_times.append(episode_time * 1000)  # 轉換為毫秒
            
            # 進度顯示
            if (episode + 1) % progress_interval == 0:
                progress = (episode + 1) / num_episodes * 100
                current_success_rate = success_count / (episode + 1)
                print(f"進度: {progress:.1f}% ({episode + 1}/{num_episodes}), "
                      f"成功率: {current_success_rate:.3f}")
        
        experiment_time = time.time() - start_time
        
        # 計算最終統計
        success_rate = success_count / num_episodes
        avg_steps = total_steps / num_episodes
        avg_reward = total_rewards / num_episodes
        avg_computation_time = np.mean(computation_times)
        
        # 路徑效率計算 (成功案例的平均步數 vs 理論最短路徑)
        if path_lengths:
            avg_successful_steps = np.mean(path_lengths)
            # 簡化的效率估算 (實際應該用A*計算最短路徑)
            estimated_optimal_steps = self.grid_size * 0.6  # 粗略估算
            path_efficiency = estimated_optimal_steps / avg_successful_steps if avg_successful_steps > 0 else 0
        else:
            path_efficiency = 0
        
        result = {
            'algorithm_type': algorithm_type,
            'obstacle_density': obstacle_density,
            'congestion_level': congestion_level,
            'num_episodes': num_episodes,
            'success_rate': success_rate,
            'avg_steps': avg_steps,
            'avg_reward': avg_reward,
            'path_efficiency': path_efficiency,
            'avg_computation_time': avg_computation_time,
            'experiment_time': experiment_time,
            'successful_episodes': success_count,
            'total_steps': total_steps,
            'total_rewards': total_rewards
        }
        
        print(f"✅ 實驗完成:")
        print(f"   成功率: {success_rate:.4f}")
        print(f"   平均步數: {avg_steps:.2f}")
        print(f"   平均獎勵: {avg_reward:.2f}")
        print(f"   路徑效率: {path_efficiency:.4f}")
        print(f"   平均計算時間: {avg_computation_time:.2f}ms")
        print(f"   實驗總時間: {experiment_time/60:.1f}分鐘")
        
        return result
    
    def _get_random_valid_position(self, urban_grid):
        """獲取隨機有效位置（不在障礙物上）"""
        while True:
            x, y = np.random.randint(0, urban_grid.size, 2)
            if not urban_grid.obstacles[x, y]:
                return (x, y)
    
    def _run_single_episode(self, vehicle, agent, urban_grid, max_steps):
        """運行單個回合
        
        Returns:
            (success, steps, total_reward)
        """
        # 設置代理的目標位置（用於狀態計算）
        agent.current_destination = vehicle.destination
        
        total_reward = 0
        steps = 0
        
        for step in range(max_steps):
            # 檢查是否到達目標
            if vehicle.position == vehicle.destination or vehicle.reached:
                return True, steps, total_reward
            
            # 車輛移動（包含狀態、動作、獎勵、Q表更新）
            reward = vehicle.move()
            
            total_reward += reward
            steps += 1
            
            # 更新環境
            urban_grid.update_traffic_lights()
            urban_grid.update_congestion([vehicle.position])
        
        # 未在最大步數內到達
        return False, steps, total_reward
    
    def analyze_results(self):
        """分析實驗結果"""
        if not self.results:
            return {}
        
        analysis = {
            'total_experiments': len(self.results),
            'overall_success_rate': np.mean([r['success_rate'] for r in self.results]),
            'overall_avg_steps': np.mean([r['avg_steps'] for r in self.results]),
            'overall_avg_reward': np.mean([r['avg_reward'] for r in self.results]),
            'overall_path_efficiency': np.mean([r['path_efficiency'] for r in self.results]),
            'overall_avg_computation_time': np.mean([r['avg_computation_time'] for r in self.results]),
            'by_algorithm': {},
            'by_density': {},
            'by_congestion': {}
        }
        
        # 按演算法分析
        algorithms = set(r['algorithm_type'] for r in self.results)
        for algo in algorithms:
            algo_results = [r for r in self.results if r['algorithm_type'] == algo]
            analysis['by_algorithm'][algo] = {
                'success_rate': np.mean([r['success_rate'] for r in algo_results]),
                'avg_steps': np.mean([r['avg_steps'] for r in algo_results]),
                'avg_reward': np.mean([r['avg_reward'] for r in algo_results]),
                'path_efficiency': np.mean([r['path_efficiency'] for r in algo_results]),
                'avg_computation_time': np.mean([r['avg_computation_time'] for r in algo_results])
            }
        
        # 按密度分析
        densities = set(r['obstacle_density'] for r in self.results)
        for density in densities:
            density_results = [r for r in self.results if r['obstacle_density'] == density]
            analysis['by_density'][density] = {
                'success_rate': np.mean([r['success_rate'] for r in density_results]),
                'avg_steps': np.mean([r['avg_steps'] for r in density_results]),
                'avg_reward': np.mean([r['avg_reward'] for r in density_results])
            }
        
        # 按壅塞程度分析
        congestion_levels = set(r['congestion_level'] for r in self.results)
        for level in congestion_levels:
            level_results = [r for r in self.results if r['congestion_level'] == level]
            analysis['by_congestion'][level] = {
                'success_rate': np.mean([r['success_rate'] for r in level_results]),
                'avg_steps': np.mean([r['avg_steps'] for r in level_results]),
                'avg_reward': np.mean([r['avg_reward'] for r in level_results])
            }
        
        return analysis
    
    def save_results(self, analysis=None):
        """保存實驗結果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存原始結果
        results_filename = f'experiment_results_{timestamp}.json'
        with open(results_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # 保存分析結果
        if analysis:
            analysis_filename = f'experiment_analysis_{timestamp}.json'
            with open(analysis_filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # 保存CSV格式結果
        csv_filename = f'experiment_results_{timestamp}.csv'
        with open(csv_filename, 'w', encoding='utf-8') as f:
            # 寫入標題
            f.write('algorithm_type,obstacle_density,congestion_level,success_rate,avg_steps,avg_reward,path_efficiency,avg_computation_time\n')
            
            # 寫入數據
            for result in self.results:
                f.write(f"{result['algorithm_type']},{result['obstacle_density']},{result['congestion_level']},"
                       f"{result['success_rate']:.6f},{result['avg_steps']:.4f},{result['avg_reward']:.4f},"
                       f"{result['path_efficiency']:.6f},{result['avg_computation_time']:.4f}\n")
        
        print(f"📁 結果已保存:")
        print(f"   JSON: {results_filename}")
        if analysis:
            print(f"   分析: {analysis_filename}")
        print(f"   CSV: {csv_filename}")
        
        return results_filename, analysis_filename if analysis else None, csv_filename


if __name__ == "__main__":
    # 測試實驗類
    print("🧪 測試 ComprehensiveExperiment 類")
    experiment = ComprehensiveExperiment(grid_size=10)
    
    # 運行小規模測試
    result = experiment.run_single_experiment(
        'proximity_based', 0.1, 'low', 
        num_episodes=100, max_steps=100
    )
    
    print("✅ 測試完成，實驗類正常運作")
