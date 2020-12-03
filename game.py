import pygame
from menu import *
from hunger import Hunger
from Classe_player import Player, all_sprites
from spritesheet import Spritesheet
from score import Score
from food import Food
from game_over import Game_over
from bullets import Bullets
from enemy import Enemy
from items_count import Items_count
from os import path
from scenario import Scenario
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

        # Imagem do cenário do jogo
        self.scenario_img = pygame.image.load("hirule3.png")

        # Cria instâncias das classes

        self.score = Score(self.window, 0)
        self.hunger = Hunger(self.window)
        self.menu = Menu(self)
        self.game_over = Game_over(self)
        self.scenario = Scenario()
        self.spritesheet = Spritesheet("positions_link.gif")
        self.player = Player(
            constants.BLACK, self.hunger, self, self.game_over, self.scenario
        )

        self.enemies = [Enemy(700, 600, 5, self.window)]  # Lista de inimigos na tela
        self.food_list = []  # Lista de comidas na tela

        # Contadores de itens pegos
        self.breads_caught = 100
        self.apples_caught = 100
        self.chickens_caught = 100
        self.game_score = 0

        # Dicionario com os icones das comidas
        self.food_images = {
            "apple": (pygame.image.load(path.join("", "Apple.png")).convert_alpha()),
            "bread": (pygame.image.load(path.join("", "Bread.png")).convert_alpha()),
            "chicken": (
                pygame.image.load(path.join("", "Chicken.png")).convert_alpha()
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

    # Método do loop do jogo. (Esse código antes ficava no projeto.py)
    def game_loop(self):

        if self.menu.run_display:
            # Checa se o jogo foi fechado ou se o enter foi apertado
            self.check_events()
            # Checa se o enter foi apertado no menu, e se sim, self.playing é setado pra True e self.menu.run_display é setado para false,
            # e assim o menu some da tela e o loop do jogo é iniciado
            self.menu.check_if_game_started()
        if self.playing:
            hunger = Hunger(self.window)
            Food.start_spawn()  # Inicia o spawn de comidas
            while not self.player.dead:

                dt = self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.player.dead = True
                        self.running = False
                        self.playing = False
                        self.menu.run_display = False
                    if (
                        event.type == Food.FOOD_SPAWN_EVENT
                    ):  # Spawna uma comida caso o evento seja chamado
                        Food.random_spawn(
                            [],
                            constants.DISPLAY_WIDTH,
                            constants.DISPLAY_HEIGHT,
                            self.window,
                        )
                self.player.shoot()
                self.player.check_hunger()
                self.player.check_lives()
                self.display_game(dt)
                pygame.draw.rect(
                    self.window, constants.BLACK, self.scenario.statue_left
                )

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
            self.window.blit(self.scenario_img, (0, 0))
            # Player mostrado na tela
            self.player.update(dt)
            # Score mostrado na tela
            self.score.update(0)
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

            all_sprites.update()
            # Atualiza a imagem de todas as comidas
            for food in self.food_list:
                food.update()
            # Atualiza o inimigo
            for enemy in self.enemies:
                enemy.update(self.player.coordenadas(), [] + self.enemies)
            all_sprites.draw(self.window)
            pygame.display.update()

    def retry(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over.run_display = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.hunger._curr_hungry = 100
                    self.player.lives = 5
                    self.player.dead = False
                    self.playing = True
                    self.run_game_display = True
                    self.game_over.run_display = False

                    self.player.rect.centerx = constants.DISPLAY_WIDTH / 2
                    self.player.rect.bottom = constants.DISPLAY_HEIGHT / 2

                    # TODO mandar o player pro centro da tela
                    # TODO fazer os inimigos sumirem da tela
