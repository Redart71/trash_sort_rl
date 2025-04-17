import random
import pygame


class TrashObject:
    def __init__(self, name, category, image_path):
        self.name = name
        self.category = category
        self.x = 0
        self.y = 250
        self.speed = 2
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 40))

    def move(self, speed_multiplier):
        self.x += self.speed * speed_multiplier

    def draw(self, screen, font):
        screen.blit(self.image, (self.x, self.y))
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.x + 5, self.y + 45))

    @staticmethod
    def generate_random():
        types = [
            ("bouteille plastique", "jaune", "assets/bouteille-en-plastique.png"),
            ("carton pizza", "jaune", "assets/pizza.png"),
            ("journal", "bleue", "assets/journal.png"),
            ("papier", "bleue", "assets/papier-froisse.png"),
            ("verre", "verte", "assets/verre-brise.png"),
            ("canette alu", "noire", "assets/canette-de-soda.png")
        ]
        return TrashObject(*random.choice(types))
