
import chess
from math import inf
import multiprocessing
from functools import partial


def evaluate(board, maximizing_color):
    AIscore = 0
    notAIscore = 0
    for (piece, value) in [(chess.PAWN, 1),
                           (chess.BISHOP, 4),
                           (chess.KING, 0),
                           (chess.QUEEN, 10),
                           (chess.KNIGHT, 5),
                           (chess.ROOK, 3)]:

        AIscore += len(board.pieces(piece, maximizing_color)) * value
        notAIscore += len(board.pieces(piece, not maximizing_color)) * value
    return AIscore - notAIscore


def minimax(board, depth, alpha, beta, maximizing_player, maximizing_color):
    if depth == 0 or board.is_game_over == True:
        return None, evaluate(board, maximizing_color)
    moves = list(board.legal_moves)
    best_move = None

    if maximizing_player:
        max_eval = -inf
        for move in moves:

            board.push(move)
            current_eval = minimax(
                board, depth - 1, alpha, beta, False, maximizing_color)[1]
            board.pop()
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move

            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:

            board.push(move)
            current_eval = minimax(
                board, depth - 1, alpha, beta, True, maximizing_color)[1]
            board.pop()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move

            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval


def parallelMinMax(board, depth, alpha, beta, maximizing_player, maximizing_color):
    if depth == 0 or board.is_game_over == True:
        return None, evaluate(board, maximizing_color)

    def legalMoves():
        with multiprocessing.Pool(12) as pool:
            prod_x = partial(helper_function, depth, board, alpha, beta,
                             maximizing_player, maximizing_color)
            yield from pool.map(prod_x, list(board.legal_moves))
    result = sorted(legalMoves(), key=lambda x: x[1], reverse=True)[:1]
    best_move, alpha = result[0]

    return best_move, alpha


def helper_function(depth, board, alpha, beta, maximizing_player, maximizing_color, move):
    best_move = None
    board.push(move)
    score = minimax(board, depth-1, alpha, beta,
                    not maximizing_player, maximizing_color)[1]
    board.pop()
    if score > alpha:
        alpha = score
        best_move = move
    if score > beta:
        return beta
    return best_move, alpha
