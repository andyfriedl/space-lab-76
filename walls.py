import pygame
import glob

def load_walls(level_data):
    walls = []
    x_position = 131
    for obj in level_data["objects"]:
        if obj["type"] in glob.glob("wall_l_objects/*.png"):
            obj["x"] = x_position
            obj["y"] = 390 - (x_position / 2)
            x_position += 74
            walls.append(obj)
    return walls

def draw_walls(screen, level_data, assets):
    """Draws the wall objects on the screen."""
    for obj in level_data["objects"]:
        if obj["type"] in assets:  # Ensure image exists
            screen.blit(assets[obj["type"]], (obj["x"], obj["y"]))


def is_within_iso_bounds(x, y, top_y, right_y, bottom_y, left_y):
    return (
        y > (top_y - (x / 2)) and
        y < (bottom_y - (x / 2)) and
        y < (left_y + (x / 2)) and
        y > (right_y + (x / 2))
    )
