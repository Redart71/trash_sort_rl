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
            ("bouteille plastique", "Plastique", "assets/bouteille-en-plastique.png"),
            ("carton pizza", "Papier", "assets/pizza.png"),
            ("journal", "Papier", "assets/journal.png"),
            ("papier", "Papier", "assets/papier-froisse.png"),
            ("verre", "Verre", "assets/verre-brise.png"),
            ("canette alu", "Non recyclable", "assets/canette-de-soda.png"),
            ("champagne", "Verre", "assets/champagne.png"),
            ("The", "Non recyclable", "assets/the-vert.png"),
            ("Chaussure", "Non recyclable", "assets/des-chaussures.png"),
            ("Livre", "Papier", "assets/des-chaussures.png"),

        ]
        return TrashObject(*random.choice(types), headless=headless)
