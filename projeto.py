from game import Game
from game_over import Game_over

game = Game()
game_over = Game_over(game)

while game.running:
    game.menu.display_menu()
    game.game_loop()
    game_over.display_game_over()