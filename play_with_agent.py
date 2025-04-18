import pygame
import numpy as np
import sys
from env.trash_env import TrashSortEnv

# Charger la Q-table entraînée
Q = np.load("q_table.npy")

# Initialisation Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Agent RL - Tri des déchets")

# Charger l’image de fond
background = pygame.image.load("assets/background-image.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Initialiser l'environnement visuel
env = TrashSortEnv(screen_width, screen_height)
env.load_assets()
state = env.reset()

running = True
speed = 1  # facteur de vitesse
font = pygame.font.SysFont(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Agent choisit l'action optimale
    action = np.argmax(Q[state])
    category_mapping = ["jaune", "bleue", "verte", "noire", None]

    # Si l’action n’est pas "ne rien faire"
    if action != 4:
        env.handle_action(category_mapping[action])

    env.update()
    screen.blit(background, (0, 0))
    env.draw(screen)
    pygame.display.flip()

    state = env.get_observation()
    clock.tick(30 * speed)

    if env.is_done():
        print("Fin de la partie. Score final :", env.score)
        pygame.time.wait(3000)
        running = False

pygame.quit()
sys.exit()
