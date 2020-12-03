import pygame
import constants


class Menu:
    def __init__(self, game):
        # Menu recebe os atributos e métodos de game.py
        self.game = game

        # Display do menu iniciado
        self.run_display = True

        # Posição do texto "Start Game"
        self.startx = constants.DISPLAY_WIDTH / 2
        self.starty = constants.DISPLAY_HEIGHT / 2

        self.menu_img = pygame.image.load("./Images/start_img.png")

        self.font_zelda = "./Fonts/Ravenna.ttf"

    # Exibe o menu na tela
    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_if_game_started()
            self.game.window.blit(self.menu_img, (0, 0))
            # self.game.draw_text(
            #     "Main Menu", 30, constants.DISPLAY_WIDTH / 2, 50, self.menu_img
            # )
            self.game.draw_text(
                "START GAME",
                50,
                self.startx,
                self.starty + 200,
                self.menu_img,
                constants.RED,
                self.font_zelda,
            )
            self.game.draw_text(
                "Press ENTER",
                25,
                self.startx,
                self.starty + 250,
                self.menu_img,
                constants.RED,
                self.font_zelda,
            )
            pygame.display.update()

    # Checa se o enter foi apertado no menu, e se sim, self.playing é setado pra True e self.menu.run_display é setado para false, e assim o menu some da tela e o loop do jogo é iniciado
    def check_if_game_started(self):
        if self.game.start_key:
            self.run_display = False
            self.game.playing = True
