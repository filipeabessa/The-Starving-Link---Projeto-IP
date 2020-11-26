import pygame
pygame.init()

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, color, width, height):
        # Chama o construtor do Sprite
        pygame.sprite.Sprite.__init__(self)

        # Cria a imagem de um bloco e adiciona a cor
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)

        # Cria um Rect com as dimensões do bloco
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = height/2

        # Velocidade no eixo X
        self.speedx = 0

    def update(self):
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx