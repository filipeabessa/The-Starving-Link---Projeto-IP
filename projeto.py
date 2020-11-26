import pygame

pygame.init()
screen_width = 800
screen_height = 684
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle")
clock = pygame.time.Clock()


class thing_views:
    def __init__(self, front_view, back_view, right_view, left_view):
        self.front_view = pygame.image.load(front_view)
        self.back_view = back_view
        self.right_view = right_view
        self.left_view = left_view


# enemy_imgs = thing_views('', '', '', '')
player_imgs = thing_views('link_front2.png', '', '', '')
# floor_img = pygame.image.load('')
# food_img = pygame.image.load('')


def player(x, y):
    gameDisplay.blit(player_imgs.front_view, (x, y))


hirule_insight = pygame.image.load("hirule.png")


x = screen_width / 2
y = screen_height / 2

dead = False

while not dead:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

    gameDisplay.blit(hirule_insight, (0, 0))
    player(x, y)
    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
