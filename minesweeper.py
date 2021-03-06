#Program starts running at run() function
from tkinter import *
import random
random.seed()

#Contains all tiles and their characteristics as objects
field = []
#Contains coordinates of mines
mines = []

#Tracks important game variables that are corresponding to
#current game session
class Game:
	def __init__(self):
		self.status = True
		self.firstClick = True
		self.win = 0
		self.l = 0
		self.w = 0
		self.message = ""
		self.width = 0

	def hardReset(self):
		self.status = True
		self.firstClick = True
		self.win = 0
		self.l = 0
		self.w = 0

status = Game()

#Representation of tiles
class Mines:
	def __init__(self, v, x, y, canvas, f, index):
		self.x = x
		self.y = y
		self.index = index
		self.clickable = True
		self.flagged = False
		self.value = v
		self.fill = f
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		canvas.tag_bind(self.visual, '<Button-1>', lambda event: onObjectClick(event, self, canvas))
		canvas.tag_bind(self.visual, '<Button-2>', lambda event: flagTile(event, self, canvas))


	def uncover(self, canvas):
		self.fill = "white"
		self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		if self.value != 0:
			self.visual2 = canvas.create_text(self.x, self.y, text = self.value, font = "Helvetica 14", anchor = NW)

	def flag(self, canvas):
		if self.flagged:
			self.fill = "yellow"
			self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		else:
			self.fill = "grey"
			self.visual = canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill = self.fill, outline = "black", width = "1")
		canvas.tag_bind(self.visual, '<Button-2>', lambda event: flagTile(event, self, canvas))
		canvas.tag_bind(self.visual, '<Button-1>', lambda event: onObjectClick(event, self, canvas))

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

#Determines number of mines based on board size
def generateMines(l, w):
	if w == 9:
		makeMineLocation(10, l, w)
	elif w == 16:
		makeMineLocation(40, l, w)
	else:
		makeMineLocation(99, l, w)

#Generates mine coordinates based on board size
def makeMineLocation(s, l, w):
	for i in range(s):
			while True:
				mineLocation = (random.randint(0,l-1), random.randint(0,w-1))
				if mineLocation not in mines:
					mines.append(mineLocation)
					break
			
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

#Flags or unflags designated tile
def flagTile(event, self, canvas):
	if status.status:
		if not self.flagged:
			self.flagged = True
		else:
			self.flagged = False
	self.flag(canvas)
	canvas.update()

#Handles user selection of tile and either: shows number, 
# shows empty tile and those around them, or exposes mine 
# and calls loss message
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
			else:
				status.status = False
				canvas.delete(status.message)
				status.message = canvas.create_text(status.width/2, 17, text="You Lost :( Press R to Restart", fill="white", font="Helvetica 20 bold ")
		status.firstClick = False
		checkWin(canvas)
		canvas.update()
		


#Recursively checks all numbered or empty tiles around selected
#tile and uncovers them
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

#Resets Canvas
def resetData(canvas):
	canvas.delete(ALL)
	field.clear()
	mines.clear()
	status.message = canvas.create_text(status.width/2, 17, text="Minesweeper", fill="white", font="Helvetica 26 bold ")
	createField(canvas, status.l, status.w)
	setValues(status.l, status.w)

#Checks if user has won game and displays message if so
def checkWin(canvas):
	count = 0
	for row in range(len(field)):
		for col in range(len(field[0])):
			if field[row][col].clickable == False:
				count +=1
	if ((status.l * status.w) - len(mines)) == count :
		canvas.delete(status.message)
		status.message = canvas.create_text(status.width/2, 17, text="You Won!", fill="white", font="Helvetica 26 bold ")
		canvas.update()
		status.status = False

#Window and canvas resized based on parameters
def resizeWindow(root, canvas,h, w):
	root.geometry( str(w)+ "x" + str(h))
	canvas.config(height = str(h), width = str(w))

'''
This is the first function that runs. After a user selects
a game board size. The board size is passed to the createFieldWrapper
and the screen size is adjusted and saved along with the board size in the
status Game object for later reference. Helper funcitons are then called
to create the actual board.
'''
def run(width= 300, height = 300):


	def createFieldWrapper(canvas, l, w):
		status.hardReset()
		if l == 16:
			status.l = 16
			if w == 16:
				width = 530
				height = 550
				resizeWindow(root, canvas, height, width)
				status.w = 16
			else:
				width = 940
				height = 550
				resizeWindow(root, canvas, height, width)
				status.w = 30
		else:
			height = 310
			width = 310
			resizeWindow(root, canvas, height, width)
			status.l = 9
			status.w = 9

		status.width = width
		resetData(canvas)
		canvas.update()

	#Calls for board regeneration and reset of 
	def keyPressedWrapper(event, canvas):
		if(event.char == "r"):
			createFieldWrapper(canvas, status.l, status.w)


	#Default Menu Content
	def createMenu(canvas):
		canvas.delete(ALL)
		canvas.create_text(width/2, 17, text="Minesweeper", fill="white", font="Helvetica 26 bold ")
		canvas.create_text(width/2, 50, text="Instructions", fill="white", font="Helvetica 22 bold ")
		canvas.create_text(width/2, 80, text="Press Left-Click to Reveal Squares", fill="white", font="Helvetica 16 bold ")
		canvas.create_text(width/2, 110, text="Press Right-Click to Flag Mines", fill="white", font="Helvetica 16 bold ")
		canvas.create_text(width/2, 140, text="Press Right-Click again to Unflag Mines", fill="white", font="Helvetica 16 bold ")
		canvas.create_text(width/2, 170, text="Start a new Game at the top", fill="white", font="Helvetica 16 bold ")
		canvas.update()

	root = Tk()

	canvas = Canvas(root, width = width, height = height, background = "blue")
	canvas.pack()

	createMenu(canvas)

	#Toolbar creation
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="9x9, 10 mines", command = lambda: createFieldWrapper(canvas, 9, 9))
	filemenu.add_command(label="16x16, 40 mines", command= lambda: createFieldWrapper(canvas, 16, 16))
	filemenu.add_command(label="16x30, 99 mines", command= lambda: createFieldWrapper(canvas, 16, 30))
	menubar.add_cascade(label="New Game", menu=filemenu)


	exitmenu = Menu(menubar, tearoff=0)
	exitmenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Exit", menu=exitmenu)

	root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas))
	root.config(menu=menubar)
	canvas.focus_set()
	root.mainloop()
run()
