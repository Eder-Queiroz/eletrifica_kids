import pygame
import sys
from cruzadinha.settings import *
from cruzadinha.grid import draw_grid, grid
from cruzadinha.clues import draw_panel
from cruzadinha.input_handler import handle_mouse_down, handle_key_down
from cruzadinha.answers import all_correct

class Fase4:
    def __init__(self, largura=None, altura=None):
        # Se dimensões não forem fornecidas, use as padrão do settings
        self.largura = largura or WIDTH
        self.altura = altura or HEIGHT

        self.cell_letters = [['' for _ in range(COLS)] for _ in range(ROWS)]
        self.selected_row = None
        self.selected_block = None
        self.completed_blocks = set()
        self.tela = None

    def desenhar(self, tela):
        """Desenha todos os elementos da cruzadinha na tela."""
        self.tela = tela
        tela.fill(WHITE)
        draw_grid(tela, self.cell_letters, self.selected_row, self.selected_block, self.completed_blocks)
        draw_panel(tela)

        # Adicionar instruções para voltar ao menu
        fonte_voltar = pygame.font.SysFont('Arial', 24)
        texto_voltar = fonte_voltar.render("Pressione ESC para voltar ao menu", True, BLACK)
        tela.blit(texto_voltar, (10, 10))

    def atualizar(self, eventos):
        """Atualiza o estado do jogo com base nos eventos."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                from tela_inicial import TelaInicial
                return TelaInicial(pygame.display.get_surface())

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.selected_row, self.selected_block = handle_mouse_down(
                    evento.pos, grid, self.completed_blocks)

            elif evento.type == pygame.KEYDOWN:
                self.selected_row, self.selected_block = handle_key_down(
                    evento, self.selected_row, self.selected_block,
                    self.cell_letters, self.completed_blocks)

                # Verificar se todas as respostas estão corretas
                if all_correct(self.cell_letters):
                    # Aqui você pode adicionar uma mensagem de vitória ou retornar à tela inicial
                    pass

        return None