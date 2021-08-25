import pygame
import StreamingDownload
import InformationMenu


class MultiButton(object):
    def __init__(self, win, x, y, list_games):
        self.win = win
        self.x = x
        self.y = y
        self.status = -1
        self.list_games = list_games
        self.selected_point = None
        self.mode = None
        self.select = 0
        #############################################################################################
        self.images_multibutton = [pygame.image.load('Images/MultiButton/Button_install.png'),      #
                                   pygame.image.load('Images/MultiButton/Button_delete.png'),       #
                                   pygame.image.load('Images/MultiButton/Button_play.png'),         #
                                   pygame.image.load('Images/MultiButton/Button_offline.png')]      #
        self.rects_multibutton = [pygame.Rect(588, 438, self.images_multibutton[0].get_width(),     #
                                              self.images_multibutton[0].get_height()),             #
                                  pygame.Rect(588, 438, self.images_multibutton[1].get_width(),     #
                                              self.images_multibutton[1].get_height()),             #
                                  pygame.Rect(648, 438, self.images_multibutton[2].get_width(),     #
                                              self.images_multibutton[2].get_height())]             #
        #############################################################################################
        self.images_delete = [pygame.image.load('Images/InfoDelete/Button_delete.png'),             #
                              pygame.image.load('Images/InfoDelete/Button_back.png'),               #
                              pygame.image.load('Images/InfoDelete/Delete_windows.png'),            #
                              pygame.image.load('Images/InfoDelete/Blackout_window.png')]           #
        self.rects_delete_buttons = [pygame.Rect(412, 272, self.images_delete[0].get_width(),       #
                                                 self.images_delete[0].get_height()),               #
                                     pygame.Rect(284, 274, self.images_delete[1].get_width(),       #
                                                 self.images_delete[1].get_height())]               #
        self.call_delete = False                                                                    #
        #############################################################################################


    def draw_delete_menu(self):
        if self.call_delete:
            self.win.blit(self.images_delete[3], (0, 0))
            self.win.blit(self.images_delete[2], (self.win.get_width() / 2 - self.images_delete[2].get_width() / 2,
                                                  self.win.get_height() / 2 - self.images_delete[2].get_height() / 2))
            self.win.blit(self.images_delete[0], (412, 272))
            self.win.blit(self.images_delete[1], (284, 274))


    def action_delete_menu(self, event):
        if self.call_delete:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rects_delete_buttons[0].collidepoint(pos):
                    if StreamingDownload.delete(self.selected_point.name):
                        self.selected_point.status = 0
                        self.call_delete = False
                        return 1
                elif self.rects_delete_buttons[1].collidepoint(pos):
                    self.call_delete = False


    def draw(self, mode):
        self.mode = mode
        if self.status != -1:
            if self.status == 0:
                if mode:
                    self.win.blit(self.images_multibutton[0], (588, 438))
                else:
                    self.win.blit(self.images_multibutton[3], (588, 438))
            elif self.status == 1:
                self.win.blit(self.images_multibutton[1], (588, 438))
                self.win.blit(self.images_multibutton[2], (648, 438))


    def change_state(self, pos):
        self.list_games[pos - 1].status = 1
        self.status = 1


    def active(self, event_but, select):
        self.select = select
        if select != 0:
            self.selected_point = self.list_games[select - 1]
            self.status = self.selected_point.status
        else:
            self.status = -1
        pos = pygame.mouse.get_pos()
        if event_but.type == pygame.MOUSEBUTTONDOWN:
            if event_but.button == 1:
                if self.status == 0 and self.mode:
                    if self.rects_multibutton[0].collidepoint(pos):
                        StreamingDownload.getinfo(self.selected_point.link)
                        InformationMenu.win_info_dowbload.call = True
                elif self.status == 1:
                    if self.rects_multibutton[1].collidepoint(pos):
                        self.call_delete = True
                    elif self.rects_multibutton[2].collidepoint(pos):
                        StreamingDownload.runfile(self.selected_point.name)
