#!/usr/bin/env python3
"""
演算法參數實際使用示例
Algorithm Parameters Usage Examples

這個腳本展示如何在您的車輛導航系統中獲取、使用和調整各種演算法參數
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithm.agent import QLearningAgent
from module.urban_grid import UrbanGrid
from vehicle import Vehicle
from algorithm.reward_config import RewardConfig

def demonstrate_parameter_sources():
    """演示各種參數的來源和使用方法"""
    print("🔧 演算法參數來源和使用示例")
    print("=" * 60)
    
    # 1. 創建基礎環境
    print("\n📍 1. 環境和Agent參數")
    print("-" * 30)
    
    grid = UrbanGrid(size=20)
    agent = QLearningAgent(
        urban_grid=grid,
        learning_rate=0.2,    # α - 學習率
        discount_factor=0.95, # γ - 折扣因子  
        epsilon=0.2           # ε - 探索率
    )
    
    print(f"🧠 Agent參數來源 (agent.py):")
    print(f"   α (學習率): {agent.learning_rate}")
    print(f"   γ (折扣因子): {agent.discount_factor}")
    print(f"   ε (探索率): {agent.epsilon}")
    print(f"   動作空間: {agent.actions}")
    print(f"   Q表大小: {len(agent.q_table)} 個狀態")
    
    # 2. 獎勵配置參數
    print("\n💰 2. 獎勵配置參數")
    print("-" * 30)
    
    reward_config = RewardConfig()
    print(f"📊 獎勵參數來源 (reward_config.py):")
    print(f"   演算法類型: {reward_config.algorithm}")
    print(f"   步數懲罰: {reward_config.step_penalty}")
    print(f"   到達獎勵: {reward_config.destination_reached_reward}")
    print(f"   A*跟隨獎勵: {reward_config.astar_follow_reward}")
    print(f"   距離改善獎勵: {reward_config.closer_to_destination_reward}")
    
    # 指數距離演算法專用參數
    print(f"\n📈 指數距離演算法參數:")
    print(f"   基礎獎勵: {reward_config.exp_base_reward}")
    print(f"   振幅: {reward_config.exp_amplitude}")
    print(f"   X縮放: {reward_config.exp_x_scale}")
    print(f"   Y縮放: {reward_config.exp_y_scale}")
    
    # 3. 車輛和狀態參數
    print("\n🚗 3. 車輛狀態參數")
    print("-" * 30)
    
    vehicle = Vehicle(
        urban_grid=grid,
        agent=agent,
        position=(5, 5),
        destination=(15, 15),
        reward_config=reward_config
    )
    
    print(f"📍 車輛狀態來源 (vehicle.py):")
    print(f"   當前位置: {vehicle.position}")
    print(f"   目標位置: {vehicle.destination}")
    print(f"   最優路徑長度: {len(vehicle.optimal_path) if vehicle.optimal_path else 0}")
    print(f"   總步數: {vehicle.steps}")
    print(f"   總獎勵: {vehicle.total_reward}")
    
    # 4. 演示狀態和動作的計算
    print("\n🎯 4. 狀態和動作計算過程")
    print("-" * 30)
    
    # 獲取當前狀態
    congestion_level = grid.get_congestion_window(vehicle.position[0], vehicle.position[1])
    state = agent.get_state_key(vehicle.position, congestion_level)
    
    print(f"🔍 狀態計算:")
    print(f"   位置: {vehicle.position}")
    print(f"   擁塞度: {congestion_level:.3f}")
    print(f"   狀態Key: '{state}'")
    
    # 選擇動作
    action_idx = agent.choose_action(state, vehicle.position)
    dx, dy = agent.actions[action_idx]
    new_position = (vehicle.position[0] + dx, vehicle.position[1] + dy)
    
    print(f"\n🎮 動作選擇:")
    print(f"   動作索引: {action_idx}")
    print(f"   動作向量: ({dx}, {dy})")
    print(f"   新位置: {new_position}")
    
    # 5. 獎勵計算示例
    print("\n💎 5. 獎勵計算詳解")
    print("-" * 30)
    
    reward = vehicle.calculate_reward(new_position, dx, dy)
    print(f"🏆 獎勵計算結果: {reward:.2f}")
    
    print(f"\n📋 獎勵組成分析:")
    print(f"   基礎步數懲罰: {reward_config.step_penalty}")
    
    # 檢查是否跟隨A*路徑
    if vehicle.optimal_path and len(vehicle.optimal_path) > 1:
        next_optimal = vehicle.optimal_path[1]
        if new_position == next_optimal:
            print(f"   A*路徑跟隨獎勵: +{reward_config.astar_follow_reward}")
        elif new_position in vehicle.optimal_path:
            print(f"   A*路徑上獎勵: +{reward_config.astar_on_path_reward}")
    
    # 檢查距離改善
    from algorithm.astar import manhattan_distance
    current_dist = manhattan_distance(vehicle.position, vehicle.destination)
    new_dist = manhattan_distance(new_position, vehicle.destination)
    if new_dist < current_dist:
        print(f"   距離改善獎勵: +{reward_config.closer_to_destination_reward}")
    
    return agent, vehicle, reward_config

def demonstrate_parameter_adjustment():
    """演示如何調整參數"""
    print("\n\n⚙️ 參數調整示例")
    print("=" * 60)
    
    grid = UrbanGrid(size=15)
    
    # 1. 創建不同配置的Agent
    print("\n🔧 1. Agent參數調整")
    print("-" * 30)
    
    configs = [
        {"name": "保守型", "lr": 0.1, "df": 0.99, "eps": 0.05},
        {"name": "平衡型", "lr": 0.2, "df": 0.95, "eps": 0.20},
        {"name": "激進型", "lr": 0.4, "df": 0.90, "eps": 0.50}
    ]
    
    for config in configs:
        agent = QLearningAgent(
            urban_grid=grid,
            learning_rate=config["lr"],
            discount_factor=config["df"],
            epsilon=config["eps"]
        )
        print(f"📊 {config['name']}配置:")
        print(f"   學習率: {agent.learning_rate} (學習{'快' if agent.learning_rate > 0.3 else '慢'})")
        print(f"   折扣因子: {agent.discount_factor} ({'重視長期' if agent.discount_factor > 0.95 else '重視短期'})")
        print(f"   探索率: {agent.epsilon} ({'高探索' if agent.epsilon > 0.3 else '低探索'})")
    
    # 2. 獎勵配置調整
    print("\n💰 2. 獎勵配置調整")
    print("-" * 30)
    
    reward_configs = [
        {
            "name": "謹慎導航",
            "step_penalty": -0.5,
            "destination_reward": 50,
            "astar_follow": 5
        },
        {
            "name": "標準導航", 
            "step_penalty": -1,
            "destination_reward": 100,
            "astar_follow": 10
        },
        {
            "name": "激進導航",
            "step_penalty": -2,
            "destination_reward": 200,
            "astar_follow": 20
        }
    ]
    
    for config in reward_configs:
        reward_config = RewardConfig()
        reward_config.update_config(
            step_penalty=config["step_penalty"],
            destination_reached_reward=config["destination_reward"],
            astar_follow_reward=config["astar_follow"]
        )
        
        print(f"🎯 {config['name']}:")
        print(f"   步數成本: {reward_config.step_penalty}")
        print(f"   到達獎勵: {reward_config.destination_reached_reward}")
        print(f"   路徑跟隨: {reward_config.astar_follow_reward}")
    
    # 3. 演算法切換示例
    print("\n🔄 3. 演算法切換")
    print("-" * 30)
    
    algorithms = ["proximity_based", "exponential_distance"]
    
    for algo in algorithms:
        reward_config = RewardConfig()
        reward_config.set_algorithm_type(algo)
        
        print(f"📈 {algo.replace('_', ' ').title()}:")
        print(f"   演算法類型: {reward_config.get_algorithm_type()}")
        
        if algo == "exponential_distance":
            exp_config = reward_config.get_exponential_distance_config()
            print(f"   指數參數: 基礎={exp_config['base_reward']}, "
                  f"振幅={exp_config['multiplier']}, "
                  f"縮放=({exp_config['x_scale']}, {exp_config['y_scale']})")

def demonstrate_q_learning_update():
    """演示Q-Learning更新過程"""
    print("\n\n🧠 Q-Learning更新過程詳解")
    print("=" * 60)
    
    grid = UrbanGrid(size=10)
    agent = QLearningAgent(grid)
    
    # 模擬一次Q值更新
    state = "5_5_0.20"  # 位置(5,5)，擁塞度0.20
    action = 1  # 向右移動
    reward = 8.5  # 獲得的獎勵
    next_state = "6_5_0.15"  # 新位置(6,5)，擁塞度0.15
    
    print(f"📍 更新前狀態:")
    print(f"   當前狀態: {state}")
    print(f"   執行動作: {action} ({['上','右','下','左'][action]})")
    print(f"   獲得獎勵: {reward}")
    print(f"   下一狀態: {next_state}")
    
    # 獲取更新前的Q值
    old_q_value = agent.q_table[state][action]
    max_next_q = max(agent.q_table[next_state])
    
    print(f"\n🔢 Q值計算:")
    print(f"   舊Q值 Q(s,a): {old_q_value:.3f}")
    print(f"   最大下一Q值 max Q(s',a'): {max_next_q:.3f}")
    print(f"   學習率 α: {agent.learning_rate}")
    print(f"   折扣因子 γ: {agent.discount_factor}")
    
    # 計算目標值
    target = reward + agent.discount_factor * max_next_q
    td_error = target - old_q_value
    
    print(f"\n📊 計算過程:")
    print(f"   目標值 = r + γ × max Q(s',a')")
    print(f"          = {reward} + {agent.discount_factor} × {max_next_q:.3f}")
    print(f"          = {target:.3f}")
    print(f"   TD誤差 = 目標值 - 舊Q值")
    print(f"          = {target:.3f} - {old_q_value:.3f}")
    print(f"          = {td_error:.3f}")
    
    # 執行Q值更新
    agent.update_q_table(state, action, reward, next_state)
    new_q_value = agent.q_table[state][action]
    
    print(f"\n✅ 更新結果:")
    print(f"   新Q值 = 舊Q值 + α × TD誤差")
    print(f"         = {old_q_value:.3f} + {agent.learning_rate} × {td_error:.3f}")
    print(f"         = {new_q_value:.3f}")
    print(f"   Q值變化: {new_q_value - old_q_value:+.3f}")

def main():
    """主函數 - 執行所有演示"""
    print("🚗 車輛導航系統參數詳解演示")
    print("=" * 80)
    
    try:
        # 基本參數演示
        agent, vehicle, reward_config = demonstrate_parameter_sources()
        
        # 參數調整演示
        demonstrate_parameter_adjustment()
        
        # Q-Learning更新演示
        demonstrate_q_learning_update()
        
        print(f"\n\n💡 總結")
        print("=" * 80)
        print("📖 參數來源對照:")
        print("   • α, γ, ε → agent.py (QLearningAgent類)")
        print("   • 獎勵參數 → reward_config.py (RewardConfig類)")
        print("   • 狀態 s → vehicle.py (位置+擁塞度)")
        print("   • 動作 a → agent.py (0=上, 1=右, 2=下, 3=左)")
        print("   • 獎勵 r → vehicle.calculate_reward()")
        print("")
        print("🔧 調整方法:")
        print("   • GUI: 模擬控制器中的參數輸入框")
        print("   • 程式: 創建Agent和RewardConfig時指定")
        print("   • 動態: 運行時修改agent.learning_rate等屬性")
        print("")
        print("🎯 這些參數控制了車輛的學習行為和導航策略！")
        
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        print("請確保所有必要的模組都已正確導入")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
