import time
from typing import List, Any

import pygame
import StreamingDownload
import ProgressBar
import ZipUnpack

InformationWindow = None
win_info_dowbload = None


def PrintInformation(x, y, words, font, width):
    fin_block_text = []
    fin_coords_text = []
    timed_coords_text = []
    for text_i in words:
        text_wight = 0
        text_height = 0
        block_text = []
        block_coords = []
        min_pos = 1
        for i in text_i:
            about = 1
            block_text.append(font.render(str(i), True, (200, 200, 200)))
            if block_text[-1].get_width() + text_wight > width - 20:
                air = width - 20 - block_coords[-1][0] - block_text[-2].get_width()
                count_words = len(block_text) - min_pos
                step = air / (count_words - 1)
                for j in range(min_pos, len(block_coords)):
                    block_coords[j] = (block_coords[j][0] + step * about, block_coords[j][1])
                    about += 1
                min_pos = len(block_text)
                text_wight = 0
                text_height += font.get_height()
            block_coords.append((text_wight, y + text_height))
            text_wight += block_text[-1].get_width() + 5
        fin_block_text.append(block_text)
        timed_coords_text.append(block_coords)
    for content in timed_coords_text:
        timed_line = []
        for coord in content:
            timed_line.append((coord[0] + x, coord[1]))
        fin_coords_text.append(timed_line)
    return fin_block_text, fin_coords_text


def Wording(information):
    words = []
    for i in information:
        words.append(i.split())
    return words


class Window(object):
    def __init__(self, x, y, win, List_objects):
        self.images_backgrounds = [pygame.image.load('Images/Main/Background_info.png'),
                                   pygame.image.load('Images/Main/Background_news.png')]
        self.x = x
        self.y = y
        self.width = self.images_backgrounds[0].get_width()
        self.height = self.images_backgrounds[0].get_height()
        self.position_list = 0
        self.win = win
        self.object = pygame.Surface((self.width, self.height))
        self.List_objects = List_objects
        self.information = []
        self.images = []
        self.ReadInformation()
        self.words = Wording(self.information)
        self.block_text, self.coords_text = PrintInformation(10, 220, self.words, pygame.font.Font('Font/List.ttf', 20), self.width)


    def draw(self, position_list):
        self.position_list = position_list
        if position_list == 0:
            self.object = pygame.Surface((self.width, self.height + 60))
            self.object.blit(self.images_backgrounds[1], (0, 0))
        else:
            self.object = pygame.Surface((self.width, self.height))
            self.object.blit(self.images_backgrounds[0], (0, 0))
            self.object.blit(self.images[position_list - 1], (10, 10))
            for i in range(len(self.coords_text[position_list - 1])):
                self.object.blit(self.block_text[position_list - 1][i], self.coords_text[position_list - 1][i])
        self.win.blit(self.object, (self.x, self.y))


    def ReadInformation(self):
        for i in self.List_objects:
            self.information.append(i.text_info)
            self.images.append(pygame.image.load(i.img2))
            self.images[-1] = pygame.transform.scale(self.images[-1], (self.width - 20, 200))


class DownloadInfo:
    def __init__(self, win):
        self.images = [pygame.image.load('Images/InfoDownload/Button_install.png'),               # 0
                       pygame.image.load('Images/InfoDownload/Button_done.png'),                  # 1
                       pygame.image.load('Images/InfoDownload/Button_pause.png'),                 # 2
                       pygame.image.load('Images/InfoDownload/Button_back.png'),                  # 3
                       pygame.image.load('Images/InfoDownload/Button_stop.png'),                  # 4
                       pygame.image.load('Images/InfoDownload/Button_offline.png'),               # 5
                       pygame.image.load('Images/InfoDownload/Button_waiting.png'),               # 6
                       pygame.image.load('Images/InfoDownload/Progress_bar_download_start.png'),  # 7
                       pygame.image.load('Images/InfoDownload/Progress_bar_download_ready.png'),  # 8
                       pygame.image.load('Images/InfoDownload/Progress_bar_allready.png'),        # 9
                       pygame.image.load('Images/InfoDownload/Progress_line_unpack.png'),         # 10
                       pygame.image.load('Images/InfoDownload/Progress_line_download.png'),       # 11
                       pygame.image.load('Images/InfoDownload/Blackout_window.png'),              # 12
                       pygame.image.load('Images/InfoDownload/Info_windows.png'),                 # 13
                       pygame.image.load('Images/InfoDownload/Button_pause2.png')]                # 14
        self.rects_buttons = [pygame.Rect(487, 332, self.images[0].get_width(), self.images[0].get_height()),
                              # install, done
                              pygame.Rect(209, 334, self.images[3].get_width(), self.images[3].get_height()),
                              # cancel, back
                              pygame.Rect(244, 334, self.images[2].get_width(), self.images[2].get_height())]  # pause
        font = pygame.font.Font('Font/List.ttf', 10)
        self.label_user = [
            'Нажимая кнопку <install>, вы берёте на себя ответственность за скачивание файлов и соглашаетесь с тем, что автор не несёт никакой ответственности за ваше устройство в случае возникновения проблем. Дальнейшие ваши действия вы совершаете на свой страх и риск. Скачиваемое приложение было проверено и добавлено автором магазина, файлы не несут никакой опасности для вашего устройства. Потоковое скачивание защищено. В случае возникновения проблем с сетью, программа попытается возобновить скачивание. Возможно, что после скачивания программа перестанет подавать признаки жизни - это обозначает, что игра имеет много файлов и распаковка занимает больше времени.']
        self.label_size_file = None
        self.label_size_loading = pygame.font.Font('Font/List.ttf', 20).render('Размер: ...', True, (200, 200, 200))
        self.status_download = ['скачивание...',
                                'пауза...',
                                'отмена...',
                                'установка...',
                                'повтор...',
                                'готово']
        self.font_info = pygame.font.Font('Font/List.ttf', 15)
        self.font_fin_info = pygame.font.Font('Font/List.ttf', 25)
        self.font_fin_info2 = pygame.font.Font('Font/List.ttf', 20)
        self.progress_bar = None
        self.win = win
        timed_label_user_accect = Wording(self.label_user)
        self.fin_blocks, self.fin_coords = PrintInformation(
            self.win.get_width() / 2 - self.images[13].get_width() / 2 + 24,
            self.win.get_height() / 2 - self.images[13].get_height() / 2 + 24, timed_label_user_accect, font,
            self.images[13].get_width() - 30)
        self.call = False
        self.sosto = 0
        self.unpack = False
        self.update = False


    def draw(self, info=0):
        if self.call:
            self.win.blit(self.images[12], (0, 0))
            self.win.blit(self.images[13], (self.win.get_width() / 2 - self.images[13].get_width() / 2,
                                            self.win.get_height() / 2 - self.images[13].get_height() / 2))
            # Ожидание загрузки информации #
            if self.sosto == 0:
                self.win.blit(self.images[6], (487, 332))
                self.win.blit(self.images[3], (209, 334))
                if StreamingDownload.status_streaming_download == 2:
                    self.sosto = 4
                    if StreamingDownload.download_information[0] > 1024:
                        size = str(round(StreamingDownload.download_information[0] / 1024, 2)) + ' Mb'
                    else:
                        size = str(StreamingDownload.download_information[0]) + ' Kb'
                    self.label_size_file = pygame.font.Font('Font/List.ttf', 20).render('Размер: ' + size, True,
                                                                                        (200, 200, 200))
                elif StreamingDownload.status_streaming_download == 4:
                    self.sosto = 5
                for word in range(len(self.fin_blocks[0])):
                    self.win.blit(self.fin_blocks[0][word], self.fin_coords[0][word])
                self.win.blit(self.label_size_loading, (244, 337))
            # Загрузка файла #
            elif self.sosto == 1:
                self.win.blit(self.images[4], (209, 334))
                self.win.blit(self.images[2 if StreamingDownload.status_streaming_download != 10 else 14], (244, 334))
                if StreamingDownload.status_streaming_download == 13:
                    self.unpack = True
                    self.win.blit(self.images[8], (279, 334))
                elif StreamingDownload.status_streaming_download == 23:
                    self.win.blit(self.images[9], (279, 334))
                    self.update = True
                elif StreamingDownload.status_streaming_download == 14:
                    self.sosto = 3
                    StreamingDownload.status_streaming_download = -1
                elif StreamingDownload.status_streaming_download == 12:
                    self.sosto = 2
                else:
                    self.win.blit(self.images[7], (279, 334))
                if StreamingDownload.status_streaming_download != 12:
                    self.progress_bar.draw(StreamingDownload.download_information[3], ZipUnpack.zip_progress)
                self.win.blit(self.font_info.render('Информация', True, (200, 200, 200)), (220, 140))
                if not self.unpack:
                    self.win.blit(self.font_info.render('Загружено: ' + ((str(
                        StreamingDownload.download_information[1]) + ' Kb из ' + str(
                        StreamingDownload.download_information[0]) + ' Kb') if StreamingDownload.download_information[
                                                                                   0] < 1024 else (
                                str(round(StreamingDownload.download_information[1] / 1024, 2)) + ' Mb из ' + str(
                            round(StreamingDownload.download_information[0] / 1024, 2)) + ' Mb')), True,
                                                        (200, 200, 200)), (220, 170))
                    self.win.blit(self.font_info.render('Скорость: ' + (
                        (str(StreamingDownload.download_information[2]) + ' Kb/s ') if
                        StreamingDownload.download_information[2] < 1024 else (
                                str(round(StreamingDownload.download_information[2] / 1024, 2)) + ' Mb/s')), True,
                                                        (200, 200, 200)), (220, 190))
                    self.win.blit(
                        self.font_info.render('Прогресс: ' + (str(StreamingDownload.download_information[3]) + '% '),
                                              True,
                                              (200, 200, 200)), (220, 210))
                    self.win.blit(
                        self.font_info.render('Времени прошло: ' + (
                            (str(StreamingDownload.download_information[4][1]) + ' сек.') if
                            StreamingDownload.download_information[4][0] == 0 else (
                                    str(StreamingDownload.download_information[4][0]) + ' мин. ' + str(
                                StreamingDownload.download_information[4][1]) + ' сек.')), True, (200, 200, 200)),
                        (220, 230))
                    self.win.blit(
                        self.font_info.render('Времени осталось: ' + (
                            (str(StreamingDownload.download_information[5][1]) + ' сек.') if
                            StreamingDownload.download_information[5][0] == 0 else (
                                    str(StreamingDownload.download_information[5][0]) + ' мин. ' + str(
                                StreamingDownload.download_information[5][1]) + ' сек.')), True, (200, 200, 200)),
                        (220, 250))
                else:
                    self.win.blit(self.font_info.render('Установка пакетов: ' + str(ZipUnpack.zip_info[0]) + ' из ' + str(ZipUnpack.zip_info[1]), True, (200, 200, 200)), (220, 170))
                self.win.blit(self.font_info.render('Состояние: ' + self.status_download[
                    0 if StreamingDownload.live_status == 5 else 1 if StreamingDownload.live_status == 10 else 2 if StreamingDownload.live_status == 12 else 3 if StreamingDownload.live_status == 13 else 4 if StreamingDownload.live_status == 6 else 5],
                                                    True, (200, 200, 200)), (220, 300))
            # Состояние после отмены загрузки #
            elif self.sosto == 2:
                self.win.blit(self.images[3], (209, 334))
                self.progress_bar.thread_run = False
                self.win.blit(self.font_fin_info.render('Загрузка отменена', True, (200, 200, 200)), (260, 150))
                label_result = self.font_info.render('Затрачено времени: ' + (
                    str(StreamingDownload.download_information[4][0]) + ' мин. ' + str(
                        StreamingDownload.download_information[4][1]) + ' сек.' if
                    StreamingDownload.download_information[4][0] != 0 else str(
                        StreamingDownload.download_information[4][1]) + ' сек.'), True, (200, 200, 200))
                self.win.blit(label_result, ((self.images[13].get_width() / 2 - label_result.get_width() / 2) + (
                            self.win.get_width() / 2 - self.images[13].get_width() / 2), 220))
                label_sized = self.font_info.render('Скачено: ' + (str(StreamingDownload.download_information[1]) + ' Kb из ' if StreamingDownload.download_information[1] < 1024 else str(round(StreamingDownload.download_information[1] / 1024, 2)) + ' Mb из ') + (str(StreamingDownload.download_information[0]) + ' Kb' if StreamingDownload.download_information[0] < 1024 else str(round(StreamingDownload.download_information[0] / 1024, 2)) + ' Mb'), True, (200, 200, 200))
                self.win.blit(label_sized, ((self.images[13].get_width() / 2 - label_sized.get_width() / 2) + (
                            self.win.get_width() / 2 - self.images[13].get_width() / 2), 240))

            # Состояние после загрузки #
            elif self.sosto == 3:
                self.unpack = False
                self.progress_bar.thread_run = False
                self.win.blit(self.images[1], (487, 332))
                self.win.blit(self.font_fin_info.render('Загрузка завершена', True, (200, 200, 200)), (255, 150))
                label_result = self.font_info.render('Затрачено времени: ' + (str(StreamingDownload.download_information[4][0]) + ' мин. ' + str(StreamingDownload.download_information[4][1]) + ' сек.' if StreamingDownload.download_information[4][0] != 0 else str(StreamingDownload.download_information[4][1]) + ' сек.'), True, (200, 200, 200))
                self.win.blit(label_result, ((self.images[13].get_width() / 2 - label_result.get_width() / 2) + (self.win.get_width() / 2 - self.images[13].get_width() / 2), 220))
                label_sized = self.font_info.render('Скачено: ' + (str(StreamingDownload.download_information[1]) + ' Kb' if StreamingDownload.download_information[1] < 1024 else str(round(StreamingDownload.download_information[1] / 1024, 2)) + ' Mb'), True, (200, 200, 200))
                self.win.blit(label_sized, ((self.images[13].get_width() / 2 - label_sized.get_width() / 2) + (self.win.get_width() / 2 - self.images[13].get_width() / 2), 240))
            # Состояние после проверки наличия файлов #
            elif self.sosto == 4:
                self.win.blit(self.images[3], (209, 334))
                self.win.blit(self.images[0], (487, 332))
                for word in range(len(self.fin_blocks[0])):
                    self.win.blit(self.fin_blocks[0][word], self.fin_coords[0][word])
                self.win.blit(self.label_size_file, (244, 337))
            # Офлайн #
            elif self.sosto == 5:
                self.win.blit(self.images[3], (209, 334))
                self.win.blit(self.images[5], (487, 332))
                for word in range(len(self.fin_blocks[0])):
                    self.win.blit(self.fin_blocks[0][word], self.fin_coords[0][word])


    def active(self, event):
        if self.call:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if self.rects_buttons[0].collidepoint(pos) and self.sosto == 4:
                    self.progress_bar = ProgressBar.ProgressBar(self.win, 279, 334)
                    StreamingDownload.install()
                    self.progress_bar.start_thread()
                    self.sosto = 1
                elif (self.rects_buttons[1].collidepoint(pos) and self.sosto in (0, 4, 2, 5)) or \
                        (self.rects_buttons[0].collidepoint(pos) and self.sosto == 3):
                    self.sosto = 0
                    self.call = False
                    StreamingDownload.download_information = [0, 0, 0, 0.0, [0, 0], [0, 0]]
                    StreamingDownload.status_streaming_download = -1
                elif self.rects_buttons[1].collidepoint(pos) and self.sosto == 1 and not self.unpack:
                    StreamingDownload.cancel()
                elif self.rects_buttons[2].collidepoint(pos) and self.sosto == 1 and not self.unpack:
                    StreamingDownload.pause()


def create_info_win(win):
    global win_info_dowbload
    win_info_dowbload = DownloadInfo(win)
