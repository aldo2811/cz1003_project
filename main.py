import pygame


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


def get_user_location(user_location, mouse):
    """Displays an image of a location pin on the clicked area,
    and returns the coordinates of the 'dropped pin'.

    Args:
        user_location: coordinates of previous mouseclick on map area
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


def display_ok_pressed():
    """Changes the ok button image to an image of a pressed ok button,
    creating a real sense of clicking the button"""
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_pressed_img, ok_location)


def revert_display():
    """Reverts display to the usual display with the normal ok button"""
    screen.blit(map_img, background_location)
    screen.blit(instruction_text, instruction_location)
    screen.blit(pin_img, user_location)
    screen.blit(ok_button_img, ok_location)


def display_warning(warning):
    if warning:
        screen.blit(warning_text, warning_location)
        

# initialize pygame program
pygame.init()
resolution = (1600, 900)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('NTU F/B Recommendation')
background_location = (0, 0)
user_location = (1600, 900)
ok_location = (1200, 800)
warning_location = (1150, 750)
instruction_location = (350, 0)
map_img, pin_img, ok_button_img, ok_pressed_img = load_images()
text_font = pygame.font.SysFont('calibri', 36)
warning_text = text_font.render('Please mark your location!', False, (255, 0, 0))
instruction_text = text_font.render('Please mark your location and click the ok button to continue.', False, (0, 0, 0))
screen.blit(map_img, background_location)
screen.blit(instruction_text, instruction_location)
screen.blit(ok_button_img, ok_location)
pygame.display.flip()

clock = pygame.time.Clock()
fps = 60
running = True
ok_button_clicked = False
pin_dropped = False
warning = False
running = True
while running:
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        # breaks the loop if the user exits the pygame program
        if event.type == pygame.QUIT:
            running = False
        elif not ok_button_clicked:
            # detects events of left click only, so that other mouse buttons won't have any effect
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # detects event of clicking on the map area, which drops the pin
                if (mouse[0] < 1150 or mouse[1] < 750) and (65 < mouse[0] < 1535 and mouse[1] > 75):
                    pin_dropped = True
                    warning = False
                    user_location = get_user_location(user_location, mouse)
                # detects event of clicking the ok button
                elif 1200 <= mouse[0] <= 1505 and 800 <= mouse[1] <= 885:
                    ok_button_clicked = True
                    display_ok_pressed()
                    display_warning(warning)
        else:
            # if location has been marked, releasing the left mouse button on the ok button area finalizes the location and ends the pygame program
            if 1250 <= mouse[0] <= 1555 and 800 <= mouse[1] <= 885:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if pin_dropped:
                        running = False
                    # a warning will pop up to ensure the user marks their location before continuing
                    else:
                        ok_button_clicked = False
                        warning = True
                        revert_display()
                        display_warning(warning)
            # detects event of user hovering the mouse off the ok button while holding left mouse button down
            # hence the location is not finalized
            else:
                ok_button_clicked = False
                revert_display()
                display_warning(warning)

        print(event)

    pygame.display.flip()
    # sets the frame rate of the pygame program
    clock.tick(fps)
pygame.display.quit()
pygame.quit()



