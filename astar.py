import pygame
import math
from queue import PriorityQueue
#local imports
from colors import Colors
from square import Square

#SCREEN WIDTH & HEIGHT
WIDTH = 800
#WINDOW
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm Visualization")



# Calculate distance between 2 points
def distance(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {square: float("inf") for row in grid for square in row}
	g_score[start] = 0
	f_score = {square: float("inf") for row in grid for square in row}
	f_score[start] = distance(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + distance(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			square = Square(i, j, gap, rows)
			grid[i].append(square)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, Colors.GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, Colors.GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(Colors.WHITE)

	for row in grid:
		for square in row:
			square.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# LEFT CLIC
			if pygame.mouse.get_pressed()[0]: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				square = grid[row][col]
				if not start and square != end:
					start = square
					start.make_start()

				elif not end and square != start:
					end = square
					end.make_end()

				elif square != end and square != start:
					square.make_barrier()

			# RIGHT CLIC
			elif pygame.mouse.get_pressed()[2]: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				square = grid[row][col]
				square.reset()
				if square == start:
					start = None
				elif square == end:
					end = None
			# MID CLICK 
			elif pygame.mouse.get_pressed()[1]:
				main(WIN,WIDTH)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for square in row:
							square.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
