import pygame
import os

WIDTH = 190
HEIGHT = 340

RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = False


def Rounding(roundin):
    n = str(int(roundin)) + ".55"
    n = float(n)
    if roundin > n:
        roundoff = int(roundin) + 1
    else:
        roundoff = int(roundin)
    return roundoff


def addElements(count_el = 0, size=20):
    board = 0
    Elements = []
    for i in range(count_el):
        if i != 0:
            board += 5
        Elements.append(pygame.Rect(0, board + size * i, HEIGHT, 20))
    return Elements


def ReadDirs(Links, usePath):
    for root, dirs, files in os.walk(usePath):
        for file in files:
            Links.append(os.path.join(root, file))
    return Links


class Button(pygame.sprite.Sprite):
    def __init__(self, coords, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((coords.width, coords.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = coords.x
        self.rect.y = coords.y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect.width = coords.width
        self.rect.height = coords.height

    def TouchButton(self, position_mouse):
        if position_mouse[0] > self.rect.x + 10 and position_mouse[1] > self.rect.y + 10:
            if position_mouse[0] < self.rect.width + 10 and position_mouse[1] < self.rect.y + self.rect.height + 5:
                return True
        return False


class List:
    def __init__(self, win, slider_rect, x, y, width, height, y_max, step, count_elements, Elements, color_button, group):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win
        self.slider_rect = slider_rect
        self.main_pos_sider_serface = 5
        self.y_max = y_max
        self.step = step
        self.count_elements = count_elements
        self.Elements = Elements
        self.color_but = color_button
        self.group = group

        if self.Elements:
            for i in self.Elements:
                # pygame.draw.rect(self.slider_rect, color_button, i)
                button = Button(i, self.color_but, self.x, self.y, self.width, self.height)
                group.add(button)

    def draw(self, color):
        main.blit(self.win, (self.x, self.y))
        self.win.fill(color)
        self.slider_rect.fill(color)
        self.group.draw(self.slider_rect)
        self.win.blit(self.slider_rect, (5, self.main_pos_sider_serface))
        pygame.draw.rect(self.win, color, (0, 0, self.width + 10, self.height + 10), 10)

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
        max_el = Rounding(abs((self.main_pos_sider_serface - 5 + self.y_max - self.height) / 25))
        min_el = Rounding(abs((self.main_pos_sider_serface - 5) / 25))
        avegage_el = self.count_elements - min_el - max_el
        return min_el, avegage_el, self.main_pos_sider_serface - 5

    def TouchWindows(self, position_mouse):
        if position_mouse[0] > self.x + 5 and position_mouse[1] > self.y + 5:
            if position_mouse[0] < self.x + self.width + 5 and position_mouse[1] < self.y + self.height + 5:
                return True
        return False


buttons = pygame.sprite.Group()

count = 20
List_rects = addElements(count)
size_list_rect = len(List_rects)
max_y_list_rect = List_rects[size_list_rect - 1].y + 20

Link = "Images"
fileList = []
fileList = ReadDirs(fileList, Link)
slider_win = pygame.Surface((WIDTH, max_y_list_rect))
List_main = pygame.Surface((WIDTH + 10, HEIGHT + 10))
getList = List(List_main, slider_win, 5, 5, WIDTH, HEIGHT, max_y_list_rect, 17, count, List_rects, GREEN, buttons)


while True:
    main.fill(pygame.Color('white'))

    getList.draw(pygame.Color('gray'))
    Diapos_slide = getList.Action()

    UpButton = pygame.Rect(300, 100, 50, 50)
    pygame.draw.rect(main, pygame.Color("green"), UpButton)
    DownButton = pygame.Rect(300, 160, 50, 50)
    pygame.draw.rect(main, pygame.Color("green"), DownButton)

    font = pygame.font.Font(None, 25)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        pos_y = pos[1]
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if UpButton.collidepoint(pos):
                getList.Motion(True)
            if DownButton.collidepoint(pos):
                getList.Motion(False)
            if getList.TouchWindows(pos):
                Elements_Group = buttons.sprites()
                pos_y -= Diapos_slide[2]
                for i in range (Diapos_slide[0], Diapos_slide[0] + Diapos_slide[1]):
                    One_Element = Elements_Group[i]
                    if One_Element.TouchButton((pos[0], pos_y)):
                        print(i + 1)
                        break

    buttons.update()
    pygame.display.flip()
    clock.tick(60)