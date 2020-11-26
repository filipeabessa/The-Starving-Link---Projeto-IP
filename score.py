import pygame

class Score:

    def __init__(self, surface, score, x, y):
        #--Class Attributes--
        #Score position
        self.x = x
        self.y = y

        #Score value
        self.score_str = str(score)
        
        self.surface = surface

        #Draw score on the screen
        self.draw_score()
    

    def draw_score(self):
        #Font format
        font_name = pygame.font.match_font('arial')
        #Font size
        size = 18
        font = pygame.font.Font(font_name, size)

        text_surface = font.render(self.score_str, True, (255, 255, 255))

        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        
        self.surface.blit(text_surface, text_rect)
 
    def update(self, new_score):
        self.score_str = str(new_score)
        self.draw_score()