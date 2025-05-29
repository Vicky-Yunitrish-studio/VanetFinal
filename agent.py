import numpy as np
import random
from collections import defaultdict

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
