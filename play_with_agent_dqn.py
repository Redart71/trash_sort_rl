import torch
import torch.nn as nn
import numpy as np
import time
import cv2
from env.gym_wrapper import GymTrashSortWrapper

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Prétraitement des observations ===
def preprocess(obs):
    obs = cv2.resize(obs, (160, 90))  # Largeur x Hauteur
    obs = obs.astype(np.float32)
    obs = np.transpose(obs, (2, 0, 1))  # Channels first : (C, H, W)
    return obs

# === Classe du modèle DQN ===
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

# === Initialisation de l'environnement ===
env = GymTrashSortWrapper(render_mode=True)
obs = preprocess(env.reset())
input_shape = obs.shape
n_actions = env.action_space.n

# === Chargement du modèle ===
model = DQN(input_shape=input_shape, n_actions=n_actions).to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

# === Boucle de jeu ===
done = False
total_reward = 0

while not done:
    state = torch.from_numpy(obs).unsqueeze(0).to(device)
    with torch.no_grad():
        q_values = model(state)
        action = q_values.argmax().item()

    obs, reward, done, _ = env.step(action)
    obs = preprocess(obs)
    total_reward += reward
    print(f"Action: {action} | Reward: {reward}")

    time.sleep(0.05)  # ralentir pour visualiser

print(f"✅ Partie terminée | Score total: {total_reward}")
env.close()
