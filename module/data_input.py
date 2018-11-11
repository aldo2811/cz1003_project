import csv
from library.prettytable import PrettyTable
import module.check as check
import module.data as data


def get_canteen_name():
    """Displays the list of canteen for the data input and lets the user to choose.

    Returns:
        canteen_name (str): The name of the canteen of which the user choose.
    """
    print("Here is a list of canteen name")
    print("1: North Spine Food Court")
    print("2: Koufu")
    print("3: Canteen 1")
    print("4: Canteen 2")
    print("5: Canteen 9")
    print("6: Canteen 11")
    print("7: Canteen 13")
    print("8: Canteen 14")
    print("9: Canteen 16")
    print("10: The Quad Cafe")
    print("11: Foodgle Food Court")
    print("12: North Hill Food Court")
    print("Enter the option for canteen name:", end = " ")

    # only allow inputs from 1 to 12 for the 12 options
    option = check.user_input_index(1, 12)

    if option == 1:
        canteen_name = "North Spine Food Court"
    elif option == 2:
        canteen_name = "Koufu"
    elif option == 3:
        canteen_name = "Canteen 1"
    elif option == 4:
        canteen_name = "Canteen 2"
    elif option == 5:
        canteen_name = "Canteen 9"
    elif option == 6:
        canteen_name = "Canteen 11"
    elif option == 7:
        canteen_name = "Canteen 13"
    elif option == 8:
        canteen_name = "Canteen 14"
    elif option == 9:
        canteen_name = "Canteen 16"
    elif option == 10:
        canteen_name = "The Quad Cafe"
    elif option == 11:
        canteen_name = "Foodgle Food Court"
    elif option == 12:
        canteen_name = "North Hill Food Court"

    return canteen_name


def get_stall_category():
    """Displays the list of stall categories for the data input and lets the user choose.

    Returns:
        stall_category (str): The stall category which the user chooses.
    """
    print("Here is a list of stall categories")
    print("1: Halal")
    print("2: Chinese")
    print("3: Indian")
    print("4: Vegetarian")
    print("5: Japanese")
    print("6: Korean")
    print("7: Seafood")
    print("8: Singaporean")
    print("9: Others")
    print("Enter the option for stall category:", end = " ")

    # only allows inputs from 1 to 9 for the 9 options
    option = check.user_input_index(1, 9)

    if option == 1:
        stall_category = "Halal"
    elif option == 2:
        stall_category = "Chinese"
    elif option == 3:
        stall_category = "Indian"
    elif option == 4:
        stall_category = "Vegetarian"
    elif option == 5:
        stall_category = "Japanese"
    elif option == 6:
        stall_category = "Korean"
    elif option == 7:
        stall_category = "Seafood"
    elif option == 8:
        stall_category = "Singaporean"
    elif option == 9:
        stall_category = "Others"

    return stall_category


def menu_input_data():
    """Menu for adding new canteen data to the database. Stores the data inside a list.

    Returns:
        stall_data (list): A list containing with data of a new stall.
            Format: [canteen_name, stall_name, stall_category, stall_rating, food1, price1, food2, price2, ...]
    """
    # ask user input for the new stall data
    canteen_name = get_canteen_name()
    print("Enter stall name:", end = " ")
    # stall name cannot be empty
    stall_name = check.non_empty_input()
    stall_category = get_stall_category()
    print("Enter stall rating (0-5):", end = " ")
    stall_rating = check.user_input_index(0, 5)

    # data order is adjusted according to the file
    stall_data = [canteen_name, stall_name, stall_category, stall_rating]
    menu = 0

    while True:
        # user needs to enter at least 1 menu for each stall
        # food name cannot be empty
        if menu < 1:
            print("Enter food name:", end =" ")
            food_name = check.non_empty_input()
        else:
            print("Enter '####' to terminate, Enter food name:", end = " ")
            food_name = check.non_empty_input()
            if food_name == "####":
                break

        print("Enter price:", end = " ")
        food_price = check.user_input_float()
        stall_data.extend([food_name, food_price])
        menu += 1
    # convert the data to string to be written to file
    stall_data = [str(data) for data in stall_data]
    return stall_data


def input_data(stall_data):
    """Append new data to database file.

    Args:
        stall_data (list): A list containing data of a new stall.
    """
    with open("data/canteen_data.txt", 'a', newline='\n') as csv_file:
        rows = csv.writer(csv_file)
        rows.writerow(stall_data)


def menu_edit_database():
    """Menu for modifying data."""
    while True:
        print("1: Input data")
        print("2: Delete data")
        print("0: Back to main menu")

        option = check.user_input_index(0, 2)
        if option == 1:
            stall_data = menu_input_data()
            input_data(stall_data)
        elif option == 2:
            # get data from file
            with open("data/canteen_data.txt", "r") as csv_file:
                list_canteen = list(csv.reader(csv_file))
            stall_data = menu_delete_data(list_canteen)
            if stall_data:
                delete_data(stall_data, list_canteen)
        else == 0:
            break


def menu_delete_data(list_canteen):
    """Menu for deleting data.
    
    Args:
        list_canteen ([[str, str, str,...]] -> list): List of all stall data imported from csv file.
            List has the same format as the data in the file.
    
    Returns:
        stall ([str, str, str,...] -> list): List of one stall data.
            Same format as data in csv file.
    """
    # display table so that user can easily select which data to remove
    table = PrettyTable(['No.', 'Canteen', 'Stall Name', 'Category'])
    num = 1
    for canteen in list_canteen:
        table.add_row([num, canteen[0], canteen[1], canteen[2]])
        num += 1

    print(table)
    print("Enter the corresponding number of a stall to delete it.")
    print("0: Back")

    # allow digit input from 0 to max number of stall
    user_option = check.user_input_index(0, len(list_canteen))
    if user_option > 0:
        stall = list_canteen[user_option - 1]
        return stall
    else:
        return None


def delete_data(stall_data, list_canteen):
    with open("data/canteen_data.txt", "w", newline='\n') as csv_file:
        writer = csv.writer(csv_file)
        for data in list_canteen:
            if data != stall_data:
                writer.writerow(data)

