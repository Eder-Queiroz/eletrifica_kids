import pygame

from ligando_os_pontos.minigame import FaseLigandoOsPontos
from fase1 import Fase1
from fase3 import Fase3
from tela_inicial import TelaInicial


class GerenciadorDeCenas:
    def __init__(self):
        self.cena_atual = None

    def mudar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    # Atualizar eventos na tela
    def atualizar(self, eventos):
        if self.cena_atual:
            nova_cena = self.cena_atual.atualizar(eventos)
            if nova_cena:
                self.mudar_cena(nova_cena)

    def desenhar(self, tela):
        if self.cena_atual:
            self.cena_atual.desenhar(tela)


# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((1280, 800))
# tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
largura, altura = tela.get_size()
pygame.display.set_caption("Eletrifica Kids")
clock = pygame.time.Clock()

# Gerenciador de cenas
gerenciador = GerenciadorDeCenas()
gerenciador.mudar_cena(TelaInicial(tela))

rodando = True
while rodando:
    # recebendo eventos na tela
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    gerenciador.atualizar(eventos)
    tela.fill((0, 0, 0))  # Fundo preto
    gerenciador.desenhar(tela)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()