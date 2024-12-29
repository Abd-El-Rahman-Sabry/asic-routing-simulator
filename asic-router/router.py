import heapq
from queue import PriorityQueue
from config import LAYERS
import config
from graphics import Graphics
from tile import Tile, TileState, TileType
from grid import Grid
from collections import deque

from ui import UI

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
        self.name()

    def is_weighted(self): 
        return NotImplementedError

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
        if not self.is_weighted(): 
            return len(path)

        total_cost = 0
        for i, tile in enumerate(path):
            if i > 0:
                if path[i - 1].layer.index != path[i].layer.index:
                    total_cost += config.VIA_COST  # Layer switching penalty
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


    def __build_path_tiles(self, path: list[Tile], fan_out=False):
        """
        Set the type and state of tiles in a path.

        Args:
            path (list[Tile]): The path to process.
            fan_out (bool, optional): Whether this is for a fan-out route. Defaults to False.
        """

        if not path: 
            return

        
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

        UI.update.set_status(f"{self.name()} is currently running : Trying to find the best route !")
        for i , end in enumerate(ends):
            p = self.route(start, end, self._show_updates and i < 3)
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
                    UI.update.set_status("Constructing the minimum cost Fan out Route")
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
        self._grid.layers()[top - 1][srow][scol].type = TileType.metal
        for e in ends:
            row, col, _ = e.get_position()
            self._grid.layers()[top][row][col].type = TileType.contact
            self._grid.layers()[top - 1 ][row][col].type = TileType.metal

        self.__build_path_tiles(first_opt_path)
        for path in paths:
            self.__build_path_tiles(path)

        UI.update.set_status("Done !")

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
