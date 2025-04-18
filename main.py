import pygame
import sys
from env.trash_env import TrashSortEnv

# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Jeu de tri des déchets")

# Charger l'image de fond d'écran
try:
    background = pygame.image.load("./assets/background-image.png").convert()
    print("Image chargée avec succès")
except pygame.error as e:
    print(f"Erreur de chargement de l'image : {e}")
    sys.exit()

background = pygame.transform.scale(background, (screen_width, screen_height))
env = TrashSortEnv(screen_width, screen_height)
env.load_assets()
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
    
    # 🔥 Affichage du fond d'écran ici
    screen.blit(background, (0, 0))

    env.draw(screen)
    pygame.display.flip()
    clock.tick(70)

    if env.is_done():
        print("Fin de la partie. Score final :", env.score)
        pygame.time.wait(3000)
        running = False

pygame.quit()
sys.exit()
