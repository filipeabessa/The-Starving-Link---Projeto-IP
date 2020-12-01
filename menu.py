import pygame
import constants

class Menu():
    def __init__(self, game):
        # Menu recebe os atributos e métodos de game.py
        self.game = game

        # Display do menu iniciado
        self.run_display = True
        self.startx, self.starty = constants.DISPLAY_WIDTH / 2, constants.DISPLAY_HEIGHT / 2

    def blit_screen(self):
        self.game.window.blit(self.game.game_display, (0, 0))
        pygame.display.update()
        self.game.reset_game()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.game_display.fill(constants.BLACK)
            self.game.draw_text('Main Menu', 30, constants.DISPLAY_WIDTH / 2, 50)
            self.game.draw_text("Start Game", 25, self.startx, self.starty)
            self.game.draw_text("Press ENTER!", 15, self.startx, self.starty + 50)
            self.blit_screen()

    def check_input(self):
        if self.game.start_key:
            # Jogo é iniciado
            self.game.playing = True
            # Menu para de aparecer
            self.run_display = False