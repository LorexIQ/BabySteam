import pygame
import os

WIDTH = 190
HEIGHT = 340
count = 20
size_block = 25
Link = "Images"
fileList = []
Position_selected = 0
size_slider = 25
step_scrol = 17

gradient_color = [0, 0, 0]
status_gradient = True

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = False


def Color(color_out):
    return pygame.Color(color_out)


def DegreePercent(first_num, last_num, num, type=""):
    if type == "P":
        num_pos = (num - first_num) / (last_num - first_num)
    elif type == "D":
        num_pos = first_num + num * (last_num - first_num)
    else:
        return False
    return num_pos


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


class Slider:
    def __init__(self, x, y, width, height, win, color, under_eae):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win
        self.color = color
        self.min_range = 30
        self.max_range = height - under_eae * 10
        self.position_input = 0
        if self.max_range < self.min_range:
            self.max_range = self.min_range


    def draw(self):
        slider_rect = pygame.Rect(self.x, self.y, self.width, self.max_range)
        self.position_output = DegreePercent(self.max_range + 5, self.height + 5, self.position_input, "D")
        slider_rect.bottom = self.position_output
        pygame.draw.rect(self.win, self.color, slider_rect)


class Button(pygame.sprite.Sprite):

    def __init__(self, coords, x, y, width, height, color, ID):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((coords.width, coords.height))
        self.color = (gradient_color[0], gradient_color[1], gradient_color[2]) if not color else color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect = coords
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = ID
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
        if self.id == Position_selected and not self.active:
            self.image.fill(pygame.Color("yellow"))
            self.active = True
        elif self.active:
            self.image.fill(self.color)
            self.active = False
            if self.id == Position_selected:
                Position_selected = 0


class List:
    def __init__(self, size_slider_rect, x, y, width, height, step, count_elements, color_button):
        self.Elements = addElements(count, size_block)
        self.y_max = self.Elements[len(self.Elements) - 1].y + size_block
        self.slided_win = pygame.Surface((WIDTH, self.y_max))
        self.List_main = pygame.Surface((WIDTH + 15 + size_slider_rect, HEIGHT + 10))
        self.color_button = color_button
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.main_pos_sider_serface = 5
        self.step = step
        self.count_elements = count_elements
        self.group = pygame.sprite.Group()
        self.position_slider = 0
        self.y_min = self.y_max - self.height
        under_eae = Rounding(abs((self.main_pos_sider_serface - 5 + self.y_max - self.height) / size_block)) if count * (size_block + 5) > height - 10 else 0
        self.slider = Slider(x + width + 5, y, size_slider_rect, height, self.List_main, pygame.Color("green"),
                             under_eae)

        if self.Elements:
            id_but = 0
            for Elem in self.Elements:
                Gradient(20, 'G', 'B')
                id_but += 1
                button = Button(Elem, self.x, self.y, self.width, self.height, self.color_button, id_but)
                self.group.add(button)

    def draw(self, color):
        main.blit(self.List_main, (self.x, self.y))
        self.List_main.fill(color)
        self.slided_win.fill(color)
        self.group.draw(self.slided_win)
        self.position_slider = DegreePercent(self.main_pos_sider_serface + self.height, self.y_max,
                                             self.height - self.main_pos_sider_serface + 10, "P")
        if self.position_slider > 1:
            self.position_slider = 1.0
        self.slider.position_input = self.position_slider
        self.slider.draw()
        self.List_main.blit(self.slided_win, (5, self.main_pos_sider_serface))

        pygame.draw.rect(self.List_main, color, (0, 0, self.width + 10, self.height + 10), 10)

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

    def TouchWindows(self, position_mouse):
        if position_mouse[0] > self.x + 5 and position_mouse[1] > self.y + 5:
            if position_mouse[0] < self.x + self.width + 5 and position_mouse[1] < self.y + self.height + 5:
                return True
        return False

    def Active(self, event_list, position_mouse):
        global Position_selected
        pos_y = position_mouse[1]
        if event_list.button == 1:
            if self.TouchWindows(pos):
                pos_y -= self.main_pos_sider_serface - 5
                self.group.update((pos[0], pos_y), self.Elements)
                if Position_selected != 0:
                    return Position_selected


fileList = ReadDirs(fileList, Link)
getList = List(size_slider, 5, 5, WIDTH, HEIGHT, step_scrol, count, None)


while True:
    main.fill(Color("white"))

    getList.draw(GRAY)

    UpButton = pygame.Rect(300, 100, 50, 50)
    pygame.draw.rect(main, GREEN, UpButton)
    DownButton = pygame.Rect(300, 160, 50, 50)
    pygame.draw.rect(main, GREEN, DownButton)

    font = pygame.font.Font(None, 25)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
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
            elif event.button == 4:
                getList.Motion(True)
                break
            elif event.button == 5:
                getList.Motion(False)
                break
            print(getList.Active(event, pos))

    pygame.display.flip()
    clock.tick(60)