import pygame
import constants


class Scenario:
    def __init__(self):

        self.statue_left = pygame.Rect(
            constants.RECT_STATUE_LEFT_POS_X,
            constants.RECT_STATUE_LEFT_POS_Y,
            constants.STATUES_WIDTH,
            constants.STATUES_HEIGHT,
        )
        self.statue_right = pygame.Rect(
            constants.RECT_STATUE_RIGHT_POS_X,
            constants.RECT_STATUE_RIGHT_POS_Y,
            constants.STATUES_WIDTH,
            constants.STATUES_HEIGHT,
        )
        # Imagem do cenário do jogo
        self.scenario_img = pygame.image.load("./Images/hyrule3.png")
