import csv


def get_coordinates(canteen):
    with open('canteen_coordinates.txt') as coords:
        rows = csv.reader(coords)
        for row in rows:
            if row[0] == canteen:
                X, Y = row[1:]
        return int(X), int(Y)


def import_canteen_database():
    database = {}
    distance = 0
    with open('canteen_data.txt', mode = 'r') as csv_file:
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
                X, Y = get_coordinates(row[0])
                database[(row[0], (X, Y), row[1], row[2])] = [int(row[3]), average_price, distance, menus]
            line += 1
    return database