import math
h = None

def alphabeta_max_h(current_game, _heuristic, depth=3, alpha=-math.inf, beta=math.inf):
    global h
    h = _heuristic
    if current_game.is_terminal() or depth == 0:
        return h(current_game), None

    v = -math.inf
    moves = current_game.get_moves()
    best_move = None

    for move in moves:
        mx, _ = alphabeta_min_h(move, _heuristic, depth - 1, alpha, beta)
        if v < mx:
            v = mx
            best_move = move
        alpha = max(alpha, v)

        if alpha >= beta:
            return v, None  # Alpha cut-off

    return v, best_move

def alphabeta_min_h(current_game, _heuristic, depth=3, alpha=-math.inf, beta=math.inf):
    global h
    h = _heuristic
    if current_game.is_terminal() or depth == 0:
        return h(current_game), None

    v = math.inf
    moves = current_game.get_moves()
    best_move = None

    for move in moves:
        mx, _ = alphabeta_max_h(move, _heuristic, depth - 1, alpha, beta)
        if v > mx:
            v = mx
            best_move = move
        beta = min(beta, v)

        if alpha >= beta:
            return v, None  # Beta cut-off

    return v, best_move
