import os
import random
import pygame
from walls import is_within_iso_bounds  # Ensure items spawn within player bounds

class FloorItem:
    def __init__(self, name, x, y, directory="floor_items/placed", effect=None, hint_text=None, is_wear=False):
        """Initialize floor item properties."""
        self.name = name
        self.x = x
        self.y = y
        self.effect = effect  # e.g., "power", "damage", "hint"
        self.collected = False
        self.hint_text = hint_text  # Store hint from JSON (if any)
        self.is_wear = is_wear 

        # Load the correct image based on type
        self.image = pygame.image.load(f"{directory}/{name}.png").convert_alpha()


    def draw(self, screen):
        """Draws the floor item if not collected."""
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

    def collect(self, player):
        """Trigger effects when the player collects an item."""
        if self.is_wear:
            return
        
        self.collected = True  # Mark as picked up immediately

        if self.effect == "damage":
            player.take_damage(10)  # Damage player
        elif self.effect == "heal":
            player.power = min(100, player.power + 10)  # Restore up to 100%
        elif self.effect == "power":
            player.power = min(100, player.power + 10)  # Restore 10% power
        
        elif self.effect == "hint" and self.hint_text:
            player.show_hint(self.hint_text)  # Show hint

        if "pickup_sound" in player.assets:
            player.assets["pickup_sound"].play()


    def show_hint(self, player):
        """Reveal part of the correct wall scan order."""
        hint_index = min(player.interaction_progress, len(player.interaction_order) - 1)
        hint_item = player.interaction_order[hint_index]

def show_hint(self, player):
    """Reveal hint from JSON or fallback to interaction order hint."""
    hint_text = self.hint_text if hasattr(self, "hint_text") else None

    if not hint_text:
        # Fallback: Reveal part of the correct wall scan order
        hint_index = min(player.interaction_progress, len(player.interaction_order) - 1)
        hint_item = player.interaction_order[hint_index]
        hint_text = f"🔍 Look for {hint_item} first."

    player.show_message(hint_text) 

def load_floor_items(level_data):
    """Loads both placed and random floor items for the level."""
    floor_items = []
    
    # Get movement area from JSON (already using your values)
    bounds = level_data.get("floor_bounds", {})
    TOP_WALL_Y = bounds.get("top", 545)
    RIGHT_WALL_Y = bounds.get("right", -250)
    BOTTOM_WALL_Y = bounds.get("bottom", 820)
    LEFT_WALL_Y = bounds.get("left", 385)

    # Get player start position dynamically from levels.json
    player_start = level_data.get("player_start", {})
    # PLAYER_START_X = player_start.get("x", 257)
    # PLAYER_START_Y = player_start.get("y", 467)
    # SAFE_ZONE_RADIUS = 50  # No items within 50px of player start

    # Load placed floor items (interactive)
    if "placed" in level_data["floor_items"]:
        for item in level_data["floor_items"]["placed"]:
            floor_items.append(FloorItem(
                name=item["name"],
                x=item["x"],
                y=item["y"],
                directory="floor_items/placed",
                effect=item.get("effect"),
                hint_text=item.get("hint_text")
            ))

    # Load random floor items (non-interactive)
    if "random" in level_data["floor_items"]:
        random_settings = level_data["floor_items"]["random"]
        directory = random_settings["directory"]
        count = random_settings["count"]  

        if os.path.exists(directory):
            available_files = [f.replace(".png", "") for f in os.listdir(directory) if f.endswith(".png")]
        else:
            available_files = []

        if available_files:
            attempts = 0
            max_attempts = count * 10  

            while len(floor_items) < count and attempts < max_attempts:
                random_x = random.randint(150, 1100)
                random_y = random.randint(150, 600)

                # Check if item is within isometric movement bounds
                if is_within_iso_bounds(random_x, random_y, TOP_WALL_Y, RIGHT_WALL_Y, BOTTOM_WALL_Y, LEFT_WALL_Y):
                    floor_items.append(FloorItem(
                        name=random.choice(available_files),
                        x=random_x,
                        y=random_y,
                        directory=directory,
                        effect="power"
                    ))

                attempts += 1

    # Load wear items (NEW - Corrected)
    if "wear" in level_data["floor_items"]:
        wear_settings = level_data["floor_items"]["wear"]
        directory = wear_settings["directory"]
        count = wear_settings["count"]  

        if os.path.exists(directory):
            wear_files = [f.replace(".png", "") for f in os.listdir(directory) if f.endswith(".png")]
        else:
            wear_files = []

        if wear_files:
            attempts = 0
            max_attempts = count * 10  

            while len(floor_items) < count and attempts < max_attempts:
                wear_x = random.randint(150, 1100)
                wear_y = random.randint(150, 600)

                # Make sure wear items stay inside **isometric bounds**
                if is_within_iso_bounds(wear_x, wear_y, TOP_WALL_Y, RIGHT_WALL_Y, BOTTOM_WALL_Y, LEFT_WALL_Y):
                    floor_items.append(FloorItem(
                        name=random.choice(wear_files),
                        x=wear_x,
                        y=wear_y,
                        directory=directory,
                        is_wear=True
                    ))

                attempts += 1

    return floor_items

