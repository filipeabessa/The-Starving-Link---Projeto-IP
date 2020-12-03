import pygame
from bullets import Bullets
from os import path
from itertools import chain
import constants

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, color, hunger, game, game_over):

        self.game_over = game_over
        self.game = game
        self.hunger = hunger

        # Chama o construtor do Sprite
        pygame.sprite.Sprite.__init__(self)

        # Cria a imagem de um bloco e adiciona a cor
        img_path = path.join(
            path.dirname(__file__), "link_front.png"
        )  # Caminho para o sprite
        self.image = pygame.image.load(img_path).convert_alpha()  # Sprite sem o fundo
        self.player_img = pygame.image.load(img_path).convert_alpha()
        # self.image = pygame.Surface((30, 50))
        # self.image.fill(color)

        # Cria um Rect com as dimensões do bloco
        self.rect = self.image.get_rect()
        self.rect.centerx = constants.DISPLAY_HEIGHT / 2
        self.rect.bottom = constants.DISPLAY_WIDTH / 2

        # Velocidade no eixo X
        self.speedx = 0
        # Velocidade no eixo Y
        self.speedy = 0

        # Delay para atirar uma flecha
        self.delay_shoot = 300
        # Variável para medir o tempo
        self.timer = 0

        # Vidas do player
        self.lives = 5
        self.lives_limit = 5
        self.lives_img = pygame.image.load("8bitheart.png")

        # Se o player perder uma vida, vai ser mudado para True, para os enemies não conseguirem atacar por algum tempo
        self.invincible = False
        self.invincible_timer = pygame.time.get_ticks()

        # Player inicialmente não está morto
        self.dead = False

        # Player atingido por inimigo
        self.damaged = False

    def hit(self):
        self.invincible = True
        self.damaged = True
        self.damage_alpha = chain(constants.DAMAGE_ALPHA * 3)

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
        self.image = self.player_img.copy()
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)

            except:
                self.invincible = False
                self.damaged = False

        # Se o player estiver invencível há um segundo, o player deixar de ser invencivel
        #if self.invincible and pygame.time.get_ticks() - self.invincible_timer > 1000:
        #   self.invincible = False

        # Blit do player
        self.game.window.blit(self.image, self.coordenadas())

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

    # Se a fome chegar em 0, o player morre
    def check_hunger(self):
        if self.hunger._curr_hungry == 0:
            self.player_died()

    # Se a quantidade de vidas chegar em 0, o player morre
    def check_lives(self):
        if self.lives == 0:
            self.player_died()

    # Função faz o jogador morrer e muda valores dos booleanos para que a tela de game over apareça
    def player_died(self):
        self.dead = True
        self.game.playing = False
        self.game.run_game_display = False
        self.game_over.run_display = True
        all_sprites.empty()

    # Recebe o sprite e retorna uma tupla com as coordenadas dele
    def coordenadas(self):
        return (self.rect.x, self.rect.y)

    # Define método para atirar flechas
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
            bullet = Bullets(
                pos_x, pos_y, direction[0] * speed, direction[1] * speed, imagem
            )
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.timer = self.delay_shoot
