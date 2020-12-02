import pygame


class Hunger:
    """Classe para gerenciar a fome do player. Para usar-la é necessário criar e guarda um objeto
    da classe quando o jogo começar e chamar a função \'update\' no loop principal do jogo"""

    # Variáveis para que a barra que será mostrada na UI
    BAR_POS_X = 770
    BAR_POS_Y = 350
    BAR_WIDDTH = 20
    BAR_HEIGHT = 200

    def __init__(self, screen, curr_hungry=100, starve_time=20):
        """Construtor da classe, recebe como parâmetros a tela do jogo o valor atual da fome, o
        tempo para  o player morrer de fome com a barra cheia em segundos"""
        self._max_hungry = (
            100  # O limite do valor da fome é 100 para facilitar os cálculos
        )
        self._curr_hungry = curr_hungry  # Valor da fome atual
        self._hungry_decay = (
            self._max_hungry / starve_time
        )  # Quanto de fome decai a cada segundo
        self.screen = screen  # A tela do jogo

    @property
    def curr_hungry(self):  # Getter do curr_hungry
        """O valor atual da fome do player"""
        return self._curr_hungry

    def feed(self, value: float):
        """Soma o valor atual da fome com o parâmetro, respeitando o valor máximo que
        esse pode chegar"""
        if (
            self._curr_hungry + value < self._max_hungry
        ):  # Se a soma for menor que o máximo, faça-a
            self._curr_hungry += value
        else:  # Se a soma for maior que o máximo, usa-se o valor máximo da barra para _curr_hungry
            self._curr_hungry = self._max_hungry

    def decay(self, value: float):
        """Decaí o valor atual da fome, chamando o game over caso essa chegue a 0"""
        if self._curr_hungry - value > 0:  # Se a subtração for maior que zero, faça-a
            self._curr_hungry -= value
        else:  # Se a fome chegar a zero ou menos, chama o game over
            self._curr_hungry = 0
            # TODO: call player Game Over

    def show_hunger_bar(self):
        """Plota a barra de fome na tela com a fome atual"""
        modifier = self.BAR_HEIGHT - self.BAR_HEIGHT * self.curr_hungry / 100  #
        pygame.draw.rect(self.screen, (75, 50, 50), self._get_bar_rect())  # background
        pygame.draw.rect(
            self.screen, (0, 250, 0), self._get_bar_rect(modifier)
        )  # barra
        pygame.draw.rect(self.screen, (150, 75, 0), self._get_bar_rect(), 1)  # bordas
        pygame.display.flip()  # Mostra as barras na tela

    @classmethod  # Método estático
    def _get_bar_rect(cls, y_modifier=0):
        """Retorna o rect padrão da barra, caso nada seja passado como parâmetro, ou uma barra
        reduzida em y_modifier unidades no eixo y caso algum parametro seja passado"""
        return pygame.Rect(
            cls.BAR_POS_X,
            cls.BAR_POS_Y + y_modifier,
            cls.BAR_WIDDTH,
            cls.BAR_HEIGHT - y_modifier,
        )

    def update(self, delta_time):
        """Realiza o decaimento por segundo da fome. Necessita receber o tempo passado desde o
        último frame (o valor que retorna de Clock.tick())"""

        self.decay(
            (delta_time * self._hungry_decay) / 1000
        )  # Faz o decaimento ser fixo por segundo
        self.show_hunger_bar()  # Plota a barra na tela
