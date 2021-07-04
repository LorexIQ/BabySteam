import pygame
import os

WIDTH = 190
HEIGHT = 340
count = 120
size_block = 25
Link = "Images"
fileList = []
Position_selected = -1

gradient_color = [0, 0, 0]
status_gradient = True

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = False


def Gradient(step, main_color, grad_color):
    global gradient_color, status_gradient
    if main_color == 'R':
        gradient_color[0] = 255
    elif main_color == 'G':
        gradient_color[1] = 255
    elif main_color == 'B':
        gradient_color[2] = 255
    c = 0
    if grad_color == 'R':
        c = 0
    elif grad_color == 'G':
        c = 1
    elif grad_color == 'B':
        c = 2
    if status_gradient:
        gradient_color[c] += step
        if gradient_color[c] > 255:
            gradient_color[c] = 255
            status_gradient = False
    else:
        gradient_color[c] -= step
        if gradient_color[c] < 0:
            gradient_color[c] = 0
            status_gradient = True


def Rounding(roundin, accuracy=".55"):
    n = str(int(roundin)) + accuracy
    n = float(n)
    if roundin > n:
        roundoff = int(roundin) + 1
    else:
        roundoff = int(roundin)
    return roundoff


def addElements(count_el = 0, size=30):
    board = 0
    Elements = []
    for i in range(count_el):
        if i != 0:
            board += 5
        Elements.append(pygame.Rect(0, board + size * i, HEIGHT, size))
    return Elements


def ReadDirs(Links, usePath):
    for root, dirs, files in os.walk(usePath):
        for file in files:
            Links.append(os.path.join(root, file))
    return Links


class Button(pygame.sprite.Sprite):
    def __init__(self, coords, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((coords.width, coords.height))
        self.color = (gradient_color[0], gradient_color[1], gradient_color[2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect = coords
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = False

    def TouchButton(self, position_mouse):
        if position_mouse[0] > self.rect.x + 10 and position_mouse[1] > self.rect.y + 10:
            if position_mouse[0] < self.rect.width + 10 and position_mouse[1] < self.rect.y + self.rect.height + 5:
                return True
        return False

    def update(self, position_mouse, rects):
        global Position_selected
        if position_mouse[0] > self.rect.x + 10 and position_mouse[1] > self.rect.y + 10:
            if position_mouse[0] < self.rect.width + 10 and position_mouse[1] < self.rect.y + self.rect.height + 10:
                Position_selected = rects.index(self.rect) + 1
                if not self.active:
                    self.active = True
                else:
                    self.active = False
        if self.active:
            self.image.fill(pygame.Color("green"))
        else:
            self.image.fill(self.color)

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
        self.group = group

        if self.Elements:
            for Elem in self.Elements:
                Gradient(20, 'B', 'R')
                button = Button(Elem, self.x, self.y, self.width, self.height)
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

    def Indent(self):
        return self.main_pos_sider_serface - 5

    def TouchWindows(self, position_mouse):
        if position_mouse[0] > self.x + 5 and position_mouse[1] > self.y + 5:
            if position_mouse[0] < self.x + self.width + 5 and position_mouse[1] < self.y + self.height + 5:
                return True
        return False


buttons = pygame.sprite.Group()

List_rects = addElements(count, size_block)
max_y_list_rect = List_rects[len(List_rects) - 1].y + size_block

fileList = ReadDirs(fileList, Link)
slider_win = pygame.Surface((WIDTH, max_y_list_rect))
List_main = pygame.Surface((WIDTH + 40, HEIGHT + 10))
getList = List(List_main, slider_win, 5, 5, WIDTH, HEIGHT, max_y_list_rect, 17, count, List_rects, GREEN, buttons)


while True:
    main.fill(pygame.Color('white'))

    getList.draw(GRAY)
    Indent = getList.Indent()

    UpButton = pygame.Rect(300, 100, 50, 50)
    pygame.draw.rect(main, GREEN, UpButton)
    DownButton = pygame.Rect(300, 160, 50, 50)
    pygame.draw.rect(main, GREEN, DownButton)

    font = pygame.font.Font(None, 25)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        pos_y = pos[1]
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if UpButton.collidepoint(pos):
                    getList.Motion(True)
                    break
                if DownButton.collidepoint(pos):
                    getList.Motion(False)
                    break
                if getList.TouchWindows(pos):
                    pos_y -= Indent
                    buttons.update((pos[0], pos_y), List_rects)
                    if Position_selected != -1:
                        print(Position_selected)
                    Position_selected = -1
                    break
            elif event.button == 4:
                getList.Motion(True)
                break
            elif event.button == 5:
                getList.Motion(False)
                break

    pygame.display.flip()
    clock.tick(60)