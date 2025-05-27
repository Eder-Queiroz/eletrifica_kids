import pygame
import sys
from settings import *
from grid import draw_grid, grid
from clues import draw_panel
from input_handler import handle_mouse_down, handle_key_down

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cruzadinha EletrificaKids")

    cell_letters = [['' for _ in range(COLS)] for _ in range(ROWS)]
    selected_row = None
    selected_block = None
    completed_blocks = set()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_row, selected_block = handle_mouse_down(event.pos, grid, completed_blocks)

            elif event.type == pygame.KEYDOWN:
                selected_row, selected_block = handle_key_down(
                    event, selected_row, selected_block, cell_letters, completed_blocks)

        screen.fill(WHITE)
        draw_grid(screen, cell_letters, selected_row, selected_block, completed_blocks)
        draw_panel(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
