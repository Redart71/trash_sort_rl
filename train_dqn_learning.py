import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random
from env.gym_wrapper import GymTrashSortWrapper
import cv2
import argparse
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Argument pour reprise d'entraînement ===
parser = argparse.ArgumentParser()
parser.add_argument("--resume", action="store_true", help="Reprendre l'entraînement depuis le dernier checkpoint")
args = parser.parse_args()

# === Réseau de neurones CNN ===
class DQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )

        with torch.no_grad():
            dummy_input = torch.zeros(1, *input_shape)
            conv_out = self.conv(dummy_input)
            conv_out_size = conv_out.view(1, -1).shape[1]

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions)
        )

    def forward(self, x):
        x = x.float() / 255.0
        x = self.conv(x)
        x = self.fc(x)
        return x

# === Hyperparamètres ===
epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.995
gamma = 0.99
lr = 1e-4
batch_size = 32
replay_buffer = deque(maxlen=10000)
n_episodes = 500
max_steps = 1000
update_target_freq = 10

# === Initialisation ===
env = GymTrashSortWrapper(render_mode=False)
n_actions = env.action_space.n

def preprocess(obs):
    obs = cv2.resize(obs, (160, 90))
    obs = obs.astype(np.float32) / 255.0
    obs = np.transpose(obs, (2, 0, 1))
    return obs

obs = preprocess(env.reset())
input_shape = obs.shape

policy_net = DQN(input_shape=input_shape, n_actions=n_actions).to(device)
target_net = DQN(input_shape=input_shape, n_actions=n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.Adam(policy_net.parameters(), lr=lr)
loss_fn = nn.MSELoss()

scores = []
start_episode = 0

# === Reprise de l'entraînement ===
if args.resume and os.path.exists("checkpoint.pth"):
    checkpoint = torch.load("checkpoint.pth", map_location=device)
    policy_net.load_state_dict(checkpoint['model_state_dict'])
    target_net.load_state_dict(checkpoint['target_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epsilon = checkpoint['epsilon']
    scores = checkpoint['scores']
    start_episode = checkpoint['episode'] + 1
    print(f"✅ Reprise de l'entraînement à l'épisode {start_episode}")
elif args.resume:
    print("⚠️ Aucun checkpoint trouvé. Démarrage d’un nouvel entraînement.")

best_score = max(scores) if scores else float('-inf')


# === Boucle d'entraînement ===
for episode in range(start_episode, n_episodes):
    obs = preprocess(env.reset())
    total_reward = 0

    for t in range(max_steps):
        if np.random.rand() < epsilon:
            action = random.randrange(n_actions)
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(obs, device=device).unsqueeze(0)
                q_values = policy_net(state_tensor)
                action = q_values.argmax().item()

        next_obs, reward, done, _ = env.step(action)
        next_obs = preprocess(next_obs)

        replay_buffer.append((obs, action, reward, next_obs, done))
        obs = next_obs
        total_reward += reward

        if len(replay_buffer) >= batch_size:
            minibatch = random.sample(replay_buffer, batch_size)
            states, actions, rewards, next_states, dones = zip(*minibatch)

            states = torch.tensor(np.array(states), device=device)
            actions = torch.tensor(actions, device=device).unsqueeze(1)
            rewards = torch.tensor(rewards, device=device).unsqueeze(1)
            next_states = torch.tensor(np.array(next_states), device=device)
            dones = torch.tensor(dones, device=device).unsqueeze(1)

            q_values = policy_net(states).gather(1, actions)
            with torch.no_grad():
                max_next_q_values = target_net(next_states).max(1)[0].unsqueeze(1)
                target_q = rewards + gamma * max_next_q_values * (~dones)

            loss = loss_fn(q_values, target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if done:
            break

    scores.append(total_reward)
    if total_reward > best_score:
        best_score = total_reward
        torch.save(policy_net.state_dict(), "best_model.pth")
        print(f"💾 Nouveau meilleur modèle sauvegardé ! Score: {best_score}")

    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if episode % update_target_freq == 0:
        target_net.load_state_dict(policy_net.state_dict())

    print(f"Episode {episode+1} | Score: {total_reward} | Epsilon: {epsilon:.3f}")

    # === Sauvegarde du checkpoint ===
    torch.save({
        'episode': episode,
        'model_state_dict': policy_net.state_dict(),
        'target_state_dict': target_net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'epsilon': epsilon,
        'scores': scores
    }, "checkpoint.pth")

# === Sauvegarde finale du modèle uniquement ===
policy_net.eval()
torch.save(policy_net.state_dict(), "dqn_trash_sort.pth")

env.close()
