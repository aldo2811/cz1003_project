import functions.tr as tr
database = {("canteen1",(500,200),"yong tau foo","chinese"):[{"wanton seafood":5, "wanton behoon":4}],
                ("canteen2",(200,100),"the western place","western"):[{"beef":4}],
                ("canteen3",(480,122),"indian cuisine","indian") :[{"spicy":2}],
                ("canteen1",(500,200),"the pork specialty","western"):[{"pork belly":3}]}
user_location = (0,0)

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
    for key in database.keys():
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
        pass
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
    sort_selection_menu()


def sort_option():
    sort_choice = input("\nSort?[Y/n]").lower().strip()
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
        print("3: Sort by price")
        print("0: Back to main menu")
        user_option = input()
        if user_option == "0":
            main_menu()
        elif user_option == "1":
            sorted_data = tr.sort_by_rank(database)
            print(sorted_data)  # for now
        elif user_option == "2":
            sorted_data = tr.sort_distance(user_location, database)
            print(sorted_data)  # for now
        elif user_option == "3":
            sorted_data = tr.sort_by_price(database)
            print(sorted_data)
        else:
            print("Error! Invalid input!")
            return selection_menu
    else:
        print("0: Back to main menu")
        user_option = input()
        if user_option == "0":
            main_menu()
        else: pass


main_menu()
        
        