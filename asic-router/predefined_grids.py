

from config import LAYERS, ROWS, WIDTH
from grid import Grid
from tile import Layer, LayerOrientation, Tile, TileState, TileType


class CrossGrid(Grid):
    """
    Represents a cross-layer grid structure with specific layer orientations.
    """

    def __init__(self):
        """
        Initializes a CrossGrid object and builds the grid structure.
        """
        super().__init__()

    def build_grid(self):
        """
        Builds the cross-layer grid with specific dimensions and tile types.
        """
        tile_width = WIDTH
        layers = self.build_cross_grid_layers(LAYERS)

        for layer in layers: 
            print(layer.index)

        for layer in layers:
            grid_layer = []

            for i in range(ROWS):
                grid_layer.append([])

                for j in range(ROWS):
                    tile = Tile(i, j, layer, tile_width, TileType.metal)
                    grid_layer[i].append(tile)

            self._grid.append(grid_layer)

    def build_cross_grid_layers(
        self, count, initial_orientation=LayerOrientation.horizontal
    ) -> list[Layer]:
        """
        Creates a list of layers with alternating orientations.

        Args:
            count (int): The number of layers to create.
            initial_orientation (LayerOrientation): The orientation of the first layer.

        Returns:
            list[Layer]: A list of layers with alternating orientations.
        """
        layers: list[Layer] = []

        for i in range(count + 1):
            if i % 2 == initial_orientation.value:
                layers.append(Layer(i, LayerOrientation.horizontal))
            else:
                layers.append(Layer(i, LayerOrientation.vertical))

        return layers

    def update_tile_neighbors(self, tile: Tile):
        """
        Updates the neighbors of a given tile based on its position and orientation.

        Args:
            tile (Tile): The tile whose neighbors are to be updated.
        """
        tile.clear_neighbors()

        row, col, index = tile.get_position()

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
