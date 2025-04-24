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
    pygame.K_1: "Plastique",
    pygame.K_2: "Papier",
    pygame.K_3: "Verre",
    pygame.K_4: "Non recyclable"
}

def show_end_message(screen, font, message, screen_width, screen_height, duration_ms=3000):
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    text_surf = font.render(message, True, (255, 215, 0))
    text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    pygame.time.delay(duration_ms)

# Paramètres du chrono
TOTAL_GAME_DURATION = 60000  # 1 minutes en millisecondes
END_SCREEN_DURATION = 30000   # 30 seconcdes à l'écran
start_time = pygame.time.get_ticks()

# Boucle principale
running = True
SUCCESS_THRESHOLD = 20
font = pygame.font.SysFont(None, 55)
font.set_bold(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_bin:
                env.handle_action(key_to_bin[event.key])

    env.update()
    screen.blit(background, (0, 0))
    env.draw(screen)
    pygame.display.flip()
    clock.tick(70)

    # Chrono global
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= TOTAL_GAME_DURATION or env.is_done():
        if env.score >= SUCCESS_THRESHOLD:
            msg = "RÉUSSITE !"
        else:
            msg = "GAME OVER !"
        msg += f" Score final : {env.score}"

        show_end_message(screen, font, msg, screen_width, screen_height, END_SCREEN_DURATION)
        running = False

pygame.quit()
sys.exit()