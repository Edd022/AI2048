# 🧠 Workshop 3 - Reinforcement Learning Agent for 2048

This repository contains the implementation of a Deep Q-Network (DQN) agent for the game **2048**, developed as part of Workshop 3 at Universidad Distrital Francisco José de Caldas. The project integrates reinforcement learning, cybernetic feedback concepts, and a custom environment simulation.

## 🎯 Objective

Develop an autonomous agent using **Deep Q-Learning (DQN)** capable of learning strategies to reach or exceed the 2048 tile by maximizing cumulative reward through interaction with a simulated environment.

## 🗂️ Project Structure

Workshop_3/
├── dqn_agent.py # DQN agent class and training logic
├── env_2048.py # Custom 2048 environment interface
├── game_logic.py # Core logic for tile movement and game rules
├── random_agent.py # Baseline random agent
├── game_2048.py # GUI with random agent
├── Test_dqn.py # GUI and evaluation for the DQN agent

markdown
Copiar
Editar

## 🚀 Features

- ✅ Custom simulation of the 2048 environment (no Gymnasium required)  
- ✅ DQN agent using PyTorch  
- ✅ Feedback loop based on board state and score  
- ✅ Reward function based on score delta, tile value, and empty cell count  
- ✅ Baseline random agent for comparison  
- ✅ Visual testing via Pygame GUI  

## 🧪 Running the Agent

### ▶️ To test the trained DQN agent (GUI):
```bash
python Test_dqn.py
If the model file dqn_model.pth exists, it will be loaded automatically. If not, the agent plays untrained.

🎲 To run the random agent (GUI):
bash
Copiar
Editar
python game_2048.py
📦 Dependencies
Install dependencies with:

bash
Copiar
Editar
pip install torch numpy pygame
ℹ️ Gymnasium is not used due to compatibility issues; the environment is implemented manually.

📈 Current Status
DQN shows more consistent performance and better scores than a random agent.

Training is still ongoing to improve convergence.

The reward function and feedback loop are being refined.

Monte Carlo Tree Search (MCTS) is a candidate for future comparison.

🔮 Future Work
Add a second feedback loop (e.g., based on mobility or clustering)

Improve reward shaping for better learning signals

Compare DQN agent vs. MCTS agent

Add plots to track learning progress

Move training to GPU for performance boost

👥 Authors
Edward Julian Garcia Gaitan

Miguel Alejandro Chavez Porras

Artificial Intelligence – Workshop 3
Universidad Distrital Francisco José de Caldas – 2025
