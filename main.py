from library.prettytable import PrettyTable
import pygame
import sys
import module.menu as menu
import module.data as data


def load_images():
    """Loads images.

    Returns:
        map_img: Image of NTU Map.
        pin_img: Image of location pin.
        ok_button_img: Image of ok button.
        ok_pressed_img: Image of ok button when pressed.
    """
    map_img = pygame.image.load("image_files/map.png")
    map_img = pygame.transform.scale(map_img, (1600, 900))
    pin_img = pygame.image.load("image_files/pin.png")
    ok_button_img = pygame.image.load("image_files/ok_button.png")
    ok_pressed_img = pygame.image.load("image_files/ok_button_pressed.png")
    return map_img, pin_img, ok_button_img, ok_pressed_img


def load_text():
    """Loads and renders text.

    Returns:
        warning_text: Warning text if user have not marked their location.
        instruction_text: Instruction text for the pygame program.
    """
    instruction_font = pygame.font.SysFont('calibri', 36)
    warning_text = instruction_font.render('Please mark your location!', False, (255, 0, 0))
    instruction_text = instruction_font.render('Please mark your location and click the ok button to continue.', False, (0, 0, 0))
    return warning_text, instruction_text


def get_user_location(mouse):
    """Displays an image of a location pin on the clicked area,
    and returns the coordinates of the 'dropped pin'.

    Args:
        mouse ((int, int) -> list or tuple): Coordinates of current mouseclick.

    Returns:
        user_location ([int, int] -> list): Coordinates of current mouseclick with an adjustment.
    """
    user_location = mouse
    # there's an offset of '-16' to adjust the pin image with the cursor
    display_location = [user_location[i] - 16 for i in range(2)]

    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(ok_button_img, ok_location)
    screen.blit(pin_img, display_location)
    return user_location


def display_ok_pressed(user_location):
    """Changes the ok button image to an image of a pressed ok button,
    creating a real sense of clicking the button.
    
    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
    """
    # display adjustment
    display_location = [user_location[i] - 16 for i in range(2)]

    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, display_location)
    screen.blit(ok_pressed_img, ok_location)


def revert_display(user_location):
    """Reverts display to the usual display with the normal ok button.
    
    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
    """
    # display adjustment
    display_location = [user_location[i] - 16 for i in range(2)]

    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, display_location)
    screen.blit(ok_button_img, ok_location)


def display_warning(warning):
    """Displays warning text.
    
    Args:
        warning (bool): False if the user has marked location, otherwise True.
    """
    if warning:
        screen.blit(warning_text, warning_location)


def display_popup(coordinates):
    """Displays pop-up box.
    
    Args:
        coordinates ((int, int) -> tuple): Canteen coordinates.
    """
    x, y = coordinates
    pygame.draw.rect(screen, (0, 0, 150), [x-60, y-30, 120, 20])


def display_popup_text(canteen, coordinates):
    """Displays canteen name on the pop-up box.
    
    Args:
        canteen (str): Canteen name.
        coordinates ((int, int) -> tuple): Canteen coordinates.
    """
    x, y = coordinates
    # create font object of pop-up
    # initialize only when needed, to prevent it from causing errors
    popup_font = pygame.font.SysFont('calibri', 12)
    popup_text = popup_font.render(canteen, False, (255, 255, 255))

    # assign center location of text to align it with the pop-up box
    text_rect = popup_text.get_rect()
    text_rect.center = (x, y - 20)
    screen.blit(popup_text, text_rect)


def detect_point_hover(user_location, mouse, ok_button_clicked, warning):
    """Detects event of user hovering their mouse cursor over the canteen locations / points.

    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by user.
        mouse ((int, int) -> tuple): Current coordinates of mouse cursor.
        ok_button_clicked (bool): True if ok button is being clicked, otherwise False.
        warning (bool): True if user clicks ok button but has not marked their location, otherwise False.
    """
    # no need to check if ok button is clicked
    if not ok_button_clicked:
        # check every canteen's location / point
        for canteen, xy in canteen_coordinates:
            # size of each canteen point is 16x16, 
            # hence the surface adjustment of ± 8 pixels
            if xy[0] - 8 <= mouse[0] <= xy[0] + 8 and xy[1] - 8 <= mouse[1] <= xy[1] + 8:
                display_popup(xy)
                display_popup_text(canteen, xy)
                break
        # if loop does not break
        else:
            revert_display(user_location)
            display_warning(warning)


def pygame_main(user_location):
    """Main pygame interface function.

    Returns:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user, if the program is not force closed. 
    """
    # use to set how fast the screen updates
    clock = pygame.time.Clock()

    # initial values
    if start == 1:
        pin_dropped = False
    else:
       pin_dropped = True
    ok_button_clicked = False
    warning = False
    pygame_running = True

    while pygame_running:
        pygame.event.pump()
        for event in pygame.event.get():
            # gets current position of mouse cursor in the form of (X,Y)
            mouse = pygame.mouse.get_pos()
 
            # quit python if user closes pygame window
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif not ok_button_clicked:
                # detects events of left click only, so that other mouse buttons won't have any effect
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # detects event of clicking on the map area, which drops the pin
                    if (mouse[0] < 1150 or mouse[1] < 750) and (65 < mouse[0] < 1535 and mouse[1] > 75):
                        pin_dropped, warning = True, False
                        user_location = get_user_location(mouse)
                    # detects event of clicking the ok button
                    elif 1200 <= mouse[0] <= 1505 and 800 <= mouse[1] <= 885:
                        ok_button_clicked = True
                        display_ok_pressed(user_location)
                        display_warning(warning)

                detect_point_hover(user_location, mouse, ok_button_clicked, warning)

            # if location has been marked, releasing the left mouse button on the ok button area finalizes the location and ends the pygame program
            elif 1250 <= mouse[0] <= 1555 and 800 <= mouse[1] <= 885:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if pin_dropped:
                        pygame_running = False
                        break
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

    # make sure pygame program is properly closed
    pygame.font.quit()
    pygame.display.quit()
    pygame.quit()

    return user_location

start = 0
canteen_coordinates = data.import_canteen_coordinates()
while True:
    start += 1
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
    if start == 1:
        # user_location is set to the bottom right corner of the screen (1600x900),
        # to ensure that it is out of the display initially
        user_location = (1600, 900)

    

    # load and display images and text
    map_img, pin_img, ok_button_img, ok_pressed_img = load_images()
    warning_text, instruction_text = load_text()
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(ok_button_img, ok_location)
    pygame.display.flip()

    # run pygame interface
    user_location = pygame_main(user_location)

    if user_location:
        # pass user_location variable to menu.py file
        menu.import_user_location(user_location)

        # run command line interface
        menu.main_menu()
    # if pygame is closed
    else:
        break