from SimpleGraphics import *
import sys
import random
from queue import PriorityQueue
from snake_ai import *
from game_data import *
from helper_functions import *

def game_loop():
    '''
    main loop for the game
    '''
    blocksize = game_data["block_size"]
    rows = game_data["rows"]
    cols = game_data["cols"]

    game_data["grid"] = create_grid()
    game_data["graph"] = make_graph()

    sleep_time = 0.05
    sleep_step = sleep_time / 50

    resize(rows*blocksize, cols*blocksize)
    background("black")
    setAutoUpdate(False)

    # put snake head in correct place
    game_data["snake"][0][0] = game_data["cols"] // 2
    create_coin()

    while True:

        #print(game_data["snake"])
        points = game_data["points"]
        # save snake tail incase coin picked up
        game_data["snake_tail"] = game_data["snake"][-1]

        # a* search can sit here making decisions about the next move
        if not game_data["path"]:
            pathfinding()

        # check if snake dead, break loop
        if is_snake_dead():
            print("Snake is dead!")
            break

        update_snake_ai()

        check_coin()
        create_coin()

        draw_snake()
        draw_coin()
        
        update()
        sleep(sleep_time)
        # check if scored a point this loop, speed up time
        # if game_data["scored_point"]:
        #     sleep_time -= sleep_step
        #     game_data["scored_point"] = False

    # write gameover screen
    setOutline("white")
    text((rows/2)*blocksize, (cols/2)*blocksize, f"GAMEOVER\npoints: {points}")


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
