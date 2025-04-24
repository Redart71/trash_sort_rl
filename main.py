import pygame
import sys
from env.trash_env import TrashSortEnv
import subprocess


# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("TriXel")

# Chargement fond
try:
    background = pygame.image.load("./assets/background-image.png").convert()
except pygame.error as e:
    print(f"Erreur de chargement de l'image : {e}")
    sys.exit()

background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonts
font = pygame.font.SysFont(None, 55)
font.set_bold(True)
small_font = pygame.font.SysFont(None, 40)

# États de jeu
game_state = "menu"

# === Boutons ===
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
button_color = (70, 130, 180)
hover_color = (100, 160, 210)
text_color = (255, 255, 255)

def draw_button(text, x, y, action_name):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Hover effect
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1:
            return action_name
    else:
        pygame.draw.rect(screen, button_color, rect)
    
    text_surf = small_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return None

def draw_menu():
    screen.fill((30, 30, 30))
    title_surf = font.render("TriXel", True, (255, 255, 255))
    screen.blit(title_surf, title_surf.get_rect(center=(screen_width//2, 100)))

    b1 = draw_button("Mode Humain", screen_width//2 - BUTTON_WIDTH//2, 200, "humain")
    b2 = draw_button("Agent Q-learning", screen_width//2 - BUTTON_WIDTH//2, 300, "ql")
    b3 = draw_button("Agent DQN", screen_width//2 - BUTTON_WIDTH//2, 400, "dqn")

    pygame.display.flip()
    return b1 or b2 or b3

# === Fonction fin de partie ===
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

# Mapping clavier → actions
key_to_bin = {
    pygame.K_1: "Plastique",
    pygame.K_2: "Papier",
    pygame.K_3: "Verre",
    pygame.K_4: "Non recyclable"
}

# Paramètres jeu
TOTAL_GAME_DURATION = 60000
END_SCREEN_DURATION = 3000
SUCCESS_THRESHOLD = 20

# Initialisation environnement
env = TrashSortEnv(screen_width, screen_height)
env.load_assets()

# Boucle principale
running = True
start_time = None

while running:
    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        choice = draw_menu()
        if choice:
            game_state = choice
            env.reset()
            start_time = pygame.time.get_ticks()

    elif game_state == "humain":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in key_to_bin:
                env.handle_action(key_to_bin[event.key])

        env.update()
        screen.blit(background, (0, 0))
        env.draw(screen)
        pygame.display.flip()
        clock.tick(70)

        elapsed = pygame.time.get_ticks() - start_time
        if elapsed >= TOTAL_GAME_DURATION or env.is_done():
            msg = "RÉUSSITE !" if env.score >= SUCCESS_THRESHOLD else "GAME OVER !"
            msg += f" Score final : {env.score}"
            show_end_message(screen, font, msg, screen_width, screen_height, END_SCREEN_DURATION)
            game_state = "menu"

    elif game_state == "ql":
        pygame.quit()
        subprocess.run(["python", "play_with_agent.py"])
        sys.exit()


    elif game_state in ["dqn"]:
        # Pour l’instant : placeholder, on affiche juste un message
        screen.fill((0, 0, 0))
        txt = font.render(f"{game_state.upper()} Agent en cours...", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(screen_width//2, screen_height//2)))
        pygame.display.flip()
        pygame.time.delay(2000)
        game_state = "menu"

pygame.quit()
sys.exit()
