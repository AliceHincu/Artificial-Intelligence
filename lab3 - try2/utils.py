# -*- coding: utf-8 -*-

# creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
DIRECTION_DICT= {
    UP: [-1, 0],
    DOWN: [1, 0],
    RIGHT: [0, 1],
    LEFT: [0, -1]
}

# define map size
map_length = 20
