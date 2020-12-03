import pygame
import constants


class Scenario:
    def __init__(self):

        self.statue_left = pygame.Rect(
            50,
            10,
            constants.SCENARIO_WALKING_LIMIT_LEFT,
            constants.SCENARIO_WALKING_LIMIT_TOP,
        )
        self.statue_right = pygame.Rect(
            50,
            50,
            constants.SCENARIO_WALKING_LIMIT_TOP,
            constants.SCENARIO_WALKING_LIMIT_RIGHT - 50,
        )
