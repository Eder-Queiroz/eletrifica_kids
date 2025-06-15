import pygame

from fase1 import Fase1
from fase3 import Fase3
from cruzadinha.fase4 import Fase4

class TelaInicial:
    def __init__(self, tela_surface):
        self.tela_surface = tela_surface
        self.largura, self.altura = tela_surface.get_size()
        self.fonte_titulo = pygame.font.Font(None, 64)
        self.fonte_opcoes = pygame.font.Font(None, 48)

        # Preparar textos
        self.titulo = self.fonte_titulo.render("Eletrifica Kids", True, (255, 255, 255))
        self.opcao1 = self.fonte_opcoes.render("1 - Condutores e Componentes", True, (255, 255, 255))
        self.opcao2 = self.fonte_opcoes.render("2 - Ligando os Circuitos", True, (255, 255, 255))
        self.opcao3 = self.fonte_opcoes.render("3 - Símbolos Elétricos", True, (255, 255, 255))
        self.opcao4 = self.fonte_opcoes.render("4 - Cruzadinha Elétrica", True, (255, 255, 255))

        self.instrucao = self.fonte_opcoes.render("Escolha um minijogo (1, 2, 3 ou 4)", True, (255, 255, 0))

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return Fase1(self.largura, self.altura)
                elif evento.key == pygame.K_2:
                    # Importação apenas quando necessária
                    from ligando_os_pontos.minigame import FaseLigandoOsPontos
                    return FaseLigandoOsPontos(self.tela_surface)
                elif evento.key == pygame.K_3:
                    return Fase3()
                elif evento.key == pygame.K_4:
                    return Fase4()
        return None

    def desenhar(self, tela):
        # Desenha fundo com gradiente
        for y in range(0, self.altura):
            cor = (0, max(0, 30-y//15), max(0, 60-y//10))
            pygame.draw.line(tela, cor, (0, y), (self.largura, y))

        # Posições dos textos
        tela.blit(self.titulo, (self.largura//2 - self.titulo.get_width()//2, 100))
        tela.blit(self.opcao1, (self.largura//2 - self.opcao1.get_width()//2, 300))
        tela.blit(self.opcao2, (self.largura//2 - self.opcao2.get_width()//2, 360))
        tela.blit(self.opcao3, (self.largura//2 - self.opcao3.get_width()//2, 420))
        tela.blit(self.opcao4, (self.largura//2 - self.opcao4.get_width()//2, 480))
        # Removendo a opção 5 da tela
        # tela.blit(self.opcao5, (self.largura//2 - self.opcao5.get_width()//2, 540))
        tela.blit(self.instrucao, (self.largura//2 - self.instrucao.get_width()//2, 620))