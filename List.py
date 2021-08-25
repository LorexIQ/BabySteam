import pygame

Position_selected = 0


def DegreePercent(first_num, last_num, num, type_mode=""):
    if type_mode == "P":
        num_pos = (num - first_num) / (last_num - first_num)
    elif type_mode == "D":
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


def addElements(count_el, size, width_add=None):
    board = 0
    Elements = []
    for i in range(count_el):
        Elements.append(pygame.Rect(0, board + size * i, width_add, size))
    return Elements


class Slider:
    def __init__(self, x, y, win, under_eae, x_pos, y_pos):
        self.image = pygame.image.load('Images/Main/List_slider.png')
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x = x
        self.y = y
        self.height = self.image.get_height()
        self.win = win
        self.min_range = 30
        self.max_range = self.height - under_eae * 15 - 10
        self.position_input = 0
        if self.max_range < self.min_range:
            self.max_range = self.min_range
        self.surface = pygame.Surface((self.image.get_width(), self.max_range))
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.max_range))
        self.surface.blit(self.image, (0, 0))
        self.surface_pos = 0
        self.active = False
        self.fixed_y_position = None
        self.pos_y = None
        self.percent = 0


    def draw(self):
        transmit = DegreePercent(self.max_range + 5, self.height + 5, self.position_input, "D")
        if not self.active:
            self.surface_pos = transmit
        else:
            self.surface_pos = self.pos_y + transmit - self.fixed_y_position
            if self.surface_pos > self.height + 5:
                self.surface_pos = self.height + 5
            elif self.surface_pos - self.surface.get_height() < self.y:
                self.surface_pos = self.y + self.surface.get_height()
        self.win.blit(self.surface, (self.x + 5, self.y + self.surface_pos - self.surface.get_height() - 5))
        self.percent = DegreePercent(self.max_range + 5, self.height + 5, self.surface_pos, "P")


    def Active(self, event_slider):
        position_mouse = pygame.mouse.get_pos()
        position_mouse = (position_mouse[0] - self.x_pos - self.x - 5, position_mouse[1] - self.y_pos - self.y)
        if event_slider.type == pygame.MOUSEBUTTONDOWN and event_slider.button == 1:
            if 0 <= position_mouse[0] <= 10 and self.y + self.surface_pos - self.surface.get_height() - 10 <= position_mouse[1] <= self.y + self.surface_pos - 10 and not self.active:
                self.active = True
                self.fixed_y_position = position_mouse[1]
        elif event_slider.type == pygame.MOUSEBUTTONUP and event_slider.button == 1:
            self.active = False
        if self.active:
            self.pos_y = position_mouse[1]


class Button(pygame.sprite.Sprite):
    def __init__(self, coords, x, y, id_input, info, active_slider, mode, size_block):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.id = id_input
        self.active = False
        self.font = pygame.font.Font('Font/List.ttf', 15)
        self.mode = mode
        self.status = info.status
        self.image = pygame.Surface((coords.width, coords.height))
        self.images_buttons = [pygame.image.load('Images/Main/One_button_list_main.png'),
                               pygame.image.load('Images/Main/One_button_list_selected.png'),
                               pygame.image.load('Images/Main/One_button_list_offline.png')]
        self.size_block_list = size_block
        self.image.blit(self.images_buttons[0 if mode else 2], (0, 0))
        self.color_text = (140, 140, 140)
        self.rect = coords
        surface = pygame.image.load(info.img1)
        self.surface = pygame.transform.scale(surface, (self.size_block_list - 10, self.size_block_list - 10))
        self.image.blit(self.surface, (10, 5))
        self.text = self.font.render(str(info.name), True, self.color_text)
        backspace = False
        buffer = info.name
        while self.text.get_width() > 190 - self.size_block_list - (20 if active_slider else - 15):
            buffer = buffer[:-1]
            self.text = self.font.render(str(buffer), True, self.color_text)
            backspace = True
        if backspace:
            buffer = buffer[:-1] + "..."
            self.text = self.font.render(str(buffer), True, self.color_text)
        self.text_active = self.font.render(str(buffer), True, (255, 255, 255))
        self.image.blit(self.text_active if self.status else self.text, (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))


    def draw_active(self, mode):
        if self.id == Position_selected:
            if mode:
                self.status = 1
            else:
                self.status = 0
            self.draw_active_button()


    def TouchButton(self, position_mouse):
        if position_mouse[0] > self.rect.x + 10 and position_mouse[1] > self.rect.y + 10:
            if position_mouse[0] < self.rect.width + 10 and position_mouse[1] < self.rect.y + self.rect.height + 5:
                return True
        return False


    def update(self, rects=None, position_mouse=None):
        global Position_selected
        if self.rect.collidepoint((position_mouse[0] - self.x - 5, position_mouse[1] - self.y - 5)):
            Position_selected = rects.index(self.rect) + 1
        if self.id == Position_selected and not self.active:
            self.draw_active_button()
        elif self.active:
            self.image.blit(self.images_buttons[0 if self.mode else 2], (0, 0))
            self.image.blit(self.surface, (10, 5))
            self.image.blit(self.text_active if self.status else self.text, (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))
            self.active = False
            if self.id == Position_selected:
                Position_selected = 0


    def draw_active_button(self):
        self.image.blit(self.images_buttons[1], (0, 0))
        self.image.blit(self.surface, (10, 5))
        self.image.blit(self.text_active if self.status else self.text,
                        (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))
        self.active = True


    def update_ethernet(self, mode, info):
        self.mode = mode
        self.status = info.status
        self.image.blit(self.images_buttons[1 if self.id == Position_selected else 0 if self.mode else 2], (0, 0))
        self.image.blit(self.surface, (10, 5))
        self.image.blit(self.text_active if self.status else self.text,
                        (self.size_block_list + 10, self.size_block_list / 2 - self.font.size(str(self.text))[1] / 2))


class List:
    def __init__(self, win, x, y, images, mode):
        self.mode = mode
        self.background = [pygame.image.load('Images/Main/Background_list.png'),
                           pygame.image.load('Images/Main/Background_list_borders.png')]
        self.count_elements = len(images)
        self.size_block_list = 30
        self.step = 17
        self.width = 190
        self.height = 470
        self.main_pos_sider_serface = 5
        self.position_slider = 0
        self.win = win
        self.x = x
        self.y = y
        self.diapos_List = 0
        self.y_max = self.size_block_list * self.count_elements
        self.activate_slider = True if self.y_max > (x + self.height - 10) else False
        self.Elements = addElements(self.count_elements, self.size_block_list, self.width + (30 if not self.activate_slider else 15))
        self.slided_win = pygame.Surface((self.width + (30 if not self.activate_slider else 15), self.y_max))
        self.List_main = pygame.Surface((self.background[1].get_width(), self.background[1].get_height()))
        self.group = pygame.sprite.Group()
        self.y_min = self.y_max - self.height
        under_eae = Rounding(abs((self.main_pos_sider_serface - 5 + self.y_max - self.height) / self.size_block_list)) if self.count_elements * (self.size_block_list + 5) > self.height - 10 else 0
        self.slider = Slider(self.background[1].get_width() - 20, 5, self.List_main, under_eae, self.x, self.y)
        if self.Elements:
            id_but = 0
            for Elem in self.Elements:
                id_but += 1
                button = Button(Elem, self.x, self.y, id_but, images[id_but - 1], self.activate_slider, self.mode, self.size_block_list)
                self.group.add(button)


    def draw(self, sosto):
        self.win.blit(self.List_main, (self.x, self.y))
        self.List_main.blit(self.background[0], (5, 5))
        self.slided_win.fill((0, 22, 36))
        self.group.draw(self.slided_win)
        if self.activate_slider:
            if not self.slider.active:
                self.position_slider = self.diapos_List
                if self.position_slider > 1:
                    self.position_slider = 1.0
            else:
                self.main_pos_sider_serface = self.height - DegreePercent(self.height - 5, self.y_max - 5, self.slider.percent, "D")
            self.slider.position_input = self.position_slider
            if not sosto:
                self.diapos_List = DegreePercent(self.height - 5, self.y_max - 5, self.height - self.main_pos_sider_serface, "P")
            else:
                self.main_pos_sider_serface = self.height - DegreePercent(self.height - 5, self.y_max - 5,
                                                                          self.slider.percent, "D")
            self.slider.draw()
        self.List_main.blit(self.slided_win, (5, self.main_pos_sider_serface))
        self.List_main.blit(self.background[1], (0, 0))


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
            if position_mouse[0] < self.x + self.width + (20 if self.activate_slider else 35) and position_mouse[1] < self.y + self.height + 5:
                return True
        return False


    def Active(self, event_list):
        position_mouse = pygame.mouse.get_pos()
        global Position_selected
        if event_list.type == pygame.MOUSEBUTTONDOWN:
            pos_y = position_mouse[1]
            if event_list.button == 1:
                if self.TouchWindows(position_mouse):
                    pos_y -= self.main_pos_sider_serface - 5
                    self.group.update(self.Elements, (position_mouse[0], pos_y))
                    if Position_selected != 0:
                        return Position_selected
