import random
from astar import astar, manhattan_distance

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
            
        # Share destination with agent for better state representation
        self.agent.current_destination = self.destination
            
        # Calculate optimal path using A*
        self.optimal_path = astar(
            self.position,
            self.destination,
            self.urban_grid.size,
            self.urban_grid.obstacles,
            self.urban_grid.congestion
        )
        
        self.path = [self.position]
        self.reached = False
        self.steps = 0
        self.total_reward = 0
        
        # Track vehicle position history to detect loops
        self.position_history = {}  # {position: count}
        self.position_history[self.position] = 1
        self.loop_penalty_applied = {}  # {position: bool} Track whether loop penalty has been applied to a specific position
    
    def update_optimal_path(self):
        """Update A* path based on current traffic conditions"""
        if not self.reached:
            self.optimal_path = astar(
                self.position,
                self.destination,
                self.urban_grid.size,
                self.urban_grid.obstacles,
                self.urban_grid.congestion
            )
    
    def move(self):
        """Move the vehicle using hybrid A* and Q-learning approach"""
        if self.reached:
            return 0  # Already reached destination
            
        # Update optimal path every 10 steps or when no path exists
        if self.steps % 10 == 0 or not self.optimal_path:
            self.update_optimal_path()
        
        # Get current state
        congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
        state = self.agent.get_state_key(self.position, congestion_level)
        
        # Choose action with A* guidance
        action_idx = self.agent.choose_action(state, self.position)
        dx, dy = self.agent.actions[action_idx]
        new_position = (self.position[0] + dx, self.position[1] + dy)
        
        # Calculate base reward
        reward = -1  # Step penalty
        
        # A* path following reward
        if self.optimal_path and len(self.optimal_path) > 1:
            next_optimal = self.optimal_path[1]  # Next position in optimal path
            if new_position == next_optimal:
                reward += 10  # Strong reward for following A* path
            elif new_position in self.optimal_path:
                reward += 5  # Moderate reward for being on optimal path
        
        # Distance-based reward component
        current_dist = manhattan_distance(self.position, self.destination)
        new_dist = manhattan_distance(new_position, self.destination)
        if new_dist < current_dist:
            reward += 3  # Reward for getting closer to destination
        
        # Congestion penalties
        congestion_at_new_pos = self.urban_grid.congestion[new_position]
        if congestion_at_new_pos > 0.5:  # High congestion threshold
            reward -= 5 * congestion_at_new_pos  # Penalty proportional to congestion
        
        # Enhanced backward movement prevention
        if len(self.path) > 1:
            # Check for immediate backtracking
            if new_position == self.path[-2]:
                reward -= 30  # Doubled penalty for immediate backtracking
                
            # Check for oscillating behavior (moving back and forth)
            if len(self.path) > 3:
                if new_position == self.path[-3]:  # Moving back to position from 2 steps ago
                    reward -= 40  # Even stronger penalty for oscillation
                if len(self.path) > 5 and new_position == self.path[-5]:  # Check longer oscillation patterns
                    reward -= 50  # Severe penalty for longer oscillation patterns
        
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
                reward += loop_penalty
                self.loop_penalty_applied[self.position] = True
                
                # Reset Q-values for this position to encourage exploration of other paths
                self.agent.reset_state_q_values(state)
        else:
            self.position_history[self.position] = 1
        
        self.total_reward += reward
        
        # --- Proximity reward: the closer to the destination, the higher the reward ---
        def manhattan_dist(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        old_dist = manhattan_dist(self.position, self.destination)
        new_dist = manhattan_dist(new_position, self.destination)
        proximity_reward = old_dist - new_dist  # +1 if closer, -1 if farther, 0 if same
        
        # Scale proximity reward based on distance to destination
        # The closer to destination, the higher the reward multiplier
        max_possible_dist = self.urban_grid.size * 2  # Maximum possible Manhattan distance
        progress = 1 - (new_dist / max_possible_dist)  # 0 when furthest, 1 when at destination
        proximity_multiplier = 5 + (15 * progress)  # Scales from 5 to 20 based on progress
        reward += proximity_reward * proximity_multiplier
        # --- End proximity reward ---
        
        # --- A* path following reward ---
        if self.optimal_path:
            # Find the nearest point on optimal path
            min_dist_to_path = float('inf')
            path_progress = 0
            for i, path_point in enumerate(self.optimal_path):
                dist_to_point = manhattan_dist(new_position, path_point)
                if dist_to_point < min_dist_to_path:
                    min_dist_to_path = dist_to_point
                    path_progress = i / len(self.optimal_path)
            
            # Reward for being close to optimal path
            path_reward = max(0, 10 - min_dist_to_path * 2)  # Max 10 reward when on path
            # Scale reward based on progress along path
            path_reward *= (1 + path_progress)  # Higher reward for later parts of path
            reward += path_reward
        # --- End A* path reward ---
        
        # Get new state
        new_congestion_level = self.urban_grid.get_congestion_window(self.position[0], self.position[1])
        new_state = self.agent.get_state_key(self.position, new_congestion_level)
        
        # Update Q-table
        self.agent.update_q_table(state, action_idx, reward, new_state)
        
        return reward
    
    def get_remaining_optimal_path(self):
        """Get the remaining optimal path from current position"""
        if not self.optimal_path:
            return []
        try:
            current_index = self.optimal_path.index(self.position)
            return self.optimal_path[current_index:]
        except ValueError:
            # If current position is not in optimal path, recalculate
            self.update_optimal_path()
            return self.optimal_path if self.optimal_path else []
