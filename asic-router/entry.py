
from initializer import Initializer
from simulator import RouterSimulator
from grid import CrossGrid
from router import AStarRouter , MazeRouter , DijkstraRouter


def entry_point():
    Initializer()
    grid = CrossGrid()
    router = AStarRouter(grid,) 
    sim = RouterSimulator(grid , router) 
    sim.loop() 
    



if __name__ == "__main__" : 
    entry_point() 