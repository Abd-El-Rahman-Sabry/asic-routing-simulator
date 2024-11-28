
from initializer import Initializer
from simulator import RouterSimulation
from grid import CrossGrid
from router import AStarRouter


def entry_point():
    Initializer()
    grid = CrossGrid()
    router = AStarRouter(grid,) 
    sim = RouterSimulation(grid , router) 
    sim.loop() 
    



if __name__ == "__main__" : 
    entry_point() 