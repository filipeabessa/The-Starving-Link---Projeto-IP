import pygame

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    '''Método para fazer a lista de imagens
    def make_image_list(self, image, num_positions):
        image_positions = pygame.image.load(image)'''
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
        # Velocidade no eixo Y
        self.speedy = 0

    def update(self):
        # A velocidade sempre será 0 para mover apenas quando uma tecla for pressionada
        self.speedx = 0
        self.speedy = 0
        # Armazena uma lista com as teclas que estão pressionadas
        keystate = pygame.key.get_pressed()
        # Condicionais para mover o player de acordo com a tecla pressionada
        if keystate[pygame.K_a]:
            self.speedx = -7
        if keystate[pygame.K_d]:
            self.speedx = 7
        if keystate[pygame.K_w]:
            self.speedy = -7
        if keystate[pygame.K_s]:
            self.speedy = 7
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
    # Recebe o sprite e retorna uma tupla com as coordenadas dele
    def coordenadas(self):
        return (self.rect.x, self.rect.y)