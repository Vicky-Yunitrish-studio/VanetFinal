"""
Main module for Q-Learning Urban Traffic Simulation
This file serves as the entry point for the simulation.
"""
from simulation import run_simulation, test_incident_response

if __name__ == "__main__":
    # 設定是否顯示圖表
    show_plots = True  # 將此變數設為 False 可暫時關閉所有圖表顯示
    
    # Train the agent
    print("Training Q-Learning agent...")
    trained_agent = run_simulation(episodes=200, visualize_interval=50, show_plots=show_plots, max_steps=2000)
    
    # Test incident response
    print("\nTesting incident response...")
    test_incident_response(trained_agent, show_plot=show_plots, num_tests=10)