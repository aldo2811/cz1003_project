from library.prettytable import PrettyTable
import pygame
import module.tr as tr
import module.data as data
import module.search as search
import module.check as check


def load_images():
    """Loads images.

    Returns:
        map_img: image of NTU Map
        pin_img: image of location pin
        ok_button_img: image of ok button
        ok_pressed_img: image of ok button when pressed
    """
    map_img = pygame.image.load("image_files/map.png")
    map_img = pygame.transform.scale(map_img, (1600, 900))          
    pin_img = pygame.image.load("image_files/pin.png")
    ok_button_img = pygame.image.load("image_files/ok_button.png")
    ok_pressed_img = pygame.image.load("image_files/ok_button_pressed.png")
    return map_img, pin_img, ok_button_img, ok_pressed_img


def load_text():
    text_font = pygame.font.SysFont('calibri', 36)
    warning_text = text_font.render('Please mark your location!', False, (255, 0, 0))
    instruction_text = text_font.render('Please mark your location and click the ok button to continue.', False, (0, 0, 0))
    return warning_text, instruction_text


def get_user_location(mouse):
    """Displays an image of a location pin on the clicked area,
    and returns the coordinates of the 'dropped pin'.

    Args:
        mouse: coordinates of current mouseclick
    
    Returns:
        user_location: coordinates of current mouseclick with an adjustment
    """
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(ok_button_img, ok_location)
    # there's an offset of '-17' to adjust the pin image with the cursor
    user_location = [mouse[i] - 17 for i in range(2)]
    screen.blit(pin_img, user_location)
    return user_location


def display_ok_pressed(user_location):
    """Changes the ok button image to an image of a pressed ok button,
    creating a real sense of clicking the button"""
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_pressed_img, ok_location)


def revert_display(user_location):
    """Reverts display to the usual display with the normal ok button"""
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_button_img, ok_location)


def display_warning(warning):
    if warning:
        screen.blit(warning_text, warning_location)
        

def pygame_main():
    # use to set how fast the screen updates
    clock = pygame.time.Clock()

    # initial values
    # user_location is set to the bottom right corner of the screen (1600x900) to ensure that it is out of the display initially
    user_location = (1600, 900)
    ok_button_clicked = False
    pin_dropped = False
    warning = False
    pygame_running = True
    force_close = False

    while pygame_running:
        for event in pygame.event.get():
            # gets current position of mouse cursor in the form of (X,Y)
            mouse = pygame.mouse.get_pos()

            # break the loop if user closes pygame window
            if event.type == pygame.QUIT:
                force_close = True
                pygame_running = False

            elif not ok_button_clicked:
                # detects events of left click only, so that other mouse buttons won't have any effect
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # detects event of clicking on the map area, which drops the pin
                    if (mouse[0] < 1150 or mouse[1] < 750) and (65 < mouse[0] < 1535 and mouse[1] > 75):
                        pin_dropped, warning = True, False
                        user_location = get_user_location(mouse)
                        print(user_location)
                    # detects event of clicking the ok button
                    elif 1200 <= mouse[0] <= 1505 and 800 <= mouse[1] <= 885:
                        ok_button_clicked = True
                        display_ok_pressed(user_location)
                        display_warning(warning)

            # if location has been marked, releasing the left mouse button on the ok button area finalizes the location and ends the pygame program
            elif 1250 <= mouse[0] <= 1555 and 800 <= mouse[1] <= 885:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if pin_dropped:
                        pygame_running = False
                    # a warning will pop up to ensure the user marks their location before continuing
                    else:
                        ok_button_clicked, warning = False, True
                        revert_display(user_location)
                        display_warning(warning)

            # detects event of user hovering the mouse off the ok button while holding left mouse button down
            # hence the location is not finalized
            else:
                ok_button_clicked = False
                revert_display(user_location)
                display_warning(warning)

        pygame.display.flip()
        # sets the frame rate limit of the pygame program (per second)
        clock.tick(60)
    pygame.display.quit()
    pygame.quit()
    if force_close:
        return None
    else:
        return user_location
    

def main_menu():
    database = data.import_canteen_database()
    print("Welcome to the NTU F/B Recommendation System!")
    print("Please enter the input number that corresponds to the option you'd like to choose.", end = "\n\n")
    print("1: Search by price")
    print("2: Search by food (category)")
    print("3: Display all")
    print("4: Edit canteen database")
    print("0: Back to location selection")

    user_option = check.user_input_index(0, 4)
    if user_option == 1:
        search_result = menu_price_search(database)
    elif user_option == 2:
        search_result = menu_food_search(database)
    elif user_option == 3:
        search_result = database
    elif user_option == 4:
        database_input()
        main_menu()
    else:
        return None

    if search_result:
        display_table(search_result)
        menu_sort_selection(search_result)
    else:
        print("Not Found!")
        main_menu()


def menu_price_search(database):
    print("Please enter the maximum price")
    price = check.user_input_float()
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
        user_option = check.user_input_index(0, 4)
        if user_option == 0:
            return main_menu()
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
    user_option = check.user_input_index(0, len(list_canteen))
    if user_option > 0:
        stall = list_canteen[user_option - 1]
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
    user_option = check.user_input_index(0, 1)
    if user_option == 0:
        main_menu()
    elif user_option == 1:
        display_table(database)
        choose_canteen(database)


#cannot assign numerical to smth
def menu_canteen_name():
    print("Here is a list of canteen name")
    print("1 = North Spine Food Court")
    print("2 = Koufu")
    print("3 = Canteen 1")
    print("4 = Canteen 2")
    print("5 = Canteen 9")
    print("6 = Canteen 11")
    print("7 = Canteen 13")
    print("8 = Canteen 14")
    print("9 = Canteen 16")
    print("10 = The Quad Cafe")
    print("11 = Foodgle Food Court")
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
        canteen_name = "Canteen 4"
    elif option == 12:
        canteen_name = "North Hill Food Court"
       
    return canteen_name


def stall_category():
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
    print("Enter the option for stall category: ")

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


def input_data():
    canteen_name = menu_canteen_name()
    stall_name = input("Enter stall name: ")
    stall_category1 = stall_category() #cant have stall_category = stall_category()
    print("Enter stall rating (0-5): ")
    stall_rating = check.user_input_index(0, 5)
    entry = [canteen_name, stall_name, stall_category1, stall_rating]
    menu = 0
    while True:
        if menu < 1:
            food_name = input("Enter food name: ")
        else:
            food_name = input("Enter '####' to terminate, Enter food name: ")
        
        if food_name == "####":
            break
        else:
            print("Enter price: ")
            food_price = check.user_input_float()
            entry.extend([food_name, food_price])
        menu += 1
    entry = [str(data) for data in entry]
    return entry


def database_input():
    while True:
        print("1: Input data")
        print("0: Back to main menu")
        option = check.user_input_index(0, 1)
        if option == 1:
            data = ",".join(input_data())
            with open("canteen_data.txt", "a") as csv_file:
                csv_file.write("\n" + data)
        elif option == 0:
            break


while True:
    # initialize pygame program
    pygame.init()

    # set window size
    screen = pygame.display.set_mode((1600, 900))

    # set window title
    pygame.display.set_caption('NTU F/B Recommendation')

    # assign initial locations
    background_location = (0, 0)
    ok_location = (1200, 800)
    warning_location = (1150, 750)
    instruction_location = (350, 0)

    # load and display images and text
    map_img, pin_img, ok_button_img, ok_pressed_img = load_images()
    warning_text, instruction_text = load_text()
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(ok_button_img, ok_location)
    pygame.display.flip()

    user_location = pygame_main()
    if user_location:
        main_menu()
    else:
        break