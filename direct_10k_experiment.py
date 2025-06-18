#!/usr/bin/env python3
"""
直接運行一萬回合實驗 - 無需確認
"""

import time
import json
import sys
from datetime import datetime

# 確保可以導入模組
sys.path.insert(0, '/home/yunitrish/workspace/School/hw/final')

from comprehensive_experiment import ComprehensiveExperiment

def main():
    print("🚀 一萬回合大規模實驗開始")
    print(f"開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
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
    
    start_time = time.time()
    
    for i, (algorithm, density, congestion) in enumerate(configs, 1):
        config_start = time.time()
        print(f"\n📊 配置 {i}/8: {algorithm}")
        print(f"   障礙物密度: {density}, 壅塞: {congestion}")
        print(f"   開始時間: {datetime.now().strftime('%H:%M:%S')}")
        
        result = experiment.run_single_experiment(
            algorithm, density, congestion,
            num_episodes=10000, max_steps=300
        )
        
        config_time = time.time() - config_start
        experiment.results.append(result)
        
        print(f"✅ 配置 {i} 完成!")
        print(f"   成功率: {result['success_rate']:.4f}")
        print(f"   平均步數: {result['avg_steps']:.1f}")
        print(f"   路徑效率: {result['avg_path_efficiency']:.4f}")
        print(f"   耗時: {config_time/60:.1f}分鐘")
        
        # 保存中間結果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'results_after_config_{i}_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(experiment.results, f, indent=2, ensure_ascii=False)
        print(f"   💾 已保存: {filename}")
    
    # 最終分析
    print("\n📈 開始最終分析...")
    final_results = experiment.analyze_results()
    final_file = experiment.save_results(final_results)
    
    total_time = time.time() - start_time
    print(f"\n🎉 所有實驗完成!")
    print(f"總耗時: {total_time/3600:.2f}小時")
    print(f"總回合數: 80,000")
    print(f"最終結果: {final_file}")

if __name__ == "__main__":
    main()
