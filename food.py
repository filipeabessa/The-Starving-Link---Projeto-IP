from random import randint, choice
from os import path
import pygame
import constants

# Food dictionary with health points for the constructor
# TODO: Edit food list with final values
food_list = {
    "apple": {
        "points": 40,
        "sprite": (pygame.image.load(path.join("", "./Images/Apple.png"))),
    },
    "bread": {
        "points": 60,
        "sprite": (pygame.image.load(path.join("", "./Images/Bread.png"))),
    },
    "chicken": {
        "points": 80,
        "sprite": (pygame.image.load(path.join("", "./Images/Chicken.png"))),
    },
}

# Food class
class Food:

    SPAWN_DELAY = 10000  # Delay entre os spawns de comida
    FOOD_SPAWN_EVENT = pygame.USEREVENT  # Evento para gerar a comida

    # Constructor
    def __init__(self, name, x_pos, y_pos, screen, random_food=False):
        global food_list

        if name not in food_list.keys():
            self._name = "apple"

        if random_food:  # Se random_food == True, escolha uma comida aleatória
            f_list = [*food_list]  # Lista com as chaves do dicionário(nome das comidas)
            self._name = choice(f_list)  # Pega uma comida aleatória da lista acima
        else:
            self._name = name

        self._points = food_list[self._name]["points"]
        self.sprite = food_list[self._name]["sprite"].convert_alpha()
        self._caught = False

        if x_pos >= constants.SCENARIO_WALKING_LIMIT_LEFT:
            self._x_pos = x_pos
        else:
            self._x_pos = constants.SCENARIO_WALKING_LIMIT_LEFT

        if y_pos >= constants.SCENARIO_WALKING_LIMIT_TOP + 20:
            self._y_pos = y_pos
        else:
            self._y_pos = constants.SCENARIO_WALKING_LIMIT_TOP + 20

        #Cria o rect da comida
        self._rect = self.sprite.get_rect()
        self._rect.x = self._x_pos
        self._rect.y = self._y_pos

        self.screen = screen

    @classmethod
    def start_spawn(cls):
        """Começa a spawnar comida no mapa por meio do evento FOOD_SPAWN_EVENT"""
        pygame.time.set_timer(cls.FOOD_SPAWN_EVENT, cls.SPAWN_DELAY)  # Inicia o evento

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

    @property
    def rect(self):
        return self._rect

    def get_coords(self):
        return self.x_pos, self.y_pos

    # Setters
    def grab(self):
        self._caught = True

    # Function for testing
    def to_string(self):
        result = "Food name: " + self.name + "\n"
        result += "Health points: " + str(self.points) + "\n"

        if self.caught:
            result += "Item in inventory!"
        else:
            result += "Position: (" + str(self.x_pos) + ", " + str(self.y_pos) + ")\n"

        return result

    @classmethod
    def random_spawn(cls, colliders: list, screen_w, screen_h, screen):
        """Spawna uma comida aleatóriia em uma posição aleatória da tela que não esteja ocupada.
        Recebe uma lista com os objetos os quais ela não deve ser instanciada em cima, a largura e
        a altura da tela e a própria tela."""
        sp_pos = (0, 0)  # Posição onde a comida será instanciada
        valid_pos = False  # Variável para checar se a posição está ocupada por uma parede ou obst.

        while (
            not valid_pos
        ):  # Enquanto a pos não for valida, gere uma nova, sempre múltipla de 10
            sp_pos = (
                randint(0, screen_w // 10) * 10,
                randint(0, screen_h // 10) * 10,
            )  # A posição da comida
            test_rect = pygame.Rect(
                sp_pos[0], sp_pos[1], 10, 10
            )  # Rect para testar se vai colidir
            valid_pos = (
                test_rect.collidelist(colliders) == -1
            )  # Se não bater em nada, a pos é válida
        #           print(f"valid_pos = {valid_pos}| pos = {sp_pos}| test = {test_rect.collidelist(colliders)}")

        f_list = [*food_list]  # Lista com as chaves do dicionário(nome das comidas)
        food = choice(f_list)  # Pega uma comida aleatória da lista acima

        return Food(food, sp_pos[0], sp_pos[1], screen)  # Retorna a comida spawnada

    def update(self):
        """Mantém o sprite da comida  na tela"""
        # Por enquanto, estou usando quadrados como Placeholder
        if hasattr(self, "name"):
            self.screen.blit(self.sprite, self.get_coords())  # Coloca o sprite na tela
