"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import csv
import module.convert as convert
import module.transport as transport

def get_canteen_coordinates(canteen):
    """Gets the coordinates of a canteen from file.

    Args:
        canteen (str): Canteen name.

    Returns:
        int: X coordinates of the canteen on the map.
        int: Y coordinates of the canteen on the map.
    """
    with open('data/canteen_coordinates.txt') as coords:
        rows = csv.reader(coords)
        for row in rows:
            if row[0] == canteen:
                X, Y = row[1:]
        return int(X), int(Y)


def import_canteen_database(user_location):
    """Gets the canteen database from file.

    Args:
        user_location ((int, int) -> tuple): Location that is marked by the user.
    
    Returns:
        database (dict): Canteen database.
    """
    database = {}
    with open('data/canteen_data.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line = 1
        for row in csv_reader:
            # data starts on the second line of the file
            if line > 1:
                menus = {}
                total_price = 0
                X, Y = get_canteen_coordinates(row[0])
                distance = transport.distance_a_b(user_location, (X, Y))
                for i in range(4, len(row), 2):
                    menus[row[i]] = float(row[i + 1])
                    total_price += float(row[i + 1])
                average_price = round(total_price / len(menus), 2)
                database[(row[0], (X, Y), row[1], row[2])] = [
                    int(row[3]), average_price, distance, menus]
            line += 1
    return database


def get_bus_coordinates(bus_loop):
    """Gets data of bus stops and their coordinates from file.

    Args:
        bus_loop (str): 'red' or 'blue' depending on the loop. Use this for the file name.

    Returns:
        bus_coords_list ([[str, (int, int)]] -> list): List of bus stops and their respective coordinates.
    """
    bus_coords_list = []
    # data/blue_coordinates.txt or data/red_coordinates.txt
    with open('data/' + bus_loop + '_coordinates.txt', 'r') as bus_coords:
        rows = csv.reader(bus_coords)
        for row in rows:
            bus_coords_list.append([row[0], (int(row[1]), int(row[2]))])
    return bus_coords_list


def get_bus_nodes(bus_loop):
    """Gets data of bus route nodes coordinates from file.

    Args:
        bus_loop (str): 'red' or 'blue' depending on the loop. Use this for the file name.

    Returns:
        nodes_list ([(int, int)] -> list): List of all node coordinates on the bus loop.
    """
    nodes_list = []
    # data/blue_nodes.txt or data/red_nodes.txt
    with open('data/' + bus_loop + '_nodes.txt', 'r') as csv_file:
        nodes = csv.reader(csv_file)
        line = 1
        # the csv file's data format is 'x coordinates,y coordinates'
        for node in nodes:
            if line > 1:
                nodes_list.append((int(node[0]), int(node[1])))
            line += 1
    return nodes_list
