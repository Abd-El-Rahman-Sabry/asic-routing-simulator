from initializer import Initializer
from simulator import RouterSimulator
from grid import CrossGrid
from router import AStarRouter, MazeRouter, DijkstraRouter


def entry_point() -> None:
    """
    Entry point for initializing and starting the routing simulation.

    This function sets up the required components for the simulation:
    - Initializes the pygame environment.
    - Creates a grid for routing visualization.
    - Selects a routing algorithm (A* Router by default).
    - Starts the router simulation loop.

    Uncomment the `sim.load_route_from_json()` line to load pre-configured
    routes from a JSON file.

    Returns:
        None
    """
    # Initialize pygame and other necessary components
    Initializer()

    # Create a grid object for the simulation
    grid = CrossGrid()

    # Choose a routing algorithm (A* Router used here by default)
    router = AStarRouter(grid)

    # Create the router simulator with the grid and router
    sim = RouterSimulator(grid, router)

    # Optional: Load routes from a JSON file
    # sim.load_route_from_json("route_2.json")

    # Start the simulation loop
    sim.loop()


def main() -> None:
    """
    Main function that serves as the program's entry point.

    Calls the `entry_point` function to initialize and run the simulation.

    Returns:
        None
    """
    entry_point()


if __name__ == "__main__":
    main()
