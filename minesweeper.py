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
			print(i)
	elif w == 16:
		pass
	else:
		pass

def run(width= 300, height = 300):

	createField(9, 9)

	root = Tk()
	canvas = Canvas(root, width = width, height = height)
	canvas.pack()
	root.mainloop()
run()