import numpy as np
from .trash_object import TrashObject

class TrashSortGymEnv:
    def __init__(self):
        self.categories = ["Plastique", "Papier" ,"Verre", "Non recyclable"]
        self.action_space = 5  # 0=jaune, 1=bleue, 2=verte, 3=noire, 4=rien faire
        self.reset()

    def reset(self):
        self.trash_queue = [TrashObject.generate_random(headless=True) for _ in range(3)]
        self.current_step = 0
        self.max_steps = 1800
        self.score = 0
        return self._get_observation()

    def step(self, action):
        done = False
        reward = 0

        if len(self.trash_queue) == 0:
            self.trash_queue.append(TrashObject.generate_random(headless=True))

        obj = self.trash_queue.pop(0)

        if action < 4:
            selected_bin = self.categories[action]
            if obj.category == selected_bin:
                reward = 1
                self.score += 1
            else:
                reward = -1
                self.score -= 1
        else:
            reward = -1

        self.trash_queue.append(TrashObject.generate_random(headless=True))

        self.current_step += 1

        if self.current_step >= self.max_steps:
            done = True

        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        obj = self.trash_queue[0]
        return self.categories.index(obj.category)

    def render(self):
        print(f"Étape {self.current_step} | Score: {self.score} | Objet: {self.trash_queue[0].name}")

    def close(self):
        pass