import module.check as check
import module.convert as convert
import module.data as data
import module.data_input as data_input
import module.search as search
import module.sort as sort
import module.transport as transport
from library.prettytable import PrettyTable


def import_user_location(location):
    """Imports user_location from the main file (main.py).
    Declares it as a global variable in this file to ease things.
    """
    global user_location
    user_location = location


def main_menu():
    """Main command line interface menu structure."""
    search_result = {}
    # imports canteen database from file
    database = data.import_canteen_database()

    print("\nWelcome to the NTU F/B Recommendation System!")
    print("Please enter the input number that corresponds to the option you'd like to choose.", end = "\n\n")
    print("1: Search by price")
    print("2: Search by food (category)")
    print("3: Display all")
    print("4: Edit canteen database")
    print("0: Back to location selection")

    user_option = check.user_input_index(0, 4)
    if user_option == 1:
        search_result = price_search(database)
    elif user_option == 2:
        search_result = food_search(database)
    elif user_option == 3:
        search_result = database
    elif user_option == 4:
        data_input.database_input()
        return main_menu()
    else:
        return None

    if search_result:
        display_table(search_result)
        sort_selection(search_result)
    else:
        print("Not Found!")
        return main_menu()


def price_search(database):
    print("\nPlease enter the maximum price:", end = " ")
    price = check.user_input_float()
    search_result = search.by_price(database, price)
    return search_result


def food_search(database):
    category = input("Please enter the category: ")
    search_result = search.by_food(database, category)
    return search_result


def sort_option():
    sort_choice = input("\nSort?[Y/n] ").lower().strip()
    if sort_choice == "y":
        return True
    elif sort_choice == "n":
        return False
    else:
        return sort_option()


def sort_selection(database):
    if sort_option():
        print("1: Sort by rank")
        print("2: Sort by distance")
        print("3: Sort by price")
        print("4: Sort by category")
        print("0: Back to main menu")
        user_option = check.user_input_index(0, 4)
        if user_option == 0:
            main_menu()
        elif user_option == 1:
            sorted_data = sort.by_rank(database)
        elif user_option == 2:
            sorted_data = sort.by_distance(user_location, database)
        elif user_option == 3:
            sorted_data = sort.by_price(database)
        elif user_option == 4:
            sorted_data = sort.by_category(database)
        display_table(sorted_data)
        choose_canteen(sorted_data)
    else:
        choose_canteen(database)


def display_table(database):
    table = PrettyTable(['No.', 'Canteen', 'Stall Name', 'Category', 'Rating', 'Average Price'])
    num = 0
    for key, value in database.items():
        num += 1
        table.add_row([num, key[0], key[2], key[3], value[0], value[1]])
    print("\nSearch Results\n", table)


def choose_canteen(database):
    list_canteen = list(database.items())
    print("Enter a number to choose a canteen stall")
    print("0: Back to main menu")
    user_option = check.user_input_index(0, len(list_canteen))
    if user_option > 0:
        stall = list_canteen[user_option - 1]
        display_info(database, stall)
    else:
        main_menu()


def display_info(database, stall):
    key, value = stall
    red_loop = data.get_bus_coordinates('red_loop')
    blue_loop = data.get_bus_coordinates('blue_loop')
    distance = display_distance(value[2], key[1])
    menu = display_food_menu(value[3])
    directions = transport.display_directions(key[1], user_location, red_loop, blue_loop)
    table = PrettyTable()
    table.add_column('', ['Canteen', 'Stall Name', 'Category', 'Rating', 'Average Price', 'Distance', 'Menu', 'Directions'])
    table.add_column('Information', [key[0], key[2], key[3], value[0], value[1], distance, menu, directions])
    print(table)
    print("0: Back to main menu")
    print("1: Back to canteen stall selection")
    user_option = check.user_input_index(0, 1)
    if user_option == 0:
        main_menu()
    elif user_option == 1:
        display_table(database)
        choose_canteen(database)


def display_food_menu(food_menu):
    str_list = []
    for food, price in food_menu.items():
        price = convert.float_to_dollar(price)
        str_list.extend([food, ": ", price, "\n"])
    return "".join(str_list)


def display_distance(distance, canteen_location):
    if distance == 0:
        distance = transport.distance_a_b(user_location, canteen_location)
        distance = convert.pixel_to_meter(distance)
    return " ".join([str(distance), "m"])
