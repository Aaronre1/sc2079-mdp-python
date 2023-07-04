import pygame
from enum import Enum

WIDTH = 500
ROWS = 20
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Face(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.face = Face.North

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False


class Arena:
    def __init__(self, width):
        self.width = width
        self.grid = []
        self.gap = width // ROWS
        for i in range(width):
            self.grid.append([])
            for j in range(width):
                cell = Cell(i, j, self.gap, ROWS)
                self.grid[i].append(cell)

    def add_obstacle(self, row, col):
        # 3x3 cell
        # 1 1 1 Entrance based on face
        # default false

        # 2 2 2
        # 1 1 1
        # 1 0 1
        # 1 1 1

        # 0 = obstacle
        # 1 = clearance
        # 2 = entrance
        pass

    def remove_obstacle(self, row, col):
        pass

    def rotate_obstacle(self, row, col):
        pass

    def draw(self, win):
        win.fill(WHITE)

        for row in self.grid:
            for cell in row:
                cell.draw(win)

        for i in range(ROWS):
            pygame.draw.line(win, GREY, (0, i * self.gap), (self.width, i * self.gap))
            for j in range(ROWS):
                pygame.draw.line(
                    win, GREY, (j * self.gap, 0), (j * self.gap, self.width)
                )

        pygame.display.update()


def main(window, width):
    arena = Arena(width)

    run = True
    while run:
        arena.draw(window)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                run = False

    pygame.quit()


main(WINDOW, WIDTH)
