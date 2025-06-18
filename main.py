"""
Main module for Q-Learning Urban Traffic Simulation
This file serves as the entry point for the simulation.
"""
import argparse
import pickle
from simulation import run_simulation, test_incident_response
from UI.simulation_controller import SimulationController

def train_mode(episodes=200, visualize_interval=50, show_plots=True, max_steps=2000, 
              save_agent=True, iterations=1, save_iterations=False, unlimited_steps=False):
    """Training mode: Train a Q-learning agent
    
    Args:
        episodes: Number of episodes per iteration
        visualize_interval: Interval for visualization (set to 0 to disable)
        show_plots: Whether to show plots during training
        max_steps: Maximum steps per episode (0 means unlimited, until all vehicles reach destination)
        save_agent: Whether to save the final agent
        iterations: Number of training iterations to run
        save_iterations: Whether to save intermediate agents after each iteration
        unlimited_steps: If True, ignore max_steps and run until all vehicles reach destination
    """
    # Adjust max_steps based on unlimited_steps parameter
    if unlimited_steps:
        max_steps = 0  # 0 means no step limit
    print(f"Training Q-Learning agent for {iterations} iterations of {episodes} episodes each...")
    
    # For the first iteration, create a new agent
    trained_agent = None
    
    for iteration in range(iterations):
        print(f"\n--- Iteration {iteration+1}/{iterations} ---")
        
        if iteration == 0 or not trained_agent:
            # First iteration: train from scratch
            trained_agent = run_simulation(episodes=episodes, 
                                          visualize_interval=visualize_interval, 
                                          show_plots=show_plots, 
                                          max_steps=max_steps)
        else:
            # Continue training the existing agent
            print(f"Continuing training from previous iteration...")
            trained_agent = run_simulation(episodes=episodes, 
                                          visualize_interval=visualize_interval, 
                                          show_plots=show_plots, 
                                          max_steps=max_steps,
                                          agent=trained_agent)
        
        # Save intermediate agent if requested
        if save_iterations and trained_agent:
            try:
                # Prepare agent for saving
                visualizer_backup = trained_agent.prepare_for_save()
                
                # Save agent with iteration number in filename
                filename = f"trained_agent_iter{iteration+1}.pkl"
                with open(filename, "wb") as f:
                    pickle.dump(trained_agent, f)
                    
                # Restore agent after saving
                trained_agent.restore_after_save(visualizer_backup)
                print(f"Intermediate agent saved to '{filename}'")
            except Exception as e:
                print(f"Error saving intermediate agent: {e}")
    
    # Test incident response on the final trained agent
    print("\nTesting incident response on final trained agent...")
    test_incident_response(trained_agent, show_plot=show_plots, num_tests=5)
    
    # Save final agent
    if save_agent and trained_agent:
        try:
            # Prepare agent for saving
            visualizer_backup = trained_agent.prepare_for_save()
            
            # Save agent to file
            with open("trained_agent.pkl", "wb") as f:
                pickle.dump(trained_agent, f)
                
            # Restore agent after saving
            trained_agent.restore_after_save(visualizer_backup)
            print("Final trained agent saved to 'trained_agent.pkl'")
        except Exception as e:
            print(f"Error saving agent: {e}")
    
    return trained_agent

def simulate_mode(agent=None):
    """Simulation mode: Launch interactive simulation controller"""
    controller = SimulationController(agent)
    print("Starting interactive simulation controller...")
    controller.run()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Q-Learning Urban Traffic Simulation")
    parser.add_argument("--mode", choices=["train", "simulate", "both"], default="both",
                      help="Choose mode: train, simulate, or both")
    parser.add_argument("--episodes", type=int, default=200,
                      help="Number of training episodes per iteration (train mode)")
    parser.add_argument("--iterations", type=int, default=1,
                      help="Number of training iterations to run (train mode)")
    parser.add_argument("--save-iterations", action="store_true",
                      help="Save intermediate agents after each iteration")
    parser.add_argument("--no-plots", action="store_true",
                      help="Disable plot display during training")
    parser.add_argument("--no-save", action="store_true",
                      help="Don't save trained agent to file")
    parser.add_argument("--continue", dest="continue_training", action="store_true",
                      help="Continue training from existing agent.pkl file")
    parser.add_argument("--unlimited-steps", action="store_true",
                      help="Run until all vehicles reach destination, regardless of step count")
    parser.add_argument("--max-steps", type=int, default=2000,
                      help="Maximum steps per episode (ignored if --unlimited-steps is set)")
    args = parser.parse_args()
    
    # Set whether to display plots
    show_plots = not args.no_plots
    
    trained_agent = None
    
    # Execute corresponding functionality based on mode
    if args.mode == "train" or args.mode == "both":
        # If continue training is selected, try to load existing agent
        if args.continue_training:
            try:
                print("Attempting to load existing agent for continued training...")
                with open("trained_agent.pkl", "rb") as f:
                    trained_agent = pickle.load(f)
                    
                # Make sure urban_grid is properly initialized
                if not hasattr(trained_agent, 'urban_grid') or trained_agent.urban_grid is None:
                    from module.urban_grid import UrbanGrid
                    trained_agent.urban_grid = UrbanGrid(
                        size=trained_agent.grid_size,
                        congestion_update_rate=trained_agent.grid_congestion_update_rate,
                        traffic_light_cycle=trained_agent.grid_traffic_light_cycle
                    )
                print("Successfully loaded existing agent for continued training")
            except FileNotFoundError:
                print("No existing agent found. Starting training from scratch.")
                trained_agent = None
            except Exception as e:
                print(f"Error loading agent: {e}")
                trained_agent = None
                
        # Train agent
        trained_agent = train_mode(
            episodes=args.episodes,
            visualize_interval=50,
            show_plots=show_plots,
            max_steps=args.max_steps,
            save_agent=not args.no_save,
            iterations=args.iterations,
            save_iterations=args.save_iterations,
            unlimited_steps=args.unlimited_steps
        )
    
    if args.mode == "simulate" or args.mode == "both":
        # If mode is simulate only, try to load the trained agent
        if args.mode == "simulate" and not trained_agent:
            try:
                with open("trained_agent.pkl", "rb") as f:
                    trained_agent = pickle.load(f)
                    
                # Make sure urban_grid is properly initialized
                if not hasattr(trained_agent, 'urban_grid') or trained_agent.urban_grid is None:
                    from module.urban_grid import UrbanGrid
                    trained_agent.urban_grid = UrbanGrid(
                        size=trained_agent.grid_size,
                        congestion_update_rate=trained_agent.grid_congestion_update_rate,
                        traffic_light_cycle=trained_agent.grid_traffic_light_cycle
                    )
                    
                print("Loaded existing trained agent")
            except FileNotFoundError:
                print("No saved agent found. Please train an agent first or create one in the simulation controller")
            except Exception as e:
                print(f"Error loading agent: {e}")
        
        simulate_mode(trained_agent)