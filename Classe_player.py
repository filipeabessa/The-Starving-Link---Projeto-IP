import pygame

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

        # Vidas do player
        self.lives = 5
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.lives_img = pygame.image.load("8bitheart.png")
        self.dead = False

    def update(self):
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()

    def draw_lives(self, screen, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x
            img_rect.y = y + 30 * i
            screen.blit(img, img_rect)
    
    def lose_life(self):
        self.lives = self.lives - 1
        if self.lives == 0:
            self.dead = True
    
    def gain_life(self):
        if self.lives < 5:
            self.lives = self.lives - 1
