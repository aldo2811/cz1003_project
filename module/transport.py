"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import module.data as data
import module.convert as convert


def nearest_bus_stop(location, bus_stop_coords):
    """Finds the nearest bus stop to the specified location.

    Args:
        Location ((int, int) -> tuple): Coordinates on the map.
        bus_stop_coords ([[str, (int, int)]] -> list): List of bus stops and its coordinates.

    Returns:
        nearest ([str, float] -> list): A list which contains the nearest bus stop and distance to the specified location in pixels.
    """
    # nearest bus stop is initially set to have an infinity distance to the specified location,
    # making sure that it will be replaced
    nearest = ['bus stop', float("inf")]
    for bus_stop, coordinates in bus_stop_coords:
        # find distance from the specified location to every bus stop on the bus loop
        distance = data.distance_a_b(location, coordinates)
        if distance < nearest[1]:
            nearest = [bus_stop, distance]
    return nearest


def route(bus_stop_coords, start, end):
    """Finds the bus route for travelling from one bus stop to another.

    Args:
        bus_stop_coords ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates.
            Can be either red loop or blue loop.
        start (str): Name of starting bus stop.
        end (str): Name of destination bus stop.

    Returns:
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.
    """
    # list all bus stop names on the bus loop,
    # to make it easier to find the index of bus stop
    bus_stops = [i[0] for i in bus_stop_coords]

    start_index = bus_stops.index(start)
    end_index = bus_stops.index(end)

    # arrange list such that the starting point is on the first index,
    # and the end point is on the last index
    if end_index >= start_index:
        bus_route = bus_stop_coords[start_index:end_index + 1]
    else:
        bus_route = bus_stop_coords[start_index:] + \
            bus_stop_coords[:end_index + 1]
    return bus_route


def directions(canteen_location, user_location, distance_user_canteen, bus_stop_coords):
    """Finds the direction / route from the user to the canteen.

    Args:
        canteen_location ((int, int) -> tuple): Coordinates of the canteen that is chosen by user.
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
        distance_user_canteen (float): Distance between user and canteen, in pixels.
        bus_stop_coords ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates.

    Returns:
        walk (bool): True if the user should walk to the canteen, otherwise False.
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.
    """
    nearest_bus_stop_canteen, distance_bus_stop_canteen = nearest_bus_stop(
        canteen_location, bus_stop_coords)
    nearest_bus_stop_user, distance_bus_stop_user = nearest_bus_stop(
        user_location, bus_stop_coords)

    # find the bus route from user to canteen
    bus_route = route(bus_stop_coords, nearest_bus_stop_user,
                      nearest_bus_stop_canteen)

    if distance_user_canteen <= distance_bus_stop_user or len(bus_route) <= 1:
        walk = True
    else:
        walk = False
    return walk, bus_route


def display_directions(stall, user_location):
    """Displays directions from user to canteen.

    Args:
        stall ((key, value) -> tuple): Tuple with same format with database, but for 1 stall.
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.

    Returns:
        str: String of directions that will be displayed on the stall information.
    """
    # get data of red and blue bus stop coordinates
    red_loop = data.get_bus_coordinates('red')
    blue_loop = data.get_bus_coordinates('blue')

    canteen_location = stall[0][1]
    distance_user_canteen = stall[1][2]

    # for each loop, check whether the user can walk straight to the canteen,
    # and find the bus route from user position to canteen
    red_walk, red_route = directions(
        canteen_location, user_location, distance_user_canteen, red_loop)
    blue_walk, blue_route = directions(
        canteen_location, user_location, distance_user_canteen, blue_loop)

    str_list = ["Recommended Routes\n"]
    if red_walk or blue_walk:
        distance_meters = convert.pixel_to_meter(distance_user_canteen)
        str_list.extend(["\nYou are near to the canteen. Walk straight ahead. (", str(
            distance_meters), " m)"])
    else:
        # find total bus distance from user to canteen for the 2 bus loops
        red_bus_distance = bus_distance(red_route, 'red')
        blue_bus_distance = bus_distance(blue_route, 'blue')

        # for each bus loop, find straight walking distance from user to starting bus stop,
        # and from end bus stop to canteen
        red_walk_distance = walk_distance(
            user_location, canteen_location, red_route)
        blue_walk_distance = walk_distance(
            user_location, canteen_location, blue_route)

        # find total travel distance from user to canteen for both bus loops
        red_travel_distance = red_bus_distance + sum(red_walk_distance)
        blue_travel_distance = blue_bus_distance + sum(blue_walk_distance)

        # shows the two loops if both loops' total number of bus stops are different within 1 stop
        # e.g. blue: 6 stops, red: 7 stops
        # usually, people think that 1 extra stop is still ok as it isn't that much of a difference
        if len(blue_route) <= len(red_route) + 1:
            # blue loop route
            str_list.append("\nBlue Loop\n\n")
            str_list.extend(display_bus_route(blue_route, blue_walk_distance))
            str_list.extend(["\nTotal bus distance: ",
                             str(blue_bus_distance), " m"])
            str_list.extend(["\nTotal travel distance: ",
                             str(blue_travel_distance), " m"])

        if len(red_route) <= len(blue_route) + 1:
            # red loop route
            str_list.append("\nRed Loop\n\n")
            str_list.extend(display_bus_route(red_route, red_walk_distance))
            str_list.extend(["\nTotal bus distance: ",
                             str(red_bus_distance), " m"])
            str_list.extend(["\nTotal travel distance: ",
                             str(red_travel_distance), " m"])
    return "".join(str_list)


def display_bus_route(bus_route, walk_distance):
    """Display format of bus route.

    Args:
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.
        walk_distance ((float, float) -> tuple): Walking distance from user to starting bus stop,
            and from end bus stop to canteen.

    Returns:
        str_list (str): List of strings describing the bus route to be displayed on the stall information.
    """
    walk_to_bus, walk_to_canteen = walk_distance
    # not exactly an arrow, but its purpose is similar,
    # to separate the bus stops and make the route look like a sequence
    str_arrow = "\n|\n"
    str_list = ["Walk to ", bus_route[0][0],
                " bus stop and board the bus. (", str(walk_to_bus), " m)", str_arrow]
    for bus_stop in bus_route:
        str_list.extend([bus_stop[0], str_arrow])

    str_list.extend(
        ["Walk straight ahead to the canteen. (", str(walk_to_canteen), " m)\n"])
    return str_list


def get_route_nodes(bus_route, bus_loop):
    """Gets bus route nodes from file.

    Args:
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.
        bus_loop (str): 'blue' or 'red' depending on the bus loop.

    Returns:
        route_nodes ([(int, int)] -> list): List of node coordinates that are travelled on the bus route.
    """
    bus_nodes = data.get_bus_nodes(bus_loop)

    # get coordinates and index of start and end bus stops
    start_coordinates = bus_route[0][1]
    end_coordinates = bus_route[-1][1]
    start_index = bus_nodes.index(start_coordinates)
    end_index = bus_nodes.index(end_coordinates)

    # arrange route nodes such that it starts from the starting bus stop,
    # and ends with the destination bus stop
    if end_index > start_index:
        route_nodes = bus_nodes[start_index:end_index + 1]
    else:
        route_nodes = bus_nodes[start_index:] + bus_nodes[:end_index + 1]
    return route_nodes


def bus_distance(bus_route, bus_loop):
    """Finds the distance travelled using bus.

    Args:
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.
        bus_loop (str): 'red' or 'blue' for choosing which loop.

    Returns:
        total_distance (float): Distance travelled using bus along the route, in meters.
    """
    route_nodes = get_route_nodes(bus_route, bus_loop)
    total_distance = 0

    # find the sum of straight distance between each nodes,
    # starting from the starting bus stop to the end bus stop
    for i in range(len(route_nodes) - 1):
        distance = data.distance_a_b(route_nodes[i], route_nodes[i+1])
        total_distance += distance

    total_distance = convert.pixel_to_meter(total_distance)
    return total_distance


def walk_distance(user_location, canteen_location, bus_route):
    """Finds the distance of user and starting bus stop,
    and canteen and end bus stop.

    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
        canteen_location ((int, int) -> tuple): Coordinates of the canteen chosen by the user.
        bus_route ([[str, (int, int)]] -> list): List of bus stops with their respective coordinates,
            starting from the starting bus stop to the destination.

    Returns:
        distance_bus_stop_user (float): Distance between user and the starting bus stop, in meters.
        distance_bus_stop_canteen (float): Distance between canteen and the end bus stop, in meters.
    """
    start_coordinates = bus_route[0][1]
    end_coordinates = bus_route[-1][1]

    # find straight walking distance from user to starting bus stop,
    # and from end bus stop to canteen, in pixels
    distance_bus_stop_user = data.distance_a_b(
        start_coordinates, user_location)
    distance_bus_stop_canteen = data.distance_a_b(
        end_coordinates, canteen_location)

    distance_bus_stop_user = convert.pixel_to_meter(distance_bus_stop_user)
    distance_bus_stop_canteen = convert.pixel_to_meter(distance_bus_stop_canteen)
    return distance_bus_stop_user, distance_bus_stop_canteen