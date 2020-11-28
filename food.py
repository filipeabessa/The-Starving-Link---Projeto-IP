from random import randint
import pygame

# Food dictionary with health points for the constructor
# TODO: Edit food list with final values
food_list = {
    'apple': {'points': 5, 'color': (255,0,0)},
    'cheese': {'points': 10, 'color': (255,255,0)},
    'egg': {'points': 20, 'color': (255,255,255)},
    'chicken': {'points': 40, 'color': (235,200,178) },
}


# Food class
class Food:

    # Constructor
    def __init__(self, name, x_pos, y_pos, screen):
        global food_list

        if name not in food_list.keys():
            name = 'apple'
        
        self._name = name
        self._points = food_list[name]['points']
        self._caught = False

        if x_pos >= 0:
            self._x_pos = x_pos
        else:
            self._x_pos = 0


        if y_pos >= 0:
            self._y_pos = y_pos
        else:
            self._y_pos = 0

        self.screen = screen
        self.sprite = pygame.Surface((10,10)) # PLACEHOLDER

    # Getters
    @property
    def name(self):
        return self._name
    
    @property
    def points(self):
        return self._points

    @property
    def caught(self):
        return self._caught

    @property
    def x_pos(self):
        return self._x_pos

    @property
    def y_pos(self):
        return self._y_pos

    def get_coords(self):
        return self.x_pos, self.y_pos

    # Setters
    def grab(self):
        self._caught = True

    # Function for testing
    def to_string(self):
        result = 'Food name: ' + self.name + '\n'
        result += 'Health points: ' + str(self.points) + '\n'

        if self.caught:
            result += 'Item in inventory!'
        else:
            result += 'Position: (' + str(self.x_pos) + ', ' + str(self.y_pos) + ')\n'

        return result

    @classmethod 
    def random_spawn(cls,colliders:list, screen_w, screen_h, screen):
        '''Spawna uma comida aleatóriia em uma posição aleatória da tela que não esteja ocupada.
        Recebe uma lista com os objetos os quais ela não deve ser instanciada em cima, a largura e
        a altura da tela e a própria tela.'''
        sp_pos = (0,0) # Posição onde a comida será instanciada
        valid_pos = False # Variável para checar se a posição está ocupada por uma parede ou obst.

        while not valid_pos: # Enquanto a pos não for valida, gere uma nova, sempre múltipla de 10
            sp_pos = randint(0,screen_w//10)*10 ,randint(0,screen_h//10)*10 # A posição da comida
            test_rect = pygame.Rect(sp_pos[0],sp_pos[1],10,10) # Rect para testar se vai colidir
            valid_pos = test_rect.collidelist(colliders) == -1 #Se não bater em nada, a pos é válida
#           print(f"valid_pos = {valid_pos}| pos = {sp_pos}| test = {test_rect.collidelist(colliders)}")

        return Food(cls.get_random_food(), sp_pos[0], sp_pos[1], screen) # Retorna a comida spawnada

    @classmethod
    def get_random_food(cls):
        '''Retorna uma string com o nome de uma comida no dicionário das comidas'''
        f_list = [*food_list] # Lista com as chaves do dicionário(nome das comidas)
        index = randint(0,len(f_list)-1) # Pega um index aleatório da lista acima
        return f_list[index] # Retorna o nome de uma comida com base no index aleatório

    def update(self):
        '''Mantém o sprite da comida  na tela'''
        # Por enquanto, estou usando quadrados como Placeholder
        self.sprite.fill(food_list[self.name]['color']) # Pinta o quadrado da cor da comida
        self.screen.blit(self.sprite,self.get_coords()) # Coloca o sprite na tela
