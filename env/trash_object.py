import random
import pygame

class TrashObject:
    def __init__(self, name, category, image_path, headless=False):
        self.name = name
        self.category = category
        self.x = 0
        self.y = 250
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
        if self.headless:
            # Dessine un rectangle coloré à la place
            color_map = {
                "jaune": (255, 255, 0),
                "bleue": (0, 0, 255),
                "verte": (0, 255, 0),
                "noire": (50, 50, 50)
            }
            pygame.draw.rect(screen, color_map.get(self.category, (128, 128, 128)), (self.x, self.y, 80, 40))
        else:
            screen.blit(self.image, (self.x, self.y))

        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.x + 5, self.y + 45))

    @staticmethod
    def generate_random(headless=False):
        types = [
            ("bouteille plastique", "jaune", "assets/bouteille-en-plastique.png"),
            ("carton pizza", "jaune", "assets/pizza.png"),
            ("journal", "bleue", "assets/journal.png"),
            ("papier", "bleue", "assets/papier-froisse.png"),
            ("verre", "verte", "assets/verre-brise.png"),
            ("canette alu", "noire", "assets/canette-de-soda.png")
        ]
        return TrashObject(*random.choice(types), headless=headless)
