import pygame


class Items_count:
    def __init__(self, surface, number, x, y, image):
        # --Class Attributes--
        # Score position
        self.x = x
        self.y = y

        # Number of items
        self.value_str = str(number)

        self.surface = surface

        # Item image
        self.image = image
        # self.image.set_colorkey((255,255,255))
        self.draw_item_count()

    def draw_item_count(self):
        # Font format
        font_name = pygame.font.match_font("arial")
        # Font size
        size = 18
        font = pygame.font.Font(font_name, size)

        text_surface = font.render((self.value_str + " x"), True, (255, 255, 255))

        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)

        self.surface.blit(text_surface, text_rect)

        # Resize image
        img = pygame.transform.scale(self.image, (18, 20))
        # Draw the item icon
        self.surface.blit(img, [self.x + 25, self.y])

    def update(self, value):
        self.value_str = str(value)
        self.draw_item_count()