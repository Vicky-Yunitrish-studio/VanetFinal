import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, urban_grid, learning_rate=0.2, discount_factor=0.95, epsilon=0.2):
        self.urban_grid = urban_grid
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon  # Increased exploration rate
        self.q_table = defaultdict(lambda: np.zeros(4))  # Up, Right, Down, Left
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
    
    def prepare_for_save(self):
        """Prepare agent for pickling by removing unpicklable parts"""
        # Store the grid parameters we need to recreate the urban_grid
        self.grid_size = self.urban_grid.size
        self.grid_congestion_update_rate = self.urban_grid.congestion_update_rate
        self.grid_traffic_light_cycle = self.urban_grid.traffic_light_cycle
        
        # Store the grid state but remove visualizer reference
        if hasattr(self.urban_grid, 'visualizer'):
            self.visualizer_existed = True
            visualizer_backup = self.urban_grid.visualizer
            self.urban_grid.visualizer = None
        else:
            self.visualizer_existed = False
            visualizer_backup = None
            
        return visualizer_backup
    
    def restore_after_save(self, visualizer_backup):
        """Restore agent after pickling"""
        if self.visualizer_existed and visualizer_backup is not None:
            self.urban_grid.visualizer = visualizer_backup
        
    def get_state_key(self, position, congestion_level):
        """Convert state to a hashable key"""
        # Discretize congestion level to 5 levels
        congestion_discrete = min(4, int(congestion_level * 5))
        
        # Get direction to destination (discretized to 8 directions)
        if hasattr(self, 'current_destination'):
            dx = self.current_destination[0] - position[0]
            dy = self.current_destination[1] - position[1]
            angle = np.arctan2(dy, dx)
            direction = int(((angle + np.pi) * 4 / np.pi + 0.5) % 8)
        else:
            direction = 0
        
        return (position[0], position[1], congestion_discrete, direction)
    
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
    
    def __getstate__(self):
        """Called when pickling the agent - prepare for serialization"""
        state = self.__dict__.copy()
        
        # Convert defaultdict q_table to regular dict for pickling
        state['q_table'] = dict(self.q_table)
        
        # Remove unpicklable parts
        visualizer_backup = self.prepare_for_save()
        state['_visualizer_backup'] = None  # We don't actually save the visualizer
        
        return state
    
    def __setstate__(self, state):
        """Called when unpickling the agent - restore after deserialization"""
        self.__dict__.update(state)
        
        # Convert back to defaultdict
        self.q_table = defaultdict(lambda: np.zeros(4))
        for k, v in state['q_table'].items():
            self.q_table[k] = v
        
        # Recreate urban_grid if needed
        if not hasattr(self, 'urban_grid') or self.urban_grid is None:
            from urban_grid import UrbanGrid
            self.urban_grid = UrbanGrid(
                size=self.grid_size, 
                congestion_update_rate=self.grid_congestion_update_rate,
                traffic_light_cycle=self.grid_traffic_light_cycle
            )
