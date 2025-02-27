import pygame
import glob

def load_assets():
    pygame.font.init() 

    assets = {
        "game_icon": pygame.image.load("images/game_icon.png").convert_alpha(),
        "background": pygame.image.load("images/space-lab76-game-blank.png").convert(),
        "door_closed": pygame.image.load("images/wall_r_objects/closed_door.png").convert_alpha(),
        "door_open": pygame.image.load("images/wall_r_objects/open_door.png").convert_alpha(),
        "tl": pygame.image.load("images/tl.png").convert_alpha(),
        "tr": pygame.image.load("images/tr.png").convert_alpha(),
        "bl": pygame.image.load("images/bl.png").convert_alpha(),
        "br": pygame.image.load("images/br.png").convert_alpha(),
        "font": pygame.font.Font("fonts/Prism-Regular.otf", 36),
        "pickup_sound": pygame.mixer.Sound("sounds/pickup1.wav"),
        "enemy_hit": pygame.mixer.Sound("sounds/static1.wav"),    # Enemy collision
        "game_over": pygame.mixer.Sound("sounds/Pixel_49.wav"),   # Game over
        "scan_fail": pygame.mixer.Sound("sounds/static2.wav"),    # Incorrect wall scan
        "scan_success": pygame.mixer.Sound("sounds/pickup3.wav"), # Incorrect wall scan
        "door_unlock": pygame.mixer.Sound("sounds/explosion_somewhere_far.mp3"), # Door unlock
        "sentry_bot": pygame.image.load("enemy/enemy_red.png").convert_alpha()
    }

    for img in glob.glob("images/wall_l_objects/*.png"):
        name = img.split("/")[-1].replace(".png", "")
        assets[name] = pygame.image.load(img).convert_alpha()

    return assets
