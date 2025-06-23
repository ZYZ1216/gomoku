BOARD_SIZE = 15


class Gomoku:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.winner = None
        self.moves = []

    def make_move(self, x: int, y: int, player: int) -> bool:
        if self.board[y][x] != 0 or self.winner:
            return False
        self.board[y][x] = player
        self.moves.append((x, y, player))
        if self.check_win(x, y, player):
            self.winner = player
        return True

    def check_win(self, x: int, y: int, player: int) -> bool:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for d in [1, -1]:
                nx, ny = x + dx*d, y + dy*d
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[ny][nx] == player:
                    count += 1
                    nx += dx*d
                    ny += dy*d
            if count >= 5:
                return True
        return False
