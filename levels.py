import json
import glob
import pygame
import random
from walls import is_within_iso_bounds  # ✅ Import boundary check

# Wall object placement settings
wall_object_x_start = 131  # First object starts at x = 131
wall_object_y_start = 390  # First object starts at y = 460
object_width = 74  # Width of each object

def load_level_data(filename):
    """Loads level data from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def get_wall_images():
    """Returns a dictionary of available wall object images."""
    return {f.split("/")[-1].replace(".png", ""): f for f in glob.glob("wall_l_objects/*.png")}

def load_object_images(wall_images):
    """Loads object images from the given file paths."""
    object_images = {}
    for obj_name, img_path in wall_images.items():
        object_images[obj_name] = pygame.image.load(img_path).convert_alpha()
    return object_images

def place_wall_objects(level_data, assets):
    """Assigns x, y values dynamically for wall objects using a starting point."""
    x_position = wall_object_x_start  # Start at 131x
    for obj in level_data["objects"]:
        if obj["name"] in assets:  # Only process wall objects
            obj["x"] = x_position
            obj["y"] = wall_object_y_start - (x_position / 2)  # Adjust for isometric slope
            x_position += object_width  # Move right for next object
    return level_data

### 🔥 NEW FUNCTION: Place random floor items within valid bounds
def place_random_floor_items(level_data):
    """Places random floor items within the player's movement bounds."""
    if "floor_items" not in level_data or "random" not in level_data["floor_items"]:
        return []  # No random items defined

    random_items = level_data["floor_items"]["random"]
    item_list = []
    
    for _ in range(random_items["count"]):  # Place the specified number of random items
        item_type = random.choice(random_items["types"])  # Pick a random item type
        
        # ✅ Ensure items are placed within the player's movement bounds
        while True:
            x = random.randint(100, 900)  # Adjust based on level bounds
            y = random.randint(150, 600)  # Adjust based on level bounds
            
            # ✅ Check if it's within the isometric bounds
            if is_within_iso_bounds(x, y, 505, -270, 780, 346):
                break  # Found a valid position

        item_list.append({"name": item_type, "x": x, "y": y, "interactive": False})
    
    return item_list
