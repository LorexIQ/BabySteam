import pygame

class MultiButton(object):
    def __init__(self, win, x, y, width, height, list_games, color_install, color_delete, color_run):
        delete_image = pygame.image.load('Images/Delete.png')
        play_image = pygame.image.load('Images/Play.png')
        install_image = pygame.image.load('Images/Install.png')
        self.color_install = color_install
        self.color_delete = color_delete
        self.color_run = color_run
        self.delete_image = pygame.transform.scale(delete_image, (height - 20, height - 20))
        self.play_image = pygame.transform.scale(play_image, (height - 20, height - 20))
        self.install_image = pygame.transform.scale(install_image, (height - 20, height - 20))
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(pygame.Color("white"))
        self.status = -1
        self.rects = [pygame.Rect(0, 0, width, height),
                      pygame.Rect(0, 0, width * 0.25, height),
                      pygame.Rect(width * 0.25, 0, width - width * 0.25, height)]
        self.list_games = list_games
        self.selected_point = None
        font = pygame.font.Font('Font\List.ttf', self.height - 20)
        self.text_play = font.render("PLAY", True, pygame.Color("white"))
        self.text_install = font.render("INSTALL", True, pygame.Color("white"))

    def draw(self):
        if self.status != -1:
            self.win.blit(self.surface, (self.x, self.y))
            if self.status == 0:
                pygame.draw.rect(self.surface, self.color_install, self.rects[0])
                self.surface.blit(self.text_install, (
                self.rects[0].center[0] - self.text_install.get_width() / 2 + 5 + self.install_image.get_width() / 2,
                self.height / 2 - self.text_install.get_height() / 2))
                self.surface.blit(self.install_image, (
                self.rects[0].center[0] - self.text_install.get_width() / 2 - 5 - self.install_image.get_width() / 2,
                self.height / 2 - self.install_image.get_height() / 2))
            elif self.status == 1:
                pygame.draw.rect(self.surface, self.color_delete, self.rects[1])
                self.surface.blit(self.delete_image, ((self.width * 0.25) / 2 - self.delete_image.get_width() / 2,
                                                      self.height / 2 - self.delete_image.get_width() / 2))
                pygame.draw.rect(self.surface, self.color_run, self.rects[2])
                self.surface.blit(self.text_play, (self.rects[2].center[0] - self.text_play.get_width() / 2 + self.play_image.get_width() / 2,
                                                   self.height / 2 - self.text_play.get_height() / 2))
                self.surface.blit(self.play_image, (self.rects[2].center[0] - self.text_play.get_width() / 2 - self.play_image.get_width() / 2,
                                                    self.height / 2 - self.play_image.get_height() / 2))


    def active(self, event_but, position_mouse, select):
        if select != 0:
            self.selected_point = self.list_games[select - 1]
            self.status = self.selected_point.GetStatus()
        else:
            self.status = -1
        position_mouse = (position_mouse[0] - self.x, position_mouse[1] - self.y)
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
