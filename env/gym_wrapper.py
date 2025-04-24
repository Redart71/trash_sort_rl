import gym
from gym import spaces
import numpy as np
import pygame
from .rl_env import TrashSortGymEnv

class GymTrashSortWrapper(gym.Env):
    def __init__(self, render_mode=True):
        super(GymTrashSortWrapper, self).__init__()

        self.env = TrashSortGymEnv(render_mode=render_mode)
        self.action_space = spaces.Discrete(5)  # 5 types de tris
        self.observation_space = spaces.Box(low=0, high=255, shape=(600, 800, 3), dtype=np.uint8)

    def get_observation(self):
        screen_surface = self.env.screen
        if screen_surface:
            frame = pygame.surfarray.array3d(screen_surface)
            frame = np.transpose(frame, (1, 0, 2))  # (H, W, C)
            return frame
        else:
            return np.zeros((600, 800, 3), dtype=np.uint8)

    def reset(self):
        self.env.reset()
        return self.get_observation()

    def step(self, action):
        _, reward, done, info = self.env.step(action)
        obs = self.get_observation()
        return obs, reward, done, info

    def render(self, mode="human"):
        self.env.render()

    def close(self):
        self.env.close()
