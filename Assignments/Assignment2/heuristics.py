import math
import copy

def base_heuristic(curr_state):

    """
    base huerisitc, player1 moves minus player2
    :rtype: object
    """
    player = curr_state.get_curr_player()
    curr_state.set_curr_player(1)
    p1_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(2)
    p2_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(player)
    return p1_moves - p2_moves



def advanced_heuristic(curr_state):
    return defensive_to_offensive_abs(curr_state)


def simple(curr_state):
    sign = -1 if curr_state.get_curr_player() == 2 else 1 #player 2 is minimizing
    return sign * len(curr_state.potential_moves())

def defensive(curr_state):
    sign = -1 if curr_state.get_curr_player() == 2 else 1 #player 2 is minimizing
    len_player_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(curr_state.get_curr_player() % 2 + 1)
    len_opponent_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(curr_state.get_curr_player() % 2 + 1)
    return sign * ((len_player_moves * 2) - len_opponent_moves)

def defensive_abs(curr_state):
    curr_state.set_curr_player(1)
    p1_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(2)
    p2_moves = len(curr_state.potential_moves())
    return (p1_moves * 2) - p2_moves

def offensive(curr_state):
    sign = -1 if curr_state.get_curr_player() == 2 else 1 #player 2 is minimizing
    len_player_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(curr_state.get_curr_player() % 2 + 1)
    len_opponent_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(curr_state.get_curr_player() % 2 + 1)
    return sign * (len_player_moves - (len_opponent_moves * 2))

def offensive_abs(curr_state):
    curr_state.set_curr_player(1)
    p1_moves = len(curr_state.potential_moves())
    curr_state.set_curr_player(2)
    p2_moves = len(curr_state.potential_moves())
    return p1_moves - (p2_moves * 2)

def defensive_to_offensive(curr_state):
    width = len(curr_state.get_grid())
    height = len(curr_state.get_grid()[0])
    ratio = ply_count(curr_state) / (width * height)
    return defensive(curr_state) if ratio <= 0.5 else offensive(curr_state)

def defensive_to_offensive_abs(curr_state):
    width = len(curr_state.get_grid())
    height = len(curr_state.get_grid()[0])
    ratio = ply_count(curr_state) / (width * height)
    return defensive_abs(curr_state) if ratio <= 0.5 else offensive_abs(curr_state)

def offensive_to_defensive(curr_state):
    height = len(curr_state.get_grid())
    width = len(curr_state.get_grid()[0])
    ratio = ply_count(curr_state) / (width * height)
    return offensive(curr_state) if ratio <= 0.5 else defensive(curr_state)
def offensive_to_defensive_abs(curr_state):
    height = len(curr_state.get_grid())
    width = len(curr_state.get_grid()[0])
    ratio = ply_count(curr_state) / (width * height)
    return offensive_abs(curr_state) if ratio <= 0.5 else defensive_abs(curr_state)

def walls(curr_state):
    dis = distance(curr_state)
    if dis >= 2:
        return defensive(curr_state)
    else: # Favor the center of the board.
        return base_heuristic(curr_state)

def walls_abs(curr_state):
    dis = distance(curr_state)
    if dis >= 2:
        return defensive_abs(curr_state)
    else: # Favor the center of the board.
        return base_heuristic(curr_state)
def ply_count(curr_state):
    count = 0
    for row in curr_state.get_grid():
        for value in row:
            if value == curr_state.get_curr_player():
                count += 1
    return count

def distance(curr_state):
    # Calculate the distance between the two positions using Manhattan distance
    return math.sqrt((curr_state.get_player_locations()[1][0] - curr_state.get_player_locations()[2][0]) ** 2 + (curr_state.get_player_locations()[1][1] - curr_state.get_player_locations()[2][1])**2)
