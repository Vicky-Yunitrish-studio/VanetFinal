import numpy as np
from visualizer import TkinterVisualizer

class UrbanGrid:
    def __init__(self, size=20, congestion_update_rate=0.1, traffic_light_cycle=10):
        self.size = size
        self.grid = np.zeros((size, size))  # Grid for the map
        self.congestion = np.zeros((size, size))  # Congestion levels
        self.obstacles = np.zeros((size, size), dtype=bool)  # Traffic incidents
        self.congestion_update_rate = congestion_update_rate
        
        # Traffic light system
        self.traffic_lights = np.zeros((size, size), dtype=int)  # 0: no light, 1: NS green, 2: EW green
        self.traffic_light_cycle = traffic_light_cycle
        self.current_cycle = 0
        self.init_traffic_lights()

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
        
    def init_traffic_lights(self):
        """Initialize traffic lights at all intersections"""
        # Place traffic lights at every second position to create proper intersections
        for i in range(1, self.size, 2):  # Start at 1, increment by 2
            for j in range(1, self.size, 2):  # Start at 1, increment by 2
                # Alternate initial states for visual pattern
                state = 1 if (i + j) % 2 == 0 else 2
                self.traffic_lights[i, j] = state
    
    def update_traffic_lights(self):
        """Update traffic light states based on cycle"""
        self.current_cycle += 1
        if self.current_cycle % self.traffic_light_cycle == 0:
            # Switch traffic light states (1->2, 2->1)
            for i in range(self.size):
                for j in range(self.size):
                    if self.traffic_lights[i, j] > 0:
                        self.traffic_lights[i, j] = 3 - self.traffic_lights[i, j]  # Toggle between 1 and 2

    def get_congestion_window(self, x, y, window_size=3):
        """Get average congestion in a window around (x, y)"""
        half_window = window_size // 2
        x_min = max(0, x - half_window)
        x_max = min(self.size - 1, x + half_window)
        y_min = max(0, y - half_window)
        y_max = min(self.size - 1, y + half_window)
        
        return np.mean(self.congestion[x_min:x_max+1, y_min:y_max+1])

    def visualize(self, vehicles=None, show_plot=True, obstacle_mode=False, congestion_mode=False):
        """Visualize the grid with congestion and vehicles using Tkinter
        
        Args:
            vehicles: List of vehicles to visualize
            show_plot: Whether to display the visualization (set to False to suppress display)
            obstacle_mode: Whether in obstacle placement mode (changes appearance)
            congestion_mode: Whether in congestion adjustment mode (changes appearance)
        """
        if not show_plot:
            return
            
        # Create or update tkinter visualizer
        if not hasattr(self, 'visualizer') or self.visualizer.is_closed:
            self.visualizer = TkinterVisualizer(grid_size=self.size, cell_size=50)
            
        # Store vehicles reference for visualization
        self.vehicles = vehicles
        
        # Update current step
        self.current_step = getattr(self, 'current_step', 0) + 1
            
        # Update the display
        self.visualizer.update_display(self, vehicles=vehicles, obstacle_mode=obstacle_mode, congestion_mode=congestion_mode)
