#!/usr/bin/env python3
"""
Test script for different reward algorithms

This script demonstrates the ability to switch between different reward algorithms
during simulation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from UI.simulation_controller import SimulationController
from algorithm.agent import QLearningAgent
from module.urban_grid import UrbanGrid
from algorithm.reward_config import RewardConfig

def main():
    """Main function - Test different reward algorithms"""
    print("=== Reward Algorithm Selection Test ===")
    print()
    print("This program will launch a simulation controller with algorithm selection capability.")
    print()
    print("Available Algorithms:")
    print("1. 🎯 Proximity Based - Original distance-based reward system")
    print("   - Uses linear and scaled proximity rewards")
    print("   - Good for general pathfinding")
    print()
    print("2. 📈 Exponential Distance - New exponential decay reward system")
    print("   - Formula: r = base_reward + amplitude × exp(-(|xi-xd|/x_scale + |yi-yd|/y_scale))")
    print("   - Better for fine-tuned destination approach")
    print("   - Configurable scale factors for x and y directions")
    print()
    print("Features:")
    print("• Algorithm selection dropdown in Reward Configuration section")
    print("• Exponential algorithm parameters in Advanced Settings tab")
    print("• Real-time algorithm switching during simulation")
    print("• Visual comparison of different approaches")
    print()
    
    try:
        # Create basic components
        print("🔧 Initializing simulation environment...")
        grid = UrbanGrid(size=15)
        agent = QLearningAgent(grid)
        
        print("✅ Environment initialization complete")
        print("🚀 Launching GUI with algorithm selection...")
        
        # Create simulation controller
        controller = SimulationController(trained_agent=agent)
        
        print()
        print("📖 Algorithm Selection Guide:")
        print("   • Find 'Algorithm:' dropdown in Reward Configuration section")
        print("   • Select between 'proximity_based' and 'exponential_distance'")
        print("   • Adjust algorithm-specific parameters in Advanced Settings tab")
        print("   • Click 'Apply Reward Config' to activate changes")
        print("   • Start simulation to compare behaviors")
        print()
        print("⚙️  Exponential Algorithm Parameters:")
        print("   • Base Reward: Usually negative (-1)")
        print("   • Amplitude: Positive multiplier (40)")
        print("   • X Scale Factor: X-direction scaling (1.5)")
        print("   • Y Scale Factor: Y-direction scaling (2.0)")
        print()
        print("🎮 Starting GUI...")
        
        # Launch GUI main loop
        controller.run()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please ensure all required modules are properly installed")
        return 1
    
    print("👋 Program ended")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
