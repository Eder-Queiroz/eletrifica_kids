import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Fase5:
    def __init__(self, tela_surface=None):
        """Inicializa a fase do eletroduto."""
        self.tela_surface = tela_surface
        if tela_surface:
            self.largura, self.altura = 1280, 800
        else:
            self.largura, self.altura = 1280, 800

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        # Carregar imagens
        self.interruptor = pygame.image.load("./eletroduto/assets/interruptor.png")
        self.lampada = pygame.image.load("./eletroduto/assets/lampada.png")
        self.tomada = pygame.image.load("./eletroduto/assets/tomada.png")

    def atualizar(self, eventos):
        """Atualiza o estado do jogo com base nos eventos."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                from tela_inicial import TelaInicial
                return TelaInicial(pygame.display.get_surface())

            # Inclua aqui a lógica de eventos do jogo eletroduto

        return None

    def desenhar(self, tela):
        """Desenha todos os elementos da fase na tela."""
        # Preenche o fundo
        tela.fill("black")

        # Desenha os componentes
        tela.blit(self.interruptor, [100, 100])
        tela.blit(self.lampada, [0, 100])
        tela.blit(self.tomada, [100, 0])

        # Adiciona instrução para voltar ao menu
        fonte_voltar = pygame.font.SysFont(None, 24)
        texto_voltar = fonte_voltar.render("Pressione ESC para voltar ao menu", True, (255, 255, 255))
        tela.blit(texto_voltar, (10, 10))