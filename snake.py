import random
import os
import sys
from game_data import *
from helper_functions import *
from ai import snake_ai_v0
from ai import snake_ai_v1
from ai import snake_ai_v2
from ai import snake_ai_v3
from ai import snake_ai_v4
from ai import snake_ai_v5
from ai import snake_ai_v6
from ai import snake_ai_v7
from ai import snake_ai
from SimpleGraphics import *


def game_loop():
    '''
    main loop for the game
    '''

    global game_data
    blocksize = game_data["block_size"]
    rows = game_data["rows"]
    cols = game_data["cols"]

    game_data["grid"] = create_grid()
    game_data["graph"] = snake_ai.make_graph()

    # sleep_time = 0.05
    # for automated testing only
    sleep_time = 0

    resize(cols*blocksize, rows*blocksize)
    background("black")
    setAutoUpdate(False)

    # put snake head in correct place
    game_data["snake"][0][0] = game_data["cols"] // 2

    # create coin
    # need for snake_ai_v#
    create_coin()

    # check if snake_ai makes an error
    # 1 is error
    # 0 is success
    error = 0

    while True:
        points = game_data["points"]
        # save snake tail incase coin picked up
        game_data["snake_tail"] = game_data["snake"][-1]

        # human player
        if game_data["ai"] == "human":
            keys = getHeldKeys()
            change_snake_direction(keys)

        # ai player
        if game_data["ai"] == "snake_ai_v0":
            error = snake_ai_v0.snake_ai_v0()
        if game_data["ai"] == "snake_ai_v1":
            error = snake_ai_v1.snake_ai_v1()
        if game_data["ai"] == "snake_ai_v2":
            error = snake_ai_v2.snake_ai_v2()
        if game_data["ai"] == "snake_ai_v3":
            error = snake_ai_v3.snake_ai_v3()
        if game_data["ai"] == "snake_ai_v4":
            error = snake_ai_v4.snake_ai_v4()
        if game_data["ai"] == "snake_ai_v5":
            error = snake_ai_v5.snake_ai_v5()
        if game_data["ai"] == "snake_ai_v6":
            error = snake_ai_v6.snake_ai_v6()
        if game_data["ai"] == "snake_ai_v7":
            error = snake_ai_v7.snake_ai_v7()
        # if error returned from snake_ai
        if error == 1:
            break

        if game_data["ai"] == "snake_ai":
            if not game_data["path"]:
                snake_ai.pathfinding()
            snake_ai.update_snake_ai_v0()

        # check if snake dead, break loop
        is_snake_dead()
        if game_data["game_over"]:
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
            sleep_time -= sleep_time * 0.05
            game_data["scored_point"] = False

    # write gameover screen
    setOutline("white")
    text((cols/2)*blocksize, (rows/2)*blocksize, f"GAMEOVER\npoints: {points}")
    # save score
    save_score(points)
    # for automated testing only
    close()


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


command_line_input()
game_loop()
