"""
Main module for Q-Learning Urban Traffic Simulation
This file serves as the entry point for the simulation.
"""
import argparse
import pickle
from simulation import run_simulation, test_incident_response
from simulation_controller import SimulationController

def train_mode(episodes=200, visualize_interval=50, show_plots=True, max_steps=2000, save_agent=True):
    """Training mode: Train a Q-learning agent"""
    print("Training Q-Learning agent...")
    trained_agent = run_simulation(episodes=episodes, 
                                   visualize_interval=visualize_interval, 
                                   show_plots=show_plots, 
                                   max_steps=max_steps)
    
    # Test incident response
    print("\nTesting incident response...")
    test_incident_response(trained_agent, show_plot=show_plots, num_tests=5)
    
    # Save trained agent
    if save_agent and trained_agent:
        try:
            with open("trained_agent.pkl", "wb") as f:
                pickle.dump(trained_agent, f)
            print("Trained agent saved to 'trained_agent.pkl'")
        except Exception as e:
            print(f"Error saving agent: {e}")
    
    return trained_agent

def simulate_mode(agent=None):
    """Simulation mode: Launch interactive simulation controller"""
    controller = SimulationController(agent)
    print("Starting interactive simulation controller...")
    controller.run()

if __name__ == "__main__":
    # 解析命令行參數
    parser = argparse.ArgumentParser(description="Q-Learning Urban Traffic Simulation")
    parser.add_argument("--mode", choices=["train", "simulate", "both"], default="both",
                      help="Choose mode: train, simulate, or both")
    parser.add_argument("--episodes", type=int, default=200,
                      help="Number of training episodes (train mode)")
    parser.add_argument("--no-plots", action="store_true",
                      help="Disable plot display during training")
    parser.add_argument("--no-save", action="store_true",
                      help="Don't save trained agent to file")
    args = parser.parse_args()
    
    # 設定是否顯示圖表
    show_plots = not args.no_plots
    
    trained_agent = None
    
    # 根據模式執行相應功能
    if args.mode == "train" or args.mode == "both":
        trained_agent = train_mode(
            episodes=args.episodes,
            visualize_interval=50,
            show_plots=show_plots,
            max_steps=2000,
            save_agent=not args.no_save
        )
    
    if args.mode == "simulate" or args.mode == "both":
        # 如果模式是只模擬，嘗試載入已訓練的代理
        if args.mode == "simulate" and not trained_agent:
            try:
                with open("trained_agent.pkl", "rb") as f:
                    trained_agent = pickle.load(f)
                print("Loaded existing trained agent")
            except FileNotFoundError:
                print("No saved agent found. Please train an agent first or create one in the simulation controller")
            except Exception as e:
                print(f"Error loading agent: {e}")
        
        simulate_mode(trained_agent)