import module.check as check

def get_coordinate(database, name):
    keys = database.keys()
    for key in keys:
        if key[0] == name:
            coordinate = key[1]
            return coordinate


#cannot assign numerical to smth
def canteen_name_and_coordinate():
    print("Here is a list of canteen name")
    print("1 = North Spine Food Court")
    print("2 = Koufu")
    print("3 = Canteen 1")
    print("4 = Canteen 2")
    print("5 = Canteen 4")
    print("6 = Canteen 9")
    print("7 = Canteen 11")
    print("8 = Canteen 13")
    print("9 = Canteen 14")
    print("10 = Canteen 16")
    print("11 = The Quad Cafe")
    print("12 = North Hill Food Court")
    print("Enter the option for canteen name: ")
#must rmb to put int if not put inverted comma for anything that is input because it is a string        
    option = check.user_input_index(0, 12)
    if option == 1:
        canteen_name = "North Spine Food Court"
    elif option == 2:
        canteen_name = "Koufu"
    elif option == 3:
        canteen_name = "Canteen 1"
    elif option == 4:
        canteen_name = "Canteen 2"
    elif option == 5:
        canteen_name = "Canteen 4"
    elif option == 6:
        canteen_name = "Canteen 9"
    elif option == 7:
        canteen_name = "Canteen 11"
    elif option == 8:
        canteen_name = "Canteen 13"
    elif option == 9:
        canteen_name = "Canteen 14"
    elif option == 10:
        canteen_name = "Canteen 16"
    elif option == 11:
        canteen_name = "The Quad Cafe"
    elif option == 12:
        canteen_name = "North Hill Food Court"
       
    coordinate = get_coordinate(database, canteen_name)
    return canteen_name, coordinate


def stall_category():
    print("Here is a list of stall categories")
    print("1 = Halal")
    print("2 = Chinese")
    print("3 = Indian")
    print("4 = Vegetarian")
    print("5 = Japanese")
    print("6 = Korean")
    print("7 = Seafood")
    print("8 = Singaporean")
    print("9 = Others")
    print("Enter the option for stall category: ")

    option = check.user_input_index(0, 9)
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


def input_data():
    canteen_name, coordinate = canteen_name_and_coordinate()
    stall_name = input("What is the stall name: ")
    stall_category1 = stall_category() #cant have stall_category = stall_category()
    print("What is the stall rating (0-5): ")
    stall_rating = check.user_input_index(0, 5)
    data = [canteen_name, coordinate[0], coordinate[1], stall_name, stall_category1, stall_rating]
    while True:
        food_name = input("Enter '####' to terminate, What is the food name: ")
        if food_name == "####":
            break
        else:
            print("what is the price: ")
            food_price = check.user_input_float()
            data.extend(food_name, food_price)
    return data


def database_input():
    with open("canteen_database.txt", "a") as csv_file:
        while True:
            print("1 = Input data")
            print("2 = Quit")
            option = int(input("Enter your option: "))
            if option == 1:
                data = ",".join(input_data())
                csv_file.write(data)
            elif option == 2:
                break
