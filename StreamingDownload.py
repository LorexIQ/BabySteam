import os
import shutil
import subprocess

import zipfile
import socket

import pygame.time
import requests
import time
import ZipUnpack
from threading import Thread
from shutil import rmtree
from subprocess import Popen
from os import remove, chdir, mkdir, path

download_body = None
status_file_server = False
thread_download = None
download_information = [0, 0, 0, 0.0, [0, 0], [0, 0]]
content_run = False
complete = False

#####################################################
# Коды состояния класса скачивания                  #
# -1 - Информации нет (информация сброшена)         #
# 0 - Попытка соединения                            #
# 1 - Соединение с интернетом установлено           #
# 2 - Файл по ссылке найден                         #
# 3 - Файл по ссылке не найден                      #
# 4 - Нет соединения с сервером                     #
# 5 - Скачивание файла                              #
# 6 - Сбой скачивания (нет или слабый интернет)     #
# 7 - Скачивание возобновлено                       #
# 8 - Информация об скачиваемом файле не загружена  #
# 9 - Скачивание завершено                          #
# 10 - Пауза скачивания                             #
# 11 - Скачивание не идёт, данные загружены         #
# 12 - Отмена скачивания                            #
# 13 - Распаковка скаченного файла                  #
# 14 - Распаковка завершена                         #
# 15 - Приложение удалено                           #
# 16 - Ошибка удаления приложения                   #
# 17 - Приложение запущено                          #
# 18 - Ошибка запуска приложения                    #
# 19 - Отмена невозможна (скачивание не запущено)   #
# 20 - Пауза невозможна (скачивание не запущено)    #
# 21 - Скачивание уже запущено                      #
# 22 - Данные уже загружены                         #
#####################################################
status_streaming_download = -1                      #
live_status = -1                                    #
#####################################################

############################################
# Конфигурация настроект отображения данных
# font
# 1/0 x y color size - Размер файла
# 1/0 x y color size - Уже скачено
# 1/0 x y color size - Скорость скачивания
############################################

config_labels = [[None],
                 [[1], [10], [10], ['red'], [25]],
                 [0],
                 [0]]


class ReadInfo(object):
    def __init__(self, name, repos, mode):
        self.status = None
        self.name = name
        if mode:
            upload = True
            if os.path.exists('babysteaminfo/' + self.name):
                if os.path.isfile('babysteaminfo/' + self.name + '/img1.bmp') and \
                        os.path.isfile('babysteaminfo/' + self.name + '/img2.bmp') and \
                        os.path.isfile('babysteaminfo/' + self.name + '/inf.txt'):
                    upload = False
            else:
                os.mkdir('babysteaminfo/' + self.name)
            if upload:
                info_packet = requests.get('%s/%s/Info.zip' % (repos, self.name), timeout=2)
                with open('babysteaminfo/info_%s.zip' % self.name, 'wb') as file_info:
                    file_info.write(info_packet.content)
                zipfile.ZipFile('babysteaminfo/info_%s.zip' % self.name).extractall('babysteaminfo/' + self.name)
                os.remove('babysteaminfo/info_%s.zip' % self.name)
        self.link = '%s/%s/%s.zip' % (repos, self.name, self.name)
        self.img1 = 'babysteaminfo/' + self.name + '/img1.bmp'
        self.img2 = 'babysteaminfo/' + self.name + '/img2.bmp'
        with open('babysteaminfo/' + self.name + '/inf.txt', 'r') as info_content:
            self.text_info = info_content.read()


def update_status(list_contents):
    for content in list_contents:
        if os.path.exists('babysteamapps'):
            if os.path.exists('babysteamapps/' + content.name):
                if os.path.isfile('babysteamapps/' + content.name + '/' + content.name + '.exe'):
                    content.status = True
                else:
                    content.status = False
            else:
                content.status = False
        else:
            content.status = False


def search_content():
    if os.path.exists('babysteaminfo'):
        list_folders = os.listdir('babysteaminfo')
        if len(list_folders) > 0:
            fin_list = []
            for fold in list_folders:
                if os.path.isfile('babysteaminfo/' + fold + '/img1.bmp') and \
                        os.path.isfile('babysteaminfo/' + fold + '/img2.bmp') and \
                        os.path.isfile('babysteaminfo/' + fold + '/inf.txt'):
                    fin_list.append(fold)
            return fin_list
        else:
            return None
    else:
        return None


def readInformationContent():
    if not os.path.exists('babysteaminfo'):
        os.mkdir('babysteaminfo')
    content_group = []
    repos_link = "https://github.com/LorexIQ/ContentForBabySteam/raw/main"
    try:
        list_contents_txt = requests.get(repos_link + '/list.txt', stream=True, timeout=2)
        with open('babysteaminfo/list.txt', 'wb') as file_list:
            file_list.write(list_contents_txt.content)
        with open('babysteaminfo/list.txt', 'r') as file_list:
            list_contents = file_list.readlines()
        os.remove('babysteaminfo/list.txt')
        for content in range(len(list_contents)):
            if '\n' in list_contents[content]:
                list_contents[content] = list_contents[content][:-1]
        for name in list_contents:
            content_group.append(ReadInfo(name, repos_link, True))
        update_status(content_group)
        return content_group, True
    except:
        list_contents = search_content()
        if list_contents is None:
            return None, False
        else:
            for name in list_contents:
                content_group.append(ReadInfo(name, repos_link, False))
            update_status(content_group)
            return content_group, False


class Download:
    def __init__(self, link, filename):
        global status_file_server, download_information, status_streaming_download
        status_streaming_download = 0
        try:
            self.done = False
            self.run = False
            self.downloading = None
            self.filename = filename
            self.file = requests.get(link, stream=True, timeout=5)
            status_streaming_download = 1
            if self.file.status_code == 200:
                status_streaming_download = 2
                status_file_server = True
                self.size_file = int(self.file.headers['Content-Length']) // 1024
                self.size_file = int(self.size_file - (self.size_file / 100) * 3)
                download_information[0] = self.size_file
                self.already = 0
                self.time = 0
                self.old_line = 0
                self.link = link
                self.bytes = 0
                self.pause_download = False
                self.active = False
                self.unpack = False
            else:
                status_streaming_download = 3
                status_file_server = False
        except:
            status_streaming_download = 4


    def install(self):
        global download_information, status_streaming_download, live_status
        if not os.path.exists('babysteamapps'):
            os.mkdir('babysteamapps')
        progres_old = 0
        thread_speed = Thread(target=self.speed, daemon=True)
        thread_speed.start()
        download_information[4][1] = 0
        with open('babysteamapps/' + self.filename + '.zip', 'wb') as local_file:
            while not self.done:
                try:
                    for data in self.file.iter_content(chunk_size=1024):
                        live_status = 5
                        if not self.active:
                            self.active = True
                        if data:
                            local_file.write(data)
                            self.already += 1
                            self.bytes += len(data)
                            download_information[3] = round((self.already * 100) / self.size_file, 1)
                            if download_information[3] > 100:
                                download_information[3] = 100
                            if download_information[3] != progres_old:
                                progres_old = download_information[3]
                            download_information[1] = self.already
                            if download_information[1] > self.size_file:
                                download_information[1] = self.size_file
                            while self.pause_download:
                                live_status = 10
                            if not self.run:
                                break
                    if download_information[3] < 100:
                        for indent in range(download_information[3] + 1, 100):
                            download_information[3] = indent
                    time.sleep(0.5)
                    self.done = True
                except:
                    status_streaming_download = 6
                    live_status = 6
                    self.file = self.resume()
                    if self.file is None:
                        break
                    status_streaming_download = 7
            local_file.close()
            if self.run:
                self.file.close()
                download_information[1] = download_information[0]
                status_streaming_download = 9
                live_status = 13
                self.unpack = True
                status_streaming_download = 13
                time.sleep(0.5)
                ZipUnpack.unzip()
                status_streaming_download = 23
                live_status = 14
                self.unpack = False
                time.sleep(0.5)
                status_streaming_download = 14
            else:
                live_status = 12
                if download_information[3] > 0:
                    for cancel_count in range(int(download_information[3]), 0, -1):
                        download_information[3] = cancel_count
                        time.sleep(60 / (download_information[3] * 100))
                    download_information[3] = 0
                time.sleep(1)
                status_streaming_download = 12
            os.remove('babysteamapps/file.zip')
            self.active = False


    def resume(self):
        global status_streaming_download
        while True:
            try:
                if not self.run:
                    break
                resume_header = {'Range': 'bytes=%d-' % self.bytes}
                return requests.get(self.link, headers=resume_header, timeout=5, stream=True)
            except:
                continue


    def speed(self):
        global download_information
        timeout_count = 0
        while True:
            if timeout_count == 2:
                try:
                    left_seconds = round((download_information[0] - download_information[1]) / download_information[2])
                    download_information[5][0] = left_seconds // 60
                    download_information[5][1] = left_seconds % 60
                except:
                    pass
                timeout_count = 0
            else:
                timeout_count += 1
            download_information[4][1] += 1
            if download_information[4][1] == 60:
                download_information[4][1] = 0
                download_information[4][0] += 1
            download_information[2] = self.already - self.old_line
            self.old_line = self.already
            if self.done or not self.run:
                break
            pygame.time.Clock().tick(1)


def pause():
    global status_streaming_download, download_body
    if download_body is not None and not download_body.run:
        status_streaming_download = 11
    elif download_body is not None and not download_body.unpack:
        if not download_body.pause_download:
            download_body.pause_download = True
            status_streaming_download = 10
        else:
            download_body.pause_download = False
            status_streaming_download = 7
    else:
        status_streaming_download = 20


def prepare(link):
    global download_body, thread_download, download_information, status_streaming_download
    if download_body is None or download_body.done or (download_body is not None and thread_download is not None and not download_body.run):
        download_information = [0, 0, 0, 0.0, [0, 0], [0, 0]]
        ZipUnpack.zip_progress = 0
        download_body = Download(link, 'file')
        if status_file_server:
            thread_download = Thread(target=download_body.install, daemon=True)
        else:
            download_body = None
    else:
        status_streaming_download = 22


def install():
    global status_streaming_download, live_status
    if thread_download is not None and status_file_server and download_body is not None:
        if thread_download.is_alive():
            status_streaming_download = 21
        else:
            download_body.run = True
            thread_download.start()
            status_streaming_download = 5
            live_status = 5
    else:
        status_streaming_download = 8


def getinfo(link):
    thread_prepare = Thread(target=prepare, args=(link,), daemon=True)
    thread_prepare.start()


def cancel():
    global download_body, status_streaming_download
    if download_body is not None and download_body.run and not download_body.unpack:
        download_body.run = False
        download_body.pause_download = False
    else:
        status_streaming_download = 19


def delete(filename):
    global status_streaming_download
    try:
        shutil.rmtree('babysteamapps/' + filename + '/')
        status_streaming_download = 15
        return True
    except FileNotFoundError:
        status_streaming_download = 16
        return False


def runfile(filename):
    global status_streaming_download
    try:
        os.chdir('babysteamapps/' + filename)
        subprocess.Popen(filename + '.exe')
        status_streaming_download = 17
        os.chdir('..')
        os.chdir('..')
    except FileNotFoundError:
        status_streaming_download = 18


def update():
    global download_body
    if download_body is not None and download_body.done:
        download_body = None


def CheckInternet():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        return False
