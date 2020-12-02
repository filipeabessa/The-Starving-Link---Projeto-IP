import pygame

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.centerx > 800 or self.rect.bottom > 684 or self.rect.centerx < 0:
            self.kill()

