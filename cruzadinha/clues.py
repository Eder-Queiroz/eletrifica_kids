import pygame
from cruzadinha.settings import *

horizontal_clues = [
    "1. Dispositivo que interrompe a corrente = ?", "2. Condutor elétrico = ?",
    "3. Condutor de retorno = ?", "4. Unidade de tensão = ?",
    "5. Condutor que transporta energia = ?", "6. Caminho da corrente = ?",
    "7. ______ solar", "8. Dispositivo de proteção contra surtos = ?",
    "9. Tipo de lâmpada gasosa = ?", "10. Condutor de proteção = ?",
    "11. Unidade de potência", "12. Iluminação elétrica = ?",
    "13. Dois condutor juntos", "14. Corrente Continua",
    "15. Corrente Alternada", "16. Quadro de distribuição",
    "17. Suporte para iluminação", "18. Fator de Potência"
]

def draw_panel(screen):
    panel_rect = pygame.Rect(GRID_WIDTH, 0, PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, GREY, panel_rect)

    title = FONT.render("Dicas", True, BLACK)
    screen.blit(title, (GRID_WIDTH + 20, 20))

    h_title = SMALL_FONT.render("Horizontal", True, BLACK)
    screen.blit(h_title, (GRID_WIDTH + 20, 60))

    for i, clue in enumerate(horizontal_clues):
        text = SMALL_FONT.render(clue, True, BLACK)
        screen.blit(text, (GRID_WIDTH + 20, 80 + i * 20))
