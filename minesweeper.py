from tkinter import *
import random
random.seed()

field = []
mines = []

def createField(l, w):
	generateMines(w)


def generateMines(w):
	if w == 9:
		for i in range(10):
			while True:
				mineLocation = (random.randint(0,9), random.randint(0,9))
				if mineLocation not in mines:
					mines.append(mineLocation)
					break
	elif w == 16:
		pass
	else:
		pass

def run(width= 300, height = 300):

	createField(9, 9)
	print(mines)
	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	root.mainloop()
run()