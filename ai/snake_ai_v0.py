import random
from game_data import *
from helper_functions import *


def snake_ai_v0():
    '''
    choose direction of snake randomly
    '''
    num = random.randrange(4)
    if num == 0:
        game_data["snake_direction"] = "up"
    elif num == 1:
        game_data["snake_direction"] = "down"
    elif num == 2:
        game_data["snake_direction"] = "left"
    elif num == 3:
        game_data["snake_direction"] = "right"
    # create new head of snake depending on current direction
    update_snake()
    return 0
