import pygame

InformationWindow = None

class Window(object):
    def __init__(self, x, y, width, height, color, win):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.win = win
        self.object = pygame.Surface((self.width, self.height))
        self.object.fill(self.color)

    def draw(self, position_list):
        if position_list == 0:
            self.object = pygame.Surface((self.width, self.height + 60))
        else:
            self.object = pygame.Surface((self.width, self.height))
        self.object.fill(self.color)
        self.win.blit(self.object, (self.x, self.y))


def draw():
    InformationWindow.draw()