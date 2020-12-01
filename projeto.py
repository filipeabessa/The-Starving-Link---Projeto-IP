import pygame
from hunger import Hunger
from Classe_player import Player
from score import Score
from food import Food

pygame.init()
screen_width = 800
screen_height = 684
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)

player = Player(BLACK, screen_width, screen_height)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
score = Score(gameDisplay, 0, screen_width - 40, 20)
hunger = Hunger(gameDisplay)

indoor_hirule = pygame.image.load("hirule.png")

x = screen_width / 2
y = screen_height / 2

dead = False

while not dead:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

    gameDisplay.blit(indoor_hirule, (0, 0))
    all_sprites.update()
    all_sprites.draw(gameDisplay)
    score.update(0)
    hunger.update(dt)
    pygame.display.update()
    pygame.display.flip()
    


pygame.quit()
quit()
