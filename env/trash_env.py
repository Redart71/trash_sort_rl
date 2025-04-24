import pygame
import random
from .trash_object import TrashObject

class TrashSortEnv:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.trash_objects = []
        self.spawn_queue = []
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.speed_multiplier = 1.0
        self.score = 0
        self.total_steps = 0
        self.max_steps = 1800
        self.font = None

        self.bin_images = {
            "Plastique": pygame.transform.scale(pygame.image.load("assets/poubelle-jaune.png"), (80, 60)),
            "Papier": pygame.transform.scale(pygame.image.load("assets/poubelle-bleue.png"), (80, 60)),
            "Verre": pygame.transform.scale(pygame.image.load("assets/poubelle-verte.png"), (80, 60)),
            "Non recyclable": pygame.transform.scale(pygame.image.load("assets/poubelle-noire.png"), (80, 60)),
        }

        self.bins = {
            "Plastique": (screen_width - 120, (255, 255, 0)),
            "Papier": (screen_width - 250, (0, 0, 255)),
            "Verre": (screen_width - 380, (0, 255, 0)),
            "Non recyclable": (screen_width - 510, (50, 50, 50)),
        }

        # Compteurs pour chaque poubelle
        self.bin_counts = {
            "Plastique": 0,
            "Papier": 0,
            "Verre": 0,
            "Non recyclable": 0,
        }

    def load_assets(self):
        """À appeler après pygame.display.set_mode()"""
        self.bin_images = {
            "Plastique": pygame.transform.scale(pygame.image.load("assets/poubelle-jaune.png").convert_alpha(), (80, 60)),
            "Papier": pygame.transform.scale(pygame.image.load("assets/poubelle-bleue.png").convert_alpha(), (80, 60)),
            "Verre": pygame.transform.scale(pygame.image.load("assets/poubelle-verte.png").convert_alpha(), (80, 60)),
            "Non recyclable": pygame.transform.scale(pygame.image.load("assets/poubelle-noire.png").convert_alpha(), (80, 60)),
        }

    def reset(self):
        self.trash_objects = []
        self.spawn_queue = []
        self.spawn_timer = 0
        self.speed_multiplier = 1.0
        self.score = 0
        self.total_steps = 0

    def update(self):
        self.total_steps += 1

        # Augmenter la vitesse progressivement
        if self.total_steps % 300 == 0:
            self.speed_multiplier += 0.2

        # Génération d'une vague de 4 objets
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_queue = [TrashObject.generate_random() for _ in range(5)]
            self.spawn_timer = 0

        # Ajout progressif des objets avec un espacement horizontal
        if self.spawn_queue and self.total_steps % 10 == 0:
            obj = self.spawn_queue.pop(0)
            obj.x -= len(self.trash_objects) * 50  # Décalage vers la gauche
            self.trash_objects.append(obj)

        # Mise à jour des positions
        for obj in self.trash_objects:
            obj.move(self.speed_multiplier)

        # Vérification des objets sortis de l'écran
        remaining_objects = []
        for obj in self.trash_objects:
            if obj.x >= self.screen_width:
                self.score -= 0.5  # Pénalité pour objet non trié
            else:
                remaining_objects.append(obj)

        self.trash_objects = remaining_objects


    def draw(self, screen):
        if not self.font:
            self.font = pygame.font.SysFont(None, 24)

        for obj in self.trash_objects:
            obj.draw(screen, self.font)

        for label, (x_pos, _) in self.bins.items():
            # Dessiner la poubelle
            screen.blit(self.bin_images[label], (x_pos, 260))
            # Dessiner le nom de la poubelle
            text = self.font.render(label.upper(), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x_pos + 40, 245))
            screen.blit(text, text_rect)

            # Afficher le nombre d'objets dans chaque poubelle
            count = self.bin_counts[label]
            text_count = self.font.render(str(count), True, (255, 215, 0))  # Couleur dorée pour le compteur
            rect_count = text_count.get_rect(center=(x_pos + 40, 225))  # Au-dessus de la poubelle
            screen.blit(text_count, rect_count)

        # Afficher le score global
        score_text = self.font.render(f"Score : {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def handle_action(self, action_bin):
        if not self.trash_objects:
            return

        obj = self.trash_objects.pop(0)
        if obj.category == action_bin:
            self.score += 1
            self.bin_counts[action_bin] += 1  # Incrémentation du compteur pour la poubelle choisie
        else:
            self.score -= 1

    def is_done(self):
        return self.total_steps >= self.max_steps

    def get_observation(self):
        if not self.trash_objects:
            return 0
        categories = ["Plastique", "Papier", "Verre", "Non recyclable"]
        return categories.index(self.trash_objects[0].category)
