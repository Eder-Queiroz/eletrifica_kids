import pygame

from ligando_os_pontos.minigame import FaseLigandoOsPontos


class TelaInicial:
    def __init__(self, tela_surface):
        self.tela_surface = tela_surface
        self.fonte = pygame.font.Font(None, 48)
        self.texto = self.fonte.render(
            "Pressione ESPAÇO para começar", True, (255, 255, 255)
        )

    # Colocar quaquer interação do usuario com o jogo aqui para ser carregado na tela
    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return FaseLigandoOsPontos(self.tela_surface)  # Transição para a Fase1
            return None
        return None

    def desenhar(self, tela):
        tela.blit(self.texto, (150, 250))  # Exibe o texto na tela
