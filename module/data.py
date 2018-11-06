import csv


def get_canteen_coordinates(canteen):
    with open('data/canteen_coordinates.txt') as coords:
        rows = csv.reader(coords)
        for row in rows:
            if row[0] == canteen:
                X, Y = row[1:]
        return int(X), int(Y)


def import_canteen_database():
    database = {}
    distance = 0
    with open('data/canteen_data.txt', mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line = 0
        for row in csv_reader:
            if line > 0:
                menus = {}
                total_price = 0
                for i in range(4, len(row), 2):
                    menus[row[i]] = float(row[i + 1])
                    total_price += float(row[i + 1])
                average_price = round(total_price / len(menus), 2)
                X, Y = get_canteen_coordinates(row[0])
                database[(row[0], (X, Y), row[1], row[2])] = [int(row[3]), average_price, distance, menus]
            line += 1
    return database


def get_bus_coordinates(bus_loop):
    bus_coords_list = []
    with open('data/' + bus_loop + '_coordinates.txt', 'r') as bus_coords:
        rows = csv.reader(bus_coords)
        for row in rows:
            bus_coords_list.append([row[0], (int(row[1]), int(row[2]))])
    return bus_coords_list


red_loop = get_bus_coordinates('red_loop')
blue_loop = get_bus_coordinates('blue_loop')
#print(red_loop)