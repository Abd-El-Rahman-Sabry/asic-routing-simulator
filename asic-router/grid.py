from drawable import Drawable
from tile import Tile, LayerOrientation, TileState, TileType, Layer
from config import ROWS, WIDTH, LAYERS

class Grid(Drawable):
    """
    Represents a grid structure composed of multiple layers of tiles.

    Attributes:
        _grid (list[list[list[Tile]]]): The 3D grid containing layers of tiles.
    """

    def __init__(self):
        """
        Initializes a Grid object.
        """
        self._grid: list[list[list[Tile]]] = []
        self.build_grid()

    def build_grid(self):
        """
        Builds the grid structure. Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def update_tile_neighbors(self, tile):
        """
        Updates the neighbors of a given tile. Must be implemented in subclasses.

        Args:
            tile (Tile): The tile whose neighbors are to be updated.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def layers(self):
        """
        Returns the grid layers.

        Returns:
            list[list[list[Tile]]]: The grid layers.
        """
        return self._grid

    def idlize_tiles(self):
        """
        Sets tiles in the grid to an idle state if they are open or closed.
        """
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    if tile.state == TileState.closed or tile.state == TileState.open :
                        tile.set_idle_state()
                    elif tile.state == TileState.end or tile.state == TileState.start: 
                        pass 


    def draw(self):
        """
        Draws all tiles in the grid.
        """
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    tile.draw()
