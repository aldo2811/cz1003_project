def user_input_float():
    user_input = input()
    try:
        return float(user_input)
    except:
        print("Error! Invalid input!")
        return user_input_float()
    

def main_menu():
    print("Welcome to the NTU F/B Recommendation System!")
    print("Please enter the input number that corresponds to the option you'd like to choose.", end = "\n\n")
    print("List of Canteens in NTU")
    canteen_list = []
    for key in dic.keys():
        if key[0] not in canteen_list:
            canteen_list.append(key[0])
            print(key[0])
    selection_menu()


def selection_menu():
    print("1: Search by price")
    print("2: Search by food (category)")
    print("3: Display all")
    print("0: Back to location selection")
    user_option = input()
    if user_option == "0":
        # location_selection()
    elif user_option == "1":
        price_search_menu()
    elif user_option == "2":
        food_search_menu()
    elif user_option == "3":
        display_all_menu()
    else:
        print("Error! Invalid input!")
        return selection_menu


def price_search_menu():
    print("Please enter the maximum price")
    price = user_input_float()
    search_result = search_by_price(price, database)
    print(search_result)  # for now
    sort_selection_menu()


def food_search_menu():
    category = input("Please enter the category")
    search_result = search_by_food(category, foodlist_canteens)
    if search_result:
        print(search_result)  # for now
    else:
        print("Not Found!")
    sort_selection_menu()


def display_all_menu():
    print(database)  # for now


def sort_option():
    sort_choice = input("Sort?[Y/n]").lower().strip()
    if sort_choice == "y":
        return True
    elif sort_choice == "n":
        return False
    else:
        return sort_option()


def sort_selection_menu():
    if sort_option():
        print("1: Sort by rank")
        print("2: Sort by distance")
        print("0: Back to main menu")
        user_option = user_input_digit()
        if user_option == "0":
            main_menu()
        elif user_option == "1":
            sorted_data = sort_by_rank()
            print(sorted_data)  # for now
        elif user_option == "2":
            sorted_data = sort_by_distance()
            print(sorted_data)  # for now


main_menu()
        
        