import pygame
import constants


class Game_over:
    def __init__(self, game):
        # Menu recebe os atributos e métodos de game.py
        self.game = game

        # é setado para True quando o loop do jogo para
        self.run_display = False

        self.game_over_img = pygame.image.load("./Images/game_over.png")
        self.font_game_over = "./Fonts/Triforce.ttf"
        self.font_retry = "./Fonts/Ravenna.ttf"

    # Exibe a tela de Game Over
    def display_game_over(self):
        if self.run_display:
            self.game.window.fill(constants.BLACK)
            self.game.window.blit(self.game.window, (0, 0))
            self.game.draw_text(
                "Game Over",
                100,
                constants.DISPLAY_WIDTH / 2,
                (constants.DISPLAY_HEIGHT / 2) - 100,
                self.game.window,
                constants.RED,
                self.font_game_over,
            )
            self.game.draw_text(
                "press SPACE to retry",
                20,
                constants.DISPLAY_WIDTH / 2,
                constants.DISPLAY_HEIGHT / 2 - 30,
                self.game.window,
                constants.RED,
                self.font_retry,
            )
            pygame.display.update()

    def game_over(self):
        self.display_game_over()
        self.game.retry()
