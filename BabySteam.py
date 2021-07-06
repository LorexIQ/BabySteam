import pygame
import List
import InformationMenu
import MyClassBSgames
import Buttons

WIDTH = 190
HEIGHT = 470
X_POS = 10
Y_POS = 10
X_BUTTON = 590
Y_BUTTON = 440
WIDTH_BUTTON = 200
HEIGHT_BUTTON = 50
X_INFORMATION_WIN = 250
Y_INFORMATION_WIN = 10
WIDTH_INFORMATION_WIN = 540
HEIGHT_INFORMATION_WIN = 420
size_block = 35
size_slider = 20
step_scrol = 17

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE_ACTIVE = (58, 101, 148)
DARK_BLUE = (0, 64, 107)
DARK_BLUE_LIST = (0, 33, 55)
DARK_BLUE_INACTIVE = (29,51,74)
BUTTON_INSTALL = (0, 103, 126)
BUTTON_DELETE = (200, 0, 0)
BUTTON_RUN = (0, 128, 0)

pygame.init()
clock = pygame.time.Clock()

Start_main = pygame.display.set_mode((300, 100), pygame.NOFRAME)
Start_main.fill(DARK_BLUE_INACTIVE)
font_loading = pygame.font.Font("Font/List.ttf", 35)
text_loading = font_loading.render("Loading...", True, GRAY)
Start_main.blit(text_loading, (Start_main.get_width() / 2 - text_loading.get_width() / 2, Start_main.get_height() / 2 - text_loading.get_height() / 2))
pygame.display.flip()


List_images = MyClassBSgames.Update()
count = len(List_images)

main = pygame.display.set_mode((800, 500))
getList = List.List(main, size_slider, X_POS, Y_POS, WIDTH, HEIGHT, step_scrol, count, DARK_BLUE, DARK_BLUE_INACTIVE, DARK_BLUE_ACTIVE, GRAY, List_images, size_block)
InformationWindow = InformationMenu.Window(X_INFORMATION_WIN, Y_INFORMATION_WIN, WIDTH_INFORMATION_WIN, HEIGHT_INFORMATION_WIN, DARK_BLUE_LIST, main, List_images)
getButton = Buttons.MultiButton(main, X_BUTTON, Y_BUTTON, WIDTH_BUTTON, HEIGHT_BUTTON, List_images, BUTTON_INSTALL, BUTTON_DELETE, BUTTON_RUN)



while True:
    main.fill(DARK_BLUE_INACTIVE)

    getList.draw(DARK_BLUE_LIST)
    getButton.draw()
    InformationWindow.draw(List.Position_selected)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                getList.Motion(True)
                break
            elif event.button == 5:
                getList.Motion(False)
                break
        action = getButton.active(event, pos, List.Position_selected)
        if action:
            List_images = MyClassBSgames.Update()
            getList = List.List(main, size_slider, X_POS, Y_POS, WIDTH, HEIGHT, step_scrol, count, DARK_BLUE,
                                DARK_BLUE_INACTIVE, DARK_BLUE_ACTIVE, GRAY, List_images, size_block)
            getList.group.update(pos, getList.Elements)
        getList.Active(event, pos)
        if getList.activate_slider:
            getList.slider.Active(event, pos)

    pygame.display.flip()
    clock.tick(60)