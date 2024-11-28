from drawable import Drawable
from tile import Tile , LayerOrientation, TileState , TileType , Layer
from config import ROWS , WIDTH , LAYERS

class Grid(Drawable): 


    def __init__(self):
        self._grid : list[list[list[Tile]]]= []

    def build_grid(self): 
        return NotImplementedError
    
    def update_tile_neighbors(self, tile): 
        return NotImplementedError 
    
    def layers(self): 
        return self._grid
    
    def idlize_tiles(self):
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    if tile.state == TileState.closed or tile.state == TileState.open:
                        tile.set_idle_state()

    def draw(self):
    
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    tile.draw()


class CrossGrid (Grid): 

    def __init__(self):
        super().__init__()
        self.build_grid() 


    def build_grid(self):
        
        tile_width = WIDTH

        layers = self.build_cross_grid_layers(LAYERS)

        for layer in layers:

            grid_layer = []

            for i in range(ROWS):

                grid_layer.append([])

                for j in range(ROWS):
                    tile = Tile(i, j, layer, tile_width, TileType.metal)
                    grid_layer[i].append(tile)

            self._grid.append(grid_layer)



    def build_cross_grid_layers(
        self, 
        count, initial_orientation=LayerOrientation.horizontal
    ) -> list[Layer]:
        layers: list[Layer] = []

        for i in range(count + 1):
            if i % 2 == initial_orientation.value:
                layers.append(Layer(i, LayerOrientation.horizontal))
            else:
                layers.append(Layer(i, LayerOrientation.vertical))

        return layers
    
    def update_tile_neighbors(self, tile : Tile):
        tile.clear_neighbors()

        row , col , index  = tile.get_position()

        # Same Layer
        step = 1

        if tile.layer.orientation == LayerOrientation.horizontal:

            # EAST
            if col < ROWS - step and not (
                self._grid[index][row][col + step].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row][col + step]
                )
            # WEST
            if col > step and not (
                 self._grid[index][row][col - step].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row][col - step]
                )

        elif tile.layer.orientation == LayerOrientation.vertical:

            # South
            if row < ROWS - step and not (
                self._grid[index][row + step][col].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row + step][col]
                )
            # North
            if row > step and not (
                self._grid[index][row - step][col].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row - step][col]
                )

        # Different Layer

        # Up
        if index < LAYERS and not (
            self._grid[index + 1][row][col].state
            == TileState.barrier
        ):
            tile.neighbors.append(
                self._grid[index + 1][row][col]
            )
        # Down
        if index > 0 and not (
            self._grid[index - 1][row][col].state
            == TileState.barrier
        ):
            tile.neighbors.append(
                self._grid[index - 1][row][col]
            ) 