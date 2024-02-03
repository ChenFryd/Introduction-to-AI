import math


def alphabeta_max(current_game, alpha=-math.inf, beta=math.inf):
    if current_game.is_terminal():
        return current_game.get_score(), None

    v = -math.inf
    moves = current_game.get_moves()
    best_move = None

    for move in moves:
        mx, _ = alphabeta_min(move, alpha, beta)
        if v < mx:
            v = mx
            best_move = move
        alpha = max(alpha, v)

        if alpha >= beta:
            return v, None  # Alpha cut-off

    return v, best_move

def alphabeta_min(current_game, alpha=-math.inf, beta=math.inf):
    if current_game.is_terminal():
        return current_game.get_score(), None

    v = math.inf
    moves = current_game.get_moves()
    best_move = None

    for move in moves:
        mx, _ = alphabeta_max(move, alpha, beta)
        if v > mx:
            v = mx
            best_move = move
        beta = min(beta, v)

        if alpha >= beta:
            return v, None  # Beta cut-off

    return v, best_move