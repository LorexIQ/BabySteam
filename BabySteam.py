import sys
import time
import pygame
import List
import InformationMenu
import Buttons
import StreamingDownload
import threading
from threading import Thread
import ZipUnpack

X_POS = 10
Y_POS = 10
WIDTH_WIN = 800
HEIGHT_WIN = 500
X_BUTTON = 590
Y_BUTTON = 440
X_INFORMATION_WIN = 250
Y_INFORMATION_WIN = 10
action = 0

pygame.init()
clock = pygame.time.Clock()

main = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pygame.display.set_caption("BabySteam")
main.blit(pygame.image.load('Images/Main/main_loading.png'), (0, 0))
pygame.display.flip()
List_images, Internet = StreamingDownload.readInformationContent()
if not List_images:
    main.blit(pygame.image.load('Images/Main/main_error.png'), (0, 0))
    pygame.display.flip()
    time.sleep(3)
    sys.exit()

background_main = pygame.image.load('Images/Main/Background_main.png')

getList = List.List(main, X_POS, Y_POS, List_images, Internet)
InformationWindow = InformationMenu.Window(X_INFORMATION_WIN, Y_INFORMATION_WIN, main, List_images)
getButton = Buttons.MultiButton(main, X_BUTTON, Y_BUTTON, List_images)
InformationMenu.create_info_win(main)


def offlineOnline():
    global List_images, getList, Internet, action
    old_internet = Internet
    internet = old_internet
    count = [0, 0]
    while True:
        count_bool = StreamingDownload.CheckInternet()
        if count_bool:
            count[0] += 1
            count[1] += 1
        else:
            count[0] -= 1
            count[1] += 1
        if count[0] in (-2, 2):
            internet = count_bool
            count = [0, 0]
        elif count[1] == 2:
            count = [0, 0]
        if old_internet != internet:
            List_images, old_internet = StreamingDownload.readInformationContent()
            getList.images = List_images
            getList.mode = internet
            for button_update in getList.group:
                button_update.update_ethernet(internet, List_images[button_update.id - 1])
            Internet = internet
        pygame.time.Clock().tick(1)


thread_on_off = Thread(target=offlineOnline, daemon=True)
thread_on_off.start()


while True:
    if action == 1:
        action = 0
        for button in getList.group:
            button.draw_active(False)
    elif action == 2:
        action = 0
        for button in getList.group:
            button.draw_active(True)
    elif StreamingDownload.live_status == 14:
        getButton.change_state(List.Position_selected)
        StreamingDownload.live_status = -1
        action = 2
    main.blit(background_main, (0, 0))
    getList.draw(action)
    getButton.draw(Internet)
    InformationWindow.draw(List.Position_selected)
    InformationMenu.win_info_dowbload.draw()
    getButton.draw_delete_menu()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not InformationMenu.win_info_dowbload.call and not getButton.call_delete:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    getList.Motion(True)
                    break
                elif event.button == 5:
                    getList.Motion(False)
                    break
                elif event.button == 3:
                    for button in getList.group:
                        button.draw_active()
            getList.Active(event)
            if getList.activate_slider:
                getList.slider.Active(event)
            getButton.active(event, List.Position_selected)
        InformationMenu.win_info_dowbload.active(event)
        action = getButton.action_delete_menu(event)
    pygame.display.flip()
    clock.tick(60)
