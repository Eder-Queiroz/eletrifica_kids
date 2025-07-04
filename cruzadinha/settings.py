import pygame

WIDTH, HEIGHT = 1280, 800
GRID_WIDTH = int(WIDTH * 0.7)
PANEL_WIDTH = WIDTH - GRID_WIDTH

ROWS, COLS = 10, 10
CELL_SIZE = GRID_WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
BLOCKED = (100, 100, 100)
HIGHLIGHT = (173, 216, 230)
CORRECT_COLOR = (144, 238, 144)
WRONG_COLOR = (255, 182, 193)

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)
SMALL_FONT = pygame.font.SysFont('Arial', 14)
