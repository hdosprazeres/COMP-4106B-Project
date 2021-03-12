from SimpleGraphics import *

#create the size and background of the playable environment 
row = 50 #number of blocks wide
col = 50 #number of blocks long
blocksize = 10 #how long and wide each block will be
resize(row*blocksize, col*blocksize)
background("black")
setAutoUpdate(False)

#define the initial state of the snake
snakeHeadx = 25 #snake head x locaiton
snakeHeady = 1 #snake head y location
snakeTailx= 25 #snake tail x location
snakeTaily = 0 #snake tail y location
snakeDirection = "down" #current direction of the snake (maybe we can add randomization for initial setting)
snakeColour = "red" #colour of the snake

gameover = False

while not closed() and not gameover:

    keys = getHeldKeys()

    #Test for gameover
    # if gameover:
    #     print("GAMEOVER!")
    
    # snakeDirection = snakeDirection.lower()

    if "w" in keys:
        snakeDirection = "up"
        # snakeHeady -= 1           #This can act as a small speed boost when pressing the direction key if we ever decide to implement that
    elif "s" in keys:
        snakeDirection = "down"
        # snakeHeady += 1
    elif "a" in keys:
        snakeDirection = "left"
        # snakeHeadx -= 1
        # gameover = True
    elif "d" in keys:
        snakeDirection = "right"
        # snakeHeadx += 1
    
    snakeTailx = snakeHeadx
    snakeTaily = snakeHeady

    if snakeDirection == "up":
        snakeHeady -= 1
    elif snakeDirection == "down":
        snakeHeady += 1
    elif snakeDirection == "left":
        snakeHeadx -= 1
    elif snakeDirection == "right":
        snakeHeadx += 1

    clear()

    setFill(snakeColour)
    rect(snakeHeadx*blocksize, snakeHeady*blocksize, blocksize, blocksize)
    rect(snakeTailx*blocksize, snakeTaily*blocksize, blocksize, blocksize)

    update()
    sleep(0.1)

setColor("black")
text(25*blocksize, 25*blocksize,"GAMEOVER")   
