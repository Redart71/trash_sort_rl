import numpy as np
import pygame
from .trash_object import TrashObject
from .trash_env import TrashSortEnv  # Assure-toi que c’est bien le bon chemin

class TrashSortGymEnv:
    def __init__(self, screen_width=800, screen_height=600, render_mode=False):
        self.categories = ["Plastique", "Papier" ,"Verre", "Non recyclable"]
        self.action_space = 5  # 0=jaune, 1=bleue, 2=verte, 3=noire, 4=rien faire

        self.render_mode = render_mode
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialisation du moteur Pygame si nécessaire
        if self.render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Trash Sort RL")

            self.env = TrashSortEnv(screen_width, screen_height)
            self.env.load_assets()
        else:
            self.screen = None
            self.trash_queue = []
        
        self.current_step = 0
        self.max_steps = 1800
        self.score = 0

    def reset(self):
        self.current_step = 0
        self.score = 0

        if self.render_mode:
            self.env.reset()
            self.render()
        else:
            self.trash_queue = [TrashObject.generate_random(headless=True) for _ in range(3)]

        return self._get_observation()

    def step(self, action):
        done = False
        reward = 0

        if self.render_mode:
            # Mapping action vers label
            label = self.categories[action] if action < 4 else None
            self.env.handle_action(label)
            self.env.update()
            self.render()
            reward = self.env.score  # Peut être affiné avec un système de delta score
            obs = self._get_observation()
            done = self.env.is_done()
        else:
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
            obs = self._get_observation()
            self.current_step += 1
            done = self.current_step >= self.max_steps

        return obs, reward, done, {}

    def _get_observation(self):
        if self.render_mode:
            if self.screen:
                frame = pygame.surfarray.array3d(self.screen)
                frame = np.transpose(frame, (1, 0, 2))  # HWC
                return frame
            else:
                return np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
        else:
            if not self.trash_queue:
                return 0
            obj = self.trash_queue[0]
            return self.categories.index(obj.category)

    def render(self):
        if self.render_mode and self.screen:
            self.screen.fill((30, 30, 30))  # fond gris foncé
            self.env.draw(self.screen)
            pygame.display.flip()

    def close(self):
        if self.render_mode:
            pygame.quit()
