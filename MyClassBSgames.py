import tempfile
import os
import zipfile
import requests
import subprocess
import shutil


class BSgame(object):
	def __init__(self, wayGame):
		f = open(wayGame + '/inf.txt')
		self.name = f.readline()[:-1]
		self.inf = f.read()
		f.close()

		self.way = wayGame
		self.wayImg = wayGame + '/img.bmp'

		f = open(wayGame + '/status.txt')
		if f.read(1) == '0':
			self.__status = False   #приватный
		else:
			self.__status = True
		f.close()

		f = open(wayGame + '/links.txt')
		self.linkLoad = f.readline()
		f.close

	def startGame(self):
		if self.__status:
			os.chdir(self.name)
			subprocess.Popen(self.name + '.exe')

	def instalGame(self):
		if not self.__status:
			response = requests.get(self.linkLoad)
			file = tempfile.TemporaryFile()
			file.write(response.content)
			fzip = zipfile.ZipFile(file)
			fzip.extractall()
			file.close()
			fzip.close()

			self.__status = True
			f = open(self.way + '/status.txt', 'w')
			f.write('1')
			f.close()

	def deleteGame(self):
		if self.__status:
			shutil.rmtree(self.name)

			self.__status = False
			f = open(self.way + '/status.txt', 'w')
			f.write('0')
			f.close()

	def GetStatus(self):
		return self.__status

def updateListGame():
	ListGame = []

	f = open('list_games.txt')
	for line in f:
		if line.endswith('\n'): #если закнчивается на \n
			line = line[:-1] #переписываем но без последнего символа
		ListGame.append(BSgame(line))
	f.close()

	return ListGame 
