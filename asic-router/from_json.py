import json
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ROWS, LAYERS

class RouteLoader:
    """
    RouteLoader loads routes from a JSON file and validates them against grid constraints.
    """

    def __init__(self, json_file):
        """
        Initializes the RouteLoader with a JSON file.

        Args:
            json_file (str): Path to the JSON file containing routes.
        """
        self.json_file = json_file
        self.__routes = self.__load_routes()

    @property
    def routes(self):
        return self.__routes

    @routes.setter
    def routes(self, routes):
        self.__routes = routes


    def __load_routes(self):
        """
        Loads and validates routes from the JSON file.

        Returns:
            list: A list of validated routes.
        """
        with open(self.json_file, 'r') as file:
            routes = json.load(file)
            print(routes)
        
        validated_routes = []
        for route in routes['routes']:
            for name ,values in route.items():
                print(f"Working on route {name}")
                current_point_route = []
                for value in values:
                    point = list(value.values())
                    current_point_route.append(point)
                validated_route = self.__validate_route(current_point_route)
                if validated_route:
                    validated_routes.append(validated_route)

        
        return validated_routes

    def __validate_route(self, route):
        """
        Validates a single route to ensure all points are within grid bounds.

        Args:
            route (list): A list of points where each point is a list [x, y, z].

        Returns:
            list: The validated route or None if invalid.
        """
        if (len(route) < 2):
            print("Route is empty. Skipping route.")
            return None

        validated_route = []
        for point in route:
            x, y, z = point
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT and 0 <= z < LAYERS:
                validated_route.append(point)
            else:
                print(f"Invalid point {point} in route {route}. Skipping route.")
                return None
        return validated_route



if __name__ == "__main__": 
    obj = RouteLoader("routes.json")

    print(obj.__routes) 

    