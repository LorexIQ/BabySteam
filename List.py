import pygame
import MyClassBSgames
#import InformationMenu

Position_selected = 0


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


def Rounding(roundin, accuracy=".55"):
    n = str(int(roundin)) + accuracy
    n = float(n)
    if roundin > n:
        roundoff = int(roundin) + 1
    else:
        roundoff = int(roundin)
    return roundoff


def addElements(count_el = 0, size=30, width_add=None):
    board = 0
    Elements = []
    for i in range(count_el):
        if i != 0:
            board += 5
        Elements.append(pygame.Rect(0, board + size * i, width_add, size))
    return Elements


class Slider:
    def __init__(self, x, y, width, height, win, color, under_eae, x_pos, y_pos):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.win = win
        self.color = color
        self.min_range = 30
        self.max_range = height - under_eae * 5
        self.position_input = 0
        if self.max_range < self.min_range:
            self.max_range = self.min_range
        self.active = False
        self.slider_rect = None
        self.fixed_y_position = None
        self.pos_y = None
        self.transmit = None
        self.percent = 0
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self):
        self.transmit = DegreePercent(self.max_range + 5, self.height + 5, self.position_input, "D")
        self.slider_rect = pygame.Rect(self.x + 5, self.y, self.width, self.max_range)
        if not self.active:
            self.slider_rect.bottom = self.transmit
        else:
            self.slider_rect.bottom = self.pos_y + self.transmit - self.fixed_y_position
            if self.slider_rect.bottom > self.height + 5:
                self.slider_rect.bottom = self.height + 5
            elif self.slider_rect.top < self.y:
                self.slider_rect.top = self.y
        pygame.draw.rect(self.win, self.color, self.slider_rect)
        self.percent = DegreePercent(self.max_range + 5, self.height + 5, self.slider_rect.bottom, "P")

    def Active(self, event_slider, posinion_mouse):
        posinion_mouse = (posinion_mouse[0] - self.x_pos, posinion_mouse[1] - self.y_pos)
        if event_slider.type == pygame.MOUSEBUTTONDOWN and event_slider.button == 1:
            if self.slider_rect.collidepoint(posinion_mouse) and not self.active:
                self.active = True
                self.fixed_y_position = posinion_mouse[1]
        elif event_slider.type == pygame.MOUSEBUTTONUP and event_slider.button == 1:
            self.active = False
        if self.active:
            self.pos_y = posinion_mouse[1]


class Button(pygame.sprite.Sprite):

    def __init__(self, coords, x, y, width, height, color, color_inactive, color_active, color_text, ID, img, font, active_slider, size_block_list, size_slider_rect):
        self.size_block_list = size_block_list
        self.status = img.GetStatus()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((coords.width, coords.height))
        self.color = color
        if self.status:
            self.image.fill(self.color)
        else:
            self.image.fill(color_inactive)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color_text = color_text
        self.rect = self.image.get_rect()
        self.rect = coords
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = ID
        self.active = False
        self.font = font
        surface = pygame.image.load(img.wayImg)
        self.surface = pygame.transform.scale(surface, (self.size_block_list - 10, self.size_block_list - 10))
        self.image.blit(self.surface, (10, 5))
        self.text = self.font.render(str(img.name), True, self.color_text)
        len_text = self.text.get_width()
        backspace = False
        while len_text > width - self.size_block_list - (20 if active_slider else (- size_slider_rect + 5)):
            print(len_text, img.name)
            img.name = img.name[:-1]
            self.text = self.font.render(str(img.name), True, self.color_text)
            len_text = self.text.get_width()
            backspace = True
        if backspace:
            img.name = img.name[:-1] + "..."
            self.text = self.font.render(str(img.name), True, self.color_text)
        self.image.blit(self.text, (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))

    def TouchButton(self, position_mouse):
        if position_mouse[0] > self.rect.x + 10 and position_mouse[1] > self.rect.y + 10:
            if position_mouse[0] < self.rect.width + 10 and position_mouse[1] < self.rect.y + self.rect.height + 5:
                return True
        return False

    def update(self, position_mouse, rects):
        global Position_selected
        if self.rect.collidepoint((position_mouse[0] - self.x - 5, position_mouse[1] - self.y - 5)):
            Position_selected = rects.index(self.rect) + 1
        if self.id == Position_selected and not self.active:
            self.image.fill(self.color_active)
            self.image.blit(self.surface, (10, 5))
            self.image.blit(self.text, (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))
            self.active = True
        elif self.active:
            self.image.fill(self.color if self.status else self.color_inactive)
            self.image.blit(self.surface, (10, 5))
            self.image.blit(self.text, (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))
            self.active = False
            if self.id == Position_selected:
                Position_selected = 0


class List:
    def __init__(self, win, size_slider_rect, x, y, width, height, step, count_elements, color_button, color_inactive,
                 color_active, color_text, images, size_block_list):
        self.size_block_list = size_block_list
        self.font = pygame.font.Font('Font\List.ttf', self.size_block_list - 15)
        self.size_slider = size_slider_rect
        self.y_max = (self.size_block_list + 5) * count_elements - 5
        self.activate_slider = True if self.y_max > x + height else False
        self.Elements = addElements(count_elements, self.size_block_list, width + ((self.size_slider + 10) if not self.activate_slider else 0))
        self.slided_win = pygame.Surface((width + ((self.size_slider + 10) if not self.activate_slider else 0), self.y_max))
        self.List_main = pygame.Surface((width + 20 + self.size_slider, height + 10))
        self.win = win
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
        under_eae = Rounding(abs((self.main_pos_sider_serface - 5 + self.y_max - self.height) / self.size_block_list)) if count_elements * (self.size_block_list + 5) > height - 10 else 0
        self.slider = Slider(width + 10, 5, self.size_slider, height, self.List_main, color_button,
                             under_eae, self.x, self.y)
        self.diapos_List = 0
        self.images = images

        if self.Elements:
            id_but = 0
            for Elem in self.Elements:
                id_but += 1
                button = Button(Elem, self.x, self.y, self.width, self.height, color_button, color_inactive,
                                color_active, color_text, id_but, self.images[id_but - 1], self.font,
                                self.activate_slider, self.size_block_list, self.size_slider)
                self.group.add(button)

    def draw(self, color):
        self.win.blit(self.List_main, (self.x, self.y))
        self.List_main.fill(color)
        self.slided_win.fill(color)
        self.group.draw(self.slided_win)
        if self.activate_slider:
            if not self.slider.active:
                self.position_slider = self.diapos_List
                if self.position_slider > 1:
                    self.position_slider = 1.0
            else:
                self.main_pos_sider_serface = self.height - DegreePercent(self.height - 5, self.y_max - 5, self.slider.percent, "D")
            self.slider.position_input = self.position_slider
            self.diapos_List = DegreePercent(self.height - 5, self.y_max - 5, self.height - self.main_pos_sider_serface, "P")
            self.slider.draw()
        self.List_main.blit(self.slided_win, (5, self.main_pos_sider_serface))
        pygame.draw.rect(self.List_main, color, (0, 0, self.width + self.size_slider + 20, self.height + 10), 10)


    def Motion(self, position):
        if position:
            if self.main_pos_sider_serface < 5:
                self.main_pos_sider_serface += self.step
                while self.main_pos_sider_serface > 5:
                    self.main_pos_sider_serface -= 1
        else:
            if self.main_pos_sider_serface + self.y_max > self.height + 5:
                self.main_pos_sider_serface -= self.step
                while self.main_pos_sider_serface + self.y_max < self.height + 5:
                    self.main_pos_sider_serface += 1

    def TouchWindows(self, position_mouse):
        if position_mouse[0] > self.x + 5 and position_mouse[1] > self.y + 5:
            if position_mouse[0] < self.x + self.width + (5 if self.activate_slider else (self.size_slider + 15)) and position_mouse[1] < self.y + self.height + 5:
                return True
        return False

    def Active(self, event_list, position_mouse):
        global Position_selected
        if event_list.type == pygame.MOUSEBUTTONDOWN:
            pos_y = position_mouse[1]
            if event_list.button == 1:
                if self.TouchWindows(position_mouse):
                    pos_y -= self.main_pos_sider_serface - 5
                    self.group.update((position_mouse[0], pos_y), self.Elements)
                    if Position_selected != 0:
                        return Position_selected
