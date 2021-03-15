from SimpleGraphics import *

#create the size and background of the playable environment 
row = 50 #number of blocks wide
col = 50 #number of blocks long
blocksize = 10 #how long and wide each block will be
resize(row*blocksize, col*blocksize)
background("black")
setAutoUpdate(False)

#define the initial state of the snake
snake_body = []
snakeHead = [25,1] #snake head x locaiton
snakeTail= [25,0] #snake tail x location
snake_body.append(snakeHead)
snake_body.append(snakeTail)
snake_size = len(snake_body)
snakeColour = "red" #colour of the snake
snakeDirection = "down" #current direction of the snake (maybe we can add randomization for initial setting)
gameover = False

def main_program():

    while not closed() and not gameover:

        keys = getHeldKeys()

        #Test for gameover
        # if gameover:
        #     print("GAMEOVER!")
        
        # snakeDirection = snakeDirection.lower()
        
        direction(keys)

        clear()
        draw_snake()

        update()
        sleep(0.1)

    setColor("white")
    text(25*blocksize, 25*blocksize,"GAME OVER")   

def direction(keys):

    global snakeDirection

    #Prevents user from going the opposite direction
    
    if "w" in keys and snakeDirection != "down":
        snakeDirection = "up"
        # snakeHeady -= 1           #This can act as a small speed boost when pressing the direction key if we ever decide to implement that
    elif "s" in keys and snakeDirection != "up":
        snakeDirection = "down"
        # snakeHeady += 1
    elif "a" in keys and snakeDirection != "right":
        snakeDirection = "left"
        # snakeHeadx -= 1
        # gameover = True
    elif "d" in keys and snakeDirection != "left":
        snakeDirection = "right"
        # snakeHeadx += 1

    move_snake(snakeDirection)
    draw_snake()

def move_snake(dir):
    global snake_body

    #sets coordinate change to be passed to move_helper function
    if dir == "up":
        temp = (0,-1)
    elif dir == "down":
        temp = (0,1)
    elif dir == "left":
        temp = (-1,0)
    elif dir == "right":
        temp = (1,0)
    
    snake_body = move_helper(temp)

    check_boundary()

#Generates a new body (list of blocks coordinates) for the snake
def move_helper(tup):
    x,y  = tup
    
    new_body = []

    #Updates the head according to direction of movement and shifts every block a position towards the head of the snake
    for i in range(snake_size):
        if i == 0:
            Head_x = snake_body[i][0] + x
            Head_y = snake_body[i][1] + y
            new_body.append([Head_x,Head_y])
        else:
            new_body.append(snake_body[i-1])

    return new_body        

#iterates through snake body and draws rectangles for each of its composing blocks
def draw_snake():
    
    setFill(snakeColour)
    for block in snake_body:

        rect(block[0]*blocksize, block[1]*blocksize, blocksize, blocksize)


def check_boundary():
    global gameover
    for block in snake_body:
        #checks if snake hits walls or itself
        if (block[0] >= 50 or block[1] >= 50 or block[0] < 0 or block[1] < 0) or check_body():
            gameover = True

#checks if snake hits itself
def check_body():
    
    for i in range(snake_size):

        temp_body = snake_body[:i] + snake_body[i+1:]
        temp_body_size = len(temp_body)
        for j in range(temp_body_size):
            if (snake_body[i][0] == temp_body[j][0] and snake_body[i][1] == temp_body[j][1]):
                return True
    
    return False
        
main_program()