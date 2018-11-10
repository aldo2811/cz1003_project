"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

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
    database = data.import_canteen_database(user_location)

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
    """Menu for searching by price.

    Args:
        database (dict): Canteen database.

    Returns:
        search_result (dict): Canteen database which only contains stalls that have an average price of less than the price specified by user.
    """
    print("\nPlease enter the maximum price:", end = " ")
    price = check.user_input_float()
    search_result = search.by_price(database, price)
    return search_result


def food_search(database):
    """Menu for searching by category.

    Args:
        database (dict): Canteen database.
    
    Returns:
        search_result (dict): Canteen database which only contains stalls which are the same category as specified by user. 
    """
    category = input("Please enter the category: ")
    search_result = search.by_food(database, category)
    return search_result


def sort_option():
    """Asks user whether they want to sort or not.

    Returns:
        True if the user wants to sort, False otherwise.
        Returns itself and keeps on asking for user input if it is invalid.
    """
    sort_choice = input("\nSort?[Y/n] ").lower().strip()
    if sort_choice == "y":
        return True
    elif sort_choice == "n":
        return False
    else:
        return sort_option()


def sort_selection(database):
    """Menu for selecting which way to sort.
    
    Args:
        database (dict): Canteen database.
    """
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
            sorted_data = sort.by_distance(database)
        elif user_option == 3:
            sorted_data = sort.by_price(database)
        elif user_option == 4:
            sorted_data = sort.by_category(database)

        # display sorted database using table
        display_table(sorted_data)
        choose_canteen(sorted_data)
    else:
        choose_canteen(database)


def display_table(database):
    """Displays the database in the form of table.

    Args:
        database (dict): Canteen database.
    """
    # table header row
    table = PrettyTable(['No.', 'Canteen', 'Stall Name', 'Category', 'Rating', 'Average Price', 'Distance'])
    num = 0
    for key, value in database.items():
        num += 1
        distance = convert.pixel_to_meter(value[2])
        distance = "".join([str(distance), " m"])
        table.add_row([num, key[0], key[2], key[3], value[0], value[1], distance])
    print("\nSearch Results\n")
    print(table)


def choose_canteen(database):
    """Asks the user to choose a canteen stall from the table.

    Args:
        database (dict): Canteen database.
    """
    list_canteen = list(database.items())
    print("Enter a number to choose a canteen stall")
    print("0: Back to main menu")

    # the number options are displayed on the table
    user_option = check.user_input_index(0, len(list_canteen))
    if user_option > 0:
        stall = list_canteen[user_option - 1]
        display_info(database, stall)
    else:
        main_menu()


def display_info(database, stall):
    """Displays information of stall in the form of table.

    Args:
        database (dict): Canteen database.
        stall ((key, value) -> tuple): Data of a stall. Format is similar to database but type is tuple.
    """
    key, value = stall

    # format data for display
    avg_price = convert.float_to_dollar(value[1])
    distance = convert.pixel_to_meter(value[2])
    distance = " ".join([str(distance), "m"])
    menu = display_food_menu(value[3])
    directions = transport.display_directions(stall, user_location)

    table = PrettyTable()
    table.add_column('', ['Canteen', 'Stall Name', 'Category', 'Rating', 'Average Price', 'Distance', 'Menu', 'Directions'])
    table.add_column('Information', [key[0], key[2], key[3], value[0], avg_price, distance, menu, directions])
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
    """Formats the menu information to be displayed on the stall information.

    Args:
        food_menu ({str: float} -> dict): A dictionary that contains the stall's food and their prices
    
    Returns:
        str: Formatted string of the stall menu.
    """
    str_list = []
    for food, price in food_menu.items():
        price = convert.float_to_dollar(price)
        str_list.extend([food, ": ", price, "\n"])
    return "".join(str_list)
