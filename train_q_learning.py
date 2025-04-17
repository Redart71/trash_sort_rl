import numpy as np
import matplotlib.pyplot as plt
from env.gym_wrapper import GymTrashSortWrapper

# Paramètres Q-learning
alpha = 0.1    
gamma = 0.99      
epsilon = 1.0
epsilon_min = 0.05
epsilon_decay = 0.995

n_episodes = 1000
max_steps = 1800

# Initialiser environnement et Q-table
env = GymTrashSortWrapper()
n_states = env.observation_space.n
n_actions = env.action_space.n

Q = np.zeros((n_states, n_actions))
scores = []

for episode in range(n_episodes):
    state = env.reset()
    total_reward = 0

    for t in range(max_steps):
        # Politique epsilon-greedy
        if np.random.rand() < epsilon:
            action = np.random.choice(n_actions)
        else:
            action = np.argmax(Q[state])

        next_state, reward, done, _ = env.step(action)

        # Mise à jour Q-table
        best_next_action = np.max(Q[next_state])
        Q[state, action] += alpha * (reward + gamma * best_next_action - Q[state, action])

        state = next_state
        total_reward += reward

        if done:
            break

    # Décroissance d'epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    scores.append(total_reward)

    if (episode + 1) % 50 == 0:
        avg = np.mean(scores[-50:])
        print(f"Episode {episode+1}/{n_episodes} | Moyenne score (50 derniers) : {avg:.2f} | Epsilon: {epsilon:.3f}")


import seaborn as sns

# Affichage de la Q-table
plt.figure(figsize=(8, 4))
sns.heatmap(Q, annot=True, cmap="YlGnBu", xticklabels=["jaune", "bleue", "verte", "noire", "rien"], yticklabels=["jaune", "bleue", "verte", "noire"])
plt.title("Q-table finale (valeurs Q)")
plt.xlabel("Actions")
plt.ylabel("États (type de déchet)")
plt.show()

# Affichage final
plt.plot(scores)
plt.title("Score total par épisode")
plt.xlabel("Épisode")
plt.ylabel("Score")
plt.grid()
plt.show()

env.close()