import random
from .logic import BOARD_SIZE


def get_ai_move(board):
    empty = [
        (x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if board[y][x] == 0
    ]
    return random.choice(empty) if empty else None
