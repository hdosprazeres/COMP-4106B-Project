import random
import sys
from game_data import *
from helper_functions import *
from snake_ai_v0 import *
from snake_ai_v1 import *
from snake_ai_v2 import *
from snake_ai_v3 import *
from snake_ai_v4 import *
from snake_ai_v5 import *
from snake_ai import *
from SimpleGraphics import *
import tkinter as tk
from tkinter.constants import *


def game_loop():
    '''
    main loop for the game
    '''

    global game_data
    blocksize = game_data["block_size"]
    rows = game_data["rows"]
    cols = game_data["cols"]

    game_data["grid"] = create_grid()
    game_data["graph"] = make_graph()

    sleep_time = 0.05

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
        # keys = getHeldKeys()
        # change_snake_direction(keys)

        # ai player
        # error = snake_ai_v0()
        # error = snake_ai_v1()
        # error = snake_ai_v2()
        # error = snake_ai_v3()
        if game_data["ai"] == "snake_ai_v4":
            error = snake_ai_v4()
        if game_data["ai"] == "snake_ai_v5":
            error = snake_ai_v5()
        # if error returned from snake_ai
        if error == 1:
            break

        # uncomment along with update_snake_ai_v0()
        if game_data["ai"] == "snake_ai":
            if not game_data["path"]:
                pathfinding()

    # uncomment along with pathfinding
        if game_data["ai"] == "snake_ai":
            update_snake_ai_v0()

        # check if snake dead, break loop
        is_snake_dead()
        if game_data["game_over"]:
            break

        # uncomment along with pathfinding
        # if game_data["ai"] == "snake_ai":
        #     update_snake_ai_v0()

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


def buttonPressed_heuristic1():
    print("Heuristic 1 pressed")
    clear()
    command_line_input()
    game_loop()


def buttonPressed_heuristic2():
    print("Heuristic 2 pressed")


def buttonPressed_heuristic3():
    print("Heuristic 3 pressed")


def draw_homescreen():
    setWindowTitle("Snake AI")
    resize(500, 500)
    background("black")
    setAutoUpdate(False)

    setFont("Helvetica", "32")
    setColor("yellow")
    text(250, 65, "Welcome to Snake AI!")

    master.configure(background='black')
    button_heuristic1 = tk.Button(
        text="Heuristic 1",
        width=20,
        height=5,
        bg="red",
        fg="yellow",
        command=buttonPressed_heuristic1)
    button_heuristic1.pack(pady=20)

    button_heuristic2 = tk.Button(
        text="Heuristic 2",
        width=20,
        height=5,
        bg="red",
        fg="yellow",
        command=buttonPressed_heuristic2)
    button_heuristic2.pack(pady=20)

    button_heuristic3 = tk.Button(
        text="Heuristic 3",
        width=20,
        height=5,
        bg="red",
        fg="yellow",
        command=buttonPressed_heuristic3)
    button_heuristic3.pack(pady=20)


# draw_homescreen()
command_line_input()
game_loop()
