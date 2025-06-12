#!/usr/bin/env python3
"""
Quick test script for path visualization improvements
"""

import pickle
import tkinter as tk
from simulation_controller import SimulationController

def test_path_visualization():
    """Test the path visualization with existing trained agent"""
    
    try:
        # Try loading existing trained agent
        with open('v1.pkl', 'rb') as f:
            trained_agent = pickle.load(f)
        print("Loaded existing trained agent successfully!")
        
        # Create simulation controller with the trained agent
        controller = SimulationController(trained_agent)
        
        # Add some manual obstacles and congestion for testing
        controller.grid.obstacles[5, 5] = True
        controller.grid.obstacles[6, 5] = True
        controller.grid.obstacles[7, 5] = True
        
        # Add some congestion areas
        for i in range(8, 12):
            for j in range(8, 12):
                controller.grid.congestion[i, j] = 0.7
        
        print("\nPath Visualization Test:")
        print("- Light blue dotted lines (right offset) = Optimal A* paths")
        print("- Green dotted lines (left offset) = Actual paths taken")
        print("- The lines should now be clearly separated")
        print("\nClick 'Start Simulation' to see the improved path visualization!")
        
        # Start the GUI
        controller.start_gui()
        
    except FileNotFoundError:
        print("No trained agent found (v1.pkl). Please run training first:")
        print("python main.py")
    except Exception as e:
        print(f"Error loading agent: {e}")

if __name__ == "__main__":
    test_path_visualization()
