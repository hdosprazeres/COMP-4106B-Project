from SimpleGraphics import *
import sys
import random


game_data = {
    "rows": 10,
    "cols": 10,
    "points": 0,
    "coin": [],
    "snake": [[0, 0]],
    "snake_tail": [],
    "snake_direction": "down",
    "block_size": 25,
    "scored_point": False,
    "grid": [[]]
}


def game_loop():
    '''
    main loop for the game
    '''

    global game_data
    blocksize = game_data["block_size"]
    rows = game_data["rows"]
    cols = game_data["cols"]

    game_data["grid"] = create_grid()

    sleep_time = 0.15
    sleep_step = sleep_time / 50

    resize(rows*blocksize, cols*blocksize)
    background("black")
    setAutoUpdate(False)

    # put snake head in correct place
    game_data["snake"][0][0] = game_data["cols"] // 2

    while True:
        points = game_data["points"]
        # save snake tail incase coin picked up
        game_data["snake_tail"] = game_data["snake"][-1]

        # a* search can sit here making decisions about the next move

        keys = getHeldKeys()
        change_snake_direction(keys)
        update_snake()
        # check if snake dead, break loop
        if is_snake_dead():
            break

        check_coin()
        create_coin()

        # clear()
        draw_snake()
        draw_coin()

        update()
        sleep(sleep_time)
        # check if scored a point this loop, speed up time
        if game_data["scored_point"]:
            sleep_time -= sleep_step
            game_data["scored_point"] = False

    # write gameover screen
    setOutline("white")
    text((rows/2)*blocksize, (cols/2)*blocksize, f"GAMEOVER\npoints: {points}")


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


def command_line_input():
    '''
    takes comand line input to determine screen size
    see README
    '''
    rows_min = 5
    rows_max = 50

    if len(sys.argv) == 2:
        if int(sys.argv[1]) >= rows_min and int(sys.argv[1]) <= rows_max:
            game_data["rows"] = int(sys.argv[1])
            game_data["cols"] = int(sys.argv[1])
        else:
            print(f"rows and cols between {rows_min}-{rows_max}")
    if len(sys.argv) == 3:
        if int(sys.argv[1]) >= rows_min and int(sys.argv[1]) <= rows_max:
            game_data["rows"] = int(sys.argv[1])
        if int(sys.argv[2]) >= rows_min and int(sys.argv[2]) <= rows_max:
            game_data["cols"] = int(sys.argv[2])
        else:
            print(f"rows and cols between {rows_max}-{rows_min}")


command_line_input()
game_loop()
