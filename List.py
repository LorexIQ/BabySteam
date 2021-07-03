import pygame
import os

pygame.init()
main = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
run = True

class List:
    def __init__(self, x, y, width, heidth, count):
        self.x = x
        self.y = y
        self.width = width
        self.heidth = heidth
        self.count = count

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.heidth))


Link = "Images"
fileList = []
getList = List(10, 10, 200, 350, 0)


def ReadDirs(Links, usePath):
    for root, dirs, files in os.walk(usePath):
        for file in files:
            Links.append(os.path.join(root, file))
    return Links


while True:
    main.fill(pygame.Color('white'))

    getList.draw(main, pygame.Color('gray'))

    if run:
        fileList = ReadDirs(fileList, Link)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    pygame.display.flip()
    clock.tick(60)