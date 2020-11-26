# Food dictionary with health points for the constructor
# TODO: Edit food list with final values
food_list = {
    'apple': {'points': 5, },
    'cheese': {'points': 10, },
    'egg': {'points': 20, },
    'chicken': {'points': 40, },
}


# Food class
class Food:

    # Constructor
    # TODO: Add sprites to food objects
    def __init__(self, name, x_pos, y_pos):
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
