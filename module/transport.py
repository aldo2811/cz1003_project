import module.tr as tr


def nearest_bus_stop(location, bus_stop_list):
    nearest = [None, float("inf")]
    for bus_stop, coordinates in bus_stop_list:
        distance = tr.distance_a_b(location, coordinates)
        if distance < nearest[1]:
            nearest = [bus_stop, distance] #only if lower
    return nearest


def route(bus_stops_coords, start, end):
    bus_route = []
    bus_stops = [i[0] for i in bus_stops_coords]
    start_index = bus_stops.index(start)
    rotated_bus_stops = bus_stops[start_index:] + bus_stops[:start_index]
    for bus_stop in rotated_bus_stops:
        bus_route.append(bus_stop)
        if bus_stop == end:
            break
    return bus_route


def directions(canteen_location, user_location, distance_user_canteen, bus_stop_list):
    nearest_bus_stop_canteen, distance_bus_stop_canteen = nearest_bus_stop(canteen_location, bus_stop_list)
    nearest_bus_stop_user, distance_bus_stop_user = nearest_bus_stop(user_location, bus_stop_list)
    bus_route = route(bus_stop_list, nearest_bus_stop_user, nearest_bus_stop_canteen)
    if distance_user_canteen <= distance_bus_stop_user or len(bus_route) == 1:
        walk = True
    else:
        walk = False
    return walk, bus_route


def display_route(bus_route):
    str_list = []
    str_arrow = "\n|\n"
    str_list.extend(["Walk to ", bus_route[0], " bus stop and board the bus.", str_arrow])
    for bus_stop in bus_route:
        str_list.extend([bus_stop, str_arrow])
    str_list.append("Walk straight ahead to the canteen.\n")
    return str_list


def display_directions(canteen_location, user_location, red_loop, blue_loop):
    distance_user_canteen = tr.distance_a_b(user_location, canteen_location)
    red_walk, red_route = directions(canteen_location, user_location, distance_user_canteen, red_loop)
    blue_walk, blue_route = directions(canteen_location, user_location, distance_user_canteen, blue_loop)

    str_header = ("Recommended Routes\n")
    if red_walk or blue_walk:
        return (str_header + "You are near to the canteen. Walk straight ahead.")
    else:
        str_list = [str_header]
        if len(blue_route) <= len(red_route) + 1:
            str_list.append("\nBlue Loop\n\n")
            str_list.extend(display_route(blue_route))
        if len(red_route) <= len(blue_route) + 1:
            str_list.append("\nRed Loop\n\n")
            str_list.extend(display_route(red_route))
        return "".join(str_list)

