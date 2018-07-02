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

status = Game()

#Representation of tiles
class Mines:
	def __init__(self, v, x, y, canvas, f):
		self.clickable = True
		self.value = v
		self.fill = f
		self.visual = canvas.create_rectangle(x, y, x+30, y+30, fill = self.fill, outline = "black", width = "1")
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
				field[row].append(Mines(-1, x, y, canvas, "red"))
			
			else:
				field[row].append(Mines(0, x, y, canvas, "grey"))
			
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
		print("This passed")
		if self.value == 0:
			#Recursive function
			pass
		else:
			if self.value != -1:
				self.fill = "white"
			else:
				status.status = False
				print("You lost the game!")
	else:
		print("this did not pass")

	canvas.update()

	


def run(width= 300, height = 300):
	def createFieldWrapper(canvas):
		createField(canvas, 9, 9)
		setValues(9, 9)
		canvas.update()
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	createFieldWrapper(canvas)

	root.mainloop()
run()