from game_data import *
from queue import PriorityQueue
from math import *
def update_snake_ai():
    '''
    based on snake direction pick where new head will be
    update snake by simply adding new head and popping tail
    '''
    #print("update_snake_ai()")
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
            G[(i, j)] = [neighbors((i, j)), True,game_data["default_cost"]]
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
    for i in range(-distance_factor,distance_factor):
        x = xc + i
        for j in range(-distance_factor,distance_factor):
            y = yc + j

            if 0 <= x < game_data["rows"] and 0 <= y < game_data["cols"]:
                game_data["graph"][(x,y)][2] = game_data["graph"][(x,y)][2] - sqrt((xc-x)**2+(yc-y)**2)

def wall_proximity():
    distance_factor = 2
    discount_factor = 3
    rows = game_data["rows"]
    cols = game_data["cols"]

    for node in game_data["snake"]:
        x,y = node

        if (x - distance_factor) < 0 or (x+distance_factor) > rows or (y-distance_factor) < 0 or (y+distance_factor) > cols:
            
            game_data["graph"][(x,y)][2] = game_data["graph"][(x,y)][2] - discount_factor
    
def body_proximity():
    distance_factor = 2
    discount_factor = 3
    snake = game_data["snake"]
    head = snake[0]
    for i in range(len(snake)):
    
        x,y = snake[i]
        
        for z in range(-distance_factor,distance_factor):
            xtemp = x + z
            for j in range(-distance_factor,distance_factor):
                ytemp = y + j

                if 0 <= xtemp < game_data["rows"] and 0 <= ytemp < game_data["cols"] and game_data["graph"][(xtemp,ytemp)][1] == True:
                    game_data["graph"][(xtemp,ytemp)][2] = game_data["graph"][(xtemp,ytemp)][1] - discount_factor +20*(abs(xtemp-head[0])+abs(ytemp-head[1]))

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
    frontier.put((estimated_cost,cost_so_far, start_location, parent))

    # Iterate through frontier until goal state is found.
    while not frontier.empty():

        # get element with highest priority in frontier (lowest cost) and parses its info

        estimated_cost,current_cost, current_location, current_parent = frontier.get()
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
                    estimated_cost = current_cost + float(graph[(xn,yn)][2]) + heuristics(node, goal_location)
                    node_cost = current_cost + float(graph[(xn,yn)][2])
                print(node_cost)
            # Add value to frontier
                frontier.put((estimated_cost,node_cost, node, current_location))
 
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
        #explored list returns 0 or 1 elements when the snake dies
        if len(explored_list) <= 1:
            path.append(node)   #band aid fix, technically shouldn't be returning the goal node as path
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