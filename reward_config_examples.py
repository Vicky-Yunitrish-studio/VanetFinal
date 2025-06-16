"""
Example usage of the RewardConfig system

This file demonstrates how to use the new reward configuration system
to customize vehicle behavior without modifying the core Vehicle class.
"""

from reward_config import RewardConfig, default_reward_config
from vehicle import Vehicle
from urban_grid import UrbanGrid
from agent import Agent  # Assuming you have an Agent class

def example_basic_usage():
    """Basic example of using default reward configuration"""
    
    # Create environment components
    grid = UrbanGrid(size=10)
    agent = Agent()  # Assuming Agent class exists
    
    # Create vehicle with default reward configuration
    vehicle = Vehicle(grid, agent)
    
    print("Vehicle created with default reward configuration")
    print(f"Step penalty: {vehicle.reward_config.get_step_penalty()}")
    print(f"Destination reward: {vehicle.reward_config.get_destination_reward()}")

def example_custom_configuration():
    """Example of creating a custom reward configuration"""
    
    # Create custom reward configuration
    custom_config = RewardConfig()
    
    # Modify specific values
    custom_config.update_config(
        step_penalty=-2,  # Higher step penalty to encourage faster routes
        destination_reached_reward=200,  # Higher reward for reaching destination
        congestion_penalty_multiplier=10,  # Higher penalty for congestion
        immediate_backtrack_penalty=-50  # Stronger penalty for backtracking
    )
    
    # Create environment components
    grid = UrbanGrid(size=10)
    agent = Agent()
    
    # Create vehicle with custom configuration
    vehicle = Vehicle(grid, agent, reward_config=custom_config)
    
    print("Vehicle created with custom reward configuration")
    print(f"Step penalty: {vehicle.reward_config.get_step_penalty()}")
    print(f"Destination reward: {vehicle.reward_config.get_destination_reward()}")
    print(f"Congestion penalty multiplier: {vehicle.reward_config.congestion_penalty_multiplier}")

def example_aggressive_configuration():
    """Example configuration for aggressive, fast-moving vehicles"""
    
    aggressive_config = RewardConfig()
    aggressive_config.update_config(
        step_penalty=-3,  # High step penalty
        astar_follow_reward=20,  # High reward for following optimal path
        destination_reached_reward=300,  # Very high destination reward
        immediate_backtrack_penalty=-100,  # Severe backtracking penalty
        oscillation_penalty=-80,  # Severe oscillation penalty
        congestion_penalty_multiplier=15  # Very high congestion avoidance
    )
    
    return aggressive_config

def example_cautious_configuration():
    """Example configuration for cautious, exploration-friendly vehicles"""
    
    cautious_config = RewardConfig()
    cautious_config.update_config(
        step_penalty=-0.5,  # Low step penalty allows more exploration
        astar_follow_reward=5,  # Lower path following reward
        destination_reached_reward=50,  # Lower destination reward
        immediate_backtrack_penalty=-10,  # Mild backtracking penalty
        oscillation_penalty=-15,  # Mild oscillation penalty
        congestion_penalty_multiplier=2  # Lower congestion penalty
    )
    
    return cautious_config

def example_experiment_with_different_configs():
    """Example of running experiments with different reward configurations"""
    
    # Create different configurations
    configs = {
        'default': RewardConfig(),
        'aggressive': example_aggressive_configuration(),
        'cautious': example_cautious_configuration()
    }
    
    # Create environment
    grid = UrbanGrid(size=15)
    
    # Test each configuration
    results = {}
    for config_name, config in configs.items():
        agent = Agent()  # Fresh agent for each test
        vehicle = Vehicle(grid, agent, 
                         position=(0, 0), 
                         destination=(14, 14),
                         reward_config=config)
        
        print(f"\nTesting {config_name} configuration:")
        print(f"  Step penalty: {config.get_step_penalty()}")
        print(f"  Destination reward: {config.get_destination_reward()}")
        print(f"  A* follow reward: {config.get_astar_rewards()['follow']}")
        
        # You could run simulation here and collect results
        # results[config_name] = run_simulation(vehicle)
    
    return results

def example_dynamic_configuration_changes():
    """Example of changing configuration during runtime"""
    
    # Create vehicle with default configuration
    grid = UrbanGrid(size=10)
    agent = Agent()
    vehicle = Vehicle(grid, agent)
    
    print("Initial configuration:")
    print(f"Step penalty: {vehicle.reward_config.get_step_penalty()}")
    
    # Change configuration during runtime
    vehicle.reward_config.update_config(step_penalty=-5)
    
    print("After update:")
    print(f"Step penalty: {vehicle.reward_config.get_step_penalty()}")
    
    # Reset to defaults
    vehicle.reward_config.reset_to_defaults()
    
    print("After reset:")
    print(f"Step penalty: {vehicle.reward_config.get_step_penalty()}")

def example_save_and_load_config():
    """Example of how you might save and load configurations"""
    
    # Create custom configuration
    config = RewardConfig()
    config.update_config(
        step_penalty=-10,
        destination_reached_reward=500
    )
    
    # Get all configuration as dictionary (for saving to file)
    config_dict = config.get_all_config()
    print("Configuration dictionary:")
    for key, value in config_dict.items():
        print(f"  {key}: {value}")
    
    # You could save this to JSON, pickle, or other formats
    # import json
    # with open('reward_config.json', 'w') as f:
    #     json.dump(config_dict, f)
    
    # To load, you would create a new config and update it
    new_config = RewardConfig()
    new_config.update_config(**config_dict)

if __name__ == "__main__":
    print("=== Reward Configuration Examples ===\n")
    
    print("1. Basic Usage:")
    example_basic_usage()
    
    print("\n2. Custom Configuration:")
    example_custom_configuration()
    
    print("\n3. Different Behavior Profiles:")
    example_experiment_with_different_configs()
    
    print("\n4. Dynamic Configuration Changes:")
    example_dynamic_configuration_changes()
    
    print("\n5. Configuration Export:")
    example_save_and_load_config()
