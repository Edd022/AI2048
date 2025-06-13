import numpy as np
import random

class Game2048:
    def __init__(self):
        self.size = 4
        self.score = 0
        self.reset()

    def reset(self):
        # Reiniciar tablero y puntaje
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        # Añadir 2 fichas nuevas
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
        moved = False
        for j in range(self.size):
            col = self.board[:, j].copy()
            original = col.copy()
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            self.board[:, j] = col
            if not np.array_equal(original, col):
                moved = True
        return moved

    def move_down(self):
        moved = False
        for j in range(self.size):
            col = self.board[:, j].copy()[::-1]
            original = self.board[:, j].copy()
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            self.board[:, j] = col[::-1]
            if not np.array_equal(original, self.board[:, j]):
                moved = True
        return moved

    def move(self, direction, simulate=False):
        directions = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down
        }
        if direction in directions:
            moved = directions[direction]()
            if moved and not simulate:
                self.add_random_tile()
            return moved
        else:
            raise ValueError("Invalid move direction")

    def can_move_in_direction(self, direction):
        # Crear juego temporal para simular movimiento sin cambiar estado real
        temp_game = Game2048()
        temp_game.board = np.copy(self.board)
        temp_game.score = self.score
        return temp_game.move(direction, simulate=True)

    def can_move(self):
        # Si puede moverse en alguna dirección, entonces no es game over
        return any(self.can_move_in_direction(dir) for dir in ['left', 'right', 'up', 'down'])


# --- TEST rápido para validar reset y estado inicial ---
if __name__ == "__main__":
    game = Game2048()
    board = game.get_board()
    print("Tablero inicial:")
    print(board)
    print("Número de casillas ocupadas (debe ser 2):", np.sum(board > 0))
    print("¿Puede moverse?:", game.can_move())
