"""
Reward Configuration Module

This module contains all reward-related constants and configurations for the vehicle simulation.
It allows easy customization of reward values without modifying the core vehicle logic.
"""

class RewardConfig:
    """Configuration class for reward system parameters"""
    
    def __init__(self):
        # Algorithm selection
        self.algorithm = "proximity_based"  # Options: "proximity_based", "exponential_distance"
        
        # Basic movement rewards
        self.step_penalty = -1  # Cost for each step taken
        
        # Exponential distance algorithm parameters
        self.exp_base_reward = -1  # Base reward for exponential algorithm
        self.exp_amplitude = 40  # Amplitude for exponential reward
        self.exp_x_scale = 1.5  # X-direction scale factor
        self.exp_y_scale = 2.0  # Y-direction scale factor
        
        # A* path following rewards
        self.astar_follow_reward = 10  # Strong reward for following A* path exactly
        self.astar_on_path_reward = 5  # Moderate reward for being on optimal path
        
        # Distance-based rewards
        self.closer_to_destination_reward = 3  # Reward for moving closer to destination
        
        # Congestion penalties
        self.high_congestion_threshold = 0.5  # Threshold for high congestion
        self.congestion_penalty_multiplier = 5  # Multiplier for congestion penalty
        
        # Backward movement penalties
        self.immediate_backtrack_penalty = -30  # Penalty for immediate backtracking
        self.oscillation_penalty = -40  # Penalty for oscillating behavior
        self.long_oscillation_penalty = -50  # Penalty for longer oscillation patterns
        
        # Traffic light penalties
        self.red_light_wait_penalty = -5  # Penalty for waiting at red light
        
        # Destination reward
        self.destination_reached_reward = 100  # Large reward for reaching destination
        
        # Loop detection and penalties
        self.loop_threshold_base = 3  # Base threshold for loop detection
        self.loop_threshold_max = 5  # Maximum threshold for loop detection
        self.loop_penalty_base = -20  # Base penalty per loop occurrence
        self.loop_penalty_max = -100  # Maximum loop penalty
        
        # Proximity reward parameters
        self.proximity_base_multiplier = 5  # Base proximity reward multiplier
        self.proximity_max_multiplier = 15  # Additional proximity reward multiplier
        
        # A* path distance reward parameters
        self.path_distance_base_reward = 10  # Base reward for being near optimal path
        self.path_distance_penalty_multiplier = 2  # Penalty multiplier for distance from path
        
    def get_step_penalty(self):
        """Get the penalty for taking a step"""
        return self.step_penalty
    
    def get_astar_rewards(self):
        """Get A* path following rewards"""
        return {
            'follow': self.astar_follow_reward,
            'on_path': self.astar_on_path_reward
        }
    
    def get_distance_reward(self):
        """Get reward for moving closer to destination"""
        return self.closer_to_destination_reward
    
    def get_congestion_config(self):
        """Get congestion-related configuration"""
        return {
            'threshold': self.high_congestion_threshold,
            'penalty_multiplier': self.congestion_penalty_multiplier
        }
    
    def get_backward_movement_penalties(self):
        """Get penalties for backward movement"""
        return {
            'immediate_backtrack': self.immediate_backtrack_penalty,
            'oscillation': self.oscillation_penalty,
            'long_oscillation': self.long_oscillation_penalty
        }
    
    def get_traffic_light_penalty(self):
        """Get penalty for waiting at red light"""
        return self.red_light_wait_penalty
    
    def get_destination_reward(self):
        """Get reward for reaching destination"""
        return self.destination_reached_reward
    
    def get_loop_config(self):
        """Get loop detection configuration"""
        return {
            'threshold_base': self.loop_threshold_base,
            'threshold_max': self.loop_threshold_max,
            'penalty_base': self.loop_penalty_base,
            'penalty_max': self.loop_penalty_max
        }
    
    def get_proximity_config(self):
        """Get proximity reward configuration"""
        return {
            'base_multiplier': self.proximity_base_multiplier,
            'max_multiplier': self.proximity_max_multiplier
        }
    
    def get_path_distance_config(self):
        """Get A* path distance reward configuration"""
        return {
            'base_reward': self.path_distance_base_reward,
            'penalty_multiplier': self.path_distance_penalty_multiplier
        }
    
    def get_algorithm_type(self):
        """Get the current algorithm type"""
        return self.algorithm
    
    def set_algorithm_type(self, algorithm_type):
        """Set the algorithm type"""
        if algorithm_type in ["proximity_based", "exponential_distance"]:
            self.algorithm = algorithm_type
        else:
            print(f"Warning: Unknown algorithm type '{algorithm_type}'. Using 'proximity_based'.")
            self.algorithm = "proximity_based"
    
    def get_exponential_distance_config(self):
        """Get exponential distance algorithm configuration"""
        return {
            'base_reward': self.exp_base_reward,
            'multiplier': self.exp_amplitude,
            'x_scale': self.exp_x_scale,
            'y_scale': self.exp_y_scale
        }
    
    def update_config(self, **kwargs):
        """
        Update configuration values dynamically
        
        Args:
            **kwargs: Key-value pairs of configuration parameters to update
            
        Example:
            config.update_config(
                step_penalty=-2,
                destination_reached_reward=150,
                congestion_penalty_multiplier=7
            )
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown configuration parameter '{key}' ignored")
    
    def reset_to_defaults(self):
        """Reset all configuration values to their defaults"""
        self.__init__()
    
    def get_all_config(self):
        """Get all configuration parameters as a dictionary"""
        return {
            'step_penalty': self.step_penalty,
            'astar_follow_reward': self.astar_follow_reward,
            'astar_on_path_reward': self.astar_on_path_reward,
            'closer_to_destination_reward': self.closer_to_destination_reward,
            'high_congestion_threshold': self.high_congestion_threshold,
            'congestion_penalty_multiplier': self.congestion_penalty_multiplier,
            'immediate_backtrack_penalty': self.immediate_backtrack_penalty,
            'oscillation_penalty': self.oscillation_penalty,
            'long_oscillation_penalty': self.long_oscillation_penalty,
            'red_light_wait_penalty': self.red_light_wait_penalty,
            'destination_reached_reward': self.destination_reached_reward,
            'loop_threshold_base': self.loop_threshold_base,
            'loop_threshold_max': self.loop_threshold_max,
            'loop_penalty_base': self.loop_penalty_base,
            'loop_penalty_max': self.loop_penalty_max,
            'proximity_base_multiplier': self.proximity_base_multiplier,
            'proximity_max_multiplier': self.proximity_max_multiplier,
            'path_distance_base_reward': self.path_distance_base_reward,
            'path_distance_penalty_multiplier': self.path_distance_penalty_multiplier,
            'algorithm': self.algorithm,
            'exp_base_reward': self.exp_base_reward,
            'exp_amplitude': self.exp_amplitude,
            'exp_x_scale': self.exp_x_scale,
            'exp_y_scale': self.exp_y_scale
        }


# Create a default instance for easy import
default_reward_config = RewardConfig()
