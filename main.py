import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import time

class UrbanGrid:
    def __init__(self, size=10, congestion_update_rate=0.1):
        self.size = size
        self.grid = np.zeros((size, size))  # Grid for the map
        self.congestion = np.zeros((size, size))  # Congestion levels
        self.obstacles = np.zeros((size, size), dtype=bool)  # Traffic incidents
        self.congestion_update_rate = congestion_update_rate

    def reset_congestion(self):
        """Reset congestion to random initial levels"""
        self.congestion = np.random.uniform(0, 0.3, size=(self.size, self.size))

    def update_congestion(self, positions):
        """Update congestion based on vehicle positions"""
        # Create a heatmap of vehicle positions
        position_heatmap = np.zeros((self.size, self.size))
        for pos in positions:
            position_heatmap[pos] += 1

        # Update congestion levels
        self.congestion = (1 - self.congestion_update_rate) * self.congestion + \
                          self.congestion_update_rate * position_heatmap
        
        # Normalize congestion to [0, 1] range
        if np.max(self.congestion) > 0:
            self.congestion = self.congestion / np.max(self.congestion)

    def add_obstacle(self, x, y):
        """Add a traffic incident at position (x, y)"""
        self.obstacles[x, y] = True

    def remove_obstacle(self, x, y):
        """Remove a traffic incident from position (x, y)"""
        self.obstacles[x, y] = False

    def get_congestion_window(self, x, y, window_size=3):
        """Get average congestion in a window around (x, y)"""
        half_window = window_size // 2
        x_min = max(0, x - half_window)
        x_max = min(self.size - 1, x + half_window)
        y_min = max(0, y - half_window)
        y_max = min(self.size - 1, y + half_window)
        
        return np.mean(self.congestion[x_min:x_max+1, y_min:y_max+1])

    def visualize(self, vehicles=None, show_plot=True):
        """Visualize the grid with congestion and vehicles
        
        Args:
            vehicles: List of vehicles to visualize
            show_plot: Whether to display the plot (set to False to suppress display)
        """
        if not show_plot:
            return
            
        plt.figure(figsize=(10, 10))
        
        # Plot congestion as heatmap
        plt.imshow(self.congestion.T, cmap='YlOrRd', alpha=0.5, origin='lower')
        
        # Plot grid lines
        for i in range(self.size + 1):
            plt.axhline(i - 0.5, color='black', linewidth=0.5)
            plt.axvline(i - 0.5, color='black', linewidth=0.5)
        
        # Plot obstacles
        for i in range(self.size):
            for j in range(self.size):
                if self.obstacles[i, j]:
                    plt.plot(i, j, 's', markersize=20, color='black', alpha=0.7)
        
        # Plot vehicles
        if vehicles:
            for v in vehicles:
                plt.plot(v.position[0], v.position[1], 'o', markersize=10, 
                         color='blue', alpha=0.7)
                plt.plot(v.destination[0], v.destination[1], '*', markersize=15, 
                         color='green', alpha=0.7)
        
        plt.colorbar(label='Congestion Level')
        plt.title('Urban Grid Simulation')
        plt.grid(False)
        plt.xticks(range(self.size))
        plt.yticks(range(self.size))
        plt.pause(0.1)


class QLearningAgent:
    def __init__(self, urban_grid, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.urban_grid = urban_grid
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(4))  # Up, Right, Down, Left
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        
    def get_state_key(self, position, congestion_level):
        """Convert state to a hashable key"""
        # Discretize congestion level to 5 levels
        congestion_discrete = min(4, int(congestion_level * 5))
        return (position[0], position[1], congestion_discrete)
    
    def choose_action(self, state, position):
        """Choose an action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            # Exploration: random action
            valid_actions = self.get_valid_actions(position)
            return random.choice(valid_actions)
        else:
            # Exploitation: choose best action from Q-table
            valid_actions = self.get_valid_actions(position)
            q_values = [self.q_table[state][a] for a in valid_actions]
            max_q = max(q_values)
            # Handle multiple actions with the same max value
            best_actions = [valid_actions[i] for i in range(len(valid_actions)) if q_values[i] == max_q]
            return random.choice(best_actions)
    
    def get_valid_actions(self, position):
        """Get valid actions at current position (avoiding grid boundaries and obstacles)"""
        valid_actions = []
        for i, (dx, dy) in enumerate(self.actions):
            new_x = position[0] + dx
            new_y = position[1] + dy
            if (0 <= new_x < self.urban_grid.size and 
                0 <= new_y < self.urban_grid.size and 
                not self.urban_grid.obstacles[new_x, new_y]):
                valid_actions.append(i)
        
        # If no valid actions (surrounded by obstacles), return all directions
        # This should never happen in a proper grid, but is a failsafe
        if not valid_actions:
            valid_actions = list(range(4))
        
        return valid_actions
    
    def update_q_table(self, state, action, reward, next_state):
        """Update Q-table using Q-learning update rule"""
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                     self.learning_rate * (reward + self.discount_factor * 
                                                         self.q_table[next_state][best_next_action])


class Vehicle:
    def __init__(self, urban_grid, agent, position=None, destination=None):
        self.urban_grid = urban_grid
        self.agent = agent
        
        # Random positions if not specified
        if position is None:
            self.position = (random.randint(0, urban_grid.size-1), 
                           random.randint(0, urban_grid.size-1))
        else:
            self.position = position
            
        if destination is None:
            self.destination = (random.randint(0, urban_grid.size-1), 
                             random.randint(0, urban_grid.size-1))
            # Make sure destination is different from position
            while self.destination == self.position:
                self.destination = (random.randint(0, urban_grid.size-1), 
                                 random.randint(0, urban_grid.size-1))
        else:
            self.destination = destination
            
        self.path = [self.position]
        self.reached = False
        self.steps = 0
        self.total_reward = 0
    
    def move(self):
        """Move the vehicle according to the Q-learning policy"""
        if self.reached:
            return 0  # Already reached destination
        
        # Get current state
        congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
        state = self.agent.get_state_key(self.position, congestion_level)
        
        # Choose action
        action_idx = self.agent.choose_action(state, self.position)
        dx, dy = self.agent.actions[action_idx]
        
        # Move to new position
        new_position = (self.position[0] + dx, self.position[1] + dy)
        
        # Calculate reward
        reward = -1  # Step penalty
        
        # Add congestion penalty
        congestion_at_new_pos = self.urban_grid.congestion[new_position]
        if congestion_at_new_pos > 0.5:  # High congestion threshold
            reward -= 5 * congestion_at_new_pos  # Penalty proportional to congestion
        
        # Check if destination reached
        if new_position == self.destination:
            reward += 100  # Destination reward
            self.reached = True
        
        # Update position and path
        self.position = new_position
        self.path.append(self.position)
        self.steps += 1
        self.total_reward += reward
        
        # Get new state
        new_congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
        new_state = self.agent.get_state_key(self.position, new_congestion_level)
        
        # Update Q-table
        self.agent.update_q_table(state, action_idx, reward, new_state)
        
        return reward


def run_simulation(episodes=1000, visualize_interval=100, max_steps=200, show_plots=True):
    """Run the full simulation
    
    Args:
        episodes: Number of episodes to run
        visualize_interval: Interval for visualization (set to 0 to disable)
        max_steps: Maximum steps per episode
        show_plots: Whether to show plots (can be set to False to suppress all visualization)
    """
    urban_grid = UrbanGrid(size=10)
    agent = QLearningAgent(urban_grid)
    
    # Statistics tracking
    episode_rewards = []
    episode_steps = []
    success_rate = []
    
    for episode in range(episodes):
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
        
        while not all_reached and step < max_steps:
            # Update environment
            positions = [v.position for v in vehicles if not v.reached]
            urban_grid.update_congestion(positions)
            
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


def test_incident_response(agent, num_tests=5, visualize=True, show_plot=True):
    """Test how well agents avoid incidents after learning"""
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
        max_steps = 50
        
        while not vehicle.reached and step < max_steps:
            vehicle.move()
            step += 1
            
            if visualize and (step % 3 == 0 or vehicle.reached):
                urban_grid.visualize([vehicle], show_plot=show_plot)
                plt.title(f"Test {test+1}: Step {step}")
        
        # Report results
        if vehicle.reached:
            print(f"Vehicle reached destination in {step} steps with reward {vehicle.total_reward}")
            print(f"Path taken: {vehicle.path}")
        else:
            print("Vehicle did not reach destination within step limit")


if __name__ == "__main__":
    # 設定是否顯示圖表
    show_plots = True  # 將此變數設為 False 可暫時關閉所有圖表顯示
    
    # Train the agent
    print("Training Q-Learning agent...")
    trained_agent = run_simulation(episodes=200, visualize_interval=50, show_plots=show_plots)
    
    # Test incident response
    print("\nTesting incident response...")
    test_incident_response(trained_agent, show_plot=show_plots)