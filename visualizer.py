import tkinter as tk
from tkinter import Canvas, Frame, Label, ttk
import random
from matplotlib.colors import LinearSegmentedColormap

class TkinterVisualizer:
    def __init__(self, grid_size=20, cell_size=35):  # Adjusted for 20x20 grid
        self.grid_size = grid_size
        self.cell_size = cell_size
        
        # Increase margins to prevent roads from being cut off at edges
        self.margin = self.cell_size  # Use full cell size as margin
        self.window_width = grid_size * cell_size + 2 * self.margin
        self.window_height = grid_size * cell_size + 2 * self.margin + 50  # Extra space for info panel
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Urban Grid Q-Learning Simulation")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main frame with padding
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create canvas for drawing with a border
        self.canvas = Canvas(
            main_frame,
            width=self.window_width,
            height=self.window_height,
            bg='#d9d9d9',
            relief='ridge',
            bd=2
        )
        self.canvas.pack(side=tk.TOP)
        
        # Create info panel
        self.info_frame = Frame(self.root)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Status labels
        self.status_label = Label(self.info_frame, text="Status: Ready", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Create colormap for congestion visualization
        self.congestion_colors = self._create_congestion_colormap()
        
        # Flag to track if window is closed
        self.is_closed = False
        
    def _create_congestion_colormap(self):
        """Create a colormap for congestion levels (yellow to orange to red)"""
        colors = [(1, 1, 0.7), (1, 0.7, 0), (0.8, 0, 0)]  # Yellow to orange to red
        return LinearSegmentedColormap.from_list('congestion_cmap', colors)
    
    def _get_congestion_color(self, level):
        """Convert congestion level to a color"""
        if level < 0.1:
            return '#d9d9d9'  # Light gray for very low congestion
        
        rgba = self.congestion_colors(level)
        r, g, b = int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _get_building_color(self):
        """Generate a random building color"""
        shade = int(100 + random.random() * 100)  # Shade of gray (100-200)
        return f'#{shade:02x}{shade:02x}{shade:02x}'
    
    def update_display(self, grid, vehicles=None, obstacle_mode=False):
        """Update the display with current grid state
        
        Args:
            grid: The urban grid to display
            vehicles: Optional list of vehicles to display (if None, uses grid.vehicles)
            obstacle_mode: Whether in obstacle placement mode (changes appearance)
        """
        if self.is_closed:
            return
            
        # Clear canvas
        self.canvas.delete("all")
        
        # Use vehicles from parameter if provided, otherwise use grid.vehicles
        if vehicles is not None:
            grid.vehicles = vehicles
        
        # Draw the city grid
        for i in range(grid.size):
            for j in range(grid.size):
                x = i * self.cell_size + self.margin
                y = (grid.size - 1 - j) * self.cell_size + self.margin  # Invert y for proper orientation
                
                # Draw grid indicators when in obstacle mode
                if obstacle_mode:
                    # Draw light grid borders
                    self.canvas.create_rectangle(
                        x - self.cell_size/2, y - self.cell_size/2,
                        x + self.cell_size/2, y + self.cell_size/2,
                        outline='gray70', dash=(4, 4), width=1, fill=''
                    )
                
                # Draw building block (in each grid corner)
                if i > 0 and j > 0:
                    building_color = self._get_building_color()
                    # Add slight offset to buildings to create depth effect
                    self.canvas.create_rectangle(
                        x - self.cell_size + 8, y + 8, 
                        x - 8, y + self.cell_size - 8,
                        fill=building_color,
                        outline='gray20',
                        width=1
                    )
                
                # Draw roads with better visibility
                # Base road layers (slightly wider)
                road_width = self.cell_size/6  # Increased road width for better visibility
                congestion_color = self._get_congestion_color(grid.congestion[i, j])
                
                # Draw optimal paths for vehicles if available
                for vehicle in grid.vehicles:
                    if not vehicle.reached:
                        optimal_path = vehicle.get_remaining_optimal_path()
                        if optimal_path and len(optimal_path) > 1:
                            # Convert path coordinates to canvas coordinates
                            path_coords = []
                            for px, py in optimal_path:
                                cx = px * self.cell_size + self.margin + self.cell_size/2
                                cy = (grid.size - 1 - py) * self.cell_size + self.margin + self.cell_size/2
                                path_coords.extend([cx, cy])
                            
                            # Draw dotted line for optimal path
                            if path_coords:
                                self.canvas.create_line(
                                    path_coords,
                                    fill='blue',
                                    width=2,
                                    dash=(4, 4)  # Create dotted line
                                )
                
                # Horizontal road
                # Base layer
                self.canvas.create_rectangle(
                    x - self.cell_size/2, y - road_width,
                    x + self.cell_size/2, y + road_width,
                    fill='#222222', outline=''
                )
                # Surface layer
                self.canvas.create_rectangle(
                    x - self.cell_size/2 + 2, y - road_width + 2,
                    x + self.cell_size/2 - 2, y + road_width - 2,
                    fill='#444444', outline=''
                )
                # Congestion overlay for horizontal road
                if grid.congestion[i, j] > 0.1:
                    self.canvas.create_rectangle(
                        x - self.cell_size/2 + 2, y - road_width + 2,
                        x + self.cell_size/2 - 2, y + road_width - 2,
                        fill=congestion_color, outline='', stipple='gray50'
                    )
                
                # Vertical road
                # Base layer
                self.canvas.create_rectangle(
                    x - road_width, y - self.cell_size/2,
                    x + road_width, y + self.cell_size/2,
                    fill='#222222', outline=''
                )
                # Surface layer
                self.canvas.create_rectangle(
                    x - road_width + 2, y - self.cell_size/2 + 2,
                    x + road_width - 2, y + self.cell_size/2 - 2,
                    fill='#444444', outline=''
                )
                # Congestion overlay for vertical road
                if grid.congestion[i, j] > 0.1:
                    self.canvas.create_rectangle(
                        x - road_width + 2, y - self.cell_size/2 + 2,
                        x + road_width - 2, y + self.cell_size/2 - 2,
                        fill=congestion_color, outline='', stipple='gray50'
                    )
                

                
                # Draw obstacles
                if grid.obstacles[i, j]:
                    if obstacle_mode:
                        # Enhanced appearance in obstacle mode
                        # Red circle with X mark
                        self.canvas.create_oval(
                            x - self.cell_size/3, y - self.cell_size/3,
                            x + self.cell_size/3, y + self.cell_size/3,
                            fill='#ff6666', outline='red', width=2)
                        # X mark
                        self.canvas.create_line(
                            x - self.cell_size/4, y - self.cell_size/4,
                            x + self.cell_size/4, y + self.cell_size/4,
                            fill='black', width=2)
                        self.canvas.create_line(
                            x - self.cell_size/4, y + self.cell_size/4,
                            x + self.cell_size/4, y - self.cell_size/4,
                            fill='black', width=2)
                    else:
                        # Normal X mark
                        self.canvas.create_line(
                            x - self.cell_size/5, y - self.cell_size/5,
                            x + self.cell_size/5, y + self.cell_size/5,
                            fill='red', width=3)
                        self.canvas.create_line(
                            x - self.cell_size/5, y + self.cell_size/5,
                            x + self.cell_size/5, y - self.cell_size/5,
                            fill='red', width=3)
                    
                    # Caution circle (only in non-obstacle mode)
                    if not obstacle_mode:
                        self.canvas.create_oval(
                            x - self.cell_size/3, y - self.cell_size/3,
                            x + self.cell_size/3, y + self.cell_size/3,
                            outline='orange', width=2)
                
                # Draw traffic lights with improved visibility
                if grid.traffic_lights[i, j] > 0:
                    # Traffic light box shadow
                    self.canvas.create_rectangle(
                        x - self.cell_size/6 + 2, y - self.cell_size/6 + 2,
                        x + self.cell_size/6 + 2, y + self.cell_size/6 + 2,
                        fill='#404040', outline=''
                    )
                    
                    # Traffic light box with metallic effect
                    self.canvas.create_rectangle(
                        x - self.cell_size/6, y - self.cell_size/6,
                        x + self.cell_size/6, y + self.cell_size/6,
                        fill='#808080',
                        outline='#606060',
                        width=2
                    )
                    
                    # Light size and spacing
                    light_radius = max(4, min(8, self.cell_size/10))
                    light_spacing = light_radius * 2.5
                    
                    # North-South green (East-West red)
                    if grid.traffic_lights[i, j] == 1:
                        # NS Green light with glow effect
                        self.canvas.create_oval(
                            x - light_radius - 1, y - light_spacing - 1,
                            x + light_radius + 1, y - light_spacing + 2*light_radius + 1,
                            fill='#004400', outline=''
                        )
                        self.canvas.create_oval(
                            x - light_radius, y - light_spacing,
                            x + light_radius, y - light_spacing + 2*light_radius,
                            fill='#00ff00', outline='#008800'
                        )
                        
                        # EW Red light
                        self.canvas.create_oval(
                            x + light_spacing - light_radius, y - light_radius,
                            x + light_spacing + light_radius, y + light_radius,
                            fill='#ff0000', outline='#800000'
                        )
                    # East-West green (North-South red)
                    else:
                        # NS Red light
                        self.canvas.create_oval(
                            x - light_radius, y - light_spacing,
                            x + light_radius, y - light_spacing + 2*light_radius,
                            fill='#ff0000', outline='#800000'
                        )
                        
                        # EW Green light with glow effect
                        self.canvas.create_oval(
                            x + light_spacing - light_radius - 1, y - light_radius - 1,
                            x + light_spacing + light_radius + 1, y + light_radius + 1,
                            fill='#004400', outline=''
                        )
                        self.canvas.create_oval(
                            x + light_spacing - light_radius, y - light_radius,
                            x + light_spacing + light_radius, y + light_radius,
                            fill='#00ff00', outline='#008800'
                        )

        
        # Draw vehicles and destinations
        if hasattr(grid, 'vehicles') and grid.vehicles:
            for v in grid.vehicles:
                if not hasattr(v, 'position') or not hasattr(v, 'destination'):
                    continue
                    
                # Draw vehicle
                vx = v.position[0] * self.cell_size + self.margin
                vy = (grid.size - 1 - v.position[1]) * self.cell_size + self.margin
                
                # Draw optimal path if available
                if hasattr(v, 'optimal_path') and v.optimal_path:
                    for i in range(len(v.optimal_path) - 1):
                        p1 = v.optimal_path[i]
                        p2 = v.optimal_path[i + 1]
                        x1 = p1[0] * self.cell_size + self.margin
                        y1 = (grid.size - 1 - p1[1]) * self.cell_size + self.margin
                        x2 = p2[0] * self.cell_size + self.margin
                        y2 = (grid.size - 1 - p2[1]) * self.cell_size + self.margin
                        # Draw path segments with dotted line
                        self.canvas.create_line(
                            x1, y1, x2, y2,
                            fill='#4CAF50',  # Light green color
                            width=2,
                            dash=(5, 3)  # Dotted line pattern
                        )
                
                # Car shadow (for depth effect)
                self.canvas.create_rectangle(
                    vx - self.cell_size/6 + 2, vy - self.cell_size/10 + 2,
                    vx + self.cell_size/6 + 2, vy + self.cell_size/10 + 2,
                    fill='#000033', outline=''
                )
                
                # Car body with outline
                self.canvas.create_rectangle(
                    vx - self.cell_size/6, vy - self.cell_size/10,
                    vx + self.cell_size/6, vy + self.cell_size/10,
                    fill='#0066cc', outline='#003366', width=1
                )
                
                # Car windows with slight depth effect
                self.canvas.create_rectangle(
                    vx - self.cell_size/12, vy - self.cell_size/15,
                    vx + self.cell_size/12, vy + self.cell_size/15,
                    fill='#99ccff', outline='#6699cc', width=1
                )
                
                # Display vehicle ID with better visibility
                self.canvas.create_text(
                    vx, vy,
                    text=str(v.id),
                    font=("Arial", max(10, int(self.cell_size/4))),
                    fill='white'
                )
                
                # Draw destination
                dx = v.destination[0] * self.cell_size + self.margin
                dy = (grid.size - 1 - v.destination[1]) * self.cell_size + self.margin
                
                # Star shape for destination - yellow if reached, green otherwise
                star_color = 'yellow' if v.reached else 'limegreen'
                self.canvas.create_text(
                    dx, dy, 
                    text="★", 
                    font=("Arial", int(self.cell_size/2)), 
                    fill=star_color)
                
                # Display destination ID
                self.canvas.create_text(
                    dx, dy + self.cell_size/4,
                    text=str(v.id),
                    font=("Arial", int(self.cell_size/4)),
                    fill='black'
                )
                
                # Display start position
                sx = v.start_position[0] * self.cell_size
                sy = (grid.size - 1 - v.start_position[1]) * self.cell_size
                
                # Draw start position marker (circle)
                self.canvas.create_oval(
                    sx - self.cell_size/6, sy - self.cell_size/6,
                    sx + self.cell_size/6, sy + self.cell_size/6,
                    fill='orange', outline='black'
                )
                
                # Display start position ID
                self.canvas.create_text(
                    sx, sy,
                    text=str(v.id),
                    font=("Arial", int(self.cell_size/4)),
                    fill='black'
                )
        
        # Update info
        status_text = f"Step: {getattr(grid, 'current_step', 0)}"
        if obstacle_mode:
            status_text += " | 障礙物放置模式：點擊放置或移除障礙物"
            self.status_label.config(text=status_text, foreground="red", font=("Arial", 10, "bold"))
        else:
            self.status_label.config(text=status_text, foreground="black", font=("Arial", 10))
        
        # Update the window
        self.root.update()
    
    def on_closing(self):
        """Handle window closing"""
        self.is_closed = True
        self.root.destroy()
        
    def close(self):
        """Close the visualization window"""
        if not self.is_closed and self.root.winfo_exists():
            self.root.destroy()
            self.is_closed = True
