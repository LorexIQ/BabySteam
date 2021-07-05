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
        self.object.fill(color)

    def draw(self):
        self.win.blit(self.object, (self.x, self.y))


def Initialize(x, y, width, height, color, win):
    global InformationWindow
    InformationWindow = Window(x, y, width, height, color, win)

def draw():
    InformationWindow.draw()