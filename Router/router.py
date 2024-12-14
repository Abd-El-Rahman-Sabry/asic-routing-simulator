import heapq
from queue import PriorityQueue
from config import LAYERS
from graphics import Graphics
from tile import Tile, TileState, TileType
from grid import Grid
from collections import deque

class Router:
    """
    Base class for a routing algorithm.

    Attributes:
        _grid (Grid): The grid representing the layout of the routing area.
        _show_updates (bool): Whether to display graphical updates during routing.
    """

    def __init__(self, grid):
        """
        Initialize the Router object with a grid.

        Args:
            grid (Grid): The grid object representing the routing area.
        """
        self._grid: Grid = grid
        self._show_updates = True

    def route(self, start, end):
        """
        Abstract method for routing between two points.
        
        Args:
            start (Tile): The starting tile.
            end (Tile): The destination tile.

        Raises:
            NotImplementedError: Must be implemented in a subclass.
        """
        raise NotImplementedError

    def enable_graphics_updates(self):
        """Enable graphical updates."""
        self._show_updates = True

    def disable_graphics_updates(self):
        """Disable graphical updates."""
        self._show_updates = False

    def __remove_path(self, path: list[Tile]):
        """
        Reset tiles in a given path.

        Args:
            path (list[Tile]): The path to reset.
        """
        for tile in path:
            tile.type = TileType.metal
            tile.set_idle_state()
            tile.reset()

    def __calc_cost(self, path: list[Tile]) -> int:
        """
        Calculate the cost of a path.

        Args:
            path (list[Tile]): The path to calculate the cost for.

        Returns:
            int: The total cost of the path.
        """
        total_cost = 0
        for i, tile in enumerate(path):
            if i > 0:
                if path[i - 1].layer.index != path[i].layer.index:
                    total_cost += 20  # Layer switching penalty
                else:
                    total_cost += 1  # Regular tile traversal cost
        return total_cost

    def __find_opt_path(self, paths: list[list[Tile]]) -> tuple[int, list[Tile]]:
        """
        Find the optimal path with the lowest cost.

        Args:
            paths (list[list[Tile]]): A list of possible paths.

        Returns:
            tuple[int, list[Tile]]: The index and the optimal path.
        """
        best_cost = float("inf")
        if not len(paths):
            return -1, []

        best_path = paths[0]
        best_index = 0
        for i, p in enumerate(paths):
            cost = self.__calc_cost(p)
            if cost < best_cost:
                best_cost = cost
                best_path = p
                best_index = i
            else:
                self.__remove_path(p)

        return best_index, best_path

    def __find_closest(self, point: Tile, others: list[Tile]) -> Tile:
        """
        Find the closest tile to a given point.

        Args:
            point (Tile): The reference tile.
            others (list[Tile]): List of other tiles to compare.

        Returns:
            Tile: The closest tile to the reference point.
        """
        min_dist = float("inf")
        closest: Tile = others[0]
        x, y, z = point.get_position()
        for tile in others:
            x_t, y_t, z_t = tile.get_position()
            current_dist = (x - x_t)**2 + (y - y_t)**2 + (z - z_t)**2
            if current_dist < min_dist:
                closest = tile
                min_dist = current_dist
        return closest

    def __build_path_tiles(self, path: list[Tile], fan_out=False):
        """
        Set the type and state of tiles in a path.

        Args:
            path (list[Tile]): The path to process.
            fan_out (bool, optional): Whether this is for a fan-out route. Defaults to False.
        """
        if path[0].type == TileType.metal:
            path[0].type = TileType.contact
            path[0].state = TileState.barrier
        if path[-1].type == TileType.metal:
            path[-1].type = TileType.contact
            path[-1].state = TileState.barrier

        for i, tile in enumerate(path):
            if i > 0:
                if path[i].layer.index != path[i - 1].layer.index:
                    path[i].type = TileType.via
                    path[i - 1].type = TileType.via
            tile.state = TileState.barrier
            tile.make_path()

    def fan_out_route(self, start: Tile, ends: list[Tile]):
        """
        Route from a starting tile to multiple endpoints (fan-out).

        Args:
            start (Tile): The starting tile.
            ends (list[Tile]): List of endpoint tiles.
        """
        # Initialize grid neighbors
        for grid_layer in self._grid.layers():
            for row in grid_layer:
                for tile in row:
                    self._grid.update_tile_neighbors(tile)

        paths = []
        fan_out_list = []
        temp_paths = []

        for end in ends:
            p = self.route(start, end, True)
            temp_paths += [p]

        i, first_opt_path = self.__find_opt_path(temp_paths)
        most_close = ends[i]
        Graphics.visualize_path(first_opt_path)
        self._grid.idlize_tiles()
        Graphics.update()

        paths = [first_opt_path]
        fan_out_list = [*first_opt_path]

        for e in ends:
            if e is not most_close:
                all_paths = []
                for v_start in fan_out_list:
                    p = self.route(v_start, e, False)
                    all_paths += [p]
                    Graphics.line(v_start, e, 75, abs(self.__calc_cost(p) - 30) / 20 * 255)
                i, opt_path = self.__find_opt_path(all_paths)
                self.__build_path_tiles(opt_path)
                fan_out_list[i].type = TileType.contact
                fan_out_list += opt_path
                paths += [opt_path]
                Graphics.visualize_path(fan_out_list)
                Graphics.update()

        # Mark contacts on top layer
        top = LAYERS - 1
        srow, scol, _ = start.get_position()
        self._grid.layers()[top][srow][scol].type = TileType.contact
        for e in ends:
            row, col, _ = e.get_position()
            self._grid.layers()[top][row][col].type = TileType.contact

        self.__build_path_tiles(first_opt_path)
        for path in paths:
            self.__build_path_tiles(path)

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
        while current in came_from:
            current = came_from[current]
            path.append(current)
            if show_update:
                self.update()
        return path

    def update(self):
        """Update the graphical display."""
        Graphics.update()


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
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        return abs(x0 - x1) + abs(y0 - y1) + 10 * abs(z0 - z1)

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
                current_g_score = g_score[current] + 1

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
                self._grid.idlize_tiles()
                path = self.reconstruct_path(came_from, current, show_update)
                return path

            for neighbor in current.neighbors:
                # If the neighbor is not visited and is not a metal tile (blocked)
                if neighbor not in came_from and neighbor.state != TileState.barrier:
                    # Calculate the cost to move to the neighbor tile
                    transition_cost = 1
                    if current.layer.index != neighbor.layer.index:
                        transition_cost = 20  # Add higher cost for layer transition

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