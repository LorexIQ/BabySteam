import pygame
import List
import InformationMenu
import MyClassBSgames

WIDTH = 190
HEIGHT = 470
X_POS = 10
Y_POS = 10
size_block = 35
size_slider = 20
step_scrol = 17

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE_ACTIVE = (58, 101, 148)
DARK_BLUE = (0, 64, 107)
DARK_BLUE_INACTIVE = (29,51,74)

pygame.init()
clock = pygame.time.Clock()

Start_main = pygame.display.set_mode((300, 100), pygame.NOFRAME)
Start_main.fill(DARK_BLUE_INACTIVE)
font_loading = pygame.font.Font("Font/List.ttf", 35)
text_loading = font_loading.render("Loading...", True, GRAY)
Start_main.blit(text_loading, (Start_main.get_width() / 2 - text_loading.get_width() / 2, Start_main.get_height() / 2 - text_loading.get_height() / 2))
pygame.display.flip()

List_images = MyClassBSgames.updateListGame()
MyClassBSgames.updateBabySteam(List_images)
List_images = MyClassBSgames.updateListGame()
count = len(List_images)

main = pygame.display.set_mode((800, 500))
getList = List.List(main, size_slider, X_POS, Y_POS, WIDTH, HEIGHT, step_scrol, count, DARK_BLUE, DARK_BLUE_INACTIVE, DARK_BLUE_ACTIVE, GRAY, List_images, size_block)
InformationMenu.Initialize(250, 10, 540, 400, GRAY, main)


while True:
    main.fill(List.Color("white"))

    getList.draw(GRAY)
    InformationMenu.draw()

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
        getList.Active(event, pos)
        if getList.activate_slider:
            getList.slider.Active(event, pos)

    pygame.display.flip()
    clock.tick(60)