import pygame


def load_images():
    """Loads images.

    Returns:
        map_img: image of NTU Map
        pin_img: image of location pin
        ok_button_img: image of ok button
        ok_pressed_img: image of ok button when pressed
    """
    map_img = pygame.image.load("map_1.png")
    map_img = pygame.transform.scale(map_img, (1600, 900))          
    pin_img = pygame.image.load("pin.png")
    ok_button_img = pygame.image.load("ok_button.png")
    ok_pressed_img = pygame.image.load("ok_button_pressed.png")
    return map_img, pin_img, ok_button_img, ok_pressed_img


def display_pin(pin_location, mouse):
    """Displays an image of a location pin on the clicked area,
    and returns the coordinates of the 'dropped pin'.

    Args:
        pin_location: coordinates of previous mouseclick on map area
        mouse: coordinates of current mouseclick
    
    Returns:
        pin_location: coordinates of current mouseclick with adjustment
    """
    screen.blit(map_img, (0, 0))
    screen.blit(ok_button_img, (ok_location[0], ok_location[1]))
    # there's an offset of '-17' to adjust the pin image with the cursor
    pin_location = [mouse[i] - 17 for i in range(2)]
    screen.blit(pin_img, (pin_location[0], pin_location[1]))
    return pin_location


# displays an image of a pressed button when the user clicks on the ok button
def display_ok_pressed():
    screen.blit(map_img, (0,0))
    screen.blit(pin_img, (pin_location[0], pin_location[1]))
    screen.blit(ok_pressed_img, ok_location)


def revert_display():
    screen.blit(map_img, (0,0))
    screen.blit(pin_img, (pin_location[0], pin_location[1]))
    screen.blit(ok_button_img, (ok_location[0], ok_location[1]))


# initialize pygame program
pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('NTU F/B Recommendation')
pin_location = (0, 0)
ok_location = (1250, 800)
warning_location = (1050, 0)
map_img, pin_img, ok_button_img, ok_pressed_img = load_images()
screen.blit(map_img, (0,0))
screen.blit(ok_button_img, ok_location)
pygame.display.flip()
text_font = pygame.font.SysFont('calibri', 48)
warning_text = text_font.render('Please mark your location!', False, (255, 0, 0))
clock = pygame.time.Clock()
fps = 60
running = True
ok_button_clicked = False
pin_dropped = False
warning = False

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
                if mouse[0] < 1200 or mouse[1] < 750:
                    pin_dropped = True
                    warning = False
                    pin_location = display_pin(pin_location, mouse)
                # detects event of clicking the ok button
                elif 1250 <= mouse[0] <= 1555 and 800 <= mouse[1] <= 885:
                    ok_button_clicked = True
                    display_ok_pressed()
                    if warning:
                        screen.blit(warning_text, warning_location)
        else:
            # if location has been marked, releasing the left mouse button on the ok button area finalizes the location and ends the pygame program
            if 1250 <= mouse[0] <= 1555 and 800 <= mouse[1] <= 885:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if pin_dropped:
                        running = False
                    # a warning will pop up to ensure the user picks a location before continuing
                    else:
                        ok_button_clicked = False
                        warning = True
                        revert_display()
                        screen.blit(warning_text, warning_location)
            # detects event of user hovering the mouse off the ok button while holding left mouse button down
            # hence the location is not finalized
            else:
                ok_button_clicked = False
                revert_display()
                if warning:
                    screen.blit(warning_text, warning_location)

        print(event)

    pygame.display.flip()
    if not running:
        break
    # sets the frame rate of the pygame program
    clock.tick(fps)

pygame.display.quit()
pygame.quit()