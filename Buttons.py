import pygame

class MultiButton(object):
    def __init__(self, win, x, y, width, height, list_games):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(pygame.Color("black"))
        self.status = -1
        self.rects = [pygame.Rect(self.x, self.y, width, height),
                      pygame.Rect(self.x, self.y, width * 0.25, height),
                      pygame.Rect(self.x + width * 0.25, self.y, width - width * 0.25, height)]
        self.list_games = list_games
        self.selected_point = None

    def draw(self):
        if self.status != -1:
            self.win.blit(self.surface, (self.x, self.y))
            if self.status == 0:
                pygame.draw.rect(self.win, pygame.Color("blue"), self.rects[0])
            elif self.status == 1:
                pygame.draw.rect(self.win, pygame.Color("red"), self.rects[1])
                pygame.draw.rect(self.win, pygame.Color("green"), self.rects[2])


    def active(self, event_but, position_mouse, select):
        if select != 0:
            self.selected_point = self.list_games[select - 1]
            self.status = self.selected_point.GetStatus()
        else:
            self.status = -1
        if event_but.type == pygame.MOUSEBUTTONDOWN:
            if event_but.button == 1:
                if self.status == 0:
                    if self.rects[0].collidepoint(position_mouse):
                        self.selected_point.instalGame()
                        return True
                elif self.status == 1:
                    if self.rects[1].collidepoint(position_mouse):
                        self.selected_point.deleteGame()
                        return True
                    if self.rects[2].collidepoint(position_mouse):
                        self.selected_point.startGame()
                        return False
