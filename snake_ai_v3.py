##
# this file implements a uniform cost search snake ai
# simply chooses the best path based on path cost

import random
import sys
from itertools import permutations
from game_data import *
from helper_functions import *


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


def get_reachable_squares():
    '''
    return a array of [x,y] coordinates
    on the grid that are not snake or coin
    needs to only return array of elements that the head can currently reach
    '''
    snake_head = game_data["snake"][0]
    open_squares = get_open_squares()
    # print("\nget_reachable_squares())")
    # print("# of open_squares:", len(open_squares))
    # print("open_squares:", open_squares)
    # reachable = []
    reachable = [snake_head]
    # reachable.extend(neighbourhood(open_squares, snake_head))
    # print("init reachable len:", len(reachable))
    # print("init reachable:", reachable)
    # find all squares connected to the head of the snake that are open
    x = 0
    while True:
        # if x > len(reachable):
        #     break
        possible_neighbours = neighbourhood(open_squares, reachable[x])
        # print("possible_neighbours:", possible_neighbours)
        for possible_neighbour in possible_neighbours:
            # if not in list added
            if possible_neighbour not in reachable:
                reachable.append(possible_neighbour)
        # print("reachable len", len(reachable))
        # print("reachable", reachable)
        x += 1
        # if x == len(open_squares):
        #     break
        if x == len(reachable):
            break
    # remove head from reachable
    # we want possible moves, not current moves
    reachable.pop(0)
    # print("# of reachable squares:", len(reachable))
    # print("reachable squares:", reachable)
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
    # print("explored reversed:", explored)
    # print("path:", path)
    for node in explored:
        if path[0] == node[0]:
            # found start location
            if node[2] == snake_head:
                break
            path.insert(0, node[2])
        # print("path:", path)
    # print("final path:", path)
    return path


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
        # if possible_neighour not in grid:
        # possible_neighbours.remove(possible_neighour)
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


def find_path_to_coin(grid, start_state, goal_state):
    '''
    find and return path to coin
    '''
    path = []
    frontier = [start_state]
    explored = []
    while True:
        # nothing left to explore did not find path
        if frontier == []:
            return 1
        current = frontier.pop(0)
        explored.append(current)
        # found coin, add to path, break loop
        if current[0] == goal_state:
            break
        for node in neighbourhood(grid, current[0]):
            if not is_node_in_list(node, frontier) and not is_node_in_list(node, explored):
                # if node not in frontier and node not in explored:
                frontier.append((node, current[1]+1, current[0]))
    # create path
    # print("explored len:", len(explored))
    # print("explored:", explored)
    path = create_path_to_coin(explored)
    # print("path:", path)
    # print()
    return path


def make_random_move(grid, start_state):
    '''
    choose random valid node
    '''
    valid_moves = neighbourhood(grid, start_state)
    # print("\nmake_random_move()")
    # print("valid_moves:", valid_moves)
    if len(valid_moves) == 0:
        # print("move choosen:", [start_state[0], start_state[1]+1])
        return [[start_state[0], start_state[1]+1]]
    if len(valid_moves) == 1:
        # print("move choosen:", valid_moves)
        return valid_moves
    x = random.randint(0, len(valid_moves)-1)
    # print("move choosen:", valid_moves[x])
    return [valid_moves[x]]


def uniform_cost_search():
    '''
    using unfiorm cost search
    create a path from snake head to coin
    start_state = snake head
    goal_state = coin
    explored = [([row, col], cost, parent)]
    '''
    # grid = get_open_squares()
    grid = get_reachable_squares()
    start_state = (game_data["snake"][0], 0, None)
    goal_state = game_data["coin"]
    # print("\nuniform_cost_search()")
    if goal_state not in grid:
        # print("****************************\n*****COIN NOT REACHABLE*****\n****************************")
        goal_state = None
    path = []
    # print("start_state:", start_state[0])
    # print("goal_state:", goal_state)
    # print("grid:", grid)
    # if goal_state is not in grid of currently reachable nodes
    # then continue on a path that does not kill snake
    # if goal_state not in grid:
    if goal_state != game_data["coin"]:
        # choose a random position next
        # finding longest path takes much to long to calculate
        path = make_random_move(grid, game_data["snake"][0])
        # this should actually take a step in a direction such that it has the most reachable squares left
    else:
        path = find_path_to_coin(grid, start_state, goal_state)
    # print("path:", path)
    game_data["path"] = path
    return 0


def snake_ai_v3():
    '''
    path is created if path is currently empty
    new path is created every time a new coin is created
    '''
    ret = 0
    # if path is empty create a new path
    if game_data["path"] == []:
        ret = uniform_cost_search()
    # error occured in create_path_v0
    if ret == 1:
        print("snake_ai_v3 error")
        return ret
    update_snake_ai_v1()
    return ret
