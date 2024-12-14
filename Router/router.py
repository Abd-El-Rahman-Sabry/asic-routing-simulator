from queue import PriorityQueue
from config import LAYERS
from graphics import Graphics
from tile import Tile, TileState, TileType 
from grid import Grid



class Router:

    def __init__(self, grid):
        self._grid : Grid = grid
        self._show_updates = True

    def route(self, start, end):
        return NotImplementedError
    
    def enable_graphics_updates(self): 
        self._show_updates = True
    def disable_graphics_updates(self): 
        self._show_updates = False

    def __remove_path(self, path : list[Tile]): 

        for tile in path: 
            tile.type= TileType.metal
            tile.set_idle_state()
            tile.reset()

    def __calc_cost(self, path : list[Tile]): 
        total_cost = 0 

        for i, tile in enumerate(path):
            if i > 0 : 
                if path [i - 1].layer.index != path[i].layer.index: 
                    total_cost += 20 
                else: 
                    total_cost += 1

        return total_cost
    
    def __find_opt_path(self , paths : list[list[Tile]]): 
        best_cost = float("inf")
        if not len(paths): 
            return -1 , []

        best_path = paths[0]
        best_index = 0
        for i , p in enumerate(paths):  
            cost = self.__calc_cost(p)
            if cost < best_cost: 
                best_cost = cost 
                best_path = p
                best_index = i  
            else : 
                self.__remove_path(p)

        return best_index , best_path 
    
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
    
    def __build_path_tiles(self, path : list[Tile] , fan_out = False): 
        
        
            if path[0].type == TileType.metal:
                path[0].type = TileType.contact
                path[0].state = TileState.barrier
            if path[-1].type == TileType.metal: 
                path[-1].type = TileType.contact
                path[-1].state = TileState.barrier
        
            for i , tile in enumerate(path):

                if i > 0: 
                    if path[i].layer.index != path[i -1].layer.index : 
                        path[i].type = TileType.via  
                        path[i - 1].type = TileType.via  
                tile.state = TileState.barrier
                tile.make_path()


    def fan_out_route(self, start : Tile , ends: list[Tile]):
        if start is not None and ends is not None:
            for grid_layer in self._grid.layers():
                for row in grid_layer:
                    for tile in row:
                        self._grid.update_tile_neighbors(tile)


            
            paths = []
            fan_out_list = []
            
            temp_paths = []
            for end in ends: 
                p = self.route(start, end , True)
                temp_paths += [p]

            i , first_opt_path = self.__find_opt_path(temp_paths)
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
                        p = self.route(v_start, e , False)
                        all_paths += [p]
                        Graphics.line(v_start , e , 75 ,   abs(self.__calc_cost(p)- 30)/20*255)
                    i , opt_path = self.__find_opt_path(all_paths)
                    
                    self.__build_path_tiles(opt_path)
                    fan_out_list[i].type = TileType.contact
                    fan_out_list += opt_path 
                    paths += [opt_path] 
                    Graphics.visualize_path(fan_out_list)
                    Graphics.update()

            top = LAYERS - 1
            srow , scol , _ = start.get_position()
            self._grid.layers()[top][srow][scol].type = TileType.contact 
            for e in ends:
                row , col , _ = e.get_position()  
                self._grid.layers()[top][row][col].type = TileType.contact
            
            self.__build_path_tiles(first_opt_path)
            for path in paths: 
                self.__build_path_tiles(path)

            
    



    
    def reconstruct_path(self, came_from, current , show_update = False) -> list[Tile]:

        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)
            if show_update: 
                self.update()

        return path
    
    def update(self): 
        Graphics.update() 


class AStarRouter(Router):

    def __init__(self, grid,):
        super().__init__(grid,)

    def fan_out_route(self, start, ends):
        return super().fan_out_route(start, ends)
    
    @staticmethod
    def h(p0: tuple[float, float, float], p1: tuple[float, float, float]) -> float:
        x0, y0, z0 = p0
        x1, y1, z1 = p1

        return abs(x0 - x1) + abs(y0 - y1) + 10*abs(z0 - z1)

    def route(self, start : Tile , end : Tile , show_update = False):
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
