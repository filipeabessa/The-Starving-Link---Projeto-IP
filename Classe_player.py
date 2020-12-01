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
        self.lives_limit = 5
        self.lives_img = pygame.image.load("8bitheart.png")
        
        # Player inicialmente não está morto
        self.dead = False

    def update(self):
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx

    def draw_lives(self, screen, x, y, lives, img):
        # Desenha vidas na tela
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x
            img_rect.y = y + 30 * i
            screen.blit(img, img_rect)
    
    def lose_life(self):
        # Remove a vida em 1 quando o método é chamado. Se a quantidade de vidas vai de 1 para 0, o player morre
        self.lives = self.lives - 1
        if self.lives == 0:
            self.dead = True
    
    def gain_life(self):
        # Uma vida é adicionada quando o método é chamado, se o player tem menos que o limite de vidas
        if self.lives < self.lives_limit:
            self.lives = self.lives + 1
