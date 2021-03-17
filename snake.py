from SimpleGraphics import *
import sys
import getopt
import random

rows = 10  # number of blocks wide
cols = 10  # number of blocks long
rows_min = 5
rows_max = 50

opts, args = getopt.getopt(sys.argv, "")
# print(args)
# print(len(sys.argv))
if len(sys.argv) == 2:
    if int(sys.argv[1]) >= rows_min and int(sys.argv[1]) <= rows_max:
        rows = int(sys.argv[1])
        cols = int(sys.argv[1])
    else:
        print(f"rows and cols between {rows_min}-{rows_max}")
if len(sys.argv) == 3:
    if int(sys.argv[1]) >= rows_min and int(sys.argv[1]) <= rows_max:
        rows = int(sys.argv[1])
    if int(sys.argv[2]) >= rows_min and int(sys.argv[2]) <= rows_max:
        cols = int(sys.argv[2])
    else:
        print(f"rows and cols between {rows_max}-{rows_min}")
# print(rows, cols)

blocksize = 25  # how long and wide each block will be
resize(rows*blocksize, cols*blocksize)
background("black")
setAutoUpdate(False)

# variable init
points = 0
coin = []
# new x and y position of head
new_x = 0
new_y = 0
# snake should start in top middle of screen
snake = [[rows//2, 0]]
snakeDirection = "down"
snakeColour = "red"


# returns x,y coordinates as two separate lists
def get_snake_xs_ys():
    x = y = []
    for i in range(0, len(snake)):
        x.append(snake[i][0])
        y.append(snake[i][1])
    return x, y


while True:

    # save snake tail incase coin picked up
    snake_tail = snake[-1]

    keys = getHeldKeys()

    if "w" in keys:
        snakeDirection = "up"
    elif "s" in keys:
        snakeDirection = "down"
    elif "a" in keys:
        snakeDirection = "left"
    elif "d" in keys:
        snakeDirection = "right"

    if snakeDirection == "up":
        new_y = snake[0][1] - 1
    elif snakeDirection == "down":
        new_y = snake[0][1] + 1
    elif snakeDirection == "left":
        new_x = snake[0][0] - 1
    elif snakeDirection == "right":
        new_x = snake[0][0] + 1

    # check if snake running into self
    if [new_x, new_y] in snake:
        print(f"points: {points}")
        break

    # update snake position
    snake.insert(0, [new_x, new_y])
    snake.pop(-1)

    # check if snake out of bounds
    if snake[0][0] < 0 or snake[0][0] >= cols:
        print(f"points: {points}")
        break
    if snake[0][1] < 0 or snake[0][1] >= rows:
        print(f"points: {points}")
        break

    # create coin
    '''
    PROBLEM WITH COIN CREATION, SOMETIMES
    File "snake.py", line 115, in <module>
    coin = [random_x[x], random_y[y]]
    IndexError: list index out of range
    '''
    if coin == []:
        snake_x, snake_y = get_snake_xs_ys()
        random_x = [i for i in range(0, cols) if i not in snake_x]
        random_y = [i for i in range(0, rows) if i not in snake_y]
        x = random.randint(0, len(random_x))
        y = random.randint(0, len(random_y))
        # coin = [random_x[x], random_y[y]]
        coin = [5, 5]
        # print(coin)

    # check if snake eating coin
    if snake[0][0] == coin[0] and snake[0][1] == coin[1]:
        points += 1
        coin = []
        snake.append(snake_tail)

    clear()

    # colour in snake
    setFill(snakeColour)
    for x in range(0, len(snake)):
        rect(snake[x][0]*blocksize, snake[x][1]
             * blocksize, blocksize, blocksize)

    # colour in coin
    if coin != []:
        setFill("green")
        rect(coin[0]*blocksize, coin[1]*blocksize, blocksize, blocksize)

    update()
    sleep(0.15)

# write gameover screen
setOutline("white")
text((rows/2)*blocksize, (cols/2)*blocksize, f"GAMEOVER\npoints: {points}")
