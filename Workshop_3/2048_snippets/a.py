# evaluate_agents.py
import numpy as np
import torch
from env_2048 import Env2048
from dqn_agent import DQNAgent
from random_agent import RandomAgent  # asumiendo que existe

def evaluate_random(env, num_episodes):
    scores = []
    max_tiles = []
    for ep in range(num_episodes):
        state = env.reset()
        done = False
        total_score = 0
        while not done:
            action = RandomAgent(env.action_space).select_action(state)
            next_state, reward, done, _ = env.step(action)
            total_score = env.game.get_score()
            state = next_state
        scores.append(total_score)
        max_tiles.append(np.max(env.game.get_board()))
    return np.array(scores), np.array(max_tiles)

def evaluate_dqn(env, agent, num_episodes):
    scores = []
    max_tiles = []
    agent.epsilon = 0.0  # exploitation only
    for ep in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)
            state = next_state
        total_score = env.game.get_score()
        scores.append(total_score)
        max_tiles.append(np.max(env.game.get_board()))
    return np.array(scores), np.array(max_tiles)

def main():
    env = Env2048()
    # Carga modelo entrenado si existe
    agent = DQNAgent(state_shape=(4,4), action_size=4)
    try:
        agent.model.load_state_dict(torch.load("dqn_model.pth"))
        agent.model.eval()
        print("Loaded pretrained DQN model.")
    except FileNotFoundError:
        print("Pretrained model not found. Evaluate untrained agent (may be poor).")

    num_episodes = 50  # o 100 o más según tiempo disponible
    print("Evaluating random agent...")
    rand_scores, rand_max = evaluate_random(env, num_episodes)
    print(f"Random agent: mean score {rand_scores.mean():.1f} ± {rand_scores.std():.1f}, "
          f"mean max tile {rand_max.mean():.1f} ± {rand_max.std():.1f}")

    print("Evaluating DQN agent...")
    dqn_scores, dqn_max = evaluate_dqn(env, agent, num_episodes)
    print(f"DQN agent: mean score {dqn_scores.mean():.1f} ± {dqn_scores.std():.1f}, "
          f"mean max tile {dqn_max.mean():.1f} ± {dqn_max.std():.1f}")

    # Opcional: guardar arrays en archivos .npz o CSV para análisis posterior
    np.savez("eval_random.npz", scores=rand_scores, max_tiles=rand_max)
    np.savez("eval_dqn.npz", scores=dqn_scores, max_tiles=dqn_max)

if __name__ == "__main__":
    main()
