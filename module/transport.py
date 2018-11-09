import math
import module.sort as sort
import module.data as data
import module.convert as convert


def distance_a_b(location_of_a, location_of_b):
    """Finds the straight distance between two points.

    Args:
        location_of_a ((x, y); list or tuple): Location of first point.
        location_of_b ((x, y); list or tuple): Location of second point.

    Returns:
        distance_a_b (float): Distance between the two points (distance is measured in pixels).
    """
    distance_a_b = math.sqrt(
        (location_of_a[0]-location_of_b[0])**2 + (location_of_a[1] - location_of_b[1])**2)
    return distance_a_b


def nearest_bus_stop(location, bus_stop_list):
    nearest = [None, float("inf")]
    for bus_stop, coordinates in bus_stop_list:
        distance = distance_a_b(location, coordinates)
        if distance < nearest[1]:
            nearest = [bus_stop, distance]  # only if lower
    return nearest


def route(bus_stop_coords, start, end):
    bus_stops = [i[0] for i in bus_stop_coords]
    start_index = bus_stops.index(start)
    end_index = bus_stops.index(end)
    if end_index >= start_index:
        bus_route = bus_stop_coords[start_index:end_index + 1]
    else:
        bus_route = bus_stop_coords[start_index:] + \
            bus_stop_coords[:end_index + 1]
    return bus_route


def directions(canteen_location, user_location, distance_user_canteen, bus_stop_list):
    nearest_bus_stop_canteen, distance_bus_stop_canteen = nearest_bus_stop(
        canteen_location, bus_stop_list)
    nearest_bus_stop_user, distance_bus_stop_user = nearest_bus_stop(
        user_location, bus_stop_list)
    bus_route = route(bus_stop_list, nearest_bus_stop_user,
                      nearest_bus_stop_canteen)
    if distance_user_canteen <= distance_bus_stop_user or len(bus_route) <= 1:
        walk = True
    else:
        walk = False
    return walk, bus_route


def display_route(bus_route, walk_distance):
    walk_to_bus, walk_to_canteen = walk_distance
    str_list = []
    str_arrow = "\n|\n"
    str_list.extend(["Walk to ", bus_route[0][0], " bus stop and board the bus. (", str(
        walk_to_bus), " m)", str_arrow])
    for bus_stop, coordinates in bus_route:
        str_list.extend([bus_stop, str_arrow])
    str_list.extend(
        ["Walk straight ahead to the canteen. (", str(walk_to_canteen), " m)\n"])
    return str_list


def display_directions(canteen_location, user_location, red_loop, blue_loop):
    distance_user_canteen = distance_a_b(user_location, canteen_location)
    red_walk, red_route = directions(
        canteen_location, user_location, distance_user_canteen, red_loop)
    blue_walk, blue_route = directions(
        canteen_location, user_location, distance_user_canteen, blue_loop)

    str_header = ("Recommended Routes\n")
    if red_walk or blue_walk:
        return (str_header + "You are near to the canteen. Walk straight ahead. (", str(distance_user_canteen), ")")
    else:
        red_bus_distance = bus_distance(red_route, 'red')
        blue_bus_distance = bus_distance(blue_route, 'blue')
        red_walk_distance = walk_distance(
            user_location, canteen_location, red_route)
        blue_walk_distance = walk_distance(
            user_location, canteen_location, blue_route)
        red_travel_distance = red_bus_distance + sum(red_walk_distance)
        blue_travel_distance = blue_bus_distance + sum(blue_walk_distance)

        str_list = [str_header]
        if len(blue_route) <= len(red_route) + 1:
            str_list.append("\nBlue Loop\n\n")
            str_list.extend(display_route(blue_route, blue_walk_distance))
            str_list.extend(["\nTotal bus distance: ",
                             str(blue_bus_distance), " meters"])
            str_list.extend(["\nTotal travel distance: ",
                             str(blue_travel_distance), " meters"])
        if len(red_route) <= len(blue_route) + 1:
            str_list.append("\nRed Loop\n\n")
            str_list.extend(display_route(red_route, red_walk_distance))
            str_list.extend(["\nTotal bus distance: ",
                             str(red_bus_distance), " meters"])
            str_list.extend(["\nTotal travel distance: ",
                             str(red_travel_distance), " meters"])
        return "".join(str_list)


def get_route_nodes(bus_route, loop):
    bus_nodes = data.get_bus_nodes(loop)
    start_coordinates = bus_route[0][1]
    end_coordinates = bus_route[-1][1]
    start_index = bus_nodes.index(start_coordinates)
    end_index = bus_nodes.index(end_coordinates)
    if end_index > start_index:
        route_nodes = bus_nodes[start_index:end_index + 1]
    else:
        route_nodes = bus_nodes[start_index:] + bus_nodes[:end_index + 1]
    return route_nodes


def bus_distance(bus_route, loop):
    route_nodes = get_route_nodes(bus_route, loop)
    total_distance = 0
    for i in range(len(route_nodes) - 1):
        distance = distance_a_b(route_nodes[i], route_nodes[i+1])
        total_distance += distance
    total_distance = convert.pixel_to_meter(total_distance)
    return total_distance


def walk_distance(user_location, canteen_location, bus_route):
    start_coordinates = bus_route[0][1]
    end_coordinates = bus_route[-1][1]
    distance_bus_stop_user = distance_a_b(start_coordinates, user_location)
    distance_bus_stop_canteen = distance_a_b(end_coordinates, canteen_location)

    distance_bus_stop_user = convert.pixel_to_meter(distance_bus_stop_user)
    distance_bus_stop_canteen = convert.pixel_to_meter(
        distance_bus_stop_canteen)
    return distance_bus_stop_user, distance_bus_stop_canteen
