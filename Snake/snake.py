from tkinter import *
import random

widthWindow = 600
heightWindow = 600
blockSize = 20


class Block(object):
	def __init__(self, canvas, x=blockSize, y=blockSize):
		print("block_coord", x, y)
		self.c = canvas
		self.instance = self.c.create_rectangle(x, y, x + blockSize, y + blockSize, fill="white")



class Snake(object):
	def __init__(self, canvas):
		self.c = canvas
		x = blockSize * (random.randint(1, (widthWindow - blockSize) / blockSize))
		y = blockSize * (random.randint(1, (heightWindow - blockSize) / blockSize))
		blocks = [Block(self.c, x, y)]

		self.blocks = blocks
		self.mapping = {
			"Down": (0, 1),
			"Up": (0, -1),
			"Left": (-1, 0),
			"Right": (1, 0)}
		self.vector = self.mapping["Right"]
		self.c.itemconfig(self.blocks[-1].instance, fill='green')

	def move(self):
		for i in range(len(self.blocks) - 1):
			segment = self.blocks[i].instance
			x1, y1, x2, y2 = self.c.coords(self.blocks[i + 1].instance)
			self.c.coords(segment, x1, y1, x2, y2)

		x1, y1, x2, y2 = self.c.coords(self.blocks[-1].instance)
		self.c.coords(self.blocks[-1].instance,
				 x1 + self.vector[0] * blockSize,
				 y1 + self.vector[1] * blockSize,
				 x2 + self.vector[0] * blockSize,
				 y2 + self.vector[1] * blockSize)

	def cnange_dir(self, event):
		if event.keysym in self.mapping:
			self.vector = self.mapping[event.keysym]

	def add_block(self):
		last_block = self.c.coords(self.blocks[0].instance)

		x = last_block[1] - blockSize
		y = last_block[2] - blockSize
		print("add_block_coord:", x,y)
		self.blocks.insert(0, Block(x,y))


def add_food(c):
	global food
	x = blockSize * (random.randint(1, (widthWindow - blockSize)/blockSize))
	y = blockSize * (random.randint(1, (heightWindow - blockSize) / blockSize))
	print("food_coord:", x,y)
	food = c.create_rectangle(x, y, x + blockSize, y + blockSize, fill="red")


def main(c, s):
	global ingame
	ingame = True
	if ingame:
		s.move()
		head_coords = c.coords(s.blocks[-1].instance)
		x1, y1, x2, y2 = head_coords
		if x1 < 0 or x2 > widthWindow or y1 < 0 or y2 > heightWindow:
			ingame = False
		elif head_coords == c.coords(food):
			s.add_block()
			c.delete(food)
			add_food(c)
		else:
			for i in range(len(s.blocks) - 1):
				if c.coords(s.blocks[i].instance) == head_coords:
					ingame = False
		root.after(100, main, c, s)



def start_game():
	c = Canvas(root, width=widthWindow, height=heightWindow, bg="grey50")
	c.grid()
	c.focus_set()
	s = Snake(c)
	c.bind("<KeyPress>", s.cnange_dir)
	add_food(c)
	main(c, s)


root = Tk()
root.title("Змейка")
root.resizable(width=False, height=False)
start_game()
root.mainloop()
