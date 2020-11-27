import pygame

pygame.init()
screen_width = 800
screen_height = 684
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle")
clock = pygame.time.Clock()

indoor_hirule = pygame.image.load("hirule.png")

x = screen_width / 2
y = screen_height / 2

dead = False

while not dead:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

    gameDisplay.blit(indoor_hirule, (0, 0))
    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
