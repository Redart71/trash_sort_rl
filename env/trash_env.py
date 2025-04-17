import pygame
import random
from .trash_object import TrashObject

class TrashSortEnv:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.trash_objects = []
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.speed_multiplier = 1.0
        self.score = 0
        self.total_steps = 0
        self.max_steps = 1800  # ~60s at 30 FPS
        self.font = None

        # Poubelles (x position, color, label)
        self.bins = {
            "jaune": (screen_width - 90, (255, 255, 0)),
            "bleue": (screen_width - 180, (0, 0, 255)),
            "verte": (screen_width - 270, (0, 255, 0)),
            "noire": (screen_width - 360, (50, 50, 50)),
        }

    def reset(self):
        self.trash_objects = []
        self.spawn_timer = 0
        self.speed_multiplier = 1.0
        self.score = 0
        self.total_steps = 0

    def update(self):
        self.total_steps += 1

        # Augmenter la vitesse progressivement
        if self.total_steps % 300 == 0:
            self.speed_multiplier += 0.2

        # Génération de nouveaux déchets
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.trash_objects.append(TrashObject.generate_random())
            self.spawn_timer = 0

        # Mise à jour des positions
        for obj in self.trash_objects:
            obj.move(self.speed_multiplier)

        # Retirer les objets qui sortent de l'écran
        self.trash_objects = [obj for obj in self.trash_objects if obj.x < self.screen_width]

    def draw(self, screen):
        if not self.font:
            self.font = pygame.font.SysFont(None, 24)

        screen.fill((200, 200, 200))

        # Dessiner tapis roulant
        pygame.draw.rect(screen, (150, 150, 150), (0, 240, self.screen_width, 60))

        # Dessiner les objets
        for obj in self.trash_objects:
            obj.draw(screen, self.font)

        # Dessiner les poubelles
        for label, (x_pos, color) in self.bins.items():
            pygame.draw.rect(screen, color, (x_pos, 170, 80, 60))
            text = self.font.render(label.upper(), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x_pos + 40, 170 - 15))
            screen.blit(text, text_rect)

        # Score
        score_text = self.font.render(f"Score : {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    def handle_action(self, action_bin):
        if not self.trash_objects:
            return

        obj = self.trash_objects.pop(0)
        if obj.category == action_bin:
            self.score += 1
        else:
            self.score -= 1

    def is_done(self):
        return self.total_steps >= self.max_steps
