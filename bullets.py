import pygame
from pygame import transform

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, image):
        pygame.sprite.Sprite.__init__(self)

        # Atribui a imagem da flecha e ajusta sua rotação
        rotation = self.get_rotation(speedx, speedy) 
        self.image = pygame.image.load(image).convert_alpha()
        self.image = transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

        self.speedx = speedx
        self.speedy = speedy

    def get_rotation(self, speedx, speedy):
        '''Retorna a angulação que a flecha deve receber para que seu sprite seja
        ajustado'''
        if speedx > 0:
            if speedy == 0:
                return 0
            elif speedy > 0:
                return 45
            else: #speedy < 0
                return 45

        if speedy > 0:
            if speedx == 0:
                return 0
            else: #speedx < 0
                return -45

        if speedx < 0:
            if speedy == 0:
                return 0
            elif speedy < 0:
                return -45

        if speedy < 0:
            return 0


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.centerx > 800 or self.rect.bottom > 684 or self.rect.centerx < 0:
            self.kill()

