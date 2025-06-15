import pygame
from cruzadinha.answers import check_answer
from cruzadinha.grid import find_block
from cruzadinha.settings import *

def handle_mouse_down(pos, grid, completed_blocks):
    mouse_x, mouse_y = pos
    if mouse_x >= GRID_WIDTH:
        return None, None
    row = mouse_y // CELL_SIZE
    col = mouse_x // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS and grid[row][col] == 1:
        block = find_block(row, col)
        if (row, block[0]) not in completed_blocks:
            return row, block
    return None, None

def handle_key_down(event, selected_row, selected_block, cell_letters, completed_blocks):
    if selected_row is None or selected_block is None:
        return selected_row, selected_block

    if (selected_row, selected_block[0]) in completed_blocks:
        return selected_row, selected_block

    start_col, end_col = selected_block

    if event.key == pygame.K_SPACE:
        for c in range(start_col, end_col + 1):
            if cell_letters[selected_row][c] == '':
                cell_letters[selected_row][c] = '-'
                break
    elif event.unicode.isalpha() and len(event.unicode) == 1:
        for c in range(start_col, end_col + 1):
            if cell_letters[selected_row][c] == '':
                cell_letters[selected_row][c] = event.unicode.upper()
                break
    elif event.key == pygame.K_BACKSPACE:
        for c in range(end_col, start_col - 1, -1):
            if cell_letters[selected_row][c] != '':
                cell_letters[selected_row][c] = ''
                break

    # Verifica resposta correta
    if check_answer(selected_row, selected_block, cell_letters):
        completed_blocks.add((selected_row, selected_block[0]))
        return None, None

    return selected_row, selected_block
