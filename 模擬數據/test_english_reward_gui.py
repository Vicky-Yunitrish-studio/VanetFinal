#!/usr/bin/env python3
"""
Test script for English Reward Configuration GUI

This script demonstrates the English version of the reward configuration GUI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from UI.simulation_controller import SimulationController
from algorithm.agent import QLearningAgent
from module.urban_grid import UrbanGrid
from reward_config import RewardConfig

def main():
    """Main function - Launch English Reward Configuration GUI"""
    print("=== English Reward Configuration GUI Test ===")
    print()
    print("This program will launch a simulation controller with English reward configuration interface.")
    print()
    print("Features:")
    print("1. 🎯 Basic Rewards - Adjust step penalty, destination reward, etc.")
    print("2. 🚫 Movement Penalties - Adjust congestion penalty, backtrack penalty, etc.")
    print("3. ⚙️  Advanced Settings - Adjust loop detection, proximity rewards, etc.")
    print("4. 📋 Preset Configurations - Quickly load Aggressive, Cautious, or Balanced presets")
    print("5. 💾 Real-time Application - Apply settings immediately to simulation")
    print()
    print("Instructions:")
    print("1. After startup, you'll see a simulation controller window")
    print("2. Look for the 'Reward Configuration' section")
    print("3. There are three tabs for different types of reward adjustments")
    print("4. Modify values and click 'Apply Reward Config'")
    print("5. Use 'Load Preset' to quickly load predefined configurations")
    print("6. Start simulation to test the effects")
    print()
    
    try:
        # Create basic components
        print("🔧 Initializing simulation environment...")
        grid = UrbanGrid(size=15)  # Use medium-sized grid
        agent = QLearningAgent(grid)
        
        print("✅ Environment initialization complete")
        print("🚀 Launching GUI...")
        
        # Create simulation controller (automatically includes reward configuration GUI)
        controller = SimulationController(trained_agent=agent)
        
        print()
        print("📖 GUI Usage Tips:")
        print("   • Reward configuration is in the middle section of the main window")
        print("   • Three tabs correspond to different types of settings")
        print("   • Values can be positive (rewards) or negative (penalties)")
        print("   • Remember to click 'Apply Reward Config' after modifications")
        print("   • You can 'Reset to Defaults' anytime to restore default values")
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
