
# ASIC Routing Visualization Tool
![image](https://github.com/user-attachments/assets/d5801eb8-4e75-4e63-8aa5-19313de45bcb)

## Overview

The **ASIC Routing Visualization Tool** is an interactive educational platform designed to help users understand and visualize the detailed routing process in digital ASIC (Application-Specific Integrated Circuit) design. This tool is primarily aimed at educators, students, and professionals looking to deepen their understanding of the digital ASIC flow, focusing on the routing phase, which is critical for ensuring optimal chip performance.

## Features

- **Interactive Visualization**: View the detailed routing layout in a visual format, allowing you to explore the paths and connections within an ASIC design.
- **Educational Focus**: The tool is tailored to help users learn and understand the complex routing process in digital ASIC design.
- **Real-time Updates**: See routing updates in real-time as you make changes to the design or rerun the routing process.
- **Customizable Layers**: Visualize routing across multiple layers, including the ability to highlight layer transitions and routing obstacles.
- **Extendable Architecture**: Designed with extensibility in mind, allowing easy addition of new features and algorithms.
- **Cross-Platform Support**: Compatible with both Windows and macOS systems.

## Installation

### Prerequisites

Ensure that you have the following installed on your machine:

- Python 3.x
- Pygame (for visualization)


### Clone the repository

To get started with the tool, clone the repository to your local machine:

```bash
git clone https://github.com/Abd-El-Rahman-Sabry/asic-routing-simulator.git
cd asic-routing-simulator/asic-router
```

### Install dependencies

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

## Usage

1. **Launch the Tool**: Start the interactive visualization tool by running the following command:

    ```bash
    python entry.py
    ```

2. **Interact with the Visualization**: Use the GUI to interact with the routing visualizations, view the paths, and make adjustments as needed.

3. **Explore and Experiment**: Experiment with different configurations, layer transitions, and routing algorithms to deepen your understanding of the ASIC routing process.

4. **Documentation**: Detailed documentation of the underlying algorithms and routing strategies is available in the `docs` directory.




## Contributing

We welcome contributions to improve and extend this tool. Whether you're fixing bugs, adding new features, or improving the documentation, your contributions are highly appreciated!

### How to Contribute

1. Fork the repository to your own GitHub account.
2. Create a new branch for your feature or bugfix.
3. Make your changes and test them thoroughly.
4. Commit your changes with clear and concise commit messages.
5. Push your changes and create a pull request.


## How to Reuse this Repository  



### Functions to Implement in a Custom Router:

1. **`is_weighted()`**  
   This function determines whether the algorithm uses weighted costs for routing. Return `True` if the algorithm considers weights, otherwise `False`.

2. **`name()`**  
   This function returns the name of the routing algorithm. Useful for identifying which algorithm is being used.

3. **`route(start: Tile, end: Tile, show_update: bool = False)`**  
   The core routing logic. This function computes a path from the `start` tile to the `end` tile, optionally updating the visualization during the computation.

4. **`reconstruct_path(came_from, current, show_update: bool = False)`**  
   A helper method to backtrack and build the path once the destination is reached.

---

### Example of a Custom Router: Greedy Best-First Search

Below is an example of implementing a `GreedyBestFirstRouter` using the Manhattan distance as a heuristic:

```python
from router import Router
from tile import Tile, TileState
from heapq import heappush, heappop

class GreedyBestFirstRouter(Router):
    """
    Router implementation using the Greedy Best-First Search algorithm.
    """

    def __init__(self, grid):
        """
        Initialize the GreedyBestFirstRouter object.

        Args:
            grid (Grid): The grid object representing the routing area.
        """
        super().__init__(grid)

    def is_weighted(self):
        """
        Indicates whether the router considers weights.

        Returns:
            bool: False, as Greedy Best-First Search is unweighted.
        """
        return False

    def name(self):
        """
        Returns the name of the router.

        Returns:
            str: "Greedy Best-First Router"
        """
        return "Greedy Best-First Router"

    def route(self, start: Tile, end: Tile, show_update: bool = False):
        """
        Routes between two points using Greedy Best-First Search.

        Args:
            start (Tile): The starting tile.
            end (Tile): The destination tile.
            show_update (bool, optional): Whether to show graphical updates. Defaults to False.

        Returns:
            list[Tile]: The calculated path, or an empty list if no path is found.
        """
        open_set = []
        came_from = {}

        # Add the start tile to the open set with its heuristic value
        heappush(open_set, (self.manhattan_distance(start, end), start))
        came_from[start] = None

        start.set_open_state()

        while open_set:
            _, current = heappop(open_set)

            if current == end:
                self._grid.idlize_tiles()
                return self.reconstruct_path(came_from, current, show_update)

            for neighbor in current.neighbors:
                if neighbor not in came_from and neighbor.state != TileState.barrier:
                    heappush(open_set, (self.manhattan_distance(neighbor, end), neighbor))
                    came_from[neighbor] = current
                    neighbor.set_open_state()

            if show_update:
                self.update()

            current.set_closed_state()

        return []  # No path found

    def manhattan_distance(self, tile1: Tile, tile2: Tile) -> int:
        """
        Computes the Manhattan distance between two tiles.

        Args:
            tile1 (Tile): The first tile.
            tile2 (Tile): The second tile.

        Returns:
            int: The Manhattan distance between the tiles.
        """
        x1, y1 = tile1.get_position()[:2]
        x2, y2 = tile2.get_position()[:2]
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current, show_update: bool = False) -> list[Tile]:
        """
        Reconstructs the path from a dictionary of visited tiles.

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
        path.reverse()
        return path
```

---

### How to Use the Custom Router

1. Add the custom router to your project, such as `custom_router.py`.

2. In your `entry_point`, replace the existing router with your custom router:
   ```python
   from custom_router import GreedyBestFirstRouter

   def entry_point():
       Initializer()
       grid = CrossGrid()
       router = GreedyBestFirstRouter(grid)
       sim = RouterSimulator(grid, router)
       sim.loop()
   ```

---
### Functions to Implement:

By implementing these methods, you can create a custom router to suit specific routing scenarios, whether weighted or unweighted, heuristic-based, or otherwise.

To implement a custom grid class based on the `Grid` interface, you need to define two core functions as required by the base `Grid` class: 


1. **`build_grid()`**  
   This function defines the structure of the grid. You will create layers, rows, and tiles, and append them to the `_grid` attribute of your custom class. 

2. **`update_tile_neighbors(tile: Tile)`**  
   This function is responsible for identifying and assigning neighboring tiles to a given tile. The neighbors can be determined based on specific rules, such as connectivity constraints, layer orientation, and tile positions.

---

### Example of a Custom Grid Class

Here is an example of how you might implement a custom `DiagonalGrid` class, where tiles are connected diagonally in addition to horizontally and vertically:

```python
from grid import Grid
from tile import Tile, TileType, TileState, Layer, LayerOrientation
from config import ROWS, WIDTH, LAYERS

class DiagonalGrid(Grid):
    """
    A custom grid where tiles are connected diagonally, in addition to their direct neighbors.
    """

    def __init__(self):
        """
        Initializes a DiagonalGrid object and builds the grid structure.
        """
        super().__init__()
        self.build_grid()

    def build_grid(self):
        """
        Builds the diagonal grid structure with specified dimensions.
        """
        tile_width = WIDTH
        layers = self._create_layers(LAYERS)

        for layer in layers:
            grid_layer = []

            for i in range(ROWS):
                grid_layer.append([])

                for j in range(ROWS):
                    tile = Tile(i, j, layer, tile_width, TileType.metal)
                    grid_layer[i].append(tile)

            self._grid.append(grid_layer)

    def _create_layers(self, count, initial_orientation=LayerOrientation.horizontal):
        """
        Creates alternating horizontal and vertical layers.

        Args:
            count (int): Number of layers to create.
            initial_orientation (LayerOrientation): Orientation of the first layer.

        Returns:
            list[Layer]: List of layers.
        """
        layers = []

        for i in range(count + 1):
            orientation = (
                LayerOrientation.horizontal
                if i % 2 == initial_orientation.value
                else LayerOrientation.vertical
            )
            layers.append(Layer(i, orientation))

        return layers

    def update_tile_neighbors(self, tile: Tile):
        """
        Updates the neighbors of a given tile, including diagonal connectivity.

        Args:
            tile (Tile): The tile whose neighbors are to be updated.
        """
        tile.clear_neighbors()

        row, col, index = tile.get_position()
        step = 1

        # Connect horizontally or vertically
        if col < ROWS - step:
            tile.neighbors.append(self._grid[index][row][col + step])
        if col > step:
            tile.neighbors.append(self._grid[index][row][col - step])
        if row < ROWS - step:
            tile.neighbors.append(self._grid[index][row + step][col])
        if row > step:
            tile.neighbors.append(self._grid[index][row - step][col])

        # Connect diagonally
        if row > 0 and col > 0:
            tile.neighbors.append(self._grid[index][row - 1][col - 1])
        if row > 0 and col < ROWS - 1:
            tile.neighbors.append(self._grid[index][row - 1][col + 1])
        if row < ROWS - 1 and col > 0:
            tile.neighbors.append(self._grid[index][row + 1][col - 1])
        if row < ROWS - 1 and col < ROWS - 1:
            tile.neighbors.append(self._grid[index][row + 1][col + 1])

        # Connect to layers above and below
        if index < LAYERS:
            tile.neighbors.append(self._grid[index + 1][row][col])
        if index > 0:
            tile.neighbors.append(self._grid[index - 1][row][col])
```

---

### How to Use the Custom Grid

1. Import your new grid class:
   ```python
   from custom_grid import DiagonalGrid
   ```

2. Update the `entry_point` function to use `DiagonalGrid`:
   ```python
   def entry_point():
       Initializer()
       grid = DiagonalGrid()
       router = AStarRouter(grid)  # Or any router of your choice
       sim = RouterSimulator(grid, router)
       sim.loop()
   ```

By implementing these two functions in your custom grid, you can adapt the project to support a wide variety of routing scenarios and connectivity rules.


### Issues

If you find any bugs or have suggestions for improvements, please open an issue in the [Issues](https://github.com/your-username/asic-routing-simulator/issues) section of the repository.


## Acknowledgments

- Thanks to all contributors and supporters who help make this project possible.
- Special thanks to the open-source community for their contributions and tools that help make this project a reality.

---

Feel free to reach out if you have any questions or need assistance with the tool. Happy learning and experimenting!
![61ENAXvWUnL _AC_SX679_](https://github.com/user-attachments/assets/1af5f7e7-aed7-44a2-bd58-025a1dd2e803)
[![LinkedIn](https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo_2023.svg)](https://www.linkedin.com/in/abd-el-rahman-sabry-1025471b6)


