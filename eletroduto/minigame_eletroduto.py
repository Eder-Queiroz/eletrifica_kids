import pygame

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
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER YOUR GAME HERE

            interruptor_rect = self.interruptor.get_rect()
            lampada_rect = self.lampada.get_rect()
            tomada_rect = self.tomada.get_rect()

            # self.screen.blit(self.interruptor, interruptor_rect)
            self.screen.blit(self.interruptor, [100, 100])
            # self.screen.blit(self.lampada, lampada_rect)
            self.screen.blit(self.lampada, [0, 100])
            # self.screen.blit(self.tomada, tomada_rect)
            self.screen.blit(self.tomada, [100, 0])

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(self.fps)  # limits FPS to 60
