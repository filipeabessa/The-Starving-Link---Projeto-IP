import pygame

class HungerSystem:
    '''Classe para gerenciar a fome do player'''

    HUNGER_DECAY_EVENT = pygame.USEREVENT # Evento chamado a cada segundo para reduzir a fome

    def __init__(self, curr_hungry = 100 , starve_time = 40):
        '''Construtor da classe, recebe o valor atual da fome e o tempo para o player morrer de fome
        com a barra cheia em segundos'''
        self._max_hungry = 100 # O limite do valor da fome é 100 para facilitar os cálculos
        self._curr_hungry = curr_hungry # Valor da fome atual
        self._hungry_decay = self._max_hungry/starve_time # Quanto de fome decai a cada segundo
        pygame.time.set_timer(HungerSystem.HUNGER_DECAY_EVENT, 1000)

    @property
    def curr_hungry(self): # Getter do curr_hungry
        '''O valor atual da fome do player'''
        return self._curr_hungry

    def feed(self, value: float):
        '''Soma o valor atual da fome com o parâmetro, respeitando o valor máximo que
        esse pode chegar'''
        if self._curr_hungry + value < self._max_hungry: # Se a soma for menor que o máximo, faça-a
            self._curr_hungry += value
        else: # Se a soma for maior que o máximo, usa-se o valor máximo da barra para _curr_hungry
            self._curr_hungry = self._max_hungry

    def decay(self, value: float):
        '''Decaí o valor atual da fome, chamando o game over caso essa chegue a 0'''
        if self._curr_hungry - value > 0: # Se a subtração for maior que zero, faça-a
            self._curr_hungry -= value
        else: # Se a fome chegar a zero ou menos, chama o game over
            self._curr_hungry = 0
            #TODO: call player Game Over

    def update(self, events):
        '''Realiza o decaimento por segundo da fome. Necessita receber os eventos
        do PyGame como parâmetro'''
        event_types = [event.type for event in events] # Todos os tipos de eventos chamados no frame

        # Se o evento da fome for chamado, decaia na taxa especificada em _hungry_decay
        if HungerSystem.HUNGER_DECAY_EVENT in event_types:
            self.decay(self._hungry_decay)
            #print(f"curr hungry: {self.curr_hungry}")
