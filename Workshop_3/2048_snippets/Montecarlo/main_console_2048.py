from game_defs_2048 import board
import numpy as np
import copy
from random import randint, choice
import time

options = ['up', 'down', 'left', 'right']

def print_board(b):
    print("Score:", b.score)
    for row in b.state:
        print(' '.join(f"{x:4}" if x != 0 else "   ." for x in row))
    print()

def mcts_move(b0, simulations=50, depth=10):
    scores = np.zeros(len(options))
    counts = np.zeros(len(options))

    for i in range(simulations):
        b_copy = copy.deepcopy(b0)
        first_move = None

        for d in range(depth):
            valid_moves = [i for i, move in enumerate(options) if b_copy.valid_move(move)]
            if not valid_moves:
                break
            move_idx = choice(valid_moves)
            if d == 0:
                first_move = move_idx
            b_copy.move(options[move_idx])
            b_copy.game_state()
            if b_copy.over:
                break

        if first_move is not None:
            scores[first_move] += b_copy.score
            counts[first_move] += 1

    avg_scores = scores / (counts + 1e-5)
    best_move = int(np.argmax(avg_scores))
    return options[best_move]

def play_game():
    b = board()
    b.game_state()
    while not b.over:
        print_board(b)
        move = mcts_move(b, simulations=30, depth=10)
        b.move(move)
        b.game_state()
        time.sleep(0.2)

    print_board(b)
    print("Game Over! Final Score:", b.score)

if __name__ == "__main__":
    play_game()
