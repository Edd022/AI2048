import numpy as np
import random

class Game2048:
    def __init__(self):
        self.size = 4
        self.score = 0
        self.reset()

    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def get_board(self):
        return self.board.copy()

    def get_score(self):
        return self.score

    def add_random_tile(self):
        empty_cells = list(zip(*np.where(self.board == 0)))
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(self.size):
            original = self.board[i].copy()
            row = self.compress(self.board[i])
            row = self.merge(row)
            row = self.compress(row)
            self.board[i] = row
            if not np.array_equal(original, row):
                moved = True
        return moved

    def move_right(self):
        self.board = np.fliplr(self.board)
        moved = self.move_left()
        self.board = np.fliplr(self.board)
        return moved

    def move_up(self):
        self.board = self.board.T
        moved = self.move_left()
        self.board = self.board.T
        return moved

    def move_down(self):
        self.board = np.flipud(self.board.T)
        moved = self.move_left()
        self.board = np.flipud(self.board).T
        return moved

    def move(self, direction):
        directions = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down
        }
        if direction in directions:
            moved = directions[direction]()
            if moved:
                self.add_random_tile()
            return moved
        else:
            raise ValueError("Invalid move direction")

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
                if self.board[j][i] == self.board[j + 1][i]:
                    return True
        return False
