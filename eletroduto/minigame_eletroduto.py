import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MinigameEletroduto:
    def __init__(self, screen, clock):
        self.clock = clock
        self.screen = screen
        self.running = True
        self.fps = 60
        self.interruptor = pygame.image.load("./eletroduto/assets/interruptor.png")
        self.lampada = pygame.image.load("./eletroduto/assets/lampada.png")
        self.tomada = pygame.image.load("./eletroduto/assets/tomada.png")

    def play(self):
        while self.running:
            # poll for events
            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER YOUR GAME HERE
            self.screen.blit(self.interruptor, [100, 100])
            self.screen.blit(self.lampada, [0, 100])
            self.screen.blit(self.tomada, [100, 0])

            # Adiciona texto ESC para sair
            fonte_voltar = pygame.font.SysFont(None, 24)
            texto_voltar = fonte_voltar.render("Pressione ESC para sair", True, (255, 255, 255))
            self.screen.blit(texto_voltar, (10, 10))

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(self.fps)  # limits FPS to 60