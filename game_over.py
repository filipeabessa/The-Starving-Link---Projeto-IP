import pygame
import constants

class Game_over():
    def __init__(self, game):

        self.game = game
        # Menu recebe os atributos e métodos de game.py

        # é setado para True quando o loop do jogo para
        self.run_display = False

    # Exibe a tela de Game Over
    def display_game_over(self):
        self.game.game_display.fill(constants.BLACK)
        self.game.draw_text("Game Over", 50, constants.DISPLAY_WIDTH/2, constants.DISPLAY_HEIGHT/2)
        self.game.window.blit(self.game.game_display, (0, 0))
        pygame.display.update()

