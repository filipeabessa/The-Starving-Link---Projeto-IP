import pygame

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, color, width, height, hunger, game):

        self.game = game

        self.hunger = hunger

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

        # Se o player perder uma vida, vai ser mudado para True, para os enemies não conseguirem atacar por algum tempo
        self.invincible = False
        self.invincible_timer = pygame.time.get_ticks()
        
        # Player inicialmente não está morto
        self.dead = False

    def update(self):
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx

        # Se o player estiver invencível há um segundo, o player deixar de ser invencivel
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > 1000:
            self.invincible = False

    def draw_lives(self, screen, x, y, lives, img):
        # Desenha vidas na tela
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x
            img_rect.y = y + 30 * i
            screen.blit(img, img_rect)

    # Remove a vida em 1 quando o método é chamado. Se a quantidade de vidas vai de 1 para 0, o player morre
    def lose_life(self):
        self.lives = self.lives - 1
        self.make_invicible()

    # Uma vida é adicionada quando o método é chamado, se o player tem menos que o limite de vidas
    def gain_life(self):
        if self.lives < self.lives_limit:
            self.lives = self.lives + 1

    # Faz player ficar invencível
    def make_invincible(self):

        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()
    
    def check_hunger(self):
        if self.hunger._curr_hungry == 0:
            self.player_died()
    
    def check_lives(self):
        if self.lives == 0:
            self.player_died()

    def player_died(self):
        self.game.dead = True
        self.game.playing = False
        self.game.run_game_display = False
