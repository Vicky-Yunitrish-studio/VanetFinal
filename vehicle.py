import random

class Vehicle:
    # Class variable to track vehicle IDs
    next_id = 1
    
    def __init__(self, urban_grid, agent, position=None, destination=None):
        self.urban_grid = urban_grid
        self.agent = agent
        
        # Assign vehicle ID
        self.id = Vehicle.next_id
        Vehicle.next_id += 1
        
        # Random positions if not specified
        if position is None:
            self.position = (random.randint(0, urban_grid.size-1), 
                           random.randint(0, urban_grid.size-1))
        else:
            self.position = position
            
        # Store start position for display
        self.start_position = self.position
            
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
        
        # Track vehicle position history to detect loops
        self.position_history = {}  # {position: count}
        self.position_history[self.position] = 1
        self.loop_penalty_applied = {}  # {position: bool} Track whether loop penalty has been applied to a specific position
    
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
        
        # Check if trying to move backwards
        if len(self.path) > 1 and new_position == self.path[-2]:
            # Trying to return to the immediately previous position
            reward -= 15  # Strong penalty for moving backwards
        
        # Handle traffic lights
        x, y = new_position
        can_move = True
        if self.urban_grid.traffic_lights[x, y] > 0:
            # Check if moving against red light
            # If moving North-South (dy != 0) and EW is green (state = 2)
            # Or if moving East-West (dx != 0) and NS is green (state = 1)
            if (dy != 0 and self.urban_grid.traffic_lights[x, y] == 2) or \
               (dx != 0 and self.urban_grid.traffic_lights[x, y] == 1):
                # Stop and wait for the light to change
                can_move = False
                reward -= 5  # Small waiting penalty (less than running the red light)
                
        if can_move:
            # Check if destination reached
            if new_position == self.destination:
                reward += 100  # Destination reward
                self.reached = True
            
            # Update position and path
            self.position = new_position
            self.path.append(self.position)
        else:
            # Stay in the same position (waiting at red light)
            self.path.append(self.position)  # Record the wait as a step
        self.steps += 1
        
        # Detect loops
        if self.position in self.position_history:
            self.position_history[self.position] += 1
            
            # Calculate threshold: adjust loop threshold based on map size, smaller maps use smaller threshold
            loop_threshold = max(3, min(5, self.urban_grid.size // 5))
            
            # If we've visited the same position more than threshold times and haven't applied a loop penalty
            if self.position_history[self.position] > loop_threshold and not self.position in self.loop_penalty_applied:
                # Apply loop penalty
                loop_penalty = -20 * (self.position_history[self.position] - loop_threshold)  # More loops = bigger penalty
                loop_penalty = max(-100, loop_penalty)  # Limit maximum penalty
                print(f"Vehicle {self.id} looping at position {self.position}! Applied penalty: {loop_penalty}")
                reward += loop_penalty
                self.loop_penalty_applied[self.position] = True
        else:
            self.position_history[self.position] = 1
        
        self.total_reward += reward
        
        # --- Proximity reward: the closer to the destination, the higher the reward ---
        def manhattan_dist(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        old_dist = manhattan_dist(self.position, self.destination)
        new_dist = manhattan_dist(new_position, self.destination)
        proximity_reward = old_dist - new_dist  # +1 if closer, -1 if farther, 0 if same
        # You can scale this reward if you want a stronger effect:
        reward += proximity_reward * 2  # 2 can be adjusted for effect strength
        # --- End proximity reward ---
        
        # Get new state
        new_congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
        new_state = self.agent.get_state_key(self.position, new_congestion_level)
        
        # Update Q-table
        self.agent.update_q_table(state, action_idx, reward, new_state)
        
        return reward
