from colors import Colors
import pygame

class Square:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = Colors.WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	# Get Position
	def get_pos(self):
		return self.row, self.col

	# Get States
		
	def is_start(self):
		return self.color == Colors.BLUE

	def is_end(self):
		return self.color == Colors.TURQUOISE

	def is_closed(self):
		return self.color == Colors.GREEN

	def is_open(self):
		return self.color == Colors.RED

	def is_barrier(self):
		return self.color == Colors.BLACK

	# Make States 

	def make_start(self):
		self.color = Colors.BLUE

	def make_closed(self):
		self.color = Colors.GREEN

	def make_open(self):
		self.color = Colors.RED

	def make_barrier(self):
		self.color = Colors.BLACK

	def make_end(self):
		self.color = Colors.TURQUOISE

	def make_path(self):
		self.color = Colors.PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False
	
	# Reset square
	def reset(self):
		self.color = Colors.WHITE
