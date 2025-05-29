import random

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
        
        # Add traffic light penalty
        x, y = new_position
        if self.urban_grid.traffic_lights[x, y] > 0:
            # Check if moving against red light
            # If moving North-South (dy != 0) and EW is green (state = 2)
            # Or if moving East-West (dx != 0) and NS is green (state = 1)
            if (dy != 0 and self.urban_grid.traffic_lights[x, y] == 2) or \
               (dx != 0 and self.urban_grid.traffic_lights[x, y] == 1):
                reward -= 10  # Penalty for running a red light
        
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
