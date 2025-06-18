import heapq
import numpy as np

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid_size, obstacles):
    """Get valid neighboring positions"""
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Up, Right, Down, Left
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if (0 <= new_x < grid_size and 
            0 <= new_y < grid_size and 
            not obstacles[new_x, new_y]):
            neighbors.append((new_x, new_y))
    return neighbors

def astar(start, goal, grid_size, obstacles, congestion):
    """A* pathfinding algorithm with congestion consideration
    
    Args:
        start: Starting position (x, y)
        goal: Goal position (x, y)
        grid_size: Size of the grid
        obstacles: Boolean array of obstacles
        congestion: Array of congestion levels
    
    Returns:
        path: List of positions from start to goal, or None if no path found
    """
    def get_path_cost(pos):
        """Get movement cost considering congestion"""
        base_cost = 1.0
        if congestion[pos] > 0.5:  # High congestion threshold
            return base_cost + (congestion[pos] * 2)  # Increased cost in congested areas
        return base_cost

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for next_pos in get_neighbors(current, grid_size, obstacles):
            new_cost = cost_so_far[current] + get_path_cost(next_pos)
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan_distance(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    return None  # No path found
