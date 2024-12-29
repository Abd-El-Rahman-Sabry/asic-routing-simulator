from collections import deque
import heapq
from queue import PriorityQueue
import config
from graphics import Graphics
from router import Router
from tile import Tile, TileState




class AStarRouter(Router):
    """
    Router implementation using the A* algorithm.
    """

    def __init__(self, grid):
        """
        Initialize the AStarRouter object.

        Args:
            grid (Grid): The grid object representing the routing area.
        """
        super().__init__(grid)

    def fan_out_route(self, start, ends):
        """Perform a fan-out routing using the A* algorithm."""
        return super().fan_out_route(start, ends)
    
    def is_weighted(self):
        return True
    
    def name(self):
        return "A* Router"

    @staticmethod
    def h(p0: tuple[float, float, float], p1: tuple[float, float, float]) -> float:
        """
        Heuristic function for A*.

        Args:
            p0 (tuple[float, float, float]): Start coordinates.
            p1 (tuple[float, float, float]): End coordinates.

        Returns:
            float: The heuristic value.
        """
        return config.heuristic(p0 , p1)

    def route(self, start: Tile, end: Tile, show_update=False):
        """
        Route between two points using A*.

        Args:
            start (Tile): The starting tile.
            end (Tile): The destination tile.
            show_update (bool, optional): Whether to show graphical updates. Defaults to False.

        Returns:
            list[Tile]: The calculated path, or an empty list if no path is found.
        """
        count = 0
        open_set = PriorityQueue()
        came_from = {}

        # Initialize scores
        g_score = {
            tile: float("inf") for grid_layer in self._grid.layers() for row in grid_layer for tile in row
        }
        g_score[start] = 0

        f_score = {
            tile: float("inf") for grid_layer in self._grid.layers() for row in grid_layer for tile in row
        }
        f_score[start] = AStarRouter.h(start.get_position(), end.get_position())
        open_set.put((f_score[start], count, start))

        visited = {start}

        while not open_set.empty():
            current: Tile = open_set.get()[2]
            visited.remove(current)

            # Check if we've reached the destination
            if current == end:
                self._grid.idlize_tiles()
                path = self.reconstruct_path(came_from, current)
                return path

            for n in current.neighbors:
                
                # Calculate the cost to move to the neighbor tile
                transition_cost = 1
                if current.layer.index != n.layer.index:
                        transition_cost =  config.VIA_COST  # Add higher cost for layer transition

                current_g_score = g_score[current] + transition_cost

                if current_g_score < g_score[n]:
                    came_from[n] = current
                    g_score[n] = current_g_score
                    f_score[n] = current_g_score + AStarRouter.h(n.get_position(), end.get_position())

                    if n not in visited:
                        count += 1
                        open_set.put((f_score[n], count, n))
                        visited.add(n)
                        n.set_open_state()
            
            if show_update:
                self.update()

            if current != start:
                current.set_closed_state()

        return []

class MazeRouter(Router):
    """
    Router implementation using a maze-solving algorithm with BFS.
    """

    def __init__(self, grid):
        """
        Initialize the MazeRouter object.

        Args:
            grid (Grid): The grid object representing the routing area.
        """
        super().__init__(grid)

    def is_weighted(self):
        return False 
    
    def name(self): 
        return "Maze Router"

    def route(self, start: Tile, end: Tile, show_update=False):
        """
        Route between two points using BFS (Breadth-First Search) algorithm.

        Args:
            start (Tile): The starting tile.
            end (Tile): The destination tile.
            show_update (bool, optional): Whether to show graphical updates. Defaults to False.

        Returns:
            list[Tile]: The calculated path, or an empty list if no path is found.
        """
        queue = deque([start])  # BFS uses a queue to explore the grid
        came_from = {start: None}  # To track the path

        # Mark the start tile
        start.set_open_state()

        while queue:
            current = queue.popleft()  # Pop the first element from the queue

            if current == end:
                # Reconstruct path when destination is found
                self._grid.idlize_tiles()
                path = self.reconstruct_path(came_from, current, show_update)
                return path

            for neighbor in current.neighbors:
                # If the neighbor is not visited and is not a metal tile (blocked)
                if neighbor not in came_from and neighbor.state != TileState.barrier:
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    neighbor.set_open_state()

            if show_update:
                self.update()

            current.set_closed_state()

        return []  # Return an empty list if no path is found

    def reconstruct_path(self, came_from, current, show_update=False) -> list[Tile]:
        """
        Reconstruct the path from a dictionary of visited tiles.

        Args:
            came_from (dict): Dictionary mapping tiles to their predecessors.
            current (Tile): The end tile of the path.
            show_update (bool, optional): Whether to show updates during reconstruction. Defaults to False.

        Returns:
            list[Tile]: The reconstructed path.
        """
        path = [current]
        while current in came_from and came_from[current] is not None:
            current = came_from[current]
            path.append(current)
            if show_update:
                self.update()
        path.reverse()  # Reverse to get the path from start to end
        return path

    def update(self):
        """Update the graphical display."""
        Graphics.update()


class WeightedTile:
    """
    A class to wrap a Tile with its cost to make it comparable for use in a priority queue.
    """
    def __init__(self, tile: Tile, cost: int):
        self.tile = tile
        self.cost = cost

    def __lt__(self, other):
        """Compare WeightedTile objects based on their cost."""
        return self.cost < other.cost

    def __repr__(self):
        """String representation for debugging."""
        return f"WeightedTile(tile={self.tile}, cost={self.cost})"
    
class DijkstraRouter(Router):
    """
    Router implementation using Dijkstra's algorithm with layer transition cost.
    """

    def __init__(self, grid):
        """
        Initialize the DijkstraRouter object.

        Args:
            grid (Grid): The grid object representing the routing area.
        """
        super().__init__(grid)


    
    
    
    
    def is_weighted(self):
        """
        Check if the router uses weighted edges.
            bool: Always returns True, indicating that the router uses weighted edges.
        
        """
        
        return True 
    
    def name(self): 

        """
        Returns the name of the router.
        
        
        Returns:
            str: The name of the router, which is "Dijkstra Router".
        
        """
        return "Dijkstra Router"

    def route(self, start: Tile, end: Tile, show_update=False):
        """
        Route between two points using Dijkstra's algorithm with layer transition cost.

        Args:
            start (Tile): The starting tile.
            end (Tile): The destination tile.
            show_update (bool, optional): Whether to show graphical updates. Defaults to False.

        Returns:
            list[Tile]: The calculated path, or an empty list if no path is found.
        """
        # Min-heap for Dijkstra's algorithm (priority queue)
        open_set = []
        heapq.heappush(open_set, WeightedTile(start, 0))  # Push the start tile with a cost of 0

        # Dictionaries to track the shortest cost and the path
        cost = {start: 0}
        came_from = {start: None}

        # Mark the start tile as open
        start.set_open_state()

        while open_set:
            current_weighted_tile = heapq.heappop(open_set)  # Pop the tile with the smallest cost
            current = current_weighted_tile.tile
            current_cost = current_weighted_tile.cost

            # If we've reached the destination, reconstruct the path
            if current == end:
                print(f"Current Cost at position : {end.get_position()} = {current_weighted_tile.cost}")
                self._grid.idlize_tiles()
                path = self.reconstruct_path(came_from, current, show_update)
                return path

            for neighbor in current.neighbors:
                # If the neighbor is not visited and is not a metal tile (blocked)
                if neighbor not in came_from and neighbor.state != TileState.barrier:
                    # Calculate the cost to move to the neighbor tile
                    transition_cost = 1
                    if current.layer.index != neighbor.layer.index:
                        transition_cost =  config.VIA_COST  # Add higher cost for layer transition

                    new_cost = current_cost + transition_cost

                    # If the new cost is cheaper, update it and push to the priority queue
                    if neighbor not in cost or new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        came_from[neighbor] = current
                        heapq.heappush(open_set, WeightedTile(neighbor, new_cost))  # Store WeightedTile object
                        neighbor.set_open_state()

            if show_update:
                self.update()

            # Mark the current tile as closed (visited)
            current.set_closed_state()

        return []  # Return an empty list if no path is found

    def reconstruct_path(self, came_from, current, show_update=False) -> list[Tile]:
        """
        Reconstruct the path from a dictionary of visited tiles.

        Args:
            came_from (dict): Dictionary mapping tiles to their predecessors.
            current (Tile): The end tile of the path.
            show_update (bool, optional): Whether to show updates during reconstruction. Defaults to False.

        Returns:
            list[Tile]: The reconstructed path.
        """
        path = [current]
        while current in came_from and came_from[current] is not None:
            current = came_from[current]
            path.append(current)
            if show_update:
                self.update()
        path.reverse()  # Reverse to get the path from start to end
        return path

    def update(self):
        """Update the graphical display."""
        Graphics.update()