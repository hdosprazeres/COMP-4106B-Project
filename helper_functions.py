import random
import sys
from game_data import *


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
    snake = game_data["snake"]
    # check if snake running into self
    if snake[0] in snake[1:]:
        return True
    # check if snake out of bounds
    if snake[0][0] < 0 or snake[0][0] >= game_data["cols"]:
        return True
    if snake[0][1] < 0 or snake[0][1] >= game_data["rows"]:
        return True


def change_snake_direction(keys):
    '''
    changes directoin of snake if appropriate key was pressed
    has slightly different movement when len = 1
    len 1 snake can move back from where it came
    '''
    # change snakes direction if keystroke detected
    snake_direction = game_data["snake_direction"]
    # snake can move freely if just a head
    # print("head", game_data["snake"][0])
    # print("coin", game_data["coin"])
    if len(game_data["snake"]) == 1:
        if "w" in keys:
            game_data["snake_direction"] = "up"
        elif "s" in keys:
            game_data["snake_direction"] = "down"
        elif "a" in keys:
            game_data["snake_direction"] = "left"
        elif "d" in keys:
            game_data["snake_direction"] = "right"
    # snake can't move back on itself
    else:
        if "w" in keys and snake_direction != "down":
            game_data["snake_direction"] = "up"
        elif "s" in keys and snake_direction != "up":
            game_data["snake_direction"] = "down"
        elif "a" in keys and snake_direction != "right":
            game_data["snake_direction"] = "left"
        elif "d" in keys and snake_direction != "left":
            game_data["snake_direction"] = "right"
    # create new head of snake depending on current direction
    update_snake()


def update_snake():
    '''
    based on snake direction pick where new head will be
    update snake by simply adding new head and popping tail
    '''
    snake_direction = game_data["snake_direction"]
    snake = game_data["snake"]
    new_x = snake[0][0]
    new_y = snake[0][1]
    if snake_direction == "up":
        new_y = snake[0][1] - 1
    elif snake_direction == "down":
        new_y = snake[0][1] + 1
    elif snake_direction == "left":
        new_x = snake[0][0] - 1
    elif snake_direction == "right":
        new_x = snake[0][0] + 1
    # update snake position
    snake.insert(0, [new_x, new_y])
    snake.pop(-1)


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
            game_data["snake"].append(snake_tail)


def command_line_input():
    '''
    takes comand line input to determine screen size
    see README
    '''
    size_min = 5
    size_max = 50

    if len(sys.argv) == 2:
        if int(sys.argv[1]) >= size_min and int(sys.argv[1]) <= size_max:
            game_data["rows"] = int(sys.argv[1])
            game_data["cols"] = int(sys.argv[1])
        else:
            print(f"rows and cols between {size_min}-{size_max}")
    if len(sys.argv) == 3:
        if int(sys.argv[1]) >= size_min and int(sys.argv[1]) <= size_max:
            game_data["cols"] = int(sys.argv[1])
        if int(sys.argv[2]) >= size_min and int(sys.argv[2]) <= size_max:
            game_data["rows"] = int(sys.argv[2])
        else:
            print(f"rows and cols between {size_max}-{size_min}")
