import random
import sys
from game_data import *
from helper_functions import *
from queue import PriorityQueue
from math import *


def snake_ai_v0():
    '''
    choose direction of snake randomly
    '''
    num = random.randrange(4)
    if num == 0:
        game_data["snake_direction"] = "up"
    elif num == 1:
        game_data["snake_direction"] = "down"
    elif num == 2:
        game_data["snake_direction"] = "left"
    elif num == 3:
        game_data["snake_direction"] = "right"
    # create new head of snake depending on current direction
    update_snake()
    return 0


def snake_ai_v1():
    '''
    choose direction of snake
    go straight to coin
    no movement restricitons therefore possible to move back on self and die
    '''
    head = game_data["snake"][0]
    coin = game_data["coin"]
    print("head", head)
    print("coin", coin)
    # if snake head is below coin on grid
    # move up on grid until in same row
    if head[1] > coin[1]:
        print("up")
        game_data["snake_direction"] = "up"
    # if snake head is above coin on grid
    # move down on grid until in same row
    elif head[1] < coin[1]:
        print("down")
        game_data["snake_direction"] = "down"
    # if snake head is right of coin on grid
    # move left on grid until in same row
    elif head[0] > coin[0]:
        print("left")
        game_data["snake_direction"] = "left"
    # if snake head is left of coin on grid
    # move right on grid until in same row
    elif head[0] < coin[0]:
        print("right")
        game_data["snake_direction"] = "right"
    # create new head of snake depending on current direction
    update_snake()
    return 0


def valid_move(next_move, open_squares):
    '''
    next_move is a location [col, row]
    open_squares is a list [[col, row]] of open location on grid
    checks if next_move is a valid location in open_squares
    '''
    if next_move in open_squares:
        return True
    else:
        return False


def get_open_squares():
    '''
    return a array of [x,y] coordinates
    on the grid that are not snake or coin
    '''
    snake = game_data["snake"]
    grid = game_data["grid"]
    return [i for i in grid if i not in snake]


def create_path_v0():
    '''
    creates a path from snake head to coin
    that does not go out of bounds or hit self
    '''
    head = game_data["snake"][0]
    coin = game_data["coin"]
    rows = game_data["rows"]
    cols = game_data["cols"]
    print("head", head)
    print("coin", coin)
    # creat a list of all legal moves
    open_squares = get_open_squares()
    print(open_squares)
    current_head = head
    path = []
    # incase loop doesn't work kill after rows*cols loops
    count = 0
    # find a path from coin snake head to coin using open squares
    while True:
        # if count is not same length as path, then no moves were made
        if count != len(path):
            print("create_path_v0 error")
            print("valid move could not be made")
            return 1
        # kill incase looped more times than squares on board
        if count == rows * cols:
            sys.exit(0)
        print()
        print("path", path)
        # if first element of path is equal to coin
        # then we have found a full path from snake head to coin
        # can exit loop
        if path != [] and path[0] == coin:
            break
        # assign current head to first element of path
        # allows us to build up a path from the current_head position to the coin
        # without hitting self or stepping out of bounds
        if path != []:
            current_head = path[0]
        print("current_head", current_head)
        # current_head below coin on grid
        # try to move up
        if current_head[1] > coin[1] and valid_move([current_head[0], current_head[1]-1], open_squares):
            print("up")
            print("next_move", [current_head[0], current_head[1]-1])
            path.insert(0, [current_head[0], current_head[1]-1])
        # current_head above coin on grid
        # try to move down
        elif current_head[1] < coin[1] and valid_move([current_head[0], current_head[1]+1], open_squares):
            print("down")
            print("next_move", [current_head[0], current_head[1]+1])
            path.insert(0, [current_head[0], current_head[1]+1])
         # current_head right of coin on grid
        # try to move left
        elif current_head[0] > coin[0] and valid_move([current_head[0]-1, current_head[1]], open_squares):
            print("left")
            print("next_move", [current_head[0]-1, current_head[1]])
            path.insert(0, [current_head[0]-1, current_head[1]])
         # current_head left of coin on grid
        # try to move right
        elif current_head[0] < coin[0] and valid_move([current_head[0]+1, current_head[1]], open_squares):
            print("right")
            print("next_move", [current_head[0]+1, current_head[1]])
            path.insert(0, [current_head[0]+1, current_head[1]])
        count += 1
    # the first element of path will be the coin
    # and the last element of path will be the next position from the current snake head position
    # must reverse list so that 1st element is next move
    path.reverse()
    game_data["path"] = path
    return 0


def update_snake_ai_v1():
    '''
    update snake body
    by adding head to path head as new snake head
    '''
    new_head = game_data["path"].pop(0)
    game_data["snake"].insert(0, new_head)
    game_data["snake"].pop(-1)


def snake_ai_v2():
    '''
    choose direction of snake
    go straight to coin
    with movement restrictions not allowing coin to move back onto self or out of bounds
    first create a path that the snake will take
    then base on path choose a direction
    function only creates a new path if path is currently empty
    which means it will only create path upon game start and coin pick up
    '''
    ret = 0
    # if path is empty create a new path
    if game_data["path"] == []:
        ret = create_path_v0()
    # error occured in create_path_v0
    if ret == 1:
        print("snake_ai_v2 error")
        return ret
    update_snake_ai_v1()
    return ret


def update_snake_ai_v0():
    '''
    based on snake direction pick where new head will be
    update snake by simply adding new head and popping tail
    '''
    # print("update_snake_ai()")
    snake = game_data["snake"]
    path = game_data["path"]
    new_x = game_data["path"][0][0]
    new_y = game_data["path"][0][1]
    node = (new_x, new_y)
    xt, yt = game_data["snake_tail"]
    # update snake position
    snake.insert(0, [new_x, new_y])
    game_data["graph"][node][1] = False
    game_data["graph"][(xt, yt)][1] = True
    snake.pop(-1)
    game_data["path"].pop(0)

    graph = game_data["graph"]


def make_graph():
    '''
    This function creates a graph for each coordinate in the grid.
    The key corresponds to the coordinates and values are: [[list of neighbors],boolean].
    The boolean marks whether the node is valid(True) or invalid (False) to be visited
    '''
    G = {}

    rows = game_data["rows"]
    cols = game_data["cols"]

    for i in range(0, rows):

        for j in range(0, cols):
            G[(i, j)] = [neighbors((i, j)), True, game_data["default_cost"]]
    return G


def heuristics(node_location, coin_location):
    '''
    this function implements the manhattan distance heuristic
    '''

    (x1, y1) = node_location
    (xn, yn) = coin_location

    return abs(x1-xn) + abs(y1-yn)


def update_actual_cost():
    '''
    this function updates the actual cost of graph nodes
    '''
    radial_distance()
    wall_proximity()
    # body_proximity()


def radial_distance():
    distance_factor = int(game_data["rows"]*game_data["cols"]/10)
    xc = game_data["coin"][0]
    yc = game_data["coin"][1]
    for i in range(-distance_factor, distance_factor):
        x = xc + i
        for j in range(-distance_factor, distance_factor):
            y = yc + j

            if 0 <= x < game_data["rows"] and 0 <= y < game_data["cols"]:
                game_data["graph"][(x, y)][2] = game_data["graph"][(
                    x, y)][2] - sqrt((xc-x)**2+(yc-y)**2)


def wall_proximity():
    distance_factor = 2
    discount_factor = 3
    rows = game_data["rows"]
    cols = game_data["cols"]

    for node in game_data["snake"]:
        x, y = node

        if (x - distance_factor) < 0 or (x+distance_factor) > rows or (y-distance_factor) < 0 or (y+distance_factor) > cols:

            game_data["graph"][(x, y)][2] = game_data["graph"][(
                x, y)][2] - discount_factor


def body_proximity():
    distance_factor = 2
    discount_factor = 3
    snake = game_data["snake"]
    head = snake[0]
    for i in range(len(snake)):

        x, y = snake[i]

        for z in range(-distance_factor, distance_factor):
            xtemp = x + z
            for j in range(-distance_factor, distance_factor):
                ytemp = y + j

                if 0 <= xtemp < game_data["rows"] and 0 <= ytemp < game_data["cols"] and game_data["graph"][(xtemp, ytemp)][1] == True:
                    game_data["graph"][(xtemp, ytemp)][2] = game_data["graph"][(
                        xtemp, ytemp)][1] - discount_factor + 20*(abs(xtemp-head[0])+abs(ytemp-head[1]))


def reset_cost():

    for i in range(0, game_data["rows"]):

        for j in range(0, game_data["cols"]):
            game_data["graph"][(i, j)][2] = game_data["default_cost"]


def neighbors(node_location):
    '''
    this function returns a list of valid neighbors for a given location
    '''
    (x, y) = node_location

    neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    res = filter_bounds(neighbors)
    res = filter_wall(res)
    return res


def filter_bounds(nb_list):
    '''
    this function filters a list of neighbors according to the grid boundaries
    '''
    new_list = []
    for i in range(0, len(nb_list)):
        (x, y) = nb_list[i]
        if 0 <= x < game_data["rows"] and 0 <= y < game_data["rows"]:
            new_list.append(nb_list[i])
    return new_list


def filter_wall(nb_list):
    '''
    this function filters a list of neighbors according to the snake body
    '''
    new_list = []
    for i in range(0, len(nb_list)):

        if nb_list[i] not in game_data["snake"]:
            new_list.append(nb_list[i])
    return new_list


def pathfinding():

    found = False
    graph = game_data["graph"]

    # Start by defining what is considered a start node (snake's head) and goal node (coin location)
    x, y = game_data["snake"][0]
    start_location = (x, y)
    xg, yg = game_data["coin"]
    goal_location = (xg, yg)

    # Declare a frontier (as priority queue) and an explored list.
    frontier = PriorityQueue()
    explored = []

    # Define cost_so_far(actual cost), parent node, estimated_cost (heuristics cost) and add it to the frontier.
    update_actual_cost()
    cost_so_far = 0
    parent = None
    estimated_cost = heuristics(start_location, goal_location)

    # frontier.put((estimated_cost,cost_so_far,start_location,parent))
    frontier.put((estimated_cost, cost_so_far, start_location, parent))

    # Iterate through frontier until goal state is found.
    while not frontier.empty():

        # get element with highest priority in frontier (lowest cost) and parses its info

        estimated_cost, current_cost, current_location, current_parent = frontier.get()
        (x, y) = current_location

        # Checks whether current location is a goal and returns it if so.
        if current_location == goal_location:
            found = True
            explored.append((current_location, current_parent))
            break

        # Iterate through node's neighbors and perform A* steps
        for node in neighbors(current_location):
            xn, yn = node
            if graph[(xn, yn)][1] == False:
                continue
        # A* conditional statements
            if (not in_frontier(node, frontier) and not in_explored(node, explored)) \
                    or (in_frontier(node, frontier) and smaller_cost_frontier(node, frontier, estimated_cost)):

                # Refresh total costs
                if [xn, yn] == game_data["coin"]:
                    estimated_cost = 0
                    node_cost = 0
                else:
                    estimated_cost = current_cost + \
                        float(graph[(xn, yn)][2]) + \
                        heuristics(node, goal_location)
                    node_cost = current_cost + float(graph[(xn, yn)][2])
                print(node_cost)
            # Add value to frontier
                frontier.put(
                    (estimated_cost, node_cost, node, current_location))

    # After exploring the node, add to explored.
            if not in_explored(current_location, explored):
                explored.append((current_location, current_parent))

    path = backtracking(current_location, explored)
    final_path = path[::-1]
    game_data["path"] = final_path[1:]
    return found


def in_frontier(node, frontier):
    '''
    checks if node is already in frontier
    '''
    return any(node in item for item in frontier.queue)


def in_explored(node, explored_list):
    '''
    checks if node is in the explored list
    '''
    for item in explored_list:

        if node == item[0]:
            return True
    return False


def smaller_cost_frontier(node, frontier, cost):
    '''
    checks if current estimate of node is smaller than the one already in frontier
    '''

    if in_frontier(node, frontier):

        for item in frontier.queue:

            if item[1] == node and cost < item[0]:

                return True

        return False


def backtracking(goal_node, explored_list):
    '''
    given an explored list, it returns the path to be taken from start node to goal node
    '''
    path = []
    node = goal_node
    completed = False
    # print("explored_list: {}".format(explored_list))
    while completed != True:
        # explored list returns 0 or 1 elements when the snake dies
        if len(explored_list) <= 1:
            # band aid fix, technically shouldn't be returning the goal node as path
            path.append(node)
            break

        for item in explored_list:
            # Return when a node found has no parent, as it corresponds to the start state.
            if item[0] == node and item[1] == None:
                path.append(item[0])
                completed = True
                break
            # When node found has a parent, add to path and continue backtracking
            elif item[0] == node:
                # print("found a node %s . Append it and look for its parent %s"%(item[0],item[1]))
                path.append(item[0])
                node = item[1]
    return path
