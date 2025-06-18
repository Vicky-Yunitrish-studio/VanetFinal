#!/usr/bin/env python3
"""
Simple test script to verify UI functionality
"""
import tkinter as tk
from simulation_controller import SimulationController

def test_ui():
    """Test the UI with all features"""
    print("Testing UI with all congestion adjustment features...")
    
    # Create controller without agent (it will prompt to create new one)
    controller = SimulationController(None)
    
    print("UI initialized successfully!")
    print("Features available:")
    print("- Q-Learning parameter adjustment")
    print("- Obstacle placement mode")
    print("- Congestion adjustment mode")
    print("- All buttons should be in English")
    
    # Start the main loop
    controller.run()

if __name__ == "__main__":
    test_ui()
