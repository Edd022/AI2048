import numpy as np
from random import randint, random

n = 4

def new_game(n=4):
    return [[0] * n for _ in range(n)]

class board:
    def __init__(self):
        self.state = np.array(new_game(n))
        self.score = 0
        self.over = False
        self.win = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = list(zip(*np.where(self.state == 0)))
        if not empty:
            return
        i, j = empty[randint(0, len(empty) - 1)]
        self.state[i][j] = 2 if random() < 0.9 else 4

    def game_state(self):
        self.over = not any(self.valid_move(move) for move in ['up', 'down', 'left', 'right'])
        if 2048 in self.state:
            self.win = True

    def valid_move(self, direction):
        test = board()
        test.state = self.state.copy()
        test.score = self.score
        try:
            test.move(direction)
            return not np.array_equal(test.state, self.state)
        except:
            return False

    def move(self, direction):
        rotated = self.rotate(direction)
        moved, gained = self.merge(rotated)
        unrotated = self.unrotate(moved, direction)
        if not np.array_equal(self.state, unrotated):
            self.state = unrotated
            self.score += gained
            self.add_random_tile()

    def rotate(self, direction):
        if direction == 'up':
            return np.rot90(self.state, 1)
        elif direction == 'down':
            return np.rot90(self.state, -1)
        elif direction == 'left':
            return self.state.copy()
        elif direction == 'right':
            return np.fliplr(self.state)

    def unrotate(self, mat, direction):
        if direction == 'up':
            return np.rot90(mat, -1)
        elif direction == 'down':
            return np.rot90(mat, 1)
        elif direction == 'left':
            return mat
        elif direction == 'right':
            return np.fliplr(mat)

    def merge(self, mat):
        score = 0
        new_mat = np.zeros_like(mat)
        for i in range(n):
            row = mat[i][mat[i] != 0]
            merged = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    merged.append(row[j] * 2)
                    score += row[j] * 2
                    skip = True
                else:
                    merged.append(row[j])
            new_mat[i, :len(merged)] = merged
        return new_mat, score
