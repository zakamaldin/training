from tkinter import *
import random
root = Tk()
width = 600
heigth = 800
root.geometry(str(heigth) + 'x' + str(width))
root.resizable(False, False)
c = Canvas(root, width=heigth, height=width, bg='black')
c.pack()
x = 0
y = 0
delay = 5
spacing = 25
color = "#8ffe09 "


def draw():
	global x
	global y
	if random.random() < 0.5:
		i = c.create_line(x, y, x+spacing, y+spacing, fill=color)
	else:
		i = c.create_line(x, y+spacing, x+spacing, y, fill=color)

	x += spacing
	if x > heigth:
		x = 0
		y += spacing
	if y >= width and x >= heigth:
		return
	c.after(delay, draw)


draw()
root.mainloop()

