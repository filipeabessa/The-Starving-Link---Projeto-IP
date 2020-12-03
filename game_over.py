import pygame
import constants


class Game_over:
    def __init__(self, game):
        # Menu recebe os atributos e métodos de game.py
        self.game = game

        # é setado para True quando o loop do jogo para
        self.run_display = False

        self.game_over_img = pygame.image.load("game_over.png")
        self.font_zelda = "Ravenna.ttf"

    # Exibe a tela de Game Over
    def display_game_over(self):
        if self.run_display:
            self.game.window.blit(self.game_over_img, (0, 0))
            self.game.draw_text(
                "Game Over",
                80,
                constants.DISPLAY_WIDTH / 2,
                (constants.DISPLAY_HEIGHT / 2) - 100,
                self.game_over_img,
                constants.RED,
                self.font_zelda,
            )
            self.game.draw_text(
                "press SPACE to retry",
                20,
                constants.DISPLAY_WIDTH / 2,
                constants.DISPLAY_HEIGHT / 2 - 50,
                self.game_over_img,
                constants.RED,
                self.font_zelda,
            )
            pygame.display.update()

    def game_over(self):
        self.display_game_over()
        self.game.retry()
