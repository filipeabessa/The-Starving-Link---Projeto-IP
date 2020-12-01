import pygame
from menu import *
from hunger import Hunger
from Classe_player import Player
from score import Score
from food import Food
from game_over import Game_over
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
        self.run_game_display = False

        # Fonte padrão do pygame para usar na start menu
        self.font_name = pygame.font.get_default_font()

        # Imagem do cenário do jogo
        self.scenario_img = pygame.image.load("hirule.png")

        # Cria instâncias das classes
        
        self.score = Score(self.window, 0, constants.DISPLAY_WIDTH - 20, 20)
        self.hunger = Hunger(self.window)
        self.player = Player(constants.BLACK, constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT, self.hunger, self)
        self.menu = Menu(self)
        self.game_over = Game_over(self)


    # Método do loop do jogo. (Esse código antes ficava no projeto.py)
    def game_loop(self):


        # Checa se o jogo foi fechado ou se o enter foi apertado
        self.check_events() 
        # Checa se o enter foi apertado no menu, e se sim, self.playing é setado pra True e self.menu.run_display é setado para false,
        # e assim o menu some da tela e o loop do jogo é iniciado
        self.menu.check_if_game_started()
        if self.playing:
            while not self.dead:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.dead = True
                        self.running = False
                        self.playing = False
                        self.menu.run_display = False
                self.player.check_hunger()
                self.player.check_lives()
                self.display_game()
                
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

    # Escreve na tela
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game_display.blit(text_surface, text_rect)
    
    def display_game(self):
        if self.display_game:
            # Cenário mostrado na tela
            self.window.blit(self.scenario_img, (0, 0))
            # Player mostrado na tela
            self.player.update()
            # Score mostrado na tela
            self.score.update(0)
            # Barra de fome mostrado na tela
            self.hunger.update(self.clock.tick(60))
            # Mostrar vidas na tela
            self.player.draw_lives(self.window, constants.HUNGER_LIVES_X, constants.LIVES_Y, self.player.lives, self.player.lives_img)
            pygame.display.update()



