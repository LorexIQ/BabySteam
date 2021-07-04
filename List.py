import pygame
import os

WIDTH = 190
HEIGHT = 340

RED = (255, 0, 0)

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = True


def Rounding(roundin):
    n = str(int(roundin)) + ".7"
    n = float(n)
    if roundin > n:
        roundoff = int(roundin) + 1
    else:
        roundoff = int(roundin)
    return roundoff


def addElements(Links='', Names='', count_el = 0, size=20):
    board = 0
    Elements = []
    for i in range(count_el):
        if i != 0:
            board += 5
        Elements.append(pygame.Rect(0, board + size * i, HEIGHT, 20))
    return Elements

class List:
    def __init__(self, win, slider_rect, x, y, width, heidth, y_max, step, count_elements):
        self.x = x
        self.y = y
        self.width = width
        self.heidth = heidth
        self.win = win
        self.slider_rect = slider_rect
        self.main_pos_sider_serface = 5
        self.y_max = y_max
        self.step = step
        self.count_elements = count_elements

    def draw(self, color, color_button, Elements):
        main.blit(self.win, (self.x, self.y))
        self.win.fill(color)
        self.slider_rect.fill(color)
        if Elements:
            for i in Elements:
                pygame.draw.rect(self.slider_rect, color_button, i)
        self.win.blit(self.slider_rect, (5, self.main_pos_sider_serface))
        pygame.draw.rect(self.win, color, (0, 0, self.width + 10, self.heidth + 10), 10)

    def Motion(self, position):
        if position:
            if self.main_pos_sider_serface < 5:
                self.main_pos_sider_serface += self.step
                while self.main_pos_sider_serface > 5:
                    self.main_pos_sider_serface -= 1
        else:
            if self.main_pos_sider_serface + self.y_max > HEIGHT + 5:
                self.main_pos_sider_serface -= self.step
                while self.main_pos_sider_serface + self.y_max < HEIGHT + 5:
                    self.main_pos_sider_serface += 1

    def Action(self):
        max_el = abs((self.main_pos_sider_serface - 5 + self.y_max - self.heidth) / 25)
        min_el = abs((self.main_pos_sider_serface - 5) / 25)
        avegage_el = 0
        font = pygame.font.Font(None, 25)
        main.blit(font.render(str(Rounding(min_el)) + "   " + str(self.count_elements - Rounding(min_el) - Rounding(max_el)) + "   " + str(Rounding(max_el)), True, pygame.Color("black")), (300, 250))


count = 20
List_rects = addElements('', '', count)
size_list_rect = len(List_rects)
max_y_list_rect = List_rects[size_list_rect - 1].y + 20

Link = "Images"
fileList = []
slider_win = pygame.Surface((WIDTH, max_y_list_rect))
List_main = pygame.Surface((WIDTH + 10, HEIGHT + 10))
getList = List(List_main, slider_win, 5, 5, WIDTH, HEIGHT, max_y_list_rect, 17, count)


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

    getList.Action()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if UpButton.collidepoint(pos):
                getList.Motion(True)
                break
            if DownButton.collidepoint(pos):
                getList.Motion(False)
                break

    pygame.display.flip()
    clock.tick(60)