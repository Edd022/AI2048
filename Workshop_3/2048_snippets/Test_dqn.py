import pygame
import sys
import torch
import numpy as np
from env_2048 import Env2048
from dqn_agent import DQNAgent

TILE_SIZE = 100
TILE_MARGIN = 10
BOARD_SIZE = 4
WIDTH = HEIGHT = BOARD_SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN

BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
    8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
    64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
    512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

env = Env2048()
agent = DQNAgent(state_shape=(4, 4), action_size=4)
obs = env.reset()

try:
    agent.model.load_state_dict(torch.load("dqn_model.pth"))
    agent.model.eval()
    agent.epsilon = 0.0
    print("Modelo cargado con éxito.")
except FileNotFoundError:
    print("Modelo no encontrado. Jugando con el agente sin entrenar.")

auto_play = True

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    board = env.game.board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            value = board[i][j]
            rect = pygame.Rect(
                j * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                i * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                TILE_SIZE, TILE_SIZE
            )
            color = TILE_COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, rect)

            if value != 0:
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    score_text = font.render(f"Score: {env.game.get_score()}", True, (0,0,0))
    screen.blit(score_text, (10, HEIGHT - 50))
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto_play = not auto_play
            elif not auto_play:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = env.game.move('left')
                elif event.key == pygame.K_RIGHT:
                    moved = env.game.move('right')
                elif event.key == pygame.K_UP:
                    moved = env.game.move('up')
                elif event.key == pygame.K_DOWN:
                    moved = env.game.move('down')

                if moved:
                    obs = env.get_observation()

                draw_board()

                if not env.game.can_move():
                    print("Game Over!")
                    print(env.game.get_board())
                    pygame.time.wait(2000)
                    obs = env.reset()
                    draw_board()

    if auto_play:
        pygame.time.wait(300)
        action = agent.select_action(obs)
        obs, reward, done, _ = env.step(action)
        print(f"Acción: {action} | Recompensa: {reward:.2f} | Score: {env.game.get_score()}")

        draw_board()

        if done:
            print("Game Over!")
            print(env.game.get_board())
            pygame.time.wait(2000)
            obs = env.reset()
            draw_board()

    clock.tick(60)  # 60 FPS, controla suavidad y rendimiento