from tkinter import *
import random
random.seed()
#Contains all tiles and their characteristics as objects
field = []
#Contains coordinates of mines
mines = []
#Tracks whether user lost
class Game:
	def __init__(self):
		self.status = True
		self.firstClick = True
		self.win = 0

status = Game()

#Representation of tiles
class Mines:
	def __init__(self, v, x, y, canvas, f, index):
		self.x = x
		self.y = y
		self.index = index
		self.clickable = True
		self.value = v
		self.fill = f
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		canvas.tag_bind(self.visual, '<Button-1>', lambda event: onObjectClick(event, self, canvas))

	def uncover(self, canvas):
		self.fill = "white"
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		if self.value != 0:
			self.visual2 = canvas.create_text(self.x, self.y, text = self.value, font = "Helvetica 14", anchor = NW)


#Generates objects in array and displays tiles
def createField(canvas, l, w, x = 0, y = 0):
	generateMines(l, w)
	for row in range(l):
		x = -10
		y+=30
		field.append([])
		for col in range(w):
			x += 30
			tmpTup = (row, col)
			if tmpTup in mines:
				field[row].append(Mines(-1, x, y, canvas, "red", tmpTup))
			
			else:
				field[row].append(Mines(0, x, y, canvas, "grey", tmpTup))
			
#Goes through all objects in arrays and
# updates value for tiles based on surrounding mines
def setValues(l, w):
	for row in range(len(field)):
		for col in range(len(field[row])):
			if field[row][col].value != -1:
				if row < (l-1):
					#Check bottom
					if field[row + 1][col].value == -1:
						field[row][col].value +=1
				if row > 0:
					#Check top
					if field[row - 1][col].value == -1:
						field[row][col].value +=1
				if col > 0:
					#Check left
					if field[row][col -1].value == -1:
						field[row][col].value +=1
				if col < (w-1):
					#Check right
					if field[row][col + 1].value == -1:
						field[row][col].value +=1
				if row > 0 and col > 0:
					#Check top left
					if field[row - 1][col -1].value == -1:
						field[row][col].value +=1
				if row > 0 and col < (w-1):
					#Check top right
					if field[row - 1][col + 1].value == -1:
						field[row][col].value +=1
				if row < (l-1) and col > 0:
					#Check bottom left
					if field[row + 1][col - 1].value == -1:
						field[row][col].value +=1
				if row < (l-1) and col < (w-1):
					#Check bottom right
					if field[row + 1][col + 1].value == -1:
						field[row][col].value +=1

#Determines number of mines based on board size
def generateMines(l, w):
	if w == 9:
		makeMineLocation(10, l, w)
	elif w == 16:
		makesMineLocation(40, l, w)
	else:
		makesMineLocation(99, l, w)

#Generates mine coordinates based on board size
def makeMineLocation(s, l, w):
	for i in range(s):
			while True:
				mineLocation = (random.randint(0,l-1), random.randint(0,w-1))
				if mineLocation not in mines:
					mines.append(mineLocation)
					break

def onObjectClick(event, self, canvas):
	if status.status:
		if self.value == 0:
			recursiveUncover(self.index[0], self.index[1], canvas)
		else:
			if self.value != -1 and self.clickable == True:
				self.clickable = False
				self.uncover(canvas)
			elif status.firstClick == True:
				indexOfClick = self.index
				while field[indexOfClick[0]][indexOfClick[1]].value == -1:
					resetData(canvas)
				print(field[indexOfClick[0]][indexOfClick[1]].value)
			else:
				status.status = False
				print("You lost")
		status.firstClick = False
		checkWin()
		canvas.update()
		
	


def recursiveUncover(row, col, canvas):
	if field[row][col].value == 0 and field[row][col].clickable == True:
		field[row][col].clickable = False
		field[row][col].uncover(canvas)
		if row < (len(field)-1):
			recursiveUncover(row + 1, col, canvas)
		if row > 0:
			recursiveUncover(row - 1, col, canvas)
		if col > 0:
			recursiveUncover(row , col - 1, canvas)
		if col < (len(field[0])-1):
			recursiveUncover(row , col + 1, canvas)
	else:
		field[row][col].uncover(canvas)
		field[row][col].clickable = False

def resetData(canvas):
	canvas.delete(ALL)
	field.clear()
	mines.clear()
	createField(canvas, 9, 9)
	setValues(9,9)

def checkWin():
	count = 0
	for row in range(len(field)):
		for col in range(len(field[0])):
			if field[row][col].clickable == False:
				count +=1
	print(count)
	if (71) == count :
		print("You won the game")
		status.status = False

def run(width= 300, height = 300):
	def createFieldWrapper(canvas):
		createField(canvas, 9, 9)
		setValues(9, 9)
		canvas.update()
	root = Tk()
	
	canvas = Canvas(root, width = width, height = height, background = "blue")

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="9x9, 10 mines", command = createFieldWrapper(canvas))
	filemenu.add_command(label="16x16, 40 mines", command=onObjectClick)
	filemenu.add_command(label="16x30, 99 mines", command=onObjectClick)

	
	menubar.add_cascade(label="New Game", menu=filemenu)
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Exit", menu=editmenu)


	root.config(menu=menubar)


	canvas.pack()
	

	root.mainloop()
run()



