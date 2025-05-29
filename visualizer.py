import tkinter as tk
from tkinter import Canvas, Frame, Label
import random
from matplotlib.colors import LinearSegmentedColormap

class TkinterVisualizer:
    def __init__(self, grid_size=10, cell_size=50):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Urban Grid Q-Learning Simulation")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create canvas for drawing
        self.canvas = Canvas(self.root, width=self.window_size, height=self.window_size, bg='#d9d9d9')
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        
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
    
    def update_display(self, grid):
        """Update the display with current grid state"""
        if self.is_closed:
            return
            
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw the city grid
        for i in range(grid.size):
            for j in range(grid.size):
                x = i * self.cell_size
                y = (grid.size - 1 - j) * self.cell_size  # Invert y for proper orientation
                
                # Draw building block (in each grid corner)
                if i > 0 and j > 0:
                    building_color = self._get_building_color()
                    self.canvas.create_rectangle(
                        x - self.cell_size + 5, y + 5, 
                        x - 5, y + self.cell_size - 5,
                        fill=building_color, outline='')
                
                # Draw roads
                # Horizontal road
                congestion_color_h = self._get_congestion_color(grid.congestion[i, j])
                self.canvas.create_rectangle(
                    x - self.cell_size/2, y - self.cell_size/10, 
                    x + self.cell_size/2, y + self.cell_size/10,
                    fill='#444444', outline='')
                
                # Add congestion overlay if significant
                if grid.congestion[i, j] > 0.1:
                    self.canvas.create_rectangle(
                        x - self.cell_size/2, y - self.cell_size/10, 
                        x + self.cell_size/2, y + self.cell_size/10,
                        fill=congestion_color_h, outline='', stipple='gray50')
                
                # Vertical road
                self.canvas.create_rectangle(
                    x - self.cell_size/10, y - self.cell_size/2, 
                    x + self.cell_size/10, y + self.cell_size/2,
                    fill='#444444', outline='')
                
                # Add congestion overlay if significant
                if grid.congestion[i, j] > 0.1:
                    self.canvas.create_rectangle(
                        x - self.cell_size/10, y - self.cell_size/2, 
                        x + self.cell_size/10, y + self.cell_size/2,
                        fill=congestion_color_h, outline='', stipple='gray50')
                
                # Draw obstacles
                if grid.obstacles[i, j]:
                    # X mark
                    self.canvas.create_line(
                        x - self.cell_size/5, y - self.cell_size/5,
                        x + self.cell_size/5, y + self.cell_size/5,
                        fill='red', width=3)
                    self.canvas.create_line(
                        x - self.cell_size/5, y + self.cell_size/5,
                        x + self.cell_size/5, y - self.cell_size/5,
                        fill='red', width=3)
                    # Caution circle
                    self.canvas.create_oval(
                        x - self.cell_size/3, y - self.cell_size/3,
                        x + self.cell_size/3, y + self.cell_size/3,
                        outline='orange', width=2)
                
                # Draw traffic lights
                if grid.traffic_lights[i, j] > 0:
                    # Traffic light box
                    self.canvas.create_rectangle(
                        x - self.cell_size/6, y - self.cell_size/6,
                        x + self.cell_size/6, y + self.cell_size/6,
                        fill='gray', outline='')
                    
                    # North-South green (East-West red)
                    if grid.traffic_lights[i, j] == 1:
                        self.canvas.create_oval(
                            x - 5, y + 5,
                            x + 5, y + 15,
                            fill='green', outline='')
                        self.canvas.create_oval(
                            x + 5, y - 5,
                            x + 15, y + 5,
                            fill='red', outline='')
                    # East-West green (North-South red)
                    else:
                        self.canvas.create_oval(
                            x - 5, y + 5,
                            x + 5, y + 15,
                            fill='red', outline='')
                        self.canvas.create_oval(
                            x + 5, y - 5,
                            x + 15, y + 5,
                            fill='green', outline='')
        
        # Draw vehicles and destinations
        if hasattr(grid, 'vehicles') and grid.vehicles:
            for v in grid.vehicles:
                if not hasattr(v, 'position') or not hasattr(v, 'destination'):
                    continue
                    
                # Draw vehicle
                vx = v.position[0] * self.cell_size
                vy = (grid.size - 1 - v.position[1]) * self.cell_size
                
                # Car body
                self.canvas.create_rectangle(
                    vx - self.cell_size/6, vy - self.cell_size/10,
                    vx + self.cell_size/6, vy + self.cell_size/10,
                    fill='blue', outline='')
                # Car windows
                self.canvas.create_rectangle(
                    vx - self.cell_size/12, vy - self.cell_size/15,
                    vx + self.cell_size/12, vy + self.cell_size/15,
                    fill='lightblue', outline='')
                
                # Draw destination
                dx = v.destination[0] * self.cell_size
                dy = (grid.size - 1 - v.destination[1]) * self.cell_size
                
                # Star shape for destination
                self.canvas.create_text(
                    dx, dy, 
                    text="★", 
                    font=("Arial", int(self.cell_size/2)), 
                    fill='limegreen')
        
        # Update info
        self.status_label.config(text=f"Step: {getattr(grid, 'current_step', 0)}")
        
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
