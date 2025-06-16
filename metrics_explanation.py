#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三個性能指標的直觀比較
"""

def explain_metrics_with_examples():
    print("=== 三個性能指標詳細解釋 ===")
    print()
    
    print("🎯 1. 成功率 (Success Rate)")
    print("   意義: 車輛能否到達目標")
    print("   公式: 成功次數 ÷ 總測試次數 × 100%")
    print()
    print("   實例對比:")
    print("   演算法A: 100次測試中，95次成功 → 成功率 95%")
    print("   演算法B: 100次測試中，85次成功 → 成功率 85%")
    print("   結論: 演算法A更可靠！")
    print()
    
    print("🚶 2. 平均步數 (Average Steps)")
    print("   意義: 車輛到達目標需要多少步")
    print("   公式: 所有成功任務總步數 ÷ 成功任務數")
    print()
    print("   實例對比:")
    print("   演算法A: 平均需要25步到達目標")
    print("   演算法B: 平均需要35步到達目標")
    print("   結論: 演算法A更快速！")
    print()
    
    print("📏 3. 路徑效率 (Path Efficiency)")
    print("   意義: 實際路徑與最優路徑的接近程度")
    print("   公式: 最短路徑長度 ÷ 實際路徑長度 × 100%")
    print()
    print("   實例對比:")
    print("   從(0,0)到(5,5)最短需要10步:")
    print("   演算法A: 實際走了12步 → 效率 = 10÷12 = 83.3%")
    print("   演算法B: 實際走了15步 → 效率 = 10÷15 = 66.7%")
    print("   結論: 演算法A路徑更優！")
    print()
    
    print("=" * 50)
    print("🔄 三個指標的關係")
    print("=" * 50)
    print()
    
    print("情境1: 保守型演算法")
    print("  ✅ 成功率: 很高 (95%+)")
    print("  ⚠️  平均步數: 較多 (保守策略)")
    print("  🔄 路徑效率: 中等 (不夠優化)")
    print("  💭 特點: 穩定但效率不高")
    print()
    
    print("情境2: 激進型演算法")
    print("  ⚠️  成功率: 中等 (80-90%)")
    print("  ✅ 平均步數: 較少 (直接路徑)")
    print("  ✅ 路徑效率: 較高 (接近最優)")
    print("  💭 特點: 高效但可能不穩定")
    print()
    
    print("情境3: 理想型演算法")
    print("  ✅ 成功率: 高 (90%+)")
    print("  ✅ 平均步數: 少 (快速到達)")
    print("  ✅ 路徑效率: 高 (接近最優)")
    print("  💭 特點: 這是我們的目標！")
    print()
    
    print("=" * 50)
    print("💡 如何讀懂測試結果")
    print("=" * 50)
    print()
    
    print("1. 先看成功率:")
    print("   • >95%: 演算法很穩定")
    print("   • 85-95%: 演算法基本可用")
    print("   • <85%: 需要改進")
    print()
    
    print("2. 再看平均步數:")
    print("   • 與理論最短步數比較")
    print("   • 如果差距太大，說明有改進空間")
    print()
    
    print("3. 最後看路徑效率:")
    print("   • >80%: 路徑很優化")
    print("   • 60-80%: 路徑還可以")
    print("   • <60%: 路徑有問題")
    print()
    
    print("4. 綜合判斷:")
    print("   三個指標要平衡考慮，不能只看單一指標")
    print("   最理想的演算法是三個指標都優秀")

if __name__ == "__main__":
    explain_metrics_with_examples()
