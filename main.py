from library.prettytable import PrettyTable
import pygame
import module.menu as menu


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
    text_font = pygame.font.SysFont('calibri', 36)
    warning_text = text_font.render(
        'Please mark your location!', False, (255, 0, 0))
    instruction_text = text_font.render(
        'Please mark your location and click the ok button to continue.', False, (0, 0, 0))
    return warning_text, instruction_text


def get_user_location(mouse):
    """Displays an image of a location pin on the clicked area,
    and returns the coordinates of the 'dropped pin'.

    Args:
        mouse ((int, int) -> list or tuple): Coordinates of current mouseclick.

    Returns:
        user_location ([int, int] -> list): Coordinates of current mouseclick with an adjustment.
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
    creating a real sense of clicking the button.
    
    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
    """
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_pressed_img, ok_location)


def revert_display(user_location):
    """Reverts display to the usual display with the normal ok button.
    
    Args:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user.
    """
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_button_img, ok_location)


def display_warning(warning):
    """Displays warning text.
    
    Args:
        warning (bool): False if the user has marked location, otherwise True.
    """
    if warning:
        screen.blit(warning_text, warning_location)


def pygame_main():
    """Main pygame interface function.

    Returns:
        user_location ((int, int) -> tuple): Coordinates of location that is marked by the user, if the program is not force closed. 
    """
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

    # run pygame interface
    user_location = pygame_main()

    if user_location:
        menu.import_user_location(user_location)
        menu.main_menu()
    # if pygame is closed
    else:
        break