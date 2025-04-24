import pygame
import numpy as np
import sys
import time
from env.trash_env import TrashSortEnv

# Charger la Q-table entraînée
Q = np.load("q_table.npy")

# Initialisation Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Agent RL - Tri des déchets")

# Charger l’image de fond
background = pygame.image.load("assets/background-image.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Initialiser l'environnement visuel
env = TrashSortEnv(screen_width, screen_height)
env.load_assets()

# Initialisation de l'état
state = env.reset()

running = True
speed = 1  # facteur de vitesse
font = pygame.font.SysFont(None, 55)

# Timer global
start_time = time.time()
MAX_DURATION = 60  # 1 minute
SUCCESS_THRESHOLD = 20

def show_end_message(screen, font, msg, width, height):
    screen.fill((0, 0, 0))  # fond noir
    text = font.render(msg, True, (255, 255, 255))
    rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, rect)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            # Mise à jour de la taille de l’écran
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            # Mise à jour de l'image de fond
            background = pygame.transform.scale(
                pygame.image.load("assets/background-image.png").convert(), (screen_width, screen_height)
            )

            # Mise à jour des dimensions dans l’environnement
            env.screen_width = screen_width
            env.screen_height = screen_height

    screen.blit(background, (0, 0))
    env.update()
    env.draw(screen)

    # Exécution de l'action de tri
    if len(env.trash_objects) >= 4:
        if all(obj.x >= screen_width // 5 for obj in env.trash_objects[:4]):
            action = int(np.argmax(Q[state]))
            category_mapping = ["Plastique", "Papier", "Verre", "Non recyclable", "ne_pas_trier"]

            if action < 0 or action >= len(category_mapping):
                print(f"[AVERTISSEMENT] Action {action} invalide, on choisit 'rien'")
                action = 4

            if action != 4:
                print("Action triée :", category_mapping[action])
                env.handle_action(category_mapping[action])
            else:
                print("Action 'rien', aucun tri")

            state = env.get_observation()
            if state is None or not isinstance(state, int):
                raise ValueError(f"get_observation() doit retourner un entier, got {state}")

    # Vérification du temps écoulé
    elapsed_time = time.time() - start_time
    if elapsed_time >= MAX_DURATION:
        if env.score >= SUCCESS_THRESHOLD:
            msg = "RÉUSSITE !"
        else:
            msg = "GAME OVER !"
        msg += f" Score final : {env.score}"
        show_end_message(screen, font, msg, screen_width, screen_height)
        pygame.time.delay(30000)  # Pause 30 sec
        running = False

    pygame.display.flip()
    clock.tick(30 * speed)

pygame.quit()
sys.exit()
