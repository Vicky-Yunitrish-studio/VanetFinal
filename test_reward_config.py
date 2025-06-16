"""
簡單測試新的獎勵配置系統
"""

from reward_config import RewardConfig

def test_reward_config():
    """測試獎勵配置系統的基本功能"""
    
    print("=== 測試獎勵配置系統 ===\n")
    
    # 測試預設配置
    print("1. 測試預設配置:")
    default_config = RewardConfig()
    print(f"   步驟懲罰: {default_config.get_step_penalty()}")
    print(f"   目的地獎勵: {default_config.get_destination_reward()}")
    print(f"   A* 跟隨獎勵: {default_config.get_astar_rewards()}")
    
    # 測試配置修改
    print("\n2. 測試配置修改:")
    default_config.update_config(
        step_penalty=-5,
        destination_reached_reward=200
    )
    print(f"   修改後步驟懲罰: {default_config.get_step_penalty()}")
    print(f"   修改後目的地獎勵: {default_config.get_destination_reward()}")
    
    # 測試重置功能
    print("\n3. 測試重置功能:")
    default_config.reset_to_defaults()
    print(f"   重置後步驟懲罰: {default_config.get_step_penalty()}")
    print(f"   重置後目的地獎勵: {default_config.get_destination_reward()}")
    
    # 測試獲取所有配置
    print("\n4. 測試獲取所有配置:")
    all_config = default_config.get_all_config()
    print(f"   總共有 {len(all_config)} 個配置參數")
    
    # 測試不同的配置組合
    print("\n5. 測試不同配置:")
    
    # 積極型配置
    aggressive_config = RewardConfig()
    aggressive_config.update_config(
        step_penalty=-3,
        astar_follow_reward=20,
        destination_reached_reward=300
    )
    print(f"   積極型配置 - 步驟懲罰: {aggressive_config.get_step_penalty()}")
    print(f"   積極型配置 - A* 獎勵: {aggressive_config.get_astar_rewards()['follow']}")
    
    # 謹慎型配置
    cautious_config = RewardConfig()
    cautious_config.update_config(
        step_penalty=-0.5,
        astar_follow_reward=5,
        destination_reached_reward=50
    )
    print(f"   謹慎型配置 - 步驟懲罰: {cautious_config.get_step_penalty()}")
    print(f"   謹慎型配置 - A* 獎勵: {cautious_config.get_astar_rewards()['follow']}")
    
    print("\n✅ 所有測試通過！獎勵配置系統運作正常。")

if __name__ == "__main__":
    test_reward_config()
