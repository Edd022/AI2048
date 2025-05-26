import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import copy
from collections import deque

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, output_dim)
        )

    def forward(self, x):
        return self.model(x)

class DQNAgent:
    def __init__(self, state_shape, action_size, lr=0.001, gamma=0.99,
                 epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.995, update_freq=10):
        self.state_shape = state_shape
        self.action_size = action_size
        self.memory = deque(maxlen=50000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = 64
        self.update_freq = update_freq
        self.model = QNetwork(np.prod(state_shape), action_size)
        self.target_model = copy.deepcopy(self.model)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        self.train_step = 0

    def preprocess(self, state):
        # Convertir cada celda a log2 (si > 0) o 0
        log_state = np.where(state > 0, np.log2(state), 0)
        return log_state.astype(np.float32)

    def select_action(self, state):
        state = self.preprocess(state)
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(np.array([self.preprocess(s) for s in states]), dtype=torch.float32)
        next_states = torch.tensor(np.array([self.preprocess(s) for s in next_states]), dtype=torch.float32)
        actions = torch.tensor(actions)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        with torch.no_grad():
            next_q_values = self.target_model(next_states).max(1)[0]
            targets = rewards + self.gamma * next_q_values * (~dones)

        loss = self.loss_fn(q_values, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Actualización de red objetivo cada cierto número de pasos
        self.train_step += 1
        if self.train_step % self.update_freq == 0:
            self.target_model.load_state_dict(self.model.state_dict())
