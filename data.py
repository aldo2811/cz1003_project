import csv

def import_canteen_database():
    database = {}
    with open('canteen_data.txt', mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line = 0
        for row in csv_reader:
            if line > 0:
                menus = {}
                total_price = 0
                for i in range(6, len(row), 2):
                    menus[row[i]] = int(row[i + 1])
                    total_price += int(row[i + 1])
                average_price = round(total_price / len(menus), 2)
                database[(row[0], (int(row[1]), int(row[2])), row[3], row[4])] = [row[5], average_price, menus]
            line += 1
    return database