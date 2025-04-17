import pygame
import sys
from env.trash_env import TrashSortEnv

# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Jeu de tri des déchets")

env = TrashSortEnv(screen_width, screen_height)
env.reset()

# Mapping clavier -> poubelles
key_to_bin = {
    pygame.K_1: "jaune",
    pygame.K_2: "bleue",
    pygame.K_3: "verte",
    pygame.K_4: "noire"
}

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_bin:
                env.handle_action(key_to_bin[event.key])

    env.update()
    env.draw(screen)
    pygame.display.flip()
    clock.tick(30)

    if env.is_done():
        print("Fin de la partie. Score final :", env.score)
        pygame.time.wait(3000)
        running = False

pygame.quit()
sys.exit()
