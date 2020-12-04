import pygame


class Spritesheet(pygame.sprite.Sprite):
    """Cria a classe da imagem usada para a animação"""

    def __init__(self, filename):
        # Carrega o arquivo cujo nome é passado quando um objeto for criado
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, pos_x, pos_y, width, height):
        """Define um método para cortar as imagens de cada frame
        a partir de uma imagem com todos os frames"""
        image = pygame.Surface(
            (width, height)
        )  # Cria a superfície na qual a imagem vai ser desenhada
        # Corta cada imagem de acordo com o tamanho passado
        image.blit(self.spritesheet, (0, 0), (pos_x, pos_y, width, height))
        # Diminui a escala da imagem
        image = pygame.transform.scale(image, (width // 2, height // 2))
        # Faz a cor preta (0, 0, 0) ser transparente
        image.set_colorkey((0, 0, 0))
        return image  # Retorna a imagem cortada
