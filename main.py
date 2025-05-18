import pygame
from eletroduto.minigame_eletroduto import MinigameEletroduto

def main():
    print("Hello from eletrifica-kids!")

    pygame.init()
    # pygame.SCALED
    
    screen = pygame.display.set_mode((640, 360), pygame.RESIZABLE)
    pygame.display.set_caption("Eletrifica KIDS")

    clock = pygame.time.Clock()

    eletroduto = MinigameEletroduto(screen, clock)
    eletroduto.play()

    pygame.quit()

if __name__ == "__main__":
    main()
