import pygame
from settings import *

grid = [
    [0,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,0,1,1,1,1,1],
    [1,1,1,1,1,0,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1],
    [1,1,0,1,1,0,1,1,1,0],
    [1,1,1,1,1,0,0,1,1,1],
]

references = {
    (0, 1): 1,
    (1, 0): 2,
    (1, 4): 3,
    (2, 0): 4,
    (2, 6): 5,
    (3, 1): 6,
    (4, 0): 7,
    (4, 7): 8,
    (5, 0): 9,
    (5, 5): 10,
    (6, 0): 11,
    (6, 6): 12,
    (7, 1): 13,
    (8, 0): 14,
    (8, 3): 15,
    (8, 6): 16,
    (9, 0): 17,
    (9, 7): 18
}

def find_block(row, col):
    start = col
    while start > 0 and grid[row][start -1] == 1:
        start -= 1
    end = col
    while end < COLS -1 and grid[row][end + 1] == 1:
        end += 1
    return (start, end)

def draw_grid(screen, cell_letters, selected_row, selected_block, completed_blocks):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if grid[row][col] == 0:
                pygame.draw.rect(screen, BLOCKED, rect)
            else:
                in_completed_block = any(
                    row == br and br_start <= col <= br_end
                    for (br, br_start) in completed_blocks
                    for br_end in [find_block(br, br_start)[1]]
                )

                if in_completed_block:
                    pygame.draw.rect(screen, CORRECT_COLOR, rect)
                elif selected_row == row and selected_block and selected_block[0] <= col <= selected_block[1]:
                    pygame.draw.rect(screen, HIGHLIGHT, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)

                pygame.draw.rect(screen, BLACK, rect, 1)

                if (row, col) in references:
                    num = references[(row, col)]
                    text = SMALL_FONT.render(str(num), True, BLACK)
                    screen.blit(text, (x + 3, y + 3))

                if cell_letters[row][col]:
                    letter_text = FONT.render(cell_letters[row][col], True, BLACK)
                    screen.blit(letter_text, (x + CELL_SIZE//2 - 8, y + CELL_SIZE//2 - 12))
