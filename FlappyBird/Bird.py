class Bird:
	def __init__(self, canvas):
		self.canvas = canvas
		self.canvas.bind_all('<space>', self.jump)
		self.rad = 50
		self.x = 50
		self.y = int(self.canvas.winfo_height()/2)
		self.gravity = 2.5
		self.velocity = 0
		self.up = -25
		self.bird = self.canvas.create_oval(
			self.x,
			self.y,
			self.x + self.rad,
			self.y + self.rad,
			fill='#ffea00')

	# Change coord of bird
	def move(self):
		self.velocity += self.gravity
		self.y += self.velocity
		if self.y > (self.canvas.winfo_height()-self.rad/2):
			self.y = self.canvas.winfo_height()-self.rad/2
			self.velocity = 0
		if self.y < 0:
			self.y = 0
			self.velocity = 0
		self.update()

	# ReDraw the bird
	def update(self):
		self.canvas.delete(self.bird)
		self.bird = self.canvas.create_oval(
			self.x,
			self.y,
			self.x + self.rad,
			self.y + self.rad,
			fill='#ffea00')

	# Add velocity to the bird
	def jump(self, event=None):
		self.velocity += self.up

	# Check if bird fly between the pipes
	def fly_through(self, pipe):
		if(self.x > pipe.x + pipe.width) \
				and (self.y > pipe.y_up + pipe.heigth) \
				and (self.y + self.rad < pipe.y_down - pipe.heigth):
			return True
		return False





