import pygame
pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Faz a tela aparecer
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sistema interativo')
clock = pygame.time.Clock()

# Cria a classe do player
class Player(pygame.sprite.Sprite):
    # Construtor
    def __init__(self):
        # Chama o construtor do Sprite
        pygame.sprite.Sprite.__init__(self)

        # Cria a imagem de um bloco e adiciona a cor
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)

        # Cria um Rect com as dimensões do bloco
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10

        # Velocidade no eixo X
        self.speedx = 0

    def update(self):
        # Mover o rect de acordo com a velocidade
        self.rect.x += self.speedx

# Cria um grupo com todos os sprites
all_sprites = pygame.sprite.Group()
# Usa a classe do player para fazer um objeto
player = Player()
# Adiciona player a all_sprites
all_sprites.add(player)


# Loop com as ações do jogo
while True:
    # Mantém uma deteminada taxa de fps
    clock.tick(FPS)

    # Verifica para eventos e os processa
    for event in pygame.event.get():
        # Verifica se é para fechar a janela
        if event.type == pygame.QUIT:
            pygame.quit()

    # Update
    all_sprites.update()

    # Desenha na tela
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Só mostra a tela depois de desenhar tudo
    pygame.display.flip()
    
    pygame.display.update()