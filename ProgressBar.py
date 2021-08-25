import pygame
from threading import Thread


class ProgressBar(object):
    def __init__(self, win, pos_x, pos_y):
        self.win = win
        self.pos_x = pos_x
        self.pos_y = pos_y
        folder = 'Images/InfoDownload'
        self.download_progress = pygame.image.load(folder + '/Progress_line_download.png')
        self.unpack_progress = pygame.image.load(folder + '/Progress_line_unpack.png')
        self.clone_lines = [pygame.image.load(folder + '/Progress_line_download.png'),
                            pygame.image.load(folder + '/Progress_line_unpack.png')]
        self.pixels = []
        self.textures = [self.download_progress, self.unpack_progress]
        for texture in self.textures:
            self.pixels.append(searchPixels(texture))
        fillColor(self.download_progress, self.pixels[0])
        fillColor(self.unpack_progress, self.pixels[1])
        self.diapos_download_progress = [self.pixels[0][0], self.pixels[0][-1]]
        self.diapos_unpack_progress = [self.pixels[1][0], self.pixels[1][-1]]
        self.progress = None
        self.progress_archive = None
        self.thread = None
        self.thread_run = False


    def clear_lines(self):
        self.download_progress = fillColor(self.download_progress, self.pixels[0])
        self.unpack_progress = fillColor(self.unpack_progress, self.pixels[1])


    def thread_draw_image(self):
        progress_bool = [True, False]
        while self.thread_run:
            if progress_bool[0] and self.progress is not None:
                changeColor(self.diapos_download_progress,
                            converter(self.progress, self.diapos_download_progress), self.pixels[0],
                            self.download_progress, self.clone_lines[0])
                if self.progress == 100:
                    self.progress = pygame.image.load('Images/InfoDownload/Progress_line_download.png')
                    progress_bool = [False, True]
            if progress_bool[1] and self.progress_archive is not None:
                changeColor(self.diapos_unpack_progress,
                            converter(self.progress_archive, self.diapos_unpack_progress), self.pixels[1],
                            self.unpack_progress, self.clone_lines[1])
                if self.progress_archive == 100:
                    self.unpack_progress = self.progress = pygame.image.load('Images/InfoDownload/Progress_line_unpack.png')
                    progress_bool[1] = False
            pygame.time.Clock().tick(10)


    def start_thread(self):
        self.thread = Thread(target=self.thread_draw_image, daemon=True)
        self.thread_run = True
        self.thread.start()


    def draw(self, progres, progress_arhive):
        self.progress = progres
        self.progress_archive = progress_arhive
        self.win.blit(self.unpack_progress, (self.pos_x + 261, self.pos_y + 7))
        self.win.blit(self.download_progress, (self.pos_x + 27, self.pos_y + 7))


def changeColor(diapos, now_coord, pixels, image, clone):
    if diapos[0][0][0] <= now_coord <= diapos[1][-1][0]:
        for x_act in range(now_coord - pixels[0][0][0] + 1):
            for paint_act in pixels[x_act]:
                color = image.get_at(paint_act)
                image.set_at(paint_act, (color[0], color[1], color[2], clone.get_at(paint_act)[3]))
    if now_coord < diapos[1][-1][0]:
        for x_inact in range(now_coord - pixels[0][0][0], pixels.index(diapos[1]) + 1):
            for paint_inact in pixels[x_inact]:
                color = image.get_at(paint_inact)
                image.set_at(paint_inact, (color[0], color[1], color[2], 0))


def searchPixels(image):
    coords = []
    for x in range(image.get_width()):
        line = []
        for y in range(image.get_height()):
            if image.get_at((x, y))[3] != 0:
                line.append((x, y))
        if len(line) > 0:
            coords.append(line)
    return coords


def converter(percent, diapos):
    return int(diapos[0][0][0] + ((diapos[1][-1][0] - diapos[0][0][0]) * (percent / 100)))


def fillColor(image, pixels):
    for packet in pixels:
        for coord in packet:
            image.set_at(coord, (image.get_at(coord)[0], image.get_at(coord)[1], image.get_at(coord)[2], 0))
    return image
