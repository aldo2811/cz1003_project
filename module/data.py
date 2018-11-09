"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import csv
import module.convert as convert


def get_canteen_coordinates(canteen):
    with open('data/canteen_coordinates.txt') as coords:
        rows = csv.reader(coords)
        for row in rows:
            if row[0] == canteen:
                X, Y = row[1:]
        return int(X), int(Y)


def import_canteen_database():
    database = {}
    # initial distance is 0, will be updated when needed to show/compare distance
    distance = 0
    with open('data/canteen_data.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line = 1
        for row in csv_reader:
            if line > 1:
                menus = {}
                total_price = 0
                for i in range(4, len(row), 2):
                    menus[row[i]] = float(row[i + 1])
                    total_price += float(row[i + 1])
                average_price = round(total_price / len(menus), 2)
                X, Y = get_canteen_coordinates(row[0])
                database[(row[0], (X, Y), row[1], row[2])] = [
                    int(row[3]), average_price, distance, menus]
            line += 1
    return database


def get_bus_coordinates(bus_loop):
    bus_coords_list = []
    with open('data/' + bus_loop + '_coordinates.txt', 'r') as bus_coords:
        rows = csv.reader(bus_coords)
        for row in rows:
            bus_coords_list.append([row[0], (int(row[1]), int(row[2]))])
    return bus_coords_list


def get_bus_nodes(bus_loop):
    nodes_list = []
    with open('data/' + bus_loop + '_nodes.txt', 'r') as csv_file:
        nodes = csv.reader(csv_file)
        line = 1
        for node in nodes:
            if line > 1:
                nodes_list.append((int(node[0]), int(node[1])))
            line += 1
    return nodes_list
