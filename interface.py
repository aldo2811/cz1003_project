from library.prettytable import PrettyTable
import module.tr as tr
import module.data as data
import module.search as search

user_location = (0,0)


def user_input_index(min_index, max_index):
    user_input = input()
    if user_input.isdigit() and min_index <= int(user_input) <= max_index:
        return int(user_input)
    else:
        print("Error! Invalid input!")
        return user_input_index(min_index, max_index)


def user_input_float():
    user_input = input()
    try:
        return float(user_input)
    except:
        print("Error! Invalid input!")
        return user_input_float()
    

def main_menu():
    database = data.import_canteen_database()
    print("Welcome to the NTU F/B Recommendation System!")
    print("Please enter the input number that corresponds to the option you'd like to choose.", end = "\n\n")
    print("List of Canteens in NTU")
    canteen_list = []
    for key in database.keys():
        if key[0] not in canteen_list:
            canteen_list.append(key[0])
            print(key[0])
    main_menu_selection(database)


def main_menu_selection(database):
    print("1: Search by price")
    print("2: Search by food (category)")
    print("3: Display all")
    print("0: Back to location selection")
    user_option = user_input_index(0, 3)
    if user_option == 0:
        pass
        # location_selection()
    elif user_option == 1:
        search_result = menu_price_search(database)
    elif user_option == 2:
        search_result = menu_food_search(database)
    elif user_option == 3:
        search_result = database

    if search_result:
        display_table(search_result)
        menu_sort_selection(search_result)
    else:
        print("Not Found!")
        main_menu_selection(database)


def menu_price_search(database):
    print("Please enter the maximum price")
    price = user_input_float()
    search_result = search.search_by_price(database, price)
    return search_result


def menu_food_search(database):
    category = input("Please enter the category")
    search_result = search.search_by_food(database, category)
    return search_result


def sort_option():
    sort_choice = input("\nSort?[Y/n]").lower().strip()
    if sort_choice == "y":
        return True
    elif sort_choice == "n":
        return False
    else:
        return sort_option()


def menu_sort_selection(database):
    if sort_option():
        print("1: Sort by rank")
        print("2: Sort by distance")
        print("3: Sort by price")
        print("4: Sort by category")
        print("0: Back to main menu")
        user_option = user_input_index(0, 4)
        if user_option == 0:
            main_menu()
        elif user_option == 1:
            sorted_data = tr.sort_by_rank(database)
        elif user_option == 2:
            sorted_data = tr.sort_distance(user_location, database)
        elif user_option == 3:
            sorted_data = tr.sort_by_price(database)
        elif user_option == 4:
            sorted_data = tr.sort_by_category(database)
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
    print(table)


def choose_canteen(database):
    list_canteen = list(database.items())
    print("Enter a number to choose a canteen stall")
    print("0: Back to main menu")
    user_input = user_input_index(0, len(list_canteen))
    if user_input > 0:
        stall = list_canteen[user_input - 1]
        display_info(database, stall)
    else:
        main_menu()


def display_info(database, stall):
    key, value = stall
    if value[2] == 0:
        value[2] = tr.distance_a_b(user_location, key[1])
    table = PrettyTable()
    table.add_column('', ['Canteen', 'Stall Name', 'Category', 'Rating', 'Average Price', 'Distance', 'Menu'])
    table.add_column("Information", [key[0], key[2], key[3], value[0], value[1], value[2], value[3]])
    print(table)
    print("0: Back to main menu")
    print("1: Back to canteen stall selection")
    user_option = user_input_index(0, 1)
    if user_option == 0:
        main_menu()
    elif user_option == 1:
        display_table(database)
        choose_canteen(database)

main_menu()