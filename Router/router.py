from queue import PriorityQueue
from tile import Tile, TileState, TileType 
from grid import Grid


class Router:

    def __init__(self, grid):
        self._grid : Grid = grid

    def route(self, start, end):
        return NotImplementedError
    
    def __calc_cost(self, path : list[Tile]): 
        total_cost = 0 

        for tile in path: 
            if tile.type == TileType.metal or tile.type == TileType.contact: 
                total_cost += 1 
            elif tile.type == TileType.via: 
                total_cost += 3

        return total_cost
    
    def __find_opt_path(self , paths : list[list[Tile]]): 
        best_cost = float("inf")
        best_path = paths[0]
        for p in paths:  
            cost = self.__calc_cost(p)
            if cost < best_cost: 
                best_cost = cost 
                best_path = p 

        return best_path 
    
    def __find_closest(self, point  : Tile , others : list[Tile]): 
        min_dist = float("inf")
        closest : Tile = others[0] 
        x , y , z = point.get_position() 
        for tile in others: 
            x_t , y_t , z_t = tile.get_position() 
            current_dist = (x - x_t)**2 + (y - y_t)**2 + (z - z_t)**2 

            if current_dist < min_dist: 
                closest = tile  
                min_dist = current_dist  

        return closest
    


    def run(self, start, ends: list[Tile]):
        if start is not None and ends is not None:
            for grid_layer in self._grid.layers():
                for row in grid_layer:
                    for tile in row:
                        self._grid.update_tile_neighbors(tile)

            paths = []

            most_close = self.__find_closest(start , ends)

            first_route = self.route(start , most_close)

            for e in ends:
                if e is not most_close: 
                    all_paths = []

                    for v_start in first_route: 
                        p = self.route(v_start, e)
                        all_paths += p

                    paths += self.__find_opt_path(all_paths)

            paths = list(set(paths))

            for p in paths:
                p.state = TileState.barrier
                p.make_path()
    
    def reconstruct_path(self, came_from, current , showUpdate = False) -> list[Tile]:

        path = [current]
        current.type = TileType.contact
        prev = current

        while current in came_from:
            current = came_from[current]

            if prev.layer.index != current.layer.index:
                prev.type = TileType.via
                current.type = TileType.via

            prev = current
            path.append(current)
            if showUpdate: 
                self.update()

        path[-1].type = TileType.contact

        return path
    
    def update(self): 
        self._frame_update() 


class AStarRouter(Router):

    def __init__(self, grid,):
        super().__init__(grid,)

    def run(self, start, ends):
        return super().run(start, ends)
    
    @staticmethod
    def h(p0: tuple[float, float, float], p1: tuple[float, float, float]) -> float:
        x0, y0, z0 = p0
        x1, y1, z1 = p1

        return abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1)

    def route(self, start : Tile , end : Tile , showUpdate = False):
        count = 0
        open_set = PriorityQueue()
        came_from = {}

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

            if current == end:
                self._grid.idlize_tiles() 
                path = self.reconstruct_path(came_from, current)
                start.type = TileType.contact
                end.type = TileType.contact
                print("Done")
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
            if showUpdate: 
                pass 

            if current != start:
                current.set_closed_state()

        return []
