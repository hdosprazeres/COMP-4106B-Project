from game_data import *
from helper_functions import *
from ai import snake_ai_helper_functions as hf


def create_path_v0():
    '''
    creates a path from snake head to coin
    that does not go out of bounds or hit self
    '''
    head = game_data["snake"][0]
    coin = game_data["coin"]
    rows = game_data["rows"]
    cols = game_data["cols"]
    # creat a list of all legal moves
    open_squares = hf.get_open_squares()
    current_head = head
    path = []
    # incase loop doesn't work kill after rows*cols loops
    count = 0
    # find a path from coin snake head to coin using open squares
    while True:
        # if count is not same length as path, then no moves were made
        if count != len(path):
            return 1
        # kill incase looped more times than squares on board
        if count == rows * cols:
            return 1
        # if first element of path is equal to coin
        # then we have found a full path from snake head to coin
        # can exit loop
        if path != [] and path[0] == coin:
            break
        # assign current head to first element of path
        # allows us to build up a path from the current_head position to the coin
        # without hitting self or stepping out of bounds
        if path != []:
            current_head = path[0]
        # current_head below coin on grid
        # try to move up
        if current_head[1] > coin[1] and hf.valid_move([current_head[0], current_head[1]-1], open_squares):
            path.insert(0, [current_head[0], current_head[1]-1])
        # current_head above coin on grid
        # try to move down
        elif current_head[1] < coin[1] and hf.valid_move([current_head[0], current_head[1]+1], open_squares):
            path.insert(0, [current_head[0], current_head[1]+1])
         # current_head right of coin on grid
        # try to move left
        elif current_head[0] > coin[0] and hf.valid_move([current_head[0]-1, current_head[1]], open_squares):
            path.insert(0, [current_head[0]-1, current_head[1]])
         # current_head left of coin on grid
        # try to move right
        elif current_head[0] < coin[0] and hf.valid_move([current_head[0]+1, current_head[1]], open_squares):
            path.insert(0, [current_head[0]+1, current_head[1]])
        count += 1
    # the first element of path will be the coin
    # and the last element of path will be the next position from the current snake head position
    # must reverse list so that 1st element is next move
    path.reverse()
    game_data["path"] = path
    return 0


def update_snake_ai_v1():
    '''
    update snake body
    by adding head to path head as new snake head
    '''
    new_head = game_data["path"].pop(0)
    game_data["snake"].insert(0, new_head)
    game_data["snake"].pop(-1)


def snake_ai_v2():
    '''
    choose direction of snake
    go straight to coin
    with movement restrictions not allowing coin to move back onto self or out of bounds
    first create a path that the snake will take
    then base on path choose a direction
    function only creates a new path if path is currently empty
    which means it will only create path upon game start and coin pick up
    '''
    ret = 0
    # if path is empty create a new path
    if game_data["path"] == []:
        ret = create_path_v0()
    # error occured in create_path_v0
    if ret == 1:
        print("snake_ai_v2 error")
        return ret
    update_snake_ai_v1()
    return ret
