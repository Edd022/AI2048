import pygame
import sys
from env_2048 import Env2048
from random_agent import RandomAgent

# Configuración visual
TILE_SIZE = 100
TILE_MARGIN = 10
BOARD_SIZE = 4
WIDTH = HEIGHT = BOARD_SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN

BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

env = Env2048()
agent = RandomAgent(env.action_space)
obs = env.reset()

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
    draw_board()

    if auto_play:
        pygame.time.wait(300)
        action = agent.select_action(obs)
        obs, reward, done, _ = env.step(action)
        print(f"Acción: {action} | Recompensa: {reward} | Score: {env.game.get_score()}")

        if done:
            print("Game Over!")
            pygame.time.wait(2000)
            obs = env.reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto_play = not auto_play

            elif not auto_play:
                if event.key == pygame.K_LEFT:
                    env.game.move('left')
                elif event.key == pygame.K_RIGHT:
                    env.game.move('right')
                elif event.key == pygame.K_UP:
                    env.game.move('up')
                elif event.key == pygame.K_DOWN:
                    env.game.move('down')

                if not env.game.can_move():
                    print("Game Over!")
                    pygame.time.wait(2000)
                    obs = env.reset()

    clock.tick(10)
