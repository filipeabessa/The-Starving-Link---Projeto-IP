import pygame
from random import randint
from math import sqrt
from os import path
from food import Food
from score import Score
from pygame.sprite import Sprite
from Characters_atributtes import Classe_player


class Enemy(Sprite):
    """
    Classe do inimigo do jogo. Para usar-la, chame a função \"update\" no loop principal
    do jogo e passe a posição do player e a lista de óbstáculos como parâmetro
    """

    def __init__(self, x_pos, y_pos, screen, score, speed=5):
        Sprite.__init__(self)  # Chama o construtor da classe
        img_path = "./Images/enemy.png"  # Caminho para o sprite
        self._sprite = pygame.image.load(img_path).convert_alpha()  # Sprite sem o fundo
        self._direction = (0, 0)  # A direção a qual o inimigo vai seguir
        self._speed = speed  # A velocidade com o qual o inimigo se movimenta
        self._screen = screen  # A tela do jogo

        self.rect = (
            self._sprite.get_rect()
        )  # O Rect usado para a colisão e movimentação
        self.rect.x = x_pos
        self.rect.y = y_pos

        self._previous_pos = x_pos, y_pos  # Variável usada para facilitar o colisões
        self._is_dead = False  # Guarda se o inimigo ainda está vivo
        self.score = score

    @property
    def pos(self):
        """Tupla com a posição do inimigo"""
        return self.rect.x, self.rect.y

    def change_dir(self, x_dir: int = 0, y_dir: int = 0):
        """Muda a direção do imigo normalizando o vetor de sua direção para evitar que
        esse se mova mais rápido nas diagonais"""
        magnitude = sqrt(x_dir ** 2 + y_dir ** 2)  # Comprimento do vetor

        # Se o comprimento do vetor não for zero, aplique a direção normalizada
        if magnitude != 0:
            self._direction = (x_dir / magnitude, y_dir / magnitude)
        else:
            self._direction = 0, 0

    def _move(self, obstacles):
        """Movimenta o inimigo de acordo com sua direção e lidando com colisões"""
        self._previous_pos = self.rect.x, self.rect.y  # Guarda a posição atual

        # Movimenta o inimgo pelo seu Rect, considerando sua direção e velocidade
        mov_vector = self._direction[0] * self._speed, self._direction[1] * self._speed
        self.rect.move_ip(mov_vector)

        # Desconsidera o objeto como obstáculo para que esse não colida com si mesmo
        obs = obstacles.copy()
        if self.rect in obs:
            obs.remove(self.rect)

        # Se colidir com algo no movimento, volta à posição anterior
        if self.rect.collidelist(obs) != -1:
            self.rect.x = self._previous_pos[0]
            self.rect.y = self._previous_pos[1]

    def die(self, enemy_list, food_list):
        """Desabilita a função update e têm 30% de chance de dropar um item, sendo
        66% de chance de ser uma comida e 33% de ser um buff"""
        if self._is_dead:
            return  # Se o inimigo já está morto, retorne

        self._is_dead = True  # Marca o inimigo como morto
        rand = randint(1, 10)  # Gera um int aleatório entre 1 a 10
        enemy_list.remove(self)  # Remove o inimigo da lista para remover-lo do jogo

        # Se o num for 10, dropa um buff; se for 8 ou 9, dropa comida; senão, nada dropa
        if rand > 7:
            food_list.append(Food("", self.pos[0], self.pos[1], self._screen, True))
        self.score.increase_score()

    def update(self, player_pos: tuple, obstacles: list, enemy_list, food_list):
        """Se o inimigo estiver vivo, atualiza seu sprite na tela e o move em direção
        ao player'. Recebe a posição do player, uma lista de óbstaculos e a lista de
        inimigos."""

        # Se o inimigo for atingido por uma bala, faça o inimigo morrer e destrua a bala
        for arrow in Classe_player.bullets:
            if self.rect.colliderect(arrow.rect):
                arrow.kill()
                self.die(enemy_list, food_list)

        if self._is_dead:  # Se não está morto, move e mostra o inimigo na tela
            return

        # Faz o inimigo se mover em direção ao player passando o vetor resultante
        # entre a diferença de suas posições
        vector = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        self.change_dir(vector[0], vector[1])
        self._move(obstacles)

        # Atualiza o sprite do inimigo na tela
        self._screen.blit(self._sprite, (self.rect.x, self.rect.y))