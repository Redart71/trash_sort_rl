import gym
from env.gym_wrapper import GymTrashSortWrapper

env = GymTrashSortWrapper()
obs = env.reset()

done = False
total_reward = 0

while not done:
    action = env.action_space.sample()  # agent aléatoire
    obs, reward, done, _ = env.step(action)
    total_reward += reward
    env.render()

print(f"Score total de l'agent aléatoire : {total_reward}")
