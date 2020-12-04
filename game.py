from os import path
import pygame
from Characters_atributtes import enemy_spawner, hunger, player_class, sprite_sheet
from Objectives import score, food, items_count
from Screen_related import game_over, menu, scenario
import constants


class Game:
    """Classe do jogo, onde serão definidos os métodos e onde
    serão instanciados os objetos utilizados no loop, junto a seus métodos e atributos"""

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

        self.score = score.Score(self.window, self)
        self.hunger = hunger.Hunger(self.window)
        self.menu = menu.Menu(self)
        self.game_over = game_over.Game_over(self)
        self.scenario = scenario.Scenario()
        self.spritesheet = sprite_sheet.Spritesheet("./Images/positions_link.gif")
        self.player = player_class.Player(
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

        self.apples_count = items_count.Items_count(
            self.window,
            0,
            constants.APPLES_COUNT_POS_X,
            constants.APPLES_COUNT_POS_Y,
            self.food_images["apple"],
        )
        self.breads_count = items_count.Items_count(
            self.window,
            0,
            constants.BREADS_COUNT_POS_X,
            constants.BREADS_COUNT_POS_Y,
            self.food_images["bread"],
        )
        self.chickens_count = items_count.Items_count(
            self.window,
            0,
            constants.CHICKENS_COUNT_POS_X,
            constants.CHICKENS_COUNT_POS_Y,
            self.food_images["chicken"],
        )

        self.vidas_ganhas = 0

    def game_loop(self):
        """Método do loop do jogo, que será chamado na main para executar o jogo."""
        if self.menu.run_display:
            # Checa se o jogo foi fechado ou se o enter foi apertado
            self.check_events()
            # Checa se o enter foi apertado no menu, e se sim, self.playing
            # é setado pra True e self.menu.run_display é setado para false,
            # e assim o menu some da tela e o loop do jogo é iniciado
            self.menu.check_if_game_started()
        if self.playing:
            pygame.mixer.music.load("./Sounds/dark_sarias_song.ogg")
            pygame.mixer.music.play(-1)
            food.Food.start_spawn()  # Inicia o spawn de comidas
            first_frame = True
            while not self.player.dead:
                # Controla o delta_time
                delta_time = self.clock.tick(40)
                if first_frame:
                    delta_time = 0
                    first_frame = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.player.dead = True
                        self.running = False
                        self.playing = False
                        self.menu.run_display = False

                    # Spawna uma comida caso o evento de spawn seja chamado
                    if event.type == food.Food.FOOD_SPAWN_EVENT:
                        self.food_list.append(
                            food.Food.random_spawn(
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
                self.display_game(delta_time)
                self.enemy_spawners.update(delta_time, self.enemies, self.window)

    def check_events(self):
        """Checa se o jogo foi fechado ou se o enter foi apertado"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True
                    self.run_game_display = True

    def draw_text(self, text, size, pos_x, pos_y, display, text_color, font):
        """Escreve um texto na tela"""
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        display.blit(text_surface, text_rect)

    def display_game(self, delta_time):
        """Renderiza tudo que é necessário para o jogo"""
        if self.run_game_display:
            # Cenário mostrado na tela
            self.window.blit(self.scenario.scenario_img, (0, 0))
            # Player mostrado na tela
            self.player.update(self.food_list, self, delta_time)
            # Score mostrado na tela
            self.score.update()
            # Barra de fome mostrado na tela
            self.hunger.update(delta_time)
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

            player_class.all_sprites.update()
            # Atualiza a imagem de todas as comidas
            for single_food in self.food_list:
                single_food.update()
            # Atualiza o inimigo
            for enemy in self.enemies:
                enemy.update(
                    self.player.coordenadas(),
                    [] + self.enemies,
                    self.enemies,
                    self.food_list,
                )
            player_class.all_sprites.draw(self.window)
            pygame.display.update()

            for arrow in player_class.bullets:
                bullets_surface = pygame.Surface((arrow.rect.width, arrow.rect.height))
                bullets_surface.fill((255, 0, 0))
                self.window.blit(bullets_surface, (arrow.rect.x, arrow.rect.y))

    def retry(self):
        """Reinicia o jogo, zerando todos os pontos acumulados, fazendo as flechas e
        os inimigos sumirem do mapa e movendo o player para o centro"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over.run_display = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.enemy_spawners.reset_timer()
                    self.hunger.curr_hungry = 100
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

    def check_colission(self):
        """Checa colisão"""
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
