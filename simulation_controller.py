"""
Simulation Controller for Q-Learning Urban Traffic Simulation
This module provides interactive controls for simulating vehicle mo        # Obstacle buttons
        obstacle_frame = ttk.Fr        # Apply button
        ttk.Button(param_frame, text="Apply", command=self.apply_q_params).grid(row=1, column=2, padx=5, rowspan=1)
        
        param_frame.columnconfigure(0, weight=1)
        
        # Congestion adjustment controls
        congestion_frame = ttk.LabelFrame(control_frame, text="Congestion Controls", padding="10")
        congestion_frame.pack(fill=tk.X, pady=5)
        
        # Congestion level slider
        cong_control_frame = ttk.Frame(congestion_frame)
        cong_control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cong_control_frame, text="Congestion Level:").grid(row=0, column=0, padx=5, sticky="w")
        self.congestion_var = tk.DoubleVar(value=self.congestion_level)
        congestion_slider = ttk.Scale(
            cong_control_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
            variable=self.congestion_var, command=self.update_congestion_level
        )
        congestion_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.congestion_label = ttk.Label(cong_control_frame, text=f"{self.congestion_level:.2f}")
        self.congestion_label.grid(row=0, column=2, padx=5)
        
        # Congestion adjustment radius
        ttk.Label(cong_control_frame, text="Adjustment Radius:").grid(row=1, column=0, padx=5, sticky="w")
        self.congestion_radius_var = tk.IntVar(value=2)
        radius_slider = ttk.Scale(
            cong_control_frame, from_=1, to=5, orient=tk.HORIZONTAL,
            variable=self.congestion_radius_var, command=self.update_congestion_radius
        )
        radius_slider.grid(row=1, column=1, sticky="ew", padx=5)
        self.radius_label = ttk.Label(cong_control_frame, text="2")
        self.radius_label.grid(row=1, column=2, padx=5)
        
        # Clear congestion button
        ttk.Button(cong_control_frame, text="Clear All Congestion", 
                  command=self.clear_all_congestion).grid(row=2, column=0, columnspan=3, pady=5)
        
        cong_control_frame.columnconfigure(1, weight=1)agent_frame)
        obstacle_frame.pack(side=tk.RIGHT)
        
        ttk.Button(obstacle_frame, text="Add Random Obstacles", 
                  command=self.add_random_obstacles).pack(side=tk.RIGHT, padx=5)
                  
        # Obstacle mode toggle button
        self.obstacle_mode_btn = ttk.Button(obstacle_frame, text="Obstacle Mode", 
                                          command=self.toggle_obstacle_mode)
        self.obstacle_mode_btn.pack(side=tk.RIGHT, padx=5)
        
        # Congestion mode toggle button
        self.congestion_mode_btn = ttk.Button(obstacle_frame, text="Congestion Mode", 
                                            command=self.toggle_congestion_mode)
        self.congestion_mode_btn.pack(side=tk.RIGHT, padx=5)d on a trained Q-learning agent.
"""
import tkinter as tk
import numpy as np
import time
from tkinter import ttk, filedialog, messagebox
from urban_grid import UrbanGrid
from vehicle import Vehicle
from agent import QLearningAgent
from reward_config import RewardConfig
import pickle
import json

class SimulationController:
    def __init__(self, trained_agent=None):
        """Initialize the simulation controller with a trained agent.
        
        Args:
            trained_agent: A pre-trained QLearningAgent instance.
                           If None, will prompt to load a saved agent.
        """
        self.agent = trained_agent
        self.urban_grid = None
        if self.agent:
            self.urban_grid = self.agent.urban_grid
        
        # Simulation variables
        self.vehicles = []
        self.running = False
        self.paused = False
        self.step_delay = 500  # milliseconds between steps (default 0.5 sec)
        self.current_step = 0
        self.max_steps = 100
        
        # Store default Q-learning values but create StringVars after Tk initialization
        self.default_learning_rate = "0.2"
        self.default_discount_factor = "0.95"
        self.default_epsilon = "0.2"
        
        # Obstacle mode variables
        self.obstacle_mode = False  # Flag for obstacle placement mode
        
        # Congestion adjustment mode variables
        self.congestion_mode = False  # Flag for congestion adjustment mode
        self.congestion_level = 0.5  # Default congestion level (0.0 to 1.0)
        
        # Reward configuration
        self.reward_config = RewardConfig()
        
        # Create GUI window
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components for simulation control"""
        self.root = tk.Tk()
        self.root.title("Q-Learning Traffic Simulation Controller")
        self.root.geometry("800x650")
        
        # Now that Tk is initialized, create the StringVars
        self.learning_rate = tk.StringVar(value=self.default_learning_rate)
        self.discount_factor = tk.StringVar(value=self.default_discount_factor)
        self.epsilon = tk.StringVar(value=self.default_epsilon)
        
        # Create a custom style for buttons
        style = ttk.Style()
        # Create an accent button style for toggle buttons
        style.configure("Accent.TButton", background="#4CAF50", foreground="white", 
                      font=('Arial', 10, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel (top)
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Step control
        step_frame = ttk.Frame(control_frame)
        step_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(step_frame, text="Step Delay (ms):").grid(row=0, column=0, padx=5)
        self.delay_var = tk.IntVar(value=self.step_delay)
        delay_slider = ttk.Scale(
            step_frame, from_=4, to=2000, orient=tk.HORIZONTAL, 
            variable=self.delay_var, command=self.update_delay
        )
        delay_slider.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(step_frame, textvariable=self.delay_var).grid(row=0, column=2, padx=5)
        
        # Max steps
        ttk.Label(step_frame, text="Max Steps:").grid(row=1, column=0, padx=5)
        self.max_steps_var = tk.IntVar(value=self.max_steps)
        max_steps_slider = ttk.Scale(
            step_frame, from_=10, to=5000, orient=tk.HORIZONTAL, 
            variable=self.max_steps_var, command=self.update_max_steps
        )
        max_steps_slider.grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(step_frame, textvariable=self.max_steps_var).grid(row=1, column=2, padx=5)
        
        # Unlimited steps checkbox
        self.unlimited_steps_var = tk.BooleanVar(value=False)
        unlimited_check = ttk.Checkbutton(
            step_frame, text="Unlimited Steps (until all vehicles reach destination)", 
            variable=self.unlimited_steps_var,
            command=self.toggle_unlimited_steps
        )
        unlimited_check.grid(row=2, column=0, columnspan=3, sticky="w", padx=5)
        
        step_frame.columnconfigure(1, weight=1)
        
        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(btn_frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn.config(state="disabled")
        
        self.step_btn = ttk.Button(btn_frame, text="Single Step", command=self.step_simulation)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Agent options
        agent_frame = ttk.Frame(control_frame)
        agent_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(agent_frame, text="Load Agent", command=self.load_agent).pack(side=tk.LEFT, padx=5)
        ttk.Button(agent_frame, text="Save Agent", command=self.save_agent).pack(side=tk.LEFT, padx=5)
        
        # Obstacle buttons
        obstacle_frame = ttk.Frame(agent_frame)
        obstacle_frame.pack(side=tk.RIGHT)
        
        ttk.Button(obstacle_frame, text="Add Random Obstacles", 
                  command=self.add_random_obstacles).pack(side=tk.RIGHT, padx=5)
                  
        # Obstacle mode toggle button
        self.obstacle_mode_btn = ttk.Button(obstacle_frame, text="Obstacle Mode", 
                                          command=self.toggle_obstacle_mode)
        self.obstacle_mode_btn.pack(side=tk.RIGHT, padx=5)
        
        # Congestion mode toggle button
        self.congestion_mode_btn = ttk.Button(obstacle_frame, text="Congestion Mode", 
                                            command=self.toggle_congestion_mode)
        self.congestion_mode_btn.pack(side=tk.RIGHT, padx=5)
        
        # Number of vehicles
        veh_frame = ttk.Frame(control_frame)
        veh_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(veh_frame, text="Vehicles:").pack(side=tk.LEFT, padx=5)
        self.num_vehicles_var = tk.IntVar(value=5)
        ttk.Spinbox(veh_frame, from_=1, to=20, width=5, 
                   textvariable=self.num_vehicles_var).pack(side=tk.LEFT, padx=5)
        
        # Q-learning parameters
        qlearn_frame = ttk.LabelFrame(control_frame, text="Q-Learning parameter", padding="10")
        qlearn_frame.pack(fill=tk.X, pady=5)
        
        # Parameter entries row
        param_frame = ttk.Frame(qlearn_frame)
        param_frame.pack(fill=tk.X, pady=5)
        
        # Learning Rate
        ttk.Label(param_frame, text="Learning Rate:").grid(row=0, column=0, padx=5, sticky="w")
        self.lr_entry = ttk.Entry(param_frame, width=8, textvariable=self.learning_rate)
        self.lr_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        # Discount Factor
        ttk.Label(param_frame, text="Discount Factor:").grid(row=1, column=0, padx=5, sticky="w")
        self.df_entry = ttk.Entry(param_frame, width=8, textvariable=self.discount_factor)
        self.df_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        # Epsilon
        ttk.Label(param_frame, text="Epsilon:").grid(row=2, column=0, padx=5, sticky="w")
        self.eps_entry = ttk.Entry(param_frame, width=8, textvariable=self.epsilon)
        self.eps_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        
        # Apply button
        ttk.Button(param_frame, text="Apply", command=self.apply_q_params).grid(row=1, column=2, padx=5, rowspan=1)
        
        param_frame.columnconfigure(0, weight=1)
        
        # Reward Configuration panel
        self.setup_reward_config_gui(control_frame)
        
        # Congestion adjustment controls
        congestion_frame = ttk.LabelFrame(control_frame, text="Congestion Controls", padding="10")
        congestion_frame.pack(fill=tk.X, pady=5)
        
        # Congestion level slider
        cong_control_frame = ttk.Frame(congestion_frame)
        cong_control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cong_control_frame, text="Congestion Level:").grid(row=0, column=0, padx=5, sticky="w")
        self.congestion_var = tk.DoubleVar(value=self.congestion_level)
        congestion_slider = ttk.Scale(
            cong_control_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL,
            variable=self.congestion_var, command=self.update_congestion_level
        )
        congestion_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.congestion_label = ttk.Label(cong_control_frame, text=f"{self.congestion_level:.2f}")
        self.congestion_label.grid(row=0, column=2, padx=5)
        
        # Congestion adjustment radius
        ttk.Label(cong_control_frame, text="Adjustment Radius:").grid(row=1, column=0, padx=5, sticky="w")
        self.congestion_radius_var = tk.IntVar(value=2)
        radius_slider = ttk.Scale(
            cong_control_frame, from_=1, to=5, orient=tk.HORIZONTAL,
            variable=self.congestion_radius_var, command=self.update_congestion_radius
        )
        radius_slider.grid(row=1, column=1, sticky="ew", padx=5)
        self.radius_label = ttk.Label(cong_control_frame, text="2")
        self.radius_label.grid(row=1, column=2, padx=5)
        
        # Clear congestion button
        ttk.Button(cong_control_frame, text="Clear All Congestion", 
                  command=self.clear_all_congestion).grid(row=2, column=0, columnspan=3, pady=5)
        
        cong_control_frame.columnconfigure(1, weight=1)
        
        # Status panel
        status_frame = ttk.LabelFrame(main_frame, text="Simulation Status", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_text = tk.Text(status_frame, height=5, width=70, wrap=tk.WORD, state="disabled")
        self.status_text.pack(fill=tk.X)
        
        # Bottom controls
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Label(bottom_frame, text="Step: ").pack(side=tk.LEFT)
        self.step_label = ttk.Label(bottom_frame, text="0")
        self.step_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(bottom_frame, text="Completed: ").pack(side=tk.LEFT, padx=(20, 0))
        self.completed_label = ttk.Label(bottom_frame, text="0/0")
        self.completed_label.pack(side=tk.LEFT, padx=10)
        
        # Close behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def update_status(self, message):
        """Update the status text box"""
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update()
    
    def update_delay(self, val):
        """Update step delay"""
        self.step_delay = int(float(val))
        
    def update_max_steps(self, val):
        """Update maximum steps"""
        self.max_steps = int(float(val))
        
    def toggle_unlimited_steps(self):
        """Toggle unlimited steps mode"""
        unlimited = self.unlimited_steps_var.get()
        if unlimited:
            self.update_status("unlimited steps mode enabled: simulation will run until all vehicles reach their destination")
        else:
            self.update_status(f"set step limit to : {self.max_steps}")
            
        # Enable slider if limited steps, otherwise disable slider
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Scale) and widget.winfo_name() == "max_steps_slider":
                widget.configure(state="disabled" if unlimited else "normal")
    
    def load_agent(self):
        """Load a saved agent from file"""
        if self.running:
            self.update_status("Can't load agent while simulation is running")
            return
            
        try:
            filename = filedialog.askopenfilename(
                title="Load Trained Agent",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'rb') as f:
                    self.agent = pickle.load(f)
                
                # Make sure urban_grid is properly initialized
                if not hasattr(self.agent, 'urban_grid') or self.agent.urban_grid is None:
                    from urban_grid import UrbanGrid
                    self.agent.urban_grid = UrbanGrid(
                        size=self.agent.grid_size,
                        congestion_update_rate=self.agent.grid_congestion_update_rate,
                        traffic_light_cycle=self.agent.grid_traffic_light_cycle
                    )
                
                self.urban_grid = self.agent.urban_grid
                self.update_status(f"Agent loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load agent: {str(e)}")
            self.update_status(f"Error loading agent: {str(e)}")
    
    def save_agent(self):
        """Save current agent to file"""
        if not self.agent:
            self.update_status("No agent to save")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Agent",
                defaultextension=".pkl",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            
            if filename:
                # Prepare agent for saving (remove tkinter objects)
                visualizer_backup = self.agent.prepare_for_save()
                
                # Save to file
                with open(filename, 'wb') as f:
                    pickle.dump(self.agent, f)
                
                # Restore agent after saving
                self.agent.restore_after_save(visualizer_backup)
                self.update_status(f"Agent saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save agent: {str(e)}")
            self.update_status(f"Error saving agent: {str(e)}")
    
    def apply_q_params(self):
        """Apply Q-learning parameters to the current agent"""
        if not self.agent:
            self.update_status("Have to setup q-learning parameters when no agent loaded")
            return
            
        try:
            # Convert string vars to float
            lr = float(self.learning_rate.get())
            df = float(self.discount_factor.get())
            eps = float(self.epsilon.get())
            
            # Validate parameters
            if not (0 < lr <= 1) or not (0 < df <= 1) or not (0 <= eps <= 1):
                self.update_status("must between 0 and 1")
                return
                
            # Update agent parameters
            self.agent.learning_rate = lr
            self.agent.discount_factor = df
            self.agent.epsilon = eps
            self.update_status(f"Q-learning parameters: LR={lr}, DF={df}, EPS={eps}")
        except ValueError:
            self.update_status("must be available float values")
    
    def create_new_agent(self):
        """Create a new agent when none is loaded"""
        grid_size = 20  # Default size
        self.urban_grid = UrbanGrid(size=grid_size)
        
        try:
            # Get parameter values from UI
            lr = float(self.learning_rate.get())
            df = float(self.discount_factor.get())
            eps = float(self.epsilon.get())
            
            # Validate parameters
            if not (0 < lr <= 1) or not (0 < df <= 1) or not (0 <= eps <= 1):
                self.update_status("must between 0 and 1")
                self.agent = QLearningAgent(self.urban_grid)
            else:
                # Create agent with specified parameters
                self.agent = QLearningAgent(self.urban_grid, learning_rate=lr, 
                                           discount_factor=df, epsilon=eps)
                self.update_status(f"new agent created: LR={lr}, DF={df}, EPS={eps}")
        except ValueError:
            # If there's an error parsing parameters, use defaults
            self.update_status("value error in Q-learning parameters, using defaults")
            self.agent = QLearningAgent(self.urban_grid)
    
    def start_simulation(self):
        """Start or resume the simulation"""
        if not self.agent:
            if messagebox.askyesno("No Agent", "No agent loaded. Create new untrained agent?"):
                self.create_new_agent()
            else:
                return
        
        if not self.vehicles or not self.running:
            # New simulation
            self.reset_simulation()
            self.initialize_vehicles()
            self.running = True
            self.paused = False
            self.update_status("Simulation started")
            
            # Lock Q-learning parameter inputs
            self.lr_entry.config(state="disabled")
            self.df_entry.config(state="disabled")
            self.eps_entry.config(state="disabled")
        else:
            # Resume paused simulation
            self.paused = False
            self.update_status("Simulation resumed")
        
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal", text="Pause")
        
        # Start simulation loop
        self.run_simulation_step()
    
    def toggle_pause(self):
        """Toggle the paused state of the simulation"""
        if not self.running:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            self.pause_btn.config(text="Resume")
            self.update_status("Simulation paused")
        else:
            # If we're in obstacle mode, exit obstacle mode when resuming
            if self.obstacle_mode:
                self.toggle_obstacle_mode()  # Turn off obstacle mode
                
            # If we're in congestion mode, exit congestion mode when resuming
            if self.congestion_mode:
                self.toggle_congestion_mode()  # Turn off congestion mode
                
            self.pause_btn.config(text="Pause")
            self.update_status("Simulation resumed")
            
            # Update optimal paths for all vehicles since obstacles may have been modified
            for vehicle in self.vehicles:
                if not vehicle.reached:
                    vehicle.update_optimal_path()
                    
            self.run_simulation_step()
    
    def step_simulation(self):
        """Run a single step of the simulation"""
        if not self.agent:
            if messagebox.askyesno("No Agent", "No agent loaded. Create new untrained agent?"):
                self.create_new_agent()
            else:
                return
                
        if not self.vehicles:
            self.initialize_vehicles()
            self.running = True
            self.paused = True
        
        # Single step logic
        if self.current_step < self.max_steps:
            self.perform_simulation_step()
        
        self.pause_btn.config(text="Resume")
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
    
    def reset_simulation(self):
        """Reset the simulation to initial state"""
        self.running = False
        self.paused = False
        self.current_step = 0
        self.vehicles = []
        
        # Reset urban grid
        if self.urban_grid:
            self.urban_grid.reset_congestion()
            self.urban_grid.current_step = 0
            
            # Clear obstacles
            self.urban_grid.obstacles = np.zeros((self.urban_grid.size, self.urban_grid.size), dtype=bool)
        
        # Update UI
        self.step_label.config(text=str(self.current_step))
        self.completed_label.config(text="0/0")
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        
        # Unlock Q-learning parameter inputs
        self.lr_entry.config(state="normal")
        self.df_entry.config(state="normal")
        self.eps_entry.config(state="normal")
        
        self.update_status("Simulation reset")
    
    def initialize_vehicles(self):
        """Create vehicles for simulation"""
        if not self.urban_grid or not self.agent:
            self.update_status("Cannot initialize vehicles: No agent or grid")
            return
        
        # Get number of vehicles
        num_vehicles = self.num_vehicles_var.get()
        
        # Reset vehicle ID counter
        from vehicle import Vehicle
        Vehicle.next_id = 1
        
        # Create vehicles
        self.vehicles = []
        for _ in range(num_vehicles):
            vehicle = Vehicle(self.urban_grid, self.agent, reward_config=self.reward_config)
            self.vehicles.append(vehicle)
        
        self.update_status(f"Created {num_vehicles} vehicles")
        self.completed_label.config(text=f"0/{num_vehicles}")
    
    def update_congestion_level(self, val):
        """Update congestion level from slider"""
        self.congestion_level = float(val)
        self.congestion_label.config(text=f"{self.congestion_level:.2f}")
        
    def update_congestion_radius(self, val):
        """Update congestion adjustment radius from slider"""
        radius = int(float(val))
        self.radius_label.config(text=str(radius))
        
    def clear_all_congestion(self):
        """Clear all congestion from the grid"""
        if not self.urban_grid:
            self.update_status("No grid available")
            return
            
        self.urban_grid.congestion = np.zeros((self.urban_grid.size, self.urban_grid.size))
        self.update_status("Cleared all area congestion")
        
        # Update visualization
        if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
            self.urban_grid.visualize(self.vehicles, show_plot=True)

    def toggle_congestion_mode(self):
        """Toggle the congestion adjustment mode"""
        if not self.urban_grid:
            self.update_status("No grid available")
            return
            
        # Can only toggle congestion mode when paused or not running
        if self.running and not self.paused:
            self.update_status("Must pause before entering Congestion Mode")
            return
            
        # If in obstacle mode, exit it first
        if self.obstacle_mode:
            self.toggle_obstacle_mode()
            
        # Toggle congestion mode
        self.congestion_mode = not self.congestion_mode
        
        # Update button text and appearance
        if self.congestion_mode:
            self.congestion_mode_btn.config(text="Exit Congestion Mode", style="Accent.TButton")
            self.update_status("Congestion Mode enabled: Click on map to adjust regional congestion level")
            
            # Set up the canvas click handler in visualizer
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.bind("<Button-1>", self.on_congestion_click)
                
                # Update visualization to show it's in congestion mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles, congestion_mode=True)
        else:
            self.congestion_mode_btn.config(text="Congestion Mode", style="TButton")
            self.update_status("Exited Congestion Mode")
            
            # Remove the canvas click handler
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.unbind("<Button-1>")
                
                # Update visualization to normal mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles)
    
    def on_congestion_click(self, event):
        """Handle canvas clicks to adjust congestion"""
        if not self.congestion_mode or not self.urban_grid or not hasattr(self.urban_grid, 'visualizer'):
            return
            
        # Convert click coordinates to grid coordinates
        canvas = self.urban_grid.visualizer.canvas
        cell_size = self.urban_grid.visualizer.cell_size
        margin = self.urban_grid.visualizer.margin
        
        # Calculate grid coordinates
        x_pos = int((event.x - margin) / cell_size)
        y_pos = int(self.urban_grid.size - 1 - ((event.y - margin) / cell_size))
        
        # Ensure coordinates are within grid bounds
        if 0 <= x_pos < self.urban_grid.size and 0 <= y_pos < self.urban_grid.size:
            # Apply congestion to the area around the clicked position
            radius = self.congestion_radius_var.get()
            congestion_level = self.congestion_level
            
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    new_x = x_pos + dx
                    new_y = y_pos + dy
                    
                    # Check bounds
                    if 0 <= new_x < self.urban_grid.size and 0 <= new_y < self.urban_grid.size:
                        # Calculate distance from center for smooth falloff
                        distance = np.sqrt(dx*dx + dy*dy)
                        if distance <= radius:
                            # Apply smooth falloff
                            falloff = max(0, 1 - distance / radius)
                            self.urban_grid.congestion[new_x, new_y] = congestion_level * falloff
            
            self.update_status(f"Added obstacle at position ({x_pos}, {y_pos}) with surrounding congestion level {congestion_level:.2f}")
            
            # Update visualization
            self.urban_grid.visualize(self.vehicles, show_plot=True, congestion_mode=True)

    def toggle_obstacle_mode(self):
        """Toggle the obstacle placement mode"""
        if not self.urban_grid:
            self.update_status("No grid available")
            return
            
        # Can only toggle obstacle mode when paused or not running
        if self.running and not self.paused:
            self.update_status("Must pause before entering Obstacle Mode")
            return
            
        # If in congestion mode, exit it first
        if self.congestion_mode:
            self.toggle_congestion_mode()
            
        # Toggle obstacle mode
        self.obstacle_mode = not self.obstacle_mode
        
        # Update button text and appearance
        if self.obstacle_mode:
            self.obstacle_mode_btn.config(text="Exit Obstacle Mode", style="Accent.TButton")
            self.update_status("Obstacle Mode enabled: Click on map to add or remove obstacles")
            
            # Set up the canvas click handler in visualizer
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.bind("<Button-1>", self.on_canvas_click)
                
                # Update visualization to show it's in obstacle mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles, obstacle_mode=True)
        else:
            self.obstacle_mode_btn.config(text="Obstacle Mode", style="TButton")
            self.update_status("Exited Obstacle Mode")
            
            # Remove the canvas click handler
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.unbind("<Button-1>")
                
                # Update visualization to normal mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles)
    
    def on_canvas_click(self, event):
        """Handle canvas clicks to add/remove obstacles"""
        if not self.obstacle_mode or not self.urban_grid or not hasattr(self.urban_grid, 'visualizer'):
            return
            
        # Convert click coordinates to grid coordinates
        canvas = self.urban_grid.visualizer.canvas
        cell_size = self.urban_grid.visualizer.cell_size
        margin = self.urban_grid.visualizer.margin
        
        # Calculate grid coordinates
        x_pos = int((event.x - margin) / cell_size)
        y_pos = int(self.urban_grid.size - 1 - ((event.y - margin) / cell_size))
        
        # Ensure coordinates are within grid bounds
        if 0 <= x_pos < self.urban_grid.size and 0 <= y_pos < self.urban_grid.size:
            # Toggle obstacle at this position
            if self.urban_grid.obstacles[x_pos, y_pos]:
                self.urban_grid.remove_obstacle(x_pos, y_pos)
                self.update_status(f"Removed obstacle at position ({x_pos}, {y_pos}) ")
            else:
                self.urban_grid.add_obstacle(x_pos, y_pos)
                self.update_status(f"Added obstacle at position ({x_pos}, {y_pos}) ")
            
            # Update vehicles' optimal paths if needed
            for vehicle in self.vehicles:
                if not vehicle.reached:
                    vehicle.update_optimal_path()
            
            # Update visualization
            self.urban_grid.visualize(self.vehicles, show_plot=True)
        """Toggle the obstacle placement mode"""
        if not self.urban_grid:
            self.update_status("No grid available")
            return
            
        # Can only toggle obstacle mode when paused or not running
        if self.running and not self.paused:
            self.update_status("must stop to eneter place obstacle mode")
            return
            
        # Toggle obstacle mode
        self.obstacle_mode = not self.obstacle_mode
        
        # Update button text and appearance
        if self.obstacle_mode:
            self.obstacle_mode_btn.config(text="exit place obstacle mode", style="Accent.TButton")
            self.update_status("entered place obstacle mode：click to add/remove obstacles")
            
            # Set up the canvas click handler in visualizer
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.bind("<Button-1>", self.on_canvas_click)
                
                # Update visualization to show it's in obstacle mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles, obstacle_mode=True)
        else:
            self.obstacle_mode_btn.config(text="place obstacle mode", style="TButton")
            self.update_status("exit place obstacle mode")
            
            # Remove the canvas click handler
            if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
                self.urban_grid.visualizer.canvas.unbind("<Button-1>")
                
                # Update visualization to normal mode
                self.urban_grid.visualizer.update_display(self.urban_grid, self.vehicles)
    
    def on_canvas_click(self, event):
        """Handle canvas clicks to add/remove obstacles"""
        if not self.obstacle_mode or not self.urban_grid or not hasattr(self.urban_grid, 'visualizer'):
            return
            
        # Convert click coordinates to grid coordinates
        canvas = self.urban_grid.visualizer.canvas
        cell_size = self.urban_grid.visualizer.cell_size
        margin = self.urban_grid.visualizer.margin
        
        # Calculate grid coordinates
        x_pos = int((event.x - margin) / cell_size)
        y_pos = int(self.urban_grid.size - 1 - ((event.y - margin) / cell_size))
        
        # Ensure coordinates are within grid bounds
        if 0 <= x_pos < self.urban_grid.size and 0 <= y_pos < self.urban_grid.size:
            # Toggle obstacle at this position
            if self.urban_grid.obstacles[x_pos, y_pos]:
                self.urban_grid.remove_obstacle(x_pos, y_pos)
                self.update_status(f"removed ({x_pos}, {y_pos}) 's obstacle")
            else:
                self.urban_grid.add_obstacle(x_pos, y_pos)
                self.update_status(f"added ({x_pos}, {y_pos}) 's obstacle")
            
            # Update vehicles' optimal paths if needed
            for vehicle in self.vehicles:
                if not vehicle.reached:
                    vehicle.update_optimal_path()
            
            # Update visualization
            self.urban_grid.visualize(self.vehicles, show_plot=True)

    def add_random_obstacles(self):
        """Add random obstacles to the grid"""
        if not self.urban_grid:
            self.update_status("No grid available")
            return
            
        # Clear existing obstacles
        self.urban_grid.obstacles = np.zeros((self.urban_grid.size, self.urban_grid.size), dtype=bool)
        
        # Add new random obstacles (5% of grid)
        num_obstacles = int(0.05 * self.urban_grid.size * self.urban_grid.size)
        for _ in range(num_obstacles):
            x, y = np.random.randint(0, self.urban_grid.size-1), np.random.randint(0, self.urban_grid.size-1)
            self.urban_grid.add_obstacle(x, y)
        
        # Add one specific obstacle "incident" in the middle of the map
        mid = self.urban_grid.size // 2
        for i in range(-1, 2):
            self.urban_grid.add_obstacle(mid + i, mid)
        
        self.update_status(f"Added {num_obstacles} random obstacles and a middle incident")
        
        # If visualization is active, update it
        if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
            self.urban_grid.visualize(self.vehicles, show_plot=True)
    
    def perform_simulation_step(self):
        """Perform one step of the simulation"""
        if not self.urban_grid or not self.vehicles:
            return
        
        # Update environment
        positions = [v.position for v in self.vehicles if not v.reached]
        self.urban_grid.update_congestion(positions)
        self.urban_grid.update_traffic_lights()
        
        # Move vehicles
        for vehicle in self.vehicles:
            if not vehicle.reached:
                vehicle.move()
        
        # Visualize
        self.urban_grid.visualize(self.vehicles, show_plot=True)
        
        # Update status
        completed = sum(1 for v in self.vehicles if v.reached)
        total = len(self.vehicles)
        self.completed_label.config(text=f"{completed}/{total}")
        
        # Update step counter
        self.current_step += 1
        self.step_label.config(text=str(self.current_step))
    
    def run_simulation_step(self):
        """Run simulation steps with delay until paused or complete"""
        if self.running and not self.paused:
            all_reached = all(v.reached for v in self.vehicles)
            
            if self.current_step < self.max_steps and not all_reached:
                self.perform_simulation_step()
                
                # Schedule next step
                self.root.after(self.step_delay, self.run_simulation_step)
            else:
                # Simulation ended
                completed = sum(1 for v in self.vehicles if v.reached)
                total = len(self.vehicles)
                
                if all_reached:
                    self.update_status(f"Simulation complete! All vehicles reached destination in {self.current_step} steps.")
                else:
                    self.update_status(f"Simulation reached max steps ({self.max_steps}). {completed}/{total} vehicles reached destination.")
                
                self.running = False
                self.start_btn.config(state="normal")
                self.pause_btn.config(state="disabled")
    
    def on_close(self):
        """Handle window closing"""
        if hasattr(self.urban_grid, 'visualizer') and not self.urban_grid.visualizer.is_closed:
            self.urban_grid.visualizer.close()
        
        self.root.destroy()
    
    def run(self):
        """Start the controller's main loop"""
        self.root.mainloop()


    def setup_reward_config_gui(self, parent_frame):
        """Setup the reward configuration GUI section"""
        reward_frame = ttk.LabelFrame(parent_frame, text="Reward Configuration", padding="10")
        reward_frame.pack(fill=tk.X, pady=5)
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(reward_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Basic Rewards Tab
        basic_tab = ttk.Frame(notebook)
        notebook.add(basic_tab, text="Basic Rewards")
        self.setup_basic_rewards_tab(basic_tab)
        
        # Movement Penalties Tab
        movement_tab = ttk.Frame(notebook)
        notebook.add(movement_tab, text="Movement Penalties")
        self.setup_movement_penalties_tab(movement_tab)
        
        # Advanced Rewards Tab
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text="Advanced Settings")
        self.setup_advanced_rewards_tab(advanced_tab)
        
        # Control buttons
        btn_frame = ttk.Frame(reward_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Apply Reward Config", 
                  command=self.apply_reward_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset to Defaults", 
                  command=self.reset_reward_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Preset", 
                  command=self.load_reward_preset).pack(side=tk.LEFT, padx=5)
    
    def setup_basic_rewards_tab(self, parent):
        """Setup basic rewards configuration tab"""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Initialize StringVars for reward values
        self.step_penalty_var = tk.StringVar(value=str(self.reward_config.step_penalty))
        self.destination_reward_var = tk.StringVar(value=str(self.reward_config.destination_reached_reward))
        self.astar_follow_var = tk.StringVar(value=str(self.reward_config.astar_follow_reward))
        self.astar_path_var = tk.StringVar(value=str(self.reward_config.astar_on_path_reward))
        self.distance_reward_var = tk.StringVar(value=str(self.reward_config.closer_to_destination_reward))
        
        # Basic reward settings
        row = 0
        
        # Step penalty
        ttk.Label(scrollable_frame, text="Step Penalty:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.step_penalty_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Cost per movement step").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # Destination reward
        ttk.Label(scrollable_frame, text="Destination Reward:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.destination_reward_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Reward for reaching destination").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # A* follow reward
        ttk.Label(scrollable_frame, text="A* Follow Reward:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.astar_follow_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Reward for following A* path exactly").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # A* on path reward
        ttk.Label(scrollable_frame, text="A* On Path Reward:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.astar_path_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Reward for being on optimal path").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # Distance reward
        ttk.Label(scrollable_frame, text="Distance Reward:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.distance_reward_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Reward for getting closer to destination").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_movement_penalties_tab(self, parent):
        """Setup movement penalties configuration tab"""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Initialize StringVars for penalty values
        self.congestion_threshold_var = tk.StringVar(value=str(self.reward_config.high_congestion_threshold))
        self.congestion_penalty_var = tk.StringVar(value=str(self.reward_config.congestion_penalty_multiplier))
        self.backtrack_penalty_var = tk.StringVar(value=str(self.reward_config.immediate_backtrack_penalty))
        self.oscillation_penalty_var = tk.StringVar(value=str(self.reward_config.oscillation_penalty))
        self.red_light_penalty_var = tk.StringVar(value=str(self.reward_config.red_light_wait_penalty))
        
        row = 0
        
        # Congestion settings
        ttk.Label(scrollable_frame, text="Congestion Threshold:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.congestion_threshold_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="High congestion threshold (0.0-1.0)").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Congestion Penalty Multiplier:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.congestion_penalty_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Congestion penalty multiplier").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # Backward movement penalties
        ttk.Label(scrollable_frame, text="Backtrack Penalty:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.backtrack_penalty_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Immediate backtracking penalty").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Oscillation Penalty:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.oscillation_penalty_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Oscillating behavior penalty").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # Traffic light penalty
        ttk.Label(scrollable_frame, text="Red Light Penalty:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.red_light_penalty_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Red light waiting penalty").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_advanced_rewards_tab(self, parent):
        """Setup advanced rewards configuration tab"""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Initialize StringVars for advanced settings
        self.loop_threshold_base_var = tk.StringVar(value=str(self.reward_config.loop_threshold_base))
        self.loop_penalty_base_var = tk.StringVar(value=str(self.reward_config.loop_penalty_base))
        self.proximity_base_var = tk.StringVar(value=str(self.reward_config.proximity_base_multiplier))
        self.proximity_max_var = tk.StringVar(value=str(self.reward_config.proximity_max_multiplier))
        
        row = 0
        
        # Loop detection settings
        ttk.Label(scrollable_frame, text="Loop Threshold Base:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.loop_threshold_base_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Loop detection base threshold").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Loop Penalty Base:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.loop_penalty_base_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Loop base penalty").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        # Proximity reward settings
        ttk.Label(scrollable_frame, text="Proximity Base Multiplier:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.proximity_base_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Base proximity reward multiplier").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        ttk.Label(scrollable_frame, text="Proximity Max Multiplier:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.proximity_max_var, width=10).grid(row=row, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text="Maximum proximity reward multiplier").grid(row=row, column=2, sticky="w", padx=5, pady=2)
        row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def apply_reward_config(self):
        """Apply the reward configuration from GUI inputs"""
        try:
            # Update basic rewards
            self.reward_config.update_config(
                step_penalty=float(self.step_penalty_var.get()),
                destination_reached_reward=float(self.destination_reward_var.get()),
                astar_follow_reward=float(self.astar_follow_var.get()),
                astar_on_path_reward=float(self.astar_path_var.get()),
                closer_to_destination_reward=float(self.distance_reward_var.get()),
                
                # Movement penalties
                high_congestion_threshold=float(self.congestion_threshold_var.get()),
                congestion_penalty_multiplier=float(self.congestion_penalty_var.get()),
                immediate_backtrack_penalty=float(self.backtrack_penalty_var.get()),
                oscillation_penalty=float(self.oscillation_penalty_var.get()),
                red_light_wait_penalty=float(self.red_light_penalty_var.get()),
                
                # Advanced settings
                loop_threshold_base=int(float(self.loop_threshold_base_var.get())),
                loop_penalty_base=float(self.loop_penalty_base_var.get()),
                proximity_base_multiplier=float(self.proximity_base_var.get()),
                proximity_max_multiplier=float(self.proximity_max_var.get())
            )
            
            self.update_status("Reward configuration updated")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check input values: {str(e)}")
    
    def reset_reward_config(self):
        """Reset reward configuration to defaults"""
        self.reward_config.reset_to_defaults()
        
        # Update GUI values
        self.step_penalty_var.set(str(self.reward_config.step_penalty))
        self.destination_reward_var.set(str(self.reward_config.destination_reached_reward))
        self.astar_follow_var.set(str(self.reward_config.astar_follow_reward))
        self.astar_path_var.set(str(self.reward_config.astar_on_path_reward))
        self.distance_reward_var.set(str(self.reward_config.closer_to_destination_reward))
        
        self.congestion_threshold_var.set(str(self.reward_config.high_congestion_threshold))
        self.congestion_penalty_var.set(str(self.reward_config.congestion_penalty_multiplier))
        self.backtrack_penalty_var.set(str(self.reward_config.immediate_backtrack_penalty))
        self.oscillation_penalty_var.set(str(self.reward_config.oscillation_penalty))
        self.red_light_penalty_var.set(str(self.reward_config.red_light_wait_penalty))
        
        self.loop_threshold_base_var.set(str(self.reward_config.loop_threshold_base))
        self.loop_penalty_base_var.set(str(self.reward_config.loop_penalty_base))
        self.proximity_base_var.set(str(self.reward_config.proximity_base_multiplier))
        self.proximity_max_var.set(str(self.reward_config.proximity_max_multiplier))
        
        self.update_status("Reward configuration reset to defaults")
    
    def load_reward_preset(self):
        """Load a reward preset configuration"""
        preset_window = tk.Toplevel(self.root)
        preset_window.title("Select Reward Preset")
        preset_window.geometry("300x200")
        preset_window.resizable(False, False)
        
        ttk.Label(preset_window, text="Please select a preset configuration:").pack(pady=10)
        
        # Preset buttons
        def load_aggressive():
            self.reward_config.update_config(
                step_penalty=-3,
                astar_follow_reward=20,
                destination_reached_reward=300,
                immediate_backtrack_penalty=-100,
                congestion_penalty_multiplier=15
            )
            self.update_reward_gui_from_config()
            self.update_status("Loaded aggressive configuration")
            preset_window.destroy()
        
        def load_cautious():
            self.reward_config.update_config(
                step_penalty=-0.5,
                astar_follow_reward=5,
                destination_reached_reward=50,
                immediate_backtrack_penalty=-10,
                congestion_penalty_multiplier=2
            )
            self.update_reward_gui_from_config()
            self.update_status("Loaded cautious configuration")
            preset_window.destroy()
        
        def load_balanced():
            self.reward_config.reset_to_defaults()
            self.update_reward_gui_from_config()
            self.update_status("Loaded balanced configuration")
            preset_window.destroy()
        
        ttk.Button(preset_window, text="Aggressive (Fast & Direct)", command=load_aggressive).pack(pady=5)
        ttk.Button(preset_window, text="Cautious (Exploratory)", command=load_cautious).pack(pady=5)
        ttk.Button(preset_window, text="Balanced (Default)", command=load_balanced).pack(pady=5)
        ttk.Button(preset_window, text="Cancel", command=preset_window.destroy).pack(pady=5)
    
    def update_reward_gui_from_config(self):
        """Update GUI values from current reward configuration"""
        if hasattr(self, 'step_penalty_var'):
            self.step_penalty_var.set(str(self.reward_config.step_penalty))
            self.destination_reward_var.set(str(self.reward_config.destination_reached_reward))
            self.astar_follow_var.set(str(self.reward_config.astar_follow_reward))
            self.astar_path_var.set(str(self.reward_config.astar_on_path_reward))
            self.distance_reward_var.set(str(self.reward_config.closer_to_destination_reward))
            
            self.congestion_threshold_var.set(str(self.reward_config.high_congestion_threshold))
            self.congestion_penalty_var.set(str(self.reward_config.congestion_penalty_multiplier))
            self.backtrack_penalty_var.set(str(self.reward_config.immediate_backtrack_penalty))
            self.oscillation_penalty_var.set(str(self.reward_config.oscillation_penalty))
            self.red_light_penalty_var.set(str(self.reward_config.red_light_wait_penalty))
            
            self.loop_threshold_base_var.set(str(self.reward_config.loop_threshold_base))
            self.loop_penalty_base_var.set(str(self.reward_config.loop_penalty_base))
            self.proximity_base_var.set(str(self.reward_config.proximity_base_multiplier))
            self.proximity_max_var.set(str(self.reward_config.proximity_max_multiplier))
    
    def close_event(self):
        """Handle window close event"""
        if hasattr(self.urban_grid, 'visualizer'):
            self.urban_grid.visualizer.close()
        
        self.root.destroy()
    
def main():
    """Main function to launch the simulation controller"""
    # Try to load a recent trained agent from pickle file
    agent = None
    try:
        with open("trained_agent.pkl", "rb") as f:
            agent = pickle.load(f)
        print("Loaded existing trained agent")
    except FileNotFoundError:
        print("No saved agent found. Please train an agent or create a new one")
    except Exception as e:
        print(f"Error loading agent: {e}")
    
    # Create and run the simulation controller
    controller = SimulationController(agent)
    controller.run()


if __name__ == "__main__":
    main()

# Explicitly export the SimulationController class
__all__ = ['SimulationController']
