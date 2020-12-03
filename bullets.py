import pygame
from pygame import transform

# Cria a classe para o objeto que serão as flechas
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, image):
        pygame.sprite.Sprite.__init__(self)
        # Atribui a imagem da flecha e ajusta sua rotação
        rotation = self.get_rotation(speedx, speedy)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()  # Faz um rect da imagem
        self.rect.bottom = (
            y  # A coordenada y da qual a flecha vai sair, que é recebida como parâmetro
        )
        self.rect.centerx = (
            x  # A coordenada x da qual a flecha vai sair, que é recebida como parâmetro
        )
        self.speedx = speedx  # Velocidade no eixo x
        self.speedy = speedy  # velocidade no eixo y (ambas as velocidades são recebidas como parâmetros)

    def get_rotation(self, speedx, speedy):
        """Retorna a angulação que a flecha deve receber para que seu sprite seja
        ajustado"""
        if speedx > 0:
            if speedy == 0:
                return 0
            elif speedy > 0:
                return 45
            else:  # speedy < 0
                return 45
        if speedy > 0:
            if speedx == 0:
                return 0
            else:  # speedx < 0
                return -45
        if speedx < 0:
            if speedy == 0:
                return 0
            elif speedy < 0:
                return -45
        if speedy < 0:
            return 0
        # Método para mudar a imagem da flecha

    def update(self):
        self.rect.y += self.speedy  # Muda a posição no eixo y com base na velocidade
        self.rect.x += self.speedx  # Muda a posição no eixo x com base na velocidade
        # Condicional para verificar se a flecha saiu da tela
        # Caso a flecha tenha saído, dá um kill nela
        if (
            self.rect.bottom < 0
            or self.rect.centerx > 800
            or self.rect.bottom > 684
            or self.rect.centerx < 0
        ):
            self.kill()
