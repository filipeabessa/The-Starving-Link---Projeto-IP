import pygame
from menu import *
from Characters_atributtes import hunger
from Characters_atributtes import (
    Classe_player,
)  # DONE       #Player, all_sprites, bullets
from Characters_atributtes import spritesheet  # DONE
from score import Score
from food import Food
from game_over import Game_over
from Characters_atributtes import projectile
from Characters_atributtes import enemy
from items_count import Items_count
from os import path
from scenario import Scenario
from Characters_atributtes import enemy_spawner
import constants


class Game:
    def __init__(self):

        # Atributo booleano que recebe a informação se o jogo está rodando
        self.running = True

        # Atributo booleano que recebe a informação se o jogo está sendo jogado
        self.playing = False

        # Tecla de iniciar o jogo ainda não foi apertada
        self.start_key = False

        self.game_display = pygame.Surface(
            (constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)
        )

        # Nome do jogo mostrado no topo da programa
        self.caption = pygame.display.set_caption(constants.GAME_CAPTION)

        # Clock do jogo
        self.clock = pygame.time.Clock()

        # Tela do jogo
        self.window = pygame.display.set_mode(
            ((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT))
        )
        self.run_game_display = False

        # Fonte padrão do pygame para usar na start menu
        self.font_name = pygame.font.get_default_font()

        # Cria instâncias das classes

        self.score = Score(self.window, self)
        self.hunger = hunger.Hunger(self.window)
        self.menu = Menu(self)
        self.game_over = Game_over(self)
        self.scenario = Scenario()
        self.spritesheet = spritesheet.Spritesheet("./Images/positions_link.gif")
        self.player = Classe_player.Player(
            self.hunger, self, self.game_over, self.scenario
        )

        self.enemy_spawners = enemy_spawner.EnemySpawner(
            [
                constants.ENEMY_1_POS,
                constants.ENEMY_2_POS,
                constants.ENEMY_3_POS,
                constants.ENEMY_4_POS,
            ],
            self.score,
        )

        self.enemies = []  # Lista de inimigos na tela
        self.food_list = []  # Lista de comidas na tela

        # Contadores de itens pegos
        self.breads_caught = 0
        self.apples_caught = 0
        self.chickens_caught = 0
        self.game_score = 0

        # Dicionario com os icones das comidas
        self.food_images = {
            "apple": (
                pygame.image.load(path.join("", "./Images/Apple.png")).convert_alpha()
            ),
            "bread": (
                pygame.image.load(path.join("", "./Images/Bread.png")).convert_alpha()
            ),
            "chicken": (
                pygame.image.load(path.join("", "./Images/Chicken.png")).convert_alpha()
            ),
        }

        self.apples_count = Items_count(
            self.window,
            0,
            constants.APPLES_COUNT_POS_X,
            constants.APPLES_COUNT_POS_Y,
            self.food_images["apple"],
        )
        self.breads_count = Items_count(
            self.window,
            0,
            constants.BREADS_COUNT_POS_X,
            constants.BREADS_COUNT_POS_Y,
            self.food_images["bread"],
        )
        self.chickens_count = Items_count(
            self.window,
            0,
            constants.CHICKENS_COUNT_POS_X,
            constants.CHICKENS_COUNT_POS_Y,
            self.food_images["chicken"],
        )

        self.vidas_ganhas = 0

    # Método do loop do jogo. (Esse código antes ficava no projeto.py)
    def game_loop(self):
        if self.menu.run_display:
            # Checa se o jogo foi fechado ou se o enter foi apertado
            self.check_events()
            # Checa se o enter foi apertado no menu, e se sim, self.playing é setado pra True e self.menu.run_display é setado para false,
            # e assim o menu some da tela e o loop do jogo é iniciado
            self.menu.check_if_game_started()
        if self.playing:
            music = pygame.mixer.music.load("./Sounds/dark_sarias_song.ogg")
            pygame.mixer.music.play(-1)
            Food.start_spawn()  # Inicia o spawn de comidas
            first_frame = True
            while not self.player.dead:
                # Controla o delta_time
                dt = self.clock.tick(40)
                if first_frame:
                    dt = 0
                    first_frame = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.player.dead = True
                        self.running = False
                        self.playing = False
                        self.menu.run_display = False

                    # Spawna uma comida caso o evento de spawn seja chamado
                    if event.type == Food.FOOD_SPAWN_EVENT:
                        self.food_list.append(
                            Food.random_spawn(
                                [],
                                constants.SCENARIO_WALKING_LIMIT_RIGHT,
                                constants.SCENARIO_WALKING_LIMIT_DOWN,
                                self.window,
                            )
                        )
                self.check_colission()
                self.check_score()
                self.player.shoot()
                self.player.check_hunger()
                self.player.check_lives()
                self.display_game(dt)
                self.enemy_spawners.update(dt, self.enemies, self.window)

    # Checa se o jogo foi fechado ou se o enter foi apertado
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True
                    self.run_game_display = True

    # Escreve na tela
    def draw_text(self, text, size, x, y, display, text_color, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        display.blit(text_surface, text_rect)

    def display_game(self, dt):
        if self.run_game_display:
            # Cenário mostrado na tela
            self.window.blit(self.scenario.scenario_img, (0, 0))
            # Player mostrado na tela
            self.player.update(self.food_list, self, dt)
            # Score mostrado na tela

            # self.draw_text(
            #     "Score:",
            #     20,
            #     constants.SCORE_POS_X,
            #     constants.SCORE_POS_Y,
            #     self.window,
            #     constants.RED,
            #     self.font_name,
            # )

            self.score.update()
            # Barra de fome mostrado na tela
            self.hunger.update(dt)
            # Mostrar vidas na tela
            self.player.draw_lives(
                self.window,
                self.player.lives,
                self.player.lives_img,
            )
            # Draw Items count
            self.apples_count.update(self.apples_caught)
            self.breads_count.update(self.breads_caught)
            self.chickens_count.update(self.chickens_caught)

            Classe_player.all_sprites.update()
            # Atualiza a imagem de todas as comidas
            for food in self.food_list:
                food.update()
            # Atualiza o inimigo
            for enemy in self.enemies:
                enemy.update(
                    self.player.coordenadas(),
                    [] + self.enemies,
                    self.enemies,
                    self.food_list,
                )
            Classe_player.all_sprites.draw(self.window)
            pygame.display.update()

            for arrow in Classe_player.bullets:
                s = pygame.Surface((arrow.rect.width, arrow.rect.height))
                s.fill((255, 0, 0))
                self.window.blit(s, (arrow.rect.x, arrow.rect.y))

    def retry(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over.run_display = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.enemy_spawners.reset_timer()
                    self.hunger._curr_hungry = 100
                    self.player.lives = 5
                    self.breads_caught = 0
                    self.apples_caught = 0
                    self.chickens_caught = 0
                    self.game_score = 0
                    self.player.dead = False
                    self.playing = True
                    self.run_game_display = True
                    self.game_over.run_display = False
                    self.food_list.clear()
                    self.enemies.clear()
                    self.player.damaged = False
                    self.player.invincible = False
                    self.score.score = 0

                    self.player.player_rect.centerx = constants.DISPLAY_WIDTH / 2
                    self.player.player_rect.bottom = constants.DISPLAY_HEIGHT / 2

                    # TODO fazer os inimigos sumirem da tela

    def check_colission(self):
        for enemy in self.enemies:
            if self.player.player_rect.colliderect(enemy):
                if not self.player.invincible:
                    self.player.hit()
                    self.player.draw_lives(
                        self.window, self.player.lives, self.player.lives_img
                    )

    def check_score(self):
        if self.score.score == (10 * (1 + self.vidas_ganhas)):
            self.vidas_ganhas += 1
            self.player.gain_life()
