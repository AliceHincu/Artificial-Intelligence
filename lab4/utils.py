# -*- coding: utf-8 -*-

# map
N = 20
M = 20
INITIAL_POSITION = [N//2, M//2]
BATTERY_CAPACITY = 21
NUMBER_OF_SENSORS = 7
NUMBER_OF_ANTS = 80
NUMBER_OF_EPOCHS = 200
MAX_SENSOR_CAPACITY = 5

# other
ALPHA = 1.9
BETA = 0.9
RHO = 0.05
Q0 = 0.3

# creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
DIRECTION_DICT = {
    UP: [-1, 0],
    DOWN: [1, 0],
    RIGHT: [0, 1],
    LEFT: [0, -1]
}