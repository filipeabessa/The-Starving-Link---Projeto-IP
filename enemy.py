from random import randint
from math import sqrt
from os import path
import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    '''
    Classe do inimigo do jogo. Para usar-la, chame a função \"update\" no loop principal
    do jogo e passe a posição do player e a lista de óbstáculos como parâmetro
    '''

    def __init__(self, x_pos, y_pos, speed, screen):
        Sprite.__init__(self) # Chama o construtor da classe
        img_path = path.join(path.dirname(__file__),"enemy.png") # Caminho para o sprite
        self._sprite = pygame.image.load(img_path).convert_alpha() # Sprite sem o fundo
        self._direction = (0,0) # A direção a qual o inimigo vai seguir
        self._speed = speed # A velocidade com o qual o inimigo se movimenta
        self._screen = screen # A tela do jogo

        self._rect = self._sprite.get_rect() # O Rect usado para a colisão e movimentação
        self._rect.x = x_pos
        self._rect.y = y_pos

        self._previous_pos = x_pos,y_pos # Variável usada para facilitar o colisões
        self._is_dead = False # Guarda se o inimigo ainda está vivo

    @property
    def rect(self):
        return self._rect

    def change_dir(self, x_dir:int = 0, y_dir:int = 0):
        '''Muda a direção do imigo normalizando o vetor de sua direção para evitar que
        esse se mova mais rápido nas diagonais'''
        magnitude = sqrt(x_dir**2+y_dir**2) # Comprimento do vetor

        # Se o comprimento do vetor não for zero, aplique a direção normalizada
        if magnitude != 0:
            self.direction = (x_dir/magnitude, y_dir/magnitude)
        else:
            self.direction = 0,0

    def _move(self, obstacles):
        '''Movimenta o inimigo de acordo com sua direção e lidando com colisões'''
        self.previous_pos = self._rect.x, self._rect.y # Guarda a posição atual

        # Movimenta o inimgo pelo seu Rect, considerando sua direção e velocidade
        mov_vector = self.direction[0] * self._speed, self.direction[1]*self._speed
        self._rect.move_ip(mov_vector)

        # Desconsidera o objeto como obstáculo para que esse não colida com si mesmo
        obs = obstacles.copy()
        if self._rect in obs:
            obs.remove(self._rect)

        # Se colidir com algo no movimento, volta à posição anterior
        if self._rect.collidelist(obs) != -1:
            self._rect.x = self.previous_pos[0]
            self._rect.y = self.previous_pos[1]

    def die(self):
        ''' Desabilita a função update e têm 30% de chance de dropar um item, sendo
        66% de chance de ser uma comida e 33% de ser um buff'''
        if self._is_dead:
            return # Se o inimigo já está morto, retorne

        self._is_dead = True  # Marca o inimigo como morto
        rand = randint(1,10) # Gera um int aleatório entre 1 a 10
        # Se o num for 10, dropa um buff; se for 8 ou 9, dropa comida; senão, nada dropa
        if rand > 7:
            print(rand)
            if rand == 10:
                print("Buff")
                # TODO: dropa um buff
            else:
                print("Comida")
                #TODO: dropa uma comida


    def update(self, player_pos: tuple, obstacles:list):
        '''Se o inimigo estiver vivo, atualiza seu sprite na tela e o move em direção
        ao player'. Recebe a posição do player e uma lista de óbstaculos.'''
        if self._is_dead: # Se não está morto, move e mostra o inimigo na tela
            return

        # Faz o inimigo se mover em direção ao player passando o vetor resultante
        # entre a diferença de suas posições
        vector =  player_pos[0] - self._rect.x, player_pos[1] - self._rect.y
        self.change_dir(vector[0],vector[1])
        self._move(obstacles)

        # Atualiza o sprite do inimigo na tela
        self._screen.blit(self._sprite,(self._rect.x,self._rect.y))
