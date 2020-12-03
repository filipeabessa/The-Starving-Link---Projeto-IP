import pygame
from Characters_atributtes import enemy


class EnemySpawner:
    """Classe para controlar o spawn dos dos inimigos."""

    SPAWN_DELAY = 60000  # Delay entre os spawns dos inimigos

    def __init__(self, spawners_pos: list):
        self._spawners_pos = spawners_pos  # A posição dos spawners
        self._timer = self.SPAWN_DELAY  # O timer que registrará o tempo decorrido

    @property
    def spawns_pos(self):
        """Lista com as posições onde os inimigos serão spawnados"""
        return self._spawners_pos

    def update(self, delta_time, enemy_list: list, screen):
        """Checa se deve spawnar os inimigos agora. Receber o tempo que se passou entre
        os frames (delta time), a lista de inimigos e a tela do jogo"""

        # Se o timer chegar à 0, spawne os inimigos, senão, decremente o timer
        if self._timer <= 0:
            self.spawn(enemy_list, screen)
        else:
            self._timer -= delta_time

    def spawn(self, enemy_list: list, screen):
        """Spawna os inimigos e reseta o timer. Precisa receber a lista de inimigos e a tela"""

        self.reset_timer()
        for spawn in self.spawns_pos:  # Spawne um inimigo em cada spawn
            enemy_list.append(enemy.Enemy(spawn[0], spawn[1], screen))

    def reset_timer(self):
        """Reseta o timer"""
        self._timer = self.SPAWN_DELAY  # Faz com que o timer seja igual ao delay
