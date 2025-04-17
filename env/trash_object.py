### Structure du projet

# dossier : trash_sort_rl/
# ├── main.py              <-- Lancement du jeu
# ├── env/
# │   ├── __init__.py
# │   ├── trash_env.py     <-- Logique des objets et du jeu
# │   └── trash_object.py  <-- Classe de déchets
# └── assets/              <-- Pour les images plus tard (optionnel)


### Fichier : env/trash_object.py

import random
import pygame


class TrashObject:
    def __init__(self, name, category, color):
        self.name = name
        self.category = category  # "jaune", "bleue", "verte", "noire"
        self.color = color
        self.x = 0
        self.y = 250  # Position verticale fixe (milieu du tapis)
        self.speed = 2

    def move(self, speed_multiplier):
        self.x += self.speed * speed_multiplier

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 80, 40))
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.x + 5, self.y + 10))

    @staticmethod
    def generate_random():
        types = [
            ("bouteille plastique", "jaune", (255, 255, 0)),
            ("carton pizza", "jaune", (255, 255, 0)),
            ("journal", "bleue", (0, 0, 255)),
            ("papier", "bleue", (0, 0, 255)),
            ("verre", "verte", (0, 255, 0)),
            ("canette alu", "noire", (50, 50, 50))
        ]
        return TrashObject(*random.choice(types))
