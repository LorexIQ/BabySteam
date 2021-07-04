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
			self.status = False
		else:
			self.status = True
		f.close()

		f = open(wayGame + '/links.txt')
		self.linkLoad = f.readline()[:-1]
		self.wayExe = f.readline()
		f.close

def updateListGame():
	ListGame = []

	f = open('list_games.txt')
	for line in f:
		if line.endswith('\n'): #если закнчивается на \n
			line = line[:-1] #переписываем но без последнего символа
		ListGame.append(BSgame(line))
	f.close()

	return ListGame 


List = updateListGame()

for l in List:
	print(l.name)
	print(l.inf)
	print(l.way)
	print(l.wayImg)
	print(l.status)
	print(l.linkLoad)
	print(l.wayExe)
	print('\n')
