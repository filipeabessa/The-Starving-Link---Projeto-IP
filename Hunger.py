class HungerSystem:
    '''Classe para gerenciar a barra de fome do player'''

    def __init__(self, curr_hungry = 100 ,hungry_decay = 1):
        '''Construtor da classe, recebe o valor atual da fome e o decaimento dessa caso necessário'''
        self._max_hungry = 100 # O limite do valor da fome é 100 para facilitar os cálculos
        self._curr_hungry = curr_hungry # Valor da fome atual
        self._hungry_decay = hungry_decay # Quanto de fome decai a cada segundo

    @property
    def curr_hungry(self): # Getter do curr_hungry
        return self._curr_hungry

    def feed(self, value: int):
        '''Soma o valor atual da fosme com o passado como parâmetro, respeitando o máximo'''
        if self._curr_hungry + value < self._max_hungry: # Se a soma for menor que o máximo, faça-a
            self._curr_hungry += value
        else: # Se a soma for maior que o máximo, usa-se o valor máximo da barra para _curr_hungry
            self._curr_hungry = self._max_hungry

    def update(self, delta_time):
        '''Faz a fome decair à uma taxa fixa por segundo. Delta time é a quantidade de segundos
        passada desde o último frame.
        '''
        self._curr_hungry -= self._hungry_decay * (1/delta_time)

