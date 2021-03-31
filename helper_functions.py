from game_data import *
import random
from SimpleGraphics import *

def create_grid():
    '''
    create list of coordinates on board
    for creation of a new coin randomly
    '''
    rows = game_data["rows"]
    cols = game_data["cols"]
    grid = []
    for col in range(cols):
        for row in range(rows):
            grid.append([col, row])
    return grid


def is_snake_dead():
    '''
    checks if snake as moved into itself
    or if snake as moved out of bounds
    '''
    #print("is_snake_dead()")
    snake = game_data["snake"]
    # check if snake running into self
    if snake[0] in snake[1:] or not game_data["path"]:
        return True
    # check if snake out of bounds
    if snake[0][0] < 0 or snake[0][0] >= game_data["cols"]:
        return True
    if snake[0][1] < 0 or snake[0][1] >= game_data["rows"]:
        return True

def create_coin():
    '''
    create a coin at any coordinate on the grid
    that doesn't contain snake
    '''
    snake = game_data["snake"]
    coin = game_data["coin"]
    grid = game_data["grid"]
    # create coin
    if coin == []:
        open_squares = [i for i in grid if i not in snake]
        point = random.randint(0, len(open_squares)-1)
        game_data["coin"] = open_squares[point]


def check_coin():
    '''
    check if snake ate coin
    if yes add points and increase snake length
    '''
    snake = game_data["snake"]
    snake_tail = game_data["snake_tail"]
    coin = game_data["coin"]
    if coin != []:
        if snake[0][0] == coin[0] and snake[0][1] == coin[1]:
            game_data["scored_point"] = True
            game_data["points"] += 1
            game_data["coin"] = []
            snake.append(snake_tail)


def draw_snake():
    '''
    draw snake by only drawing the new head
    and erasing the old tail
    saves on rect calls
    '''
    snake = game_data["snake"]
    snake_tail = game_data["snake_tail"]
    blocksize = game_data["block_size"]
    # draw snake
    # colour red
    # draw new head
    setFill("red")
    rect(snake[0][0]*blocksize, snake[0][1]
         * blocksize, blocksize, blocksize)
    # erase old tail
    setFill("black")
    rect(snake_tail[0]*blocksize, snake_tail[1]
         * blocksize, blocksize, blocksize)


def draw_coin():
    '''
    draw coin
    '''
    blocksize = game_data["block_size"]
    coin = game_data["coin"]
    # draw coin
    if coin != []:
        setFill("yellow")
        rect(coin[0]*blocksize, coin[1]*blocksize, blocksize, blocksize)
