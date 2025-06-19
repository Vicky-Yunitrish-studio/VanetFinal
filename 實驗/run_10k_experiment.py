#!/usr/bin/env python3
"""
一萬回合實驗啟動器
"""

import time
import json
from datetime import datetime
from comprehensive_experiment import ComprehensiveExperiment

print("🚀 準備運行一萬回合大規模實驗")
print("📊 配置: 8個實驗配置，每個10,000回合")
print("⏱️  預估時間: 2-4小時")
print("="*50)

# 詢問用戶確認
print("實驗配置詳情:")
print("- 演算法: A*+Q-learning+鄰近性 vs 純指數型")
print("- 障礙物密度: 10%, 25%")
print("- 壅塞程度: 低, 高")
print("- 每配置回合數: 10,000")
print("- 總測試回合數: 80,000")

response = input("\n確定要開始實驗嗎？(y/N): ")
if response.lower() != 'y':
    print("實驗已取消")
    exit()

print("\n🚀 開始大規模實驗...")
start_time = datetime.now()

# 創建實驗實例
experiment = ComprehensiveExperiment(grid_size=20)

# 實驗配置
configs = [
    ('proximity_based', 0.10, 'low'),
    ('proximity_based', 0.10, 'high'),
    ('proximity_based', 0.25, 'low'),
    ('proximity_based', 0.25, 'high'),
    ('exponential_distance', 0.10, 'low'),
    ('exponential_distance', 0.10, 'high'),
    ('exponential_distance', 0.25, 'low'),
    ('exponential_distance', 0.25, 'high'),
]

results = []

for i, (algorithm, density, congestion) in enumerate(configs, 1):
    print(f"\n🧪 配置 {i}/{len(configs)}: {algorithm}, 密度{density}, 壅塞{congestion}")
    config_start = time.time()
    
    result = experiment.run_single_experiment(
        algorithm, density, congestion,
        num_episodes=10000, max_steps=300
    )
    
    results.append(result)
    config_time = time.time() - config_start
    
    print(f"✅ 配置完成，耗時: {config_time/60:.1f}分鐘")
    print(f"📊 成功率: {result['success_rate']:.4f}")
    
    # 保存中間結果
    if i % 2 == 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'intermediate_results_{i}_{timestamp}.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 中間結果已保存")

# 保存最終結果
experiment.results = results
final_results = experiment.analyze_results()
experiment.save_results(final_results)

end_time = datetime.now()
total_time = end_time - start_time

print(f"\n🎉 大規模實驗完成！")
print(f"⏱️  總耗時: {total_time}")
print("📊 詳細結果已保存")
