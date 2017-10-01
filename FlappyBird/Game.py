from tkinter import *
from Bird import *
from Pipe import *
import time


# Setup of window
width = 600
height = 800
color_bg = '#61c3ff'
root = Tk()
root.geometry(str(width) + 'x' + str(height))
root.resizable(False, False)
root.title("My Own FlappyBird Game")
canvas = Canvas(root, width=width,
						height=height, bg=color_bg)

canvas.pack()
canvas.update()
score = 0
score_label = canvas.create_text((500, 30), text=score, fill='red', font=("Courier", 44))

bird = Bird(canvas)
pipes = [Pipe(canvas)]


# ReDraw the score label
def update_score():
	global score_label
	canvas.delete(score_label)
	global score
	score_label = canvas.create_text((500, 30), text=score, fill='red', font=("Courier", 44))
	canvas.lift(score_label)


# Game loop
while True:
	bird.move()
	# Add one more pipe
	if pipes[-1].x < width/2:
		pipes.append(Pipe(canvas))
	# Check the pos of bird and update score
	if pipes[0].beyond():
		if bird.fly_through(pipes[0]):
			score += 1
		else:
			score = 0
		update_score()
		pipes.pop(0)
	# Move all pipes to the left side
	for p in pipes:
		p.move()

	root.update()
	time.sleep(0.033)

root.mainloop()