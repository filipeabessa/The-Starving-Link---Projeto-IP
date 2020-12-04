from itertools import chain
from math import sqrt
import pygame
from Characters_atributtes import arrow_projectile
import constants

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, hunger, game, game_over, scenario):

        self.game_over = game_over
        self.game = game
        self.hunger = hunger

        # Chama o construtor do Sprite
        pygame.sprite.Sprite.__init__(self)

        # Chama o método make_sprite_list() para fazer uma lista das imagens que vão ser usadas
        self.list_images = self.make_image_list(32, 100, 100)

        self.last_update = (
            0  # Cria um atributo para marcar o tempo desde o último update chamado
        )
        self.current_frame = (
            0  # Marca o frame atual, para que seja possível saber qual posição usar
        )
        self.walking = False  # Booleano para saber se o player está se movimentando
        self.chosen_player_img = (
            0  # Atributo que vai ser usado na escolha da imagem mostrada
        )

        # Cria um Rect com as dimensões do bloco do Player
        self.image = self.list_images[0]
        #
        self.player_img = self.image

        self.player_rect = self.image.get_rect()
        self.player_rect.centerx = constants.DISPLAY_HEIGHT / 2
        self.player_rect.bottom = constants.DISPLAY_WIDTH / 2

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
        self.lives_img = pygame.image.load("./Images/8bitheart.png")
        self.lives_empty_img = pygame.image.load("./Images/8bitheartempty.png")

        # Se o player perder uma vida, vai ser mudado para True, para os enemies não conseguirem atacar por algum tempo
        self.invincible = False
        self.invincible_timer = pygame.time.get_ticks()

        # Player inicialmente não está morto
        self.dead = False

        self.scenario = scenario

        # Player atingido por inimigo
        self.damaged = False

        # Som ao atirar flecha
        self.arrow_shot_sound = pygame.mixer.Sound("./Sounds/arrow_shot.wav")

        # Som ao ganhar uma vida
        self.gain_life_sound = pygame.mixer.Sound("./Sounds/heart_beat.wav")

        # Som ao perder vida
        self.lose_life_sound = pygame.mixer.Sound("./Sounds/stab.wav")

        # Inicialização de damage_alpha
        self.damage_alpha = 0

    def hit(self):
        """
        A função hit é chamada quando o player é atingido. Ela executa
        um efeito de som, diminui a quantidade de vidas pra zero e torna o player invisível
        """
        self.lose_life_sound.play()
        self.lives = self.lives - 1
        self.invincible = True
        self.damaged = True
        self.damage_alpha = chain(constants.DAMAGE_ALPHA * 4)

    def update(self, food_list, game, delta_time=0):
        # Para funcionar do jeito certo, o update precisa mudar o atributo de andar para false,
        # de modo que seja possível chamar a função para mudar as imagens várias vezes
        self.walking = False
        # A velocidade sempre será 0 para mover apenas quando uma tecla for pressionada
        self.speedx = 0
        self.speedy = 0
        # Armazena uma lista com as teclas que estão pressionadas
        keystate = pygame.key.get_pressed()
        # Condicionais para mover o player de acordo com a tecla pressionada
        if keystate[pygame.K_a]:
            if self.player_rect.x > constants.SCENARIO_WALKING_LIMIT_LEFT:
                if not self.player_rect.colliderect(self.scenario.statue_left):
                    self.speedx = -7
                    self.walking = True
                    # Só vai ser true se o player estiver andando (em qualquer direção)
                    self.chosen_player_img = 2
            # O valor para achar o frame correto dessa imagem é 2
            # Ele tem o mesmo significado nas outras condicionais
        if keystate[pygame.K_d]:
            if self.player_rect.x < constants.SCENARIO_WALKING_LIMIT_RIGHT:
                if not self.player_rect.colliderect(self.scenario.statue_right):
                    self.speedx = 7
                    self.walking = True
                    self.chosen_player_img = 0
        if keystate[pygame.K_w]:
            if self.player_rect.y > constants.SCENARIO_WALKING_LIMIT_TOP:
                if (not self.player_rect.colliderect(self.scenario.statue_left)) and (
                    not self.player_rect.colliderect(self.scenario.statue_right)
                ):
                    self.speedy = -7
                    self.walking = True
                    self.chosen_player_img = 3
        if keystate[pygame.K_s]:
            if self.player_rect.y < constants.SCENARIO_WALKING_LIMIT_DOWN:
                self.speedy = 7
                self.walking = True
                self.chosen_player_img = 1
        # Chama o método animate() passando como parâmetro o
        # self.chosen_player_img, para poder achar o frame correto
        self.animate(self.chosen_player_img)

        # Normalização da velocidade
        magnitude = (self.speedx ** 2 + self.speedy ** 2) ** 0.5
        if magnitude != 0:
            speed_vec = (self.speedx / magnitude * 7, self.speedy / magnitude * 7)
        else:
            speed_vec = 0, 0

        # Mover o rect de acordo com a velocidade
        self.player_rect.x += speed_vec[0]
        self.player_rect.y += speed_vec[1]

        if self.timer > 0:
            self.timer = self.timer - delta_time

        for food in food_list:
            if food.rect.colliderect(self.player_rect):
                if food.name == "apple":
                    game.apples_caught += 1
                if food.name == "bread":
                    game.breads_caught += 1
                if food.name == "chicken":
                    game.chickens_caught += 1

                self.hunger.feed(food.points)
                food_list.remove(food)

        # self.breads_caught = 0
        # self.apples_caught = 0
        # self.chickens_caught = 0

        # Se o player estiver invencível há um segundo, o player deixar de ser invencivel
        # if self.invincible and pygame.time.get_ticks() - self.invincible_timer > 1000:
        #    self.invincible = False

        # Blit do player
        self.game.window.blit(self.image, self.coordenadas())

        self.image = self.player_img.copy()

        if self.damaged:
            try:
                if self.speedy == 0 and self.speedx == 0:
                    next(self.damage_alpha)
                else:
                    self.image.fill(
                        (0, 0, 0, next(self.damage_alpha)),
                        special_flags=pygame.BLEND_RGBA_MULT,
                    )
            except:
                self.invincible = False
                self.damaged = False

    # Define método para fazer uma lista de imagens a partir de uma imagem passada como atributo
    # em self.game.spritesheet
    def make_image_list(self, number_positions, image_width, image_height):
        image_list = []
        # Loop for que itera x vezes, onde x é o número de imagens que forem passadas
        for image_number in range(number_positions):
            # Chama o método get_image() da classe Spritesheet, o qual retorna uma imagem por vez
            position = self.game.spritesheet.get_image(
                image_number * image_width, 0, image_width, image_height
            )
            image_list.append(position)
        return image_list

    # Define o método para animar o player passando o n da posição como parâmetro
    def animate(self, n):
        # Armazena o número de ticks do clock desde a última vez que o método foi chamado
        now = pygame.time.get_ticks()
        # Só vai entrar no if se o player estiver andando
        if self.walking:
            # Só vai mudar a imagem mostrada se o tempo passado entre a última chamada do método
            # e a chamada atual dor maior que 60 ms
            if (now - self.last_update) > 60:
                self.last_update = (
                    now  # Armazena o tempo em que a função está sendo chamada
                )
                # ((self.current_frame+1)%8) vai resultar em um número de 0 a 8,
                # já que cada posição do Link (cima, baixo, direita e esquerda)
                # tem 8 imagens. n*8 vai usar o n passado em update para "escolher"
                # a posição a ser mostrada (cima é 3, baixo é 1, direita é 0 e
                # esquerda é 2). Isso dá os números múltiplos de 8 até 24, que,
                # somados ao outro número, # resultam em todos os números de 0 a 31
                self.current_frame = n * 8 + ((self.current_frame + 1) % 8)
                # Escolhe a imagem a ser mostrada com base na posição e no frame determinados
                self.image = self.list_images[self.current_frame]
                self.player_img = self.image.copy()

    def draw_lives(self, screen, lives, img):
        # Desenha vidas na tela
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = constants.LIVES_POS_X
            img_rect.y = constants.LIVES_POS_Y + 30 * i
            screen.blit(img, img_rect)

        for i in range(self.lives_limit - lives):
            img_rect = img.get_rect()
            img_rect.x = constants.LIVES_POS_X
            img_rect.y = constants.LIVES_POS_Y + 30 * (i + lives)
            screen.blit(self.lives_empty_img, img_rect)

    # Remove a vida em 1 quando o método é chamado.
    # Se a quantidade de vidas vai de 1 para 0, o player morre
    def lose_life(self):
        self.lose_life_sound.play()
        self.lives = self.lives - 1
        self.make_invicible()

    # Uma vida é adicionada quando o método é chamado, se o player tem menos que o limite de vidas
    def gain_life(self):
        if self.lives < self.lives_limit:
            self.gain_life_sound.play()
            self.lives = self.lives + 1

    # Faz player ficar invencível
    """ def make_invincible(self):

        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks() """

    # Se a fome chegar em 0, o player morre
    def check_hunger(self):
        if self.hunger.curr_hungry == 0:
            self.player_died()

    # Se a quantidade de vidas chegar em 0, o player morre
    def check_lives(self):
        if self.lives == 0:
            self.player_died()

    # Função faz o jogador morrer e muda valores dos booleanos para que a tela de game over apareça
    def player_died(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./Sounds/the_giants_theme.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.dead = True
        self.game.playing = False
        self.game.run_game_display = False
        self.game_over.run_display = True
        all_sprites.empty()

    # Recebe o sprite e retorna uma tupla com as coordenadas do player
    def coordenadas(self):
        return (self.player_rect.x, self.player_rect.y)

    # Define método para atirar flechas
    def shoot(self):
        if self.timer > 0:
            return

        # Armazena uma lista de booleanos com as teclas que estão pressionadas
        keystate = pygame.key.get_pressed()
        direction = [0, 0]  # "Tupla" com o vetor direção inicial
        speed = 10  # Velocidade da flecha
        imagem = ""
        pos_x = 0  # Posição no eixo x de onde a flecha vai sair
        pos_y = 0  # Posição no eixo y de onde a flecha vai sair
        # Condicionais para verificar se as setas direcionais estão pressionadas
        if keystate[pygame.K_UP]:
            self.arrow_shot_sound.set_volume(0.6)
            self.arrow_shot_sound.play()
            direction[1] = -1  # Muda o valor do vetor direção no eixo y
            imagem = "./Images/Arrow_up.png"
            # Escolhe a imagem a ser mostrada (válido para os outros if's)
            pos_x = (
                self.player_rect.centerx
            )  # Define a posição da flecha se atirada para cima
            pos_y = (
                self.player_rect.top
            )  # Define a posição da flecha se atirada para cima
        if keystate[pygame.K_RIGHT]:
            self.arrow_shot_sound.set_volume(0.6)
            self.arrow_shot_sound.play()
            direction[0] = 1
            imagem = "./Images/Arrow_right.png"
            pos_x = (
                self.player_rect.right
            )  # Define a posição da flecha se atirada para a direita
            pos_y = (
                self.player_rect.centery
            )  # Define a posição da flecha se atirada para a direita
        if keystate[pygame.K_LEFT]:
            self.arrow_shot_sound.set_volume(0.6)
            self.arrow_shot_sound.play()
            direction[0] = -1
            imagem = "./Images/Arrow_left.png"
            pos_x = (
                self.player_rect.left
            )  # Define a posição da flecha se atirada para a esquerda
            pos_y = (
                self.player_rect.centery
            )  # Define a posição da flecha se atirada para a esquerda
        if keystate[pygame.K_DOWN]:
            self.arrow_shot_sound.set_volume(0.6)
            self.arrow_shot_sound.play()
            direction[1] = 1
            imagem = "./Images/Arrow_down.png"
            pos_x = (
                self.player_rect.centerx
            )  # Define a posição da flecha se atirada para baixo
            pos_y = (
                self.player_rect.bottom
            )  # Define a posição da flecha se atirada para baixo

        # Só permite atirar se o vetor for diferente de [0, 0],
        # ou seja, se alguma seta for pressionada
        if direction != [0, 0]:
            magnitude = sqrt(direction[0] ** 2 + direction[1] ** 2)
            # Cria a classe da flecha
            bullet = arrow_projectile.Bullets(
                pos_x,
                pos_y,
                (direction[0] * speed) / magnitude,
                (direction[1] * speed) / magnitude,
                imagem,
            )
            all_sprites.add(bullet)  # Adiciona o objeto a um grupo com todos os sprites
            bullets.add(bullet)  # Adiciona o objeto a um grupo só das flechas
            # Só permite atirar se o cooldown já tiver resetado
            self.timer = self.delay_shoot
