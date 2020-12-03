import pygame
import constants


class Score:
    def __init__(self, surface, game):
        # --Class Attributes--
        self.game = game

        self.score = 0
        # Score value
        self.score_str = str(self.score)

        self.surface = surface

        # Fonte do score
        self.font = pygame.font.match_font("arial")

    def increase_score(self):
        self.score += 1

    def update(self):
        self.score_str = str(self.score)
        self.game.draw_text(
            f"Score: {self.score_str} ",
            20,
            constants.SCORE_POS_X,
            constants.SCORE_POS_Y,
            self.game.window,
            constants.RED,
            self.font,
        )