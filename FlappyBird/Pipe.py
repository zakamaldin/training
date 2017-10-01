import random


class Pipe():
	def __init__(self, canvas):
		self.canvas = canvas
		self.x = 600
		self.y_up = 0
		self.y_down = 800
		self.velocity = 10
		self.width = 50
		self.heigth = random.randint(200, 350)
		self.pipe_up = self.canvas.create_rectangle(
								self.x,
								self.y_up,
								self.x + self.width,
								self.y_up + self.heigth,
								fill='green')

		self.pipe_down = self.canvas.create_rectangle(
								self.x,
								self.y_down - self.heigth,
								self.x + self.width,
								self.y_down,
								fill='green')

	# Change coord of pipe
	def move(self):
		self.x -= self.velocity
		self.update()

	# ReDraw the pipe
	def update(self):
		self.canvas.delete(self.pipe_down)
		self.canvas.delete(self.pipe_up)
		self.pipe_down = self.canvas.create_rectangle(
								self.x,
								self.y_down - self.heigth,
								self.x + self.width,
								self.y_down,
								fill='green')
		self.pipe_up = self.canvas.create_rectangle(
								self.x,
								self.y_up,
								self.x + self.width,
								self.y_up + self.heigth,
								fill='green')
		self.canvas.lower(self.pipe_up)
		self.canvas.lower(self.pipe_down)

	# Check if pipe off the screen
	def beyond(self):
		if self.x < -self.width:
			return True
		else:
			return False

