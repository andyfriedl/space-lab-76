import pygame

class Door:
    def __init__(self, progression_data):
        """Initialize the door with its position, floor zone, and state."""
        self.position = progression_data["door_position"]
        self.door_floor_zone = progression_data["door_floor_zone"]
        self.is_open = False
        self.open_time = None  # Store the time the door opens
        self.required_floor_items = len(progression_data.get("required_floor_items", []))
        self.fade_alpha = 255  # Start fully opaque for the closed door
        self.fade_speed = 5  # Controls how fast the fade occurs

    def check_door_zone(self, player, floor_items_collected):
        """Check if the player is in the door zone and unlock if conditions are met."""
        
        # Check if all required items are collected
        if len(floor_items_collected) < self.required_floor_items:
            return False  

        # Check interaction progress
        if player.interaction_progress == len(player.interaction_order) - 1:
            if (
                self.door_floor_zone["x2"] <= player.x <= self.door_floor_zone["x1"]
                and self.door_floor_zone["y1"] <= player.y <= (self.door_floor_zone["y2"] + self.door_floor_zone["height_extension"])
            ):
                if not self.is_open:
                    self.is_open = True
                    self.open_time = pygame.time.get_ticks()  # Store time of opening
                    player.assets["door_unlock"].play()
                return True  # Always return True once door is open

        return False  # ❌ Keep returning False until all conditions are met


    def draw(self, screen, assets):
        """Draw the door with a fade transition from closed to open."""
        closed_image = assets["door_closed"]
        open_image = assets["door_open"]

        if self.is_open and self.fade_alpha > 0:
            self.fade_alpha -= self.fade_speed  # Reduce opacity gradually

        if self.fade_alpha > 0:
            temp_closed = closed_image.copy()
            temp_closed.set_alpha(self.fade_alpha)
            screen.blit(temp_closed, (self.position["x"], self.position["y"]))

        if self.is_open:
            temp_open = open_image.copy()
            temp_open.set_alpha(255 - self.fade_alpha)
            screen.blit(temp_open, (self.position["x"], self.position["y"]))
