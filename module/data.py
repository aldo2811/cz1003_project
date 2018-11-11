"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import csv
import math


def import_canteen_coordinates():
    """Gets data of canteens and their respective coordinates from file.
    
    Returns:
        canteen_coordinates ([str, (int, int)] -> list): List of canteen names and their coordinates.
    """
    canteen_coordinates = []
    with open('data/canteen_coordinates.txt') as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            canteen_coordinates.append([row[0], (int(row[1]), int(row[2]))])
    return canteen_coordinates


def get_canteen_coordinates(canteen_coordinates, canteen_name):
    """Gets the coordinates of a canteen from list.

    Args:
        canteen_coordinates ([str, (int, int)] -> list): List of canteen names and their coordinates.
        canteen_name (str): Name of canteen.

    Returns:
        coordinates ((int, int) -> tuple): Coordinates of the canteen.
    """
    for canteen, coordinates in canteen_coordinates:
        if canteen == canteen_name:
            return coordinates


def distance_a_b(a, b):
    """Finds the straight distance between two points.

    Args:
        a ((x, y) -> list or tuple): Location of first point.
        b ((x, y) -> list or tuple): Location of second point.

    Returns:
        distance_a_b (float): Distance between the two points (distance is measured in pixels).
    """
    distance_a_b = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return distance_a_b


def import_canteen_database(user_location):
    """Gets the canteen database from file.

    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
    
    Returns:
        database (dict): Canteen database.
    """
    database = {}
    with open('data/canteen_data.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        canteen_coordinates = import_canteen_coordinates()
        for row in csv_reader:
            menus = {}
            total_price = 0

            # first data on every row is the canteen name
            X, Y = get_canteen_coordinates(canteen_coordinates, row[0])
            distance = distance_a_b(user_location, (X, Y))

            # inserting food menu to database
            # inside the data file, menu starts from row[4] until end of the line
            for i in range(4, len(row), 2):
                menus[row[i]] = float(row[i + 1])
                total_price += float(row[i + 1])
            average_price = round(total_price / len(menus), 2)

            # create database
            database[(row[0], (X, Y), row[1], row[2])] = [int(row[3]), average_price, distance, menus]
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
    # csv file format: bus_stop,X_coordinate,Y_coordinate
    with open('data/' + bus_loop + '_coordinates.txt', 'r') as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            bus_coords_list.append([row[0], (int(row[1]), int(row[2]))])
    return bus_coords_list


def get_bus_nodes(bus_loop):
    """Gets data of bus route node's coordinates from file.
    The purpose of creating route nodes is to increase the accuracy of travel distance.

    Args:
        bus_loop (str): 'red' or 'blue' depending on the loop. Use this for the file name.

    Returns:
        nodes_list ([(int, int)] -> list): List of all node coordinates on the bus loop.
    """
    nodes_list = []
    # data/blue_nodes.txt or data/red_nodes.txt
    # csv file format: X_coordinate,Y_coordinate
    with open('data/' + bus_loop + '_nodes.txt', 'r') as csv_file:
        nodes = csv.reader(csv_file)
        line = 1
        
        for node in nodes:
            if line > 1:
                nodes_list.append((int(node[0]), int(node[1])))
            line += 1
    return nodes_list