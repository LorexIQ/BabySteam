import pygame

class MultiButton(object):
    def __init__(self, win, x, y, width, height, list_games, color_install, color_delete, color_run, color_offline, color_text):
        delete_image = pygame.image.load('Images/Delete.png')
        play_image = pygame.image.load('Images/Play.png')
        install_image = pygame.image.load('Images/Install.png')
        internet_image = pygame.image.load('Images/Internet.png')
        accept_image = pygame.image.load('Images/Accept.png')
        cancel_image = pygame.image.load('Images/Cancel.png')
        self.color_install = color_install
        self.color_delete = color_delete
        self.color_run = color_run
        self.color_offline = color_offline
        self.delete_image = pygame.transform.scale(delete_image, (height - 20, height - 20))
        self.play_image = pygame.transform.scale(play_image, (height - 20, height - 20))
        self.install_image = pygame.transform.scale(install_image, (height - 20, height - 20))
        self.internet_image = pygame.transform.scale(internet_image, (height - 20, height - 20))
        self.accept_image = pygame.transform.scale(accept_image, (height - 20, height - 20))
        self.cancel_image = pygame.transform.scale(cancel_image, (height - 20, height - 20))
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
        self.text_play = font.render("PLAY", True, color_text)
        self.text_install = font.render("INSTALL", True, color_text)
        self.text_internet = font.render("OFFLINE", True, color_text)
        self.text_loading = font.render("Download...", True, color_text)
        self.text_deleting = font.render("Deleting...", True, color_text)
        self.mode = None
        self.delete_status = False
        self.select = 0

    def draw(self, mode):
        self.mode = mode
        if self.status != -1:
            self.win.blit(self.surface, (self.x, self.y))
            if self.status == 0:
                if mode:
                    pygame.draw.rect(self.surface, self.color_install, self.rects[0])
                    self.surface.blit(self.text_install, (
                    self.rects[0].center[0] - self.text_install.get_width() / 2 + 5 + self.install_image.get_width() / 2,
                    self.height / 2 - self.text_install.get_height() / 2))
                    self.surface.blit(self.install_image, (
                    self.rects[0].center[0] - self.text_install.get_width() / 2 - 5 - self.install_image.get_width() / 2,
                    self.height / 2 - self.install_image.get_height() / 2))
                else:
                    pygame.draw.rect(self.surface, self.color_offline, self.rects[0])
                    self.surface.blit(self.text_internet, (
                    self.rects[0].center[0] - self.text_internet.get_width() / 2 + 5 + self.internet_image.get_width() / 2,
                    self.height / 2 - self.text_internet.get_height() / 2))
                    self.surface.blit(self.internet_image, (
                    self.rects[0].center[0] - self.text_internet.get_width() / 2 - 5 - self.internet_image.get_width() / 2,
                    self.height / 2 - self.internet_image.get_height() / 2))
            elif self.status == 1:
                pygame.draw.rect(self.surface, self.color_delete, self.rects[1])
                self.surface.blit(self.delete_image if not self.delete_status else self.cancel_image, ((self.width * 0.25)
                                / 2 - (self.delete_image if not self.delete_status else self.cancel_image).get_width() / 2,
                    self.height / 2 - (self.delete_image if not self.delete_status else self.cancel_image).get_width() / 2))
                pygame.draw.rect(self.surface, self.color_run, self.rects[2])
                if not self.delete_status:
                    self.surface.blit(self.text_play, (self.rects[2].center[0] - self.text_play.get_width() / 2 + self.play_image.get_width() / 2,
                                                       self.height / 2 - self.text_play.get_height() / 2))
                    self.surface.blit(self.play_image, (self.rects[2].center[0] - self.text_play.get_width() / 2 - self.play_image.get_width() / 2,
                                                        self.height / 2 - self.play_image.get_height() / 2))
                else:
                    self.surface.blit(self.accept_image, (self.rects[2].center[0] - self.accept_image.get_width() / 2,
                                                          self.rects[2].center[1] - self.accept_image.get_height() / 2))


    def active(self, event_but, position_mouse, select):
        if self.select != select:
            self.delete_status = False
        self.select = select
        if select != 0:
            self.selected_point = self.list_games[select - 1]
            self.status = self.selected_point.GetStatus()
        else:
            self.status = -1
        position_mouse = (position_mouse[0] - self.x, position_mouse[1] - self.y)
        if event_but.type == pygame.MOUSEBUTTONDOWN:
            if event_but.button == 1:
                if self.status == 0 and self.mode:
                    if self.rects[0].collidepoint(position_mouse):
                        self.delete_status = False
                        self.win.blit(self.text_loading, (255, self.y + self.height / 2 - self.text_loading.get_height() / 2))
                        pygame.display.flip()
                        self.selected_point.instalGame()
                        return True
                elif self.status == 1:
                    if self.rects[1].collidepoint(position_mouse):
                        if not self.delete_status:
                            self.delete_status = True
                        else:
                            self.delete_status = False
                        return False
                    if self.rects[2].collidepoint(position_mouse):
                        if not self.delete_status:
                            self.selected_point.startGame()
                            return False
                        else:
                            self.win.blit(self.text_deleting,
                                          (255, self.y + self.height / 2 - self.text_deleting.get_height() / 2))
                            pygame.display.flip()
                            self.selected_point.deleteGame()
                            return True

