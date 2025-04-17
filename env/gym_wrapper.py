import gym
from gym import spaces
from .rl_env import TrashSortGymEnv
import numpy as np

class GymTrashSortWrapper(gym.Env):
    def __init__(self):
        super(GymTrashSortWrapper, self).__init__()

        self.env = TrashSortGymEnv()
        self.action_space = spaces.Discrete(5)  # 0 à 4
        self.observation_space = spaces.Discrete(4)  # 0 à 3 (catégories)

    def reset(self):
        obs = self.env.reset()
        return obs

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return obs, reward, done, info

    def render(self, mode="human"):
        self.env.render()

    def close(self):
        self.env.close()