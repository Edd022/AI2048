import numpy as np
from game_logic import Game2048

class Env2048:
    def __init__(self):
        self.game = Game2048()
        self.action_space = [0,1,2,3]  # 0: up, 1: down, 2: left, 3: right
        self.action_map = {0:'up',1:'down',2:'left',3:'right'}

    def reset(self):
        self.game.reset()
        return self.get_observation()

    def step(self, action):
        direction = self.action_map[action]
        score_before = self.game.get_score()
        board_before = self.game.get_board().copy()

        moved = self.game.move(direction)
        board_after = self.game.get_board()
        score_after = self.game.get_score()

        if not moved:
            reward = -5  # penalización por movimiento inválido
        else:
            score_delta = score_after - score_before

            empty_cells = np.count_nonzero(board_after == 0)
            empty_bonus = empty_cells * 0.5

            max_tile = np.max(board_after)
            max_tile_bonus = np.log2(max_tile) if max_tile > 0 else 0

            reward = score_delta + empty_bonus + max_tile_bonus

        done = not self.game.can_move()

        return self.get_observation(), reward, done, {}

    def get_observation(self):
        return self.game.get_board().astype(np.float32)

    def render(self):
        print("Score:", self.game.get_score())
        print(self.game.get_board())
