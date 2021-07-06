import pygame

InformationWindow = None

class Window(object):
    def __init__(self, x, y, width, height, color, win, List_objects):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.position_list = 0
        self.win = win
        self.object = pygame.Surface((self.width, self.height))
        self.object.fill(self.color)
        self.List_objects = List_objects
        self.information = []
        self.images = []
        self.ReadInformation()
        self.font = pygame.font.Font('Font/List.ttf', 20)
        self.words = []
        self.Wording()
        self.block_text = []
        self.coords_text = []

    def draw(self, position_list):
        self.position_list = position_list
        if position_list == 0:
            self.object = pygame.Surface((self.width, self.height + 60))
            self.object.fill(self.color)
        else:
            self.object = pygame.Surface((self.width, self.height))
            self.object.fill(self.color)
            self.object.blit(self.images[position_list - 1], (10, 10))
            self.PrintInformation(10, 220)

        self.win.blit(self.object, (self.x, self.y))

    def ReadInformation(self):
        for i in self.List_objects:
            self.information.append(i.inf)
            self.images.append(pygame.image.load(i.wayImg2))
            self.images[-1] = pygame.transform.scale(self.images[-1], (self.width - 20, 200))

    def Wording(self):
        for i in self.information:
            self.words.append(i.split())

    def PrintInformation(self, x, y):
        text_wight = 0
        text_height = 0
        block_text = []
        block_coords = []
        min_pos = 1
        for i in self.words[self.position_list - 1]:
            about = 1
            block_text.append(self.font.render(str(i), True, pygame.Color("white")))
            if block_text[-1].get_width() + text_wight > self.width - 20:
                air = self.width - 20 - block_coords[-1][0] - block_text[-2].get_width()
                count_words = len(block_text) - min_pos
                step = air / (count_words - 1)
                for j in range(min_pos, len(block_coords)):
                    block_coords[j] = (block_coords[j][0] + step * about, block_coords[j][1])
                    about += 1
                min_pos = len(block_text)
                text_wight = 0
                text_height += self.font.get_height()
            block_coords.append((x + text_wight, y + text_height))
            text_wight += block_text[-1].get_width() + 5


        for i in range(len(block_text)):
            self.object.blit(block_text[i], block_coords[i])