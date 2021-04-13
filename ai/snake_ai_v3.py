##
# this file implements a uniform cost search snake ai
# simply chooses the best path based on path cost

from game_data import *
from helper_functions import *
from ai import snake_ai_helper_functions as hf


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
        for node in hf.neighbourhood(grid, current[0]):
            if not hf.is_node_in_list(node, frontier) and not hf.is_node_in_list(node, explored):
                # if node not in frontier and node not in explored:
                frontier.append((node, current[1]+1, current[0]))
    # create path
    path = hf.create_path_to_coin(explored)
    return path


def uniform_cost_search():
    '''
    using unfiorm cost search
    create a path from snake head to coin
    start_state = snake head
    goal_state = coin
    explored = [([row, col], cost, parent)]
    '''
    grid = hf.get_reachable_squares()
    start_state = (game_data["snake"][0], 0, None)
    goal_state = game_data["coin"]
    if goal_state not in grid:
        goal_state = None
    path = []
    # if goal_state is not in grid of currently reachable nodes
    # then continue on a path that does not kill snake
    # if goal_state not in grid:
    if goal_state != game_data["coin"]:
        # choose a random position next
        # finding longest path takes much to long to calculate
        path = hf.make_random_move(grid, game_data["snake"][0])
        # this should actually take a step in a direction such that it has the most reachable squares left
    else:
        path = find_path_to_coin(grid, start_state, goal_state)
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
    hf.update_snake_ai_v1()
    return ret
