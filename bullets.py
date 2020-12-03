import pygame

# Cria a classe para o objeto que serão as flechas
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha() # Carrega a imagem que for passada como parâmetro
        self.rect = self.image.get_rect() # Faz um rect da imagem
        self.rect.bottom = y # A coordenada y da qual a flecha vai sair, que é recebida como parâmetro
        self.rect.centerx = x # A coordenada x da qual a flecha vai sair, que é recebida como parâmetro
        self.speedx = speedx # Velocidade no eixo x
        self.speedy = speedy # velocidade no eixo y (ambas as velocidades são recebidas como parâmetros)

    # Método para mudar a imagem da flecha
    def update(self):
        self.rect.y += self.speedy # Muda a posição no eixo y com base na velocidade
        self.rect.x += self.speedx # Muda a posição no eixo x com base na velocidade
        # Condicional para verificar se a flecha saiu da tela
        # Caso a flecha tenha saído, dá um kill nela
        if self.rect.bottom < 0 or self.rect.centerx > 800 or self.rect.bottom > 684 or self.rect.centerx < 0:
            self.kill()

