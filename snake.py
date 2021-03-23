from SimpleGraphics import *
import sys
import random
from queue import PriorityQueue

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
    "grid": [[]],
    "graph": {}
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
    game_data["graph"] = make_graph()

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
        
        pathfinding()

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

    node = (new_x,new_y)
    xt,yt = game_data["snake_tail"]
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
    game_data["graph"][node][1] = False
    game_data["graph"][(xt,yt)][1] = True
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

def make_graph():

    G = {}

    rows = game_data["rows"]
    cols = game_data["cols"]


    for i in range (0,rows):
    
        for j in range (0,cols):
            G[(i,j)] = [neighbors((i,j)),True]
    return G


def heuristics(node_location,coin_location):
  
    (x1,y1) = node_location
    (xn,yn) = coin_location

    return abs(x1-xn)+ abs(y1-yn)


def neighbors (node_location):

    (x,y) = node_location

    neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    res = filter_bounds(neighbors)
    res = filter_wall(res)
    return res

def filter_bounds(nb_list):

    new_list = []
    for i in range(0,len(nb_list)):
        (x,y) = nb_list[i]
        if 0 <= x < game_data["rows"] and 0 <= y < game_data["rows"]:
            new_list.append(nb_list[i])
    return new_list

def filter_wall(nb_list):
    new_list = []
    for i in range(0,len(nb_list)):
    
        if nb_list[i] not in game_data["snake"]:
            new_list.append(nb_list[i])
    return new_list

def pathfinding():

#Start by defining what is considered a start and goal node
    x,y = game_data["snake"][0]
    start_location = (x,y)
    xg,yg = game_data["coin"]
    goal_location = (xg,yg)

#Declare a frontier (as priority queue) and an explored list.
    frontier = PriorityQueue()
    explored = []

#Define cost_so_far(actual cost), parent node, estimated_cost (heuristics cost) and add it to the frontier.
    cost_so_far = 0
    parent = None
    estimated_cost = heuristics(start_location,goal_location)
    #frontier.put((estimated_cost,cost_so_far,start_location,parent))
    frontier.put((estimated_cost,start_location,parent))

  #Iterate through frontier until goal state is found.
    while not frontier.empty():
    # print("current frontier is %s"%frontier.queue)

    #get element with highest priority in frontier (lowest cost) and parses its info

        estimated_cost,current_location,current_parent = frontier.get()
    
        (x,y) = current_location
    # print("current loc is %d, %d" %(x,y))

    #Checks whether current location is a goal and returns it if so.
        if current_location == goal_location:
            #print("Found goal!")
            explored.append((current_location,current_parent))
            break
    
    # print("explored now looks like this %s"%explored)
        #print("current node neighbors is %s"%neighbors(current_location))
    #Iterate through node's neighbors and perform A* steps
        for node in neighbors(current_location):
            xn,yn = node
      
      #A* conditional statements
            if (not in_frontier(node,frontier) and not in_explored(node,explored)) \
            or (in_frontier(node,frontier) and smaller_cost_frontier(node,frontier,estimated_cost)):
        
        #Refresh total costs
                if [xn,yn] == game_data["coin"]:
                    estimated_cost  = 0
                else:
                    estimated_cost  =  heuristics(node,goal_location)  
                    #node_cost = current_cost 
          # print("estimated cost is %d, and current cost is %d" %(estimated_cost,node_cost))
        
        #Add value to frontier
                frontier.put((estimated_cost,node,current_location))
    
    # print("is current node %d,%d in explored? %s"%(x,y,in_explored(current_location,explored)))
    #After exploring the node, add to explored.
            if not in_explored(current_location,explored):
                explored.append((current_location,current_parent))

  #Write results to explored list and optimal_path files
    print(backtracking(current_location,explored))

    #return print("The optimal path cost is %d"%optimal_path_cost)

def in_frontier(node,frontier):
 
    return any(node in item for item in frontier.queue)

def in_explored(node,explored_list):
  
    for item in explored_list:

        if node == item[0]:
            return True
    return False

def smaller_cost_frontier(node,frontier,cost):

    if in_frontier(node,frontier):

        for item in frontier.queue:

            if item[1] == node and cost < item[0]:

                return True

        return False

def backtracking(goal_node,explored_list):

    path = []
    node = goal_node
    completed = False
    while completed != True:
        for item in explored_list:

        #Return when a node found has no parent, as it corresponds to the start state.
            if item[0] == node and item[1] == None:
                path.append(item[0])
                completed = True
                break
            #When node found has a parent, add to path and continue backtracking
            elif item[0] == node:
                # print("found a node %s . Append it and look for its parent %s"%(item[0],item[1]))
                path.append(item[0])
                node = item[1]

    return path

command_line_input()
game_loop()
