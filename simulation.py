import numpy as np
import random
import matplotlib.pyplot as plt
from urban_grid import UrbanGrid
from agent import QLearningAgent
from vehicle import Vehicle

def run_simulation(episodes=1000, visualize_interval=100, max_steps=200, show_plots=True, agent=None):
    """Run the full simulation
    
    Args:
        episodes: Number of episodes to run
        visualize_interval: Interval for visualization (set to 0 to disable)
        max_steps: Maximum steps per episode (if 0, run until all vehicles reach destination)
        show_plots: Whether to show plots (can be set to False to suppress all visualization)
        agent: Optional pre-existing agent to continue training (if None, creates a new agent)
    """
    if agent is None:
        # Create new agent
        urban_grid = UrbanGrid(size=20)  # Changed map size from 10 to 20
        agent = QLearningAgent(urban_grid)
    else:
        # Use existing agent's urban_grid
        urban_grid = agent.urban_grid
    
    # Statistics tracking
    episode_rewards = []
    episode_steps = []
    success_rate = []
    
    for episode in range(episodes):
        # Reset vehicle ID counter
        Vehicle.next_id = 1
        
        # Reset environment
        urban_grid.reset_congestion()
        
        # Clear obstacles and add random ones (5% of grid)
        urban_grid.obstacles = np.zeros((urban_grid.size, urban_grid.size), dtype=bool)
        num_obstacles = int(0.05 * urban_grid.size * urban_grid.size)
        for _ in range(num_obstacles):
            x, y = random.randint(0, urban_grid.size-1), random.randint(0, urban_grid.size-1)
            urban_grid.add_obstacle(x, y)
        
        # Create vehicles with random start/end positions
        num_vehicles = 5
        vehicles = []
        for _ in range(num_vehicles):
            vehicle = Vehicle(urban_grid, agent)
            vehicles.append(vehicle)
        
        # Simulation loop
        step = 0
        all_reached = False
        
        # Determine if unlimited steps mode is used (max_steps=0 means unlimited steps)
        unlimited_steps = (max_steps == 0)
        
        while not all_reached and (unlimited_steps or step < max_steps):
            # Update environment
            positions = [v.position for v in vehicles if not v.reached]
            urban_grid.update_congestion(positions)
            urban_grid.update_traffic_lights()
            
            # Move vehicles
            for vehicle in vehicles:
                if not vehicle.reached:
                    vehicle.move()
            
            # Check if all vehicles reached destination
            all_reached = all(v.reached for v in vehicles)
            step += 1
            
            # Visualize if needed
            if visualize_interval > 0 and (episode % visualize_interval == 0) and (step % 5 == 0):
                urban_grid.visualize(vehicles, show_plot=show_plots)
        
        # Record episode statistics
        episode_total_reward = sum(v.total_reward for v in vehicles)
        episode_avg_steps = np.mean([v.steps for v in vehicles])
        episode_success = sum(1 for v in vehicles if v.reached) / len(vehicles)
        
        episode_rewards.append(episode_total_reward)
        episode_steps.append(episode_avg_steps)
        success_rate.append(episode_success)
        
        if episode % 10 == 0:
            print(f"Episode {episode}: Reward: {episode_total_reward:.2f}, "
                  f"Steps: {episode_avg_steps:.2f}, Success Rate: {episode_success:.2f}")
    
    # Plot learning curves
    if show_plots:
        plt.figure(figsize=(15, 5))
        
        plt.subplot(131)
        plt.plot(episode_rewards)
        plt.title('Total Reward per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        
        plt.subplot(132)
        plt.plot(episode_steps)
        plt.title('Average Steps per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Steps')
        
        plt.subplot(133)
        plt.plot(success_rate)
        plt.title('Success Rate per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Success Rate')
        
        plt.tight_layout()
        plt.show()
    
    return agent


def test_incident_response(agent, num_tests=5, visualize=True, show_plot=True, max_steps=50, unlimited_steps=False):
    """Test how well agents avoid incidents after learning
    
    Args:
        agent: The trained agent to test
        num_tests: Number of test scenarios to run
        visualize: Whether to visualize the tests
        show_plot: Whether to show visualization
        max_steps: Maximum steps per test
        unlimited_steps: If True, ignore max_steps and run until vehicle reaches destination
    """
    # Reset vehicle ID counter
    Vehicle.next_id = 1
    
    urban_grid = agent.urban_grid
    
    for test in range(num_tests):
        print(f"\nTest {test+1}: Incident Avoidance Test")
        
        # Reset environment
        urban_grid.reset_congestion()
        urban_grid.obstacles = np.zeros((urban_grid.size, urban_grid.size), dtype=bool)
        
        # Create a "roadblock" of incidents in the middle
        for i in range(3, 7):
            urban_grid.add_obstacle(i, 5)
        
        # Create vehicles with specific start/end positions that would ideally go through the middle
        start_pos = (1, 5)
        end_pos = (8, 5)
        vehicle = Vehicle(urban_grid, agent, position=start_pos, destination=end_pos)
        
        # Run simulation for this vehicle
        step = 0
        # 使用參數傳入的 max_steps 或根據地圖大小調整默認值
        if unlimited_steps:
            # 使用無限步數模式，但設置一個很大的數字作為保險
            effective_max_steps = 10000
        else:
            # 根據地圖大小調整最大步數
            effective_max_steps = max_steps if max_steps > 0 else urban_grid.size * 10
        
        while not vehicle.reached and step < effective_max_steps:
            urban_grid.update_traffic_lights()
            vehicle.move()
            step += 1
            
            if visualize and (step % 3 == 0 or vehicle.reached):
                urban_grid.visualize([vehicle], show_plot=show_plot)
        
        # Report results
        if vehicle.reached:
            print(f"Vehicle reached destination in {step} steps with reward {vehicle.total_reward}")
            print(f"Path taken: {vehicle.path}")
        else:
            print("Vehicle did not reach destination within step limit")
