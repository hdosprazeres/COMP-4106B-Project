
import math
import random
from game_data import *


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


def neighbourhood(grid, current):
    '''
    return a list of nodes around current
    current = [col, row]
    grid = [[col, row]] open square on grid
    '''
    possible_neighbours = [[current[0]+1, current[1]], [current[0]-1,
                                                        current[1]], [current[0], current[1]+1], [current[0], current[1]-1]]
    neighbours = []
    for possible_neighour in possible_neighbours:
        if possible_neighour in grid:
            neighbours.append(possible_neighour)
    # error, this function is returning invalid coords
    # return possible_neighbours
    return neighbours


def is_node_in_list(node, array):
    '''
    check if node exists in array
    node = [col, row]
    array = [([row, col], cost, parent)]
    '''
    for element in array:
        if node == element[0]:
            return True
    return False


def get_reachable_squares_v2(snake_head):
    '''
    return a array of [x,y] coordinates
    on the grid that are not snake or coin
    needs to only return array of elements that the head can currently reach
    '''
    open_squares = get_open_squares()
    reachable = [snake_head]
    # find all squares connected to the head of the snake that are open
    x = 0
    while True:
        possible_neighbours = neighbourhood(open_squares, reachable[x])
        for possible_neighbour in possible_neighbours:
            # if not in list added
            if possible_neighbour not in reachable:
                reachable.append(possible_neighbour)
        x += 1
        if x == len(reachable):
            break
    # remove head from reachable
    # we want possible moves, not current moves
    reachable.pop(0)
    return reachable


def get_reachable_squares():
    '''
    return a array of [x,y] coordinates
    on the grid that are not snake or coin
    needs to only return array of elements that the head can currently reach
    '''
    snake_head = game_data["snake"][0]
    open_squares = get_open_squares()
    reachable = [snake_head]
    # find all squares connected to the head of the snake that are open
    x = 0
    while True:
        # if x > len(reachable):
        #     break
        possible_neighbours = neighbourhood(open_squares, reachable[x])
        for possible_neighbour in possible_neighbours:
            # if not in list added
            if possible_neighbour not in reachable:
                reachable.append(possible_neighbour)
        x += 1
        if x == len(reachable):
            break
    # remove head from reachable
    # we want possible moves, not current moves
    reachable.pop(0)
    return reachable


def update_snake_ai_v1():
    '''
    update snake body
    by adding head to path head as new snake head
    '''
    new_head = game_data["path"].pop(0)
    game_data["snake"].insert(0, new_head)
    game_data["snake"].pop(-1)


def create_path_to_coin(explored):
    '''
    recreates path from explored list
    explored = [([row, col], cost, parent)]
    path = [[row, col]]
    '''
    snake_head = game_data["snake"][0]
    path = []
    explored.reverse()
    path.append(explored[0][0])
    for node in explored:
        if path[0] == node[0]:
            # found start location
            if node[2] == snake_head:
                break
            path.insert(0, node[2])
    return path


def make_random_move(grid, start_state):
    '''
    choose random valid node
    '''
    valid_moves = neighbourhood(grid, start_state)
    if len(valid_moves) == 0:
        return [[start_state[0], start_state[1]+1]]
    if len(valid_moves) == 1:
        return valid_moves
    x = random.randint(0, len(valid_moves)-1)
    return [valid_moves[x]]


def euclidean_distance(current_location, goal_location):
    '''
    calculate euclidean distance from current to goal
    '''
    heuristic = math.sqrt(
        (current_location[0] - goal_location[0])**2 + (current_location[1] - goal_location[1])**2)
    return heuristic


def manhattan_distance(current_location, goal_location):
    '''
    calculate euclidean distance from current to goal
    '''
    heuristic = abs(current_location[0] - goal_location[0]) + \
        abs(current_location[1] - goal_location[1])
    return heuristic


def take_move_biggest_reachable(grid, start_state):
    '''
    choose node that has the largest reachable space
    '''
    valid_moves = neighbourhood(grid, start_state)
    open_spaces = []
    if grid == []:
        return [[start_state[0], start_state[1]+1]]
    for move in valid_moves:
        open_space = len(get_reachable_squares_v2(move))
        open_spaces.append(open_space)
    index = 0
    spaces = 0
    for i in range(len(open_spaces)):
        if open_spaces[i] > spaces:
            index = i
            spaces = open_spaces[i]
    return [valid_moves[index]]
