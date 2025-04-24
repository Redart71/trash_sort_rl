import random
import pygame

class TrashObject:
    def __init__(self, name, category, image_path, headless=False):
        self.name = name
        self.category = category
        self.x = 0
        self.y = 340
        self.speed = 2
        self.headless = headless

        if not headless:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 40))
        else:
            self.image = None

    def move(self, speed_multiplier):
        self.x += self.speed * speed_multiplier

    def draw(self, screen, font):
        screen.blit(self.image, (self.x, self.y))
        # text = font.render(self.name, True, (255, 255, 255))
        # screen.blit(text, (self.x + 5, self.y + 45))

    @staticmethod
    def generate_random(headless=False):
        types = [
            ("bouteille plastique", "jaune", "assets/bouteille-en-plastique.png"),
            ("carton pizza", "bleue", "assets/pizza.png"),
            ("journal", "bleue", "assets/journal.png"),
            ("papier", "bleue", "assets/papier-froisse.png"),
            ("verre", "verte", "assets/verre-brise.png"),
            ("canette alu", "noire", "assets/canette-de-soda.png"),
            # Add more trash objects here
            ("champagne", "verte", "assets/champagne.png"),
            ("The", "noire", "assets/the-vert.png"),
            ("Chaussure", "noire", "assets/des-chaussures.png"),
            ("Livre", "bleue", "assets/des-chaussures.png"),

        ]
        return TrashObject(*random.choice(types), headless=headless)
