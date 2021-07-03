import pygame
import os

WIDTH = 190
HEIGHT = 340

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = True

def addElements(Links='', Names='', count=30, size=20):
    board = 0
    Elements = []
    for i in range(count):
        if i != 0:
            board += 5
        Elements.append(pygame.Rect(0, board + size * i, HEIGHT, 20))
    return Elements

class List:
    def __init__(self, win, slider_rect, x, y, width, heidth, y_max):
        self.x = x
        self.y = y
        self.width = width
        self.heidth = heidth
        self.win = win
        self.slider_rect = slider_rect
        self.main_pos_sider_serface = 5
        self.y_max = y_max

    def draw(self, color, color_button, Elements):
        main.blit(self.win, (10, 10))
        self.win.fill(color)
        self.slider_rect.fill(color)
        if Elements:
            for i in Elements:
                if i.y > self.y_max - self.y - 10:
                    break
                else:
                    pygame.draw.rect(self.slider_rect, color_button, i)

        self.win.blit(self.slider_rect, (5, self.main_pos_sider_serface))
        pygame.draw.rect(self.win, color, (0, 0, self.width + 10, self.heidth + 10), 10)

    def Motion(self, position):
        if position:
            if self.main_pos_sider_serface < 5:
                self.main_pos_sider_serface += 15
        else:
            if self.main_pos_sider_serface + self.y_max > HEIGHT + 5:
                self.main_pos_sider_serface -= 15
        while self.main_pos_sider_serface > 5:
            self.main_pos_sider_serface -= 1
        while self.main_pos_sider_serface + self.y_max < HEIGHT + 5:
            self.main_pos_sider_serface += 1


List_rects = addElements()
size_list_rect = len(List_rects)
max_y_list_rect = List_rects[size_list_rect - 1].y - 5

Link = "Images"
fileList = []
slider_win = pygame.Surface((WIDTH, max_y_list_rect))
List_main = pygame.Surface((WIDTH + 10, HEIGHT + 10))
getList = List(List_main, slider_win, 5, 5, WIDTH, HEIGHT, max_y_list_rect)


def ReadDirs(Links, usePath):
    for root, dirs, files in os.walk(usePath):
        for file in files:
            Links.append(os.path.join(root, file))
    return Links


while True:
    main.fill(pygame.Color('white'))

    getList.draw(pygame.Color('gray'), pygame.Color('red'), List_rects)

    if run:
        fileList = ReadDirs(fileList, Link)
        run = False

    UpButton = pygame.Rect(300, 100, 50, 50)
    pygame.draw.rect(main, pygame.Color("green"), UpButton)
    DownButton = pygame.Rect(300, 160, 50, 50)
    pygame.draw.rect(main, pygame.Color("green"), DownButton)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if UpButton.collidepoint(pos):
                print(1)
                getList.Motion(True)
                break
            if DownButton.collidepoint(pos):
                print(2)
                getList.Motion(False)
                break

    pygame.display.flip()
    clock.tick(60)