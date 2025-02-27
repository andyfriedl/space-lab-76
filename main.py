import pygame
from assets import load_assets
from levels import load_level_data, place_wall_objects
from player import Player
from door import Door
from ui import UI
from floor_items import load_floor_items
from enemy import SentryBot
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1122, 653))
pygame.display.set_caption("Space Lab 76")

# Load assets first
assets = load_assets()
pygame.display.set_icon(assets["game_icon"])

# Load level data
game_data = load_level_data("levels.json")
current_level = "level_1"
player = Player(assets, game_data[current_level])
title_font = pygame.font.Font("fonts/Monoton-Regular.ttf", 46)
game_over = False  
ui = UI(title_font)
current_level_index = 0
levels = list(game_data.keys())
level_complete = False
game_over_delay = 0
update_result = None

def load_new_level(level_key):
    """Load a new level when the current one is completed."""
    global current_level, level_data, door, player, floor_items, sentries, level_time_remaining, level_start_time  
    current_level = level_key  
    level_data = place_wall_objects(game_data[current_level], assets)

    # Set Level Time
    level_time_remaining = level_data.get("level_time", 300)  # Default: 300 sec (5 min)
    level_start_time = pygame.time.get_ticks()  

    # Load Floor Items
    floor_items = load_floor_items(level_data)  
    door = Door(level_data["progression"])
    player.reset(level_data)

    # Generate Sentries Dynamically
    sentry_config = level_data.get("sentries", {})
    num_sentries = sentry_config.get("count", 0)  
    speed_setting = sentry_config.get("speed", "medium")

    # 🔹 Convert speed words to numbers
    speed_map = {"slow": 0.4, "medium": 1.0, "fast": 2.0}
    speed_value = speed_map.get(speed_setting, speed_setting)  

    # Spawn sentries with randomized positions
    sentries = []
    for _ in range(num_sentries):
        x = random.randint(500, 700)  
        y = random.randint(300, 350)
        sentries.append(SentryBot(x, y, speed_value, assets))


# Load first level initially
load_new_level(current_level)
ui.draw_start_screen(screen)

# Start Screen Delay
waiting = True
start_delay = pygame.time.get_ticks() + 1000
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and pygame.time.get_ticks() > start_delay:
            waiting = False

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    ### GAME UPDATES ###
    collected_items = [item.name for item in floor_items if item.collected]
    update_result = player.update(level_data, door, floor_items, assets, collected_items, game_over, current_level, game_data)

    # Handle Game Over from final progression
    if update_result == "game_over":
        # Stop all movement by setting a flag
        game_over = True

        # Show Game Over screen
        ui.draw_game_over(screen)
        pygame.display.flip()

        # Pause before restart
        pygame.time.delay(2000)

        # Wait for user to restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False
                elif event.type == pygame.KEYDOWN:
                    load_new_level("level_1")
                    game_over = False
                    waiting_for_restart = False


    if update_result == "game_complete":
        running = False

    ### GAME OVER SCREEN (Now only triggers once) ###
    if game_over:
        ui.draw_game_over(screen)  
        pygame.display.flip()  

        pygame.event.clear()  # Prevent instant restart
        game_over_delay = pygame.time.get_ticks() + 1500  # Delay before input

        for event in pygame.event.get():  # Non-blocking event loop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                load_new_level("level_1")  
                game_over = False

    ### LEVEL TRANSITION ###
    if isinstance(update_result, str) and update_result.startswith("level_"):
        if not level_complete:
            level_complete = True  
            next_level = update_result  # Store the next level

    if level_complete:

            # Ensure door animation is fully visible before transition
        transition_delay = pygame.time.get_ticks() + 300  # Wait 1.5 sec

        while pygame.time.get_ticks() < transition_delay:
            screen.blit(assets["background"], (0, 0))
            door.draw(screen, assets)  # Keep drawing the door as it fades
            player.draw(screen)  # Keep player visible
            ui.draw(screen, player, door)  # Keep UI visible
            pygame.display.flip()

        # Now load the next level
        current_level = next_level  
        load_new_level(current_level)  # Actually load the new level
        level_complete = False

        # Fade to black
        screen.fill((0, 0, 0))
        transition_text = title_font.render(f"Entering {next_level}...", True, (255, 255, 255))
        screen.blit(transition_text, (screen.get_width() // 2 - transition_text.get_width() // 2, screen.get_height() // 2))
        pygame.display.flip()  

        # Wait before transitioning
        pygame.time.delay(1500)


    ### DRAW GAME SCREEN (Only if not game over) ###
    if not game_over:
        screen.blit(assets["background"], (0, 0))
        ui.draw_title(screen)  
        ui.draw(screen, player, door)
        door.draw(screen, assets)

        for item in floor_items:
            item.draw(screen)

        for obj in level_data["objects"]:
            if obj["name"] in assets:
                screen.blit(assets[obj["name"]], (obj["x"], obj["y"]))

        for sentry in sentries:
            sentry.update()
            sentry.check_collision(player)
            sentry.draw(screen)
        
        player.update_particles()  # Update sparks every frame

        # Draw expanding energy rings
        for wave in player.energy_waves:
            if wave["alpha"] > 0:
                wave_surface = pygame.Surface((wave["radius"] * 2, wave["radius"] * 2), pygame.SRCALPHA)

                # 🟢 Draw an expanding ring with transparency
                pygame.draw.circle(screen, (0, 255, 0, wave["alpha"]), (wave["x"], wave["y"]), wave["radius"], 2)  # Use width=2

                
                screen.blit(wave_surface, (wave["x"] - wave["radius"], wave["y"] - wave["radius"]))



        player.draw(screen)  # Draw player and effects
        ui.draw_hint(screen, player)

        pygame.display.flip()
        clock.tick(90)

pygame.quit()
