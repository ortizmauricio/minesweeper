from tkinter import *
import random
random.seed()

field = []
mines = []


class Mines:
	def __init__(self, v, x, y, canvas):
		self.clickable = True
		self.value = v
		self.visual = canvas.create_rectangle(x, y, 20, 20)

def createField(canvas, l, w, x = 30, y = 30):
	generateMines(l, w)
	for row in range(l):
		y+=20
		print(row)
		field.append([])
		for col in range(w):
			x += 20
			tmpTup = (row, col)
			if tmpTup in mines:
				field[row].append(Mines(-1, x, y, canvas))
			else:
				field[row].append(Mines(0, x, y, canvas))

def generateMines(l, w):
	if w == 9:
		makeMineLocation(10, l, w)
	elif w == 16:
		makesMineLocation(40, l, w)
	else:
		makesMineLocation(99, l, w)

def makeMineLocation(s, l, w):
	for i in range(s):
			while True:
				mineLocation = (random.randint(0,l-1), random.randint(0,w-1))
				if mineLocation not in mines:
					mines.append(mineLocation)
					break

def run(width= 300, height = 300):
	def createFieldWrapper(canvas):
		createField(canvas, 9, 9)
		canvas.update()
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	createFieldWrapper(canvas)




	root.mainloop()
run()