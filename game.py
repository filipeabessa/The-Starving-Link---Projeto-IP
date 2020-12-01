import pygame
from menu import *
from hunger import Hunger
from Classe_player import Player
from score import Score
from food import Food
import constants
class Game():
    def __init__(self):
        pygame.init()
        # Atributo booleano que recebe a informação se o jogo está rodando
        self.running = True
        # Atributo booleano que recebe a informação se o jogo está sendo jogado
        self.playing = False

        # Inicialmente o jogador não está morto
        self.dead = False
        
        # Tecla de iniciar o jogo ainda não foi apertada
        self.start_key = False

        self.game_display = pygame.Surface((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT))

        # Nome do jogo mostrado no topo da programa
        self.caption = pygame.display.set_caption(constants.GAME_CAPTION)

        # Clock do jogo
        self.clock = pygame.time.Clock()

        # Tela do jogo
        self.window = pygame.display.set_mode(((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)))

        # Fonte padrão do pygame para usar na start menu
        self.font_name = pygame.font.get_default_font()

        # Imagem do cenário do jogo
        self.scenario_img = pygame.image.load("hirule.png")

        self.player = Player(constants.BLACK, constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)
        self.score = Score(self.window, 0, constants.DISPLAY_WIDTH - 20, 20)
        self.hunger = Hunger(self.window)
        self.menu = Menu(self)

    # Método do loop do jogo. (Esse código antes ficava no projeto.py)
    def game_loop(self):
        while self.running:
            self.check_events()
            self.menu.check_input()

            if self.playing:
                while not self.dead:
                    dt = self.clock.tick(60)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.dead = True
                            self.running, self.playing = False, False
                            self.menu.run_display = False

                    self.window.blit(self.scenario_img, (0, 0))
                    self.player.update()
                    self.score.update(0)
                    self.hunger.update(dt)
                    pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True

    def reset_game(self):
        self.start_key= False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_display.blit(text_surface, text_rect)
