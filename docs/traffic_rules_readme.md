# Traffic Rules in Urban Q-Learning Simulation

This document explains the traffic rules implemented in the simulation.

## Traffic Light Rules

Vehicles in the simulation now follow traffic light rules:

1. **Traffic Light Waiting**: When a vehicle encounters a red light, it will wait rather than proceeding through the intersection. 
   - If moving North-South when East-West has a green light (traffic light state = 2), the vehicle will wait.
   - If moving East-West when North-South has a green light (traffic light state = 1), the vehicle will wait.
   - A small waiting penalty (-5) is applied, which is less than the penalty for running a red light (-10).

2. **Traffic Light Cycles**: Traffic lights alternate in a cycle defined by the `traffic_light_cycle` parameter (default: 10 steps).

## Path Following Rules

The simulation now includes improved path following rules to simulate more realistic driving behavior:

1. **Backwards Movement Restriction**: Vehicles are strongly discouraged from moving backwards to their previous position.
   - A penalty of -15 is applied when a vehicle tries to return to its immediately previous position.
   - This helps prevent vehicles from simply oscillating between two adjacent positions.

2. **Loop Detection**: The system already included loop detection that penalizes vehicles for repeatedly visiting the same position.
   - A penalty is applied when a vehicle visits the same position more than a threshold number of times.
   - The threshold scales with the map size (larger maps have a larger threshold).
   - The penalty increases with more repeated visits to discourage persistent loops.

These rules aim to make the Q-learning agent develop more realistic driving behaviors, similar to real-world traffic patterns.
