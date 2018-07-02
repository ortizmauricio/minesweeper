from tkinter import *
import random
random.seed()

field = []
mines = []

def createField(l, w):
	generateMines(l, w)

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
				mineLocation = (random.randint(0,l), random.randint(0,w))
				if mineLocation not in mines:
					mines.append(mineLocation)
					break

def run(width= 300, height = 300):

	createField(9, 9)
	print(mines)
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	root.mainloop()
run()