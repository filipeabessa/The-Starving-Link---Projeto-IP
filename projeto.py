from game import Game
from game_over import Game_over
import pygame

pygame.init()

game = Game()

while game.running:
    game.menu.display_menu()
    game.game_loop()
    game.game_over.game_over()
