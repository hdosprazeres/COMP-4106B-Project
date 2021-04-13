from game_data import *
from helper_functions import *


def snake_ai_v1():
    '''
    choose direction of snake
    go straight to coin
    no movement restricitons therefore possible to move back on self and die
    '''
    head = game_data["snake"][0]
    coin = game_data["coin"]
    # if snake head is below coin on grid
    # move up on grid until in same row
    if head[1] > coin[1]:
        game_data["snake_direction"] = "up"
    # if snake head is above coin on grid
    # move down on grid until in same row
    elif head[1] < coin[1]:
        game_data["snake_direction"] = "down"
    # if snake head is right of coin on grid
    # move left on grid until in same row
    elif head[0] > coin[0]:
        game_data["snake_direction"] = "left"
    # if snake head is left of coin on grid
    # move right on grid until in same row
    elif head[0] < coin[0]:
        game_data["snake_direction"] = "right"
    # create new head of snake depending on current direction
    update_snake()
    return 0
