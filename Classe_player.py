import pygame
from bullets import Bullets

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

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
        # Velocidade no eixo Y
        self.speedy = 0

        # Delay para atirar uma flecha
        self.delay_shoot = 300
        # Variável para medir o tempo
        self.timer = 0

    # Recebe o sprite e retorna uma tupla com as coordenadas dele
    def coordenadas(self):
        return (self.rect.x, self.rect.y)
    
    def update(self, dt=0):
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

        if self.timer > 0:
            self.timer = self.timer - dt
        
    
    def shoot(self):
        if self.timer > 0:
            return
        keystate = pygame.key.get_pressed()
        direction = [0, 0]
        speed = 15
        imagem = ""
        pos_x = 0
        pos_y = 0
        if keystate[pygame.K_UP]:
            direction[1] = -1
            imagem = "Arrow_up.png"
            pos_x = self.rect.centerx
            pos_y = self.rect.top
        if keystate[pygame.K_RIGHT]:
            direction[0] = 1
            imagem = "Arrow_right.png"
            pos_x = self.rect.right
            pos_y = self.rect.centery    
        if keystate[pygame.K_LEFT]:
            direction[0] = -1
            imagem = "Arrow_left.png"
            pos_x = self.rect.left
            pos_y = self.rect.centery
        if keystate[pygame.K_DOWN]:
            direction[1] = 1
            imagem = "Arrow_down.png"
            pos_x = self.rect.centerx
            pos_y = self.rect.bottom

        if direction != [0, 0]:
            bullet = Bullets(pos_x, pos_y, direction[0]*speed, direction[1]*speed, imagem)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.timer = self.delay_shoot