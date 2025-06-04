"""
Simulation Controller for Q-Learning Urban Traffic Simulation
This module provides interactive controls for simulating vehicle movement
based on a trained Q-learning agent.
"""
import tkinter as tk
import numpy as np
import time
from tkinter import ttk, filedialog, messagebox
from urban_grid import UrbanGrid
from vehicle import Vehicle
from agent import QLearningAgent
import pickle

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
        
        # Create GUI window
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components for simulation control"""
        self.root = tk.Tk()
        self.root.title("Q-Learning Traffic Simulation Controller")
        self.root.geometry("800x650")
        
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
            step_frame, from_=50, to=2000, orient=tk.HORIZONTAL, 
            variable=self.delay_var, command=self.update_delay
        )
        delay_slider.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(step_frame, textvariable=self.delay_var).grid(row=0, column=2, padx=5)
        
        # Max steps
        ttk.Label(step_frame, text="Max Steps:").grid(row=1, column=0, padx=5)
        self.max_steps_var = tk.IntVar(value=self.max_steps)
        max_steps_slider = ttk.Scale(
            step_frame, from_=10, to=500, orient=tk.HORIZONTAL, 
            variable=self.max_steps_var, command=self.update_max_steps
        )
        max_steps_slider.grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(step_frame, textvariable=self.max_steps_var).grid(row=1, column=2, padx=5)
        
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
        
        # Create incident button
        ttk.Button(agent_frame, text="Add Random Obstacles", 
                  command=self.add_random_obstacles).pack(side=tk.RIGHT, padx=5)
        
        # Number of vehicles
        veh_frame = ttk.Frame(control_frame)
        veh_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(veh_frame, text="Vehicles:").pack(side=tk.LEFT, padx=5)
        self.num_vehicles_var = tk.IntVar(value=5)
        ttk.Spinbox(veh_frame, from_=1, to=20, width=5, 
                   textvariable=self.num_vehicles_var).pack(side=tk.LEFT, padx=5)
        
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
    
    def create_new_agent(self):
        """Create a new agent when none is loaded"""
        grid_size = 10  # Default size
        self.urban_grid = UrbanGrid(size=grid_size)
        self.agent = QLearningAgent(self.urban_grid)
        self.update_status("New agent created")
    
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
            self.pause_btn.config(text="Pause")
            self.update_status("Simulation resumed")
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
        self.update_status("Simulation reset")
    
    def initialize_vehicles(self):
        """Create vehicles for simulation"""
        if not self.urban_grid or not self.agent:
            self.update_status("Cannot initialize vehicles: No agent or grid")
            return
        
        # Get number of vehicles
        num_vehicles = self.num_vehicles_var.get()
        
        # Create vehicles
        self.vehicles = []
        for _ in range(num_vehicles):
            vehicle = Vehicle(self.urban_grid, self.agent)
            self.vehicles.append(vehicle)
        
        self.update_status(f"Created {num_vehicles} vehicles")
        self.completed_label.config(text=f"0/{num_vehicles}")
    
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
