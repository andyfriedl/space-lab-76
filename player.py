import pygame
import random
from walls import is_within_iso_bounds

class Player:
    def __init__(self, assets, level_data):
        self.x = level_data["player_start"]["x"]
        self.y = level_data["player_start"]["y"]
        self.speed_x = 2
        self.speed_y = 1
        self.power = 100
        self.sprite = assets['tr']
        self.assets = assets
        self.is_searching = False
        self.search_timer = 0
        self.current_object = None
        self.interaction_progress = 0
        self.interaction_order = level_data['progression']['interaction_order']
        self.tint_timer = 0
        self.is_tinted = False
        self.tint_color = None  # Stores current tint (green/red)
        self.sprite_direction = "tr"  # Default to top-right
        self.hint_message = None  # Stores current hint
        self.hint_timer = 0
        self.particles = []
        self.energy_waves = []


    def show_message(self, text, duration=3000):
        """Displays a temporary message above VOX's head."""
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration

    def show_hint(self, message):
        """Show a hint above the bot for a few seconds."""
        self.hint_message = message  
        self.hint_timer = pygame.time.get_ticks() + 3000  # Show for 3 seconds
        
    def tint_sprite(self, color):
        """Apply a subtle tint to only the non-transparent areas while keeping opacity."""
        tinted_sprite = self.sprite.copy()

        # Create a mask from the original sprite (preserves transparency)
        mask = pygame.mask.from_surface(tinted_sprite)
        
        # Create a fully transparent surface the same size as the sprite
        tint_surface = pygame.Surface(tinted_sprite.get_size(), pygame.SRCALPHA)
        
        # Fill with the tint color (softly applied)
        tint_surface.fill(color + (0,))  # Alpha = 0 to avoid making it see-through
        
        # Use the mask to apply the tint **only to the visible parts**
        tinted_sprite.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return tinted_sprite

    def reset(self, level_data):
        """Resets player position and interaction progress when loading a new level."""
        self.x = level_data["player_start"]["x"]
        self.y = level_data["player_start"]["y"]
        self.message = "" 
        self.message_timer = 0 
        self.is_searching = False
        self.search_timer = 0
        self.power = 100  # Start with full power (100%)
        self.invincible_timer = 0
        self.stun_timer = 0
        self.current_object = None
        self.interaction_progress = 0  # Reset progress
        self.interaction_order = level_data["progression"]["interaction_order"]

    def take_damage(self, amount):
        """Reduce player power when hit and apply stun effect."""
        self.power = max(0, self.power - amount)  # Prevents power from dropping below 0
        self.stun_timer = pygame.time.get_ticks() + 500  # Stun for 500ms
        self.create_sparks(self.x + 25, self.y + 5)  # Sparks near the player’s lower body
    
    def create_sparks(self, x, y, num_sparks=30):
        """Creates a burst of sparks at (x, y) that shrink and fade out."""
        for _ in range(num_sparks):
            self.particles.append({
                "x": x,
                "y": y,
                "dx": random.uniform(-2, 2),  # Spread X
                "dy": random.uniform(-2, -0.1),  # Upward Y movement
                "size": random.randint(1, 4),  # Spark size
                "lifetime": pygame.time.get_ticks() + random.randint(400, 500)  # Random lifespan
            })

    def update_particles(self):
        """Update sparks: move, shrink, and remove expired ones."""
        current_time = pygame.time.get_ticks()
        for particle in self.particles[:]:  # Copy list to safely modify
            particle["x"] += particle["dx"]  # Move X
            particle["y"] += particle["dy"]  # Move Y
            particle["size"] = max(1, particle["size"] - 0.1)  # Gradually shrink

            # Remove if expired
            if current_time > particle["lifetime"]:
                self.particles.remove(particle)


    def update(self, level_data, door, floor_items, assets, collected_items, game_over, current_level, game_data):
        """Handles player movement, searching, interactions, and power drain."""

        # global game_over  # Ensure game_over state is accessible

        # If power is depleted, trigger game over immediately
        if self.power <= 0:
            self.assets["game_over"].play()
            return "game_over"  # Stop further updates and return to main loop

        # Prevent movement if stunned
        if self.stun_timer > pygame.time.get_ticks():
            return  

        # Clear messages after timer expires
        if self.message and pygame.time.get_ticks() > self.message_timer:
            self.message = ""

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        new_sprite = self.sprite

        # Player movement & power drain (if not searching)
        if not self.is_searching:
            self.power = max(0, self.power - 0.002)  # Apply passive power drain

            if keys[pygame.K_UP]:
                new_sprite = self.assets['tl']
                self.sprite_direction = "tl"
                dx -= self.speed_x
                dy -= self.speed_y
            elif keys[pygame.K_LEFT]:
                new_sprite = self.assets['bl']
                self.sprite_direction = "bl"
                dx -= self.speed_x
                dy += self.speed_y
            elif keys[pygame.K_RIGHT]:
                new_sprite = self.assets['tr']
                self.sprite_direction = "tr"
                dx += self.speed_x
                dy -= self.speed_y
            elif keys[pygame.K_DOWN]:
                new_sprite = self.assets['br']
                self.sprite_direction = "br"
                dx += self.speed_x
                dy += self.speed_y

        new_x = self.x + dx
        new_y = self.y + dy

        # Ensure movement stays within isometric bounds - player
        if is_within_iso_bounds(new_x, new_y, 505, -270, 780, 346):
            self.x = new_x
            self.y = new_y

        self.sprite = new_sprite

        # Handle Search Interaction
        if keys[pygame.K_SPACE] and not self.is_searching and self.sprite == self.assets['tl']:
            for obj in level_data["objects"]:
                if obj.get("interactive", False):
                    dx = abs(self.x - obj["x"])
                    dy = abs(self.y - obj["y"] + (dx / 2))
                    if dx < 74 and dy < 150:
                        self.is_searching = True
                        self.search_timer = pygame.time.get_ticks() + int(obj.get("search_time", 1) * 1000)
                        self.current_object = obj
                        break

        # Apply tint based on correctness
        if self.is_searching and self.current_object:
            if pygame.time.get_ticks() >= self.search_timer:
                if self.interaction_progress < len(self.interaction_order):
                    expected_object = self.interaction_order[self.interaction_progress]
                    if self.current_object["name"] == expected_object:
                        self.assets["scan_success"].play()
                        self.interaction_progress += 1
                        self.tint_color = (0, 255, 0)  # Green
                        self.energy_waves.append({
                            "x": self.x + self.sprite.get_width() // 2,  # Center of player
                            "y": self.y + self.sprite.get_height() // 2,
                            "radius": 5,   # Start small
                            "alpha": 255,  # Fully visible
                            "growth_speed": 4,  # How fast it expands
                            "fade_speed": 8    # How fast it disappears
                        })
                    else:
                        # ❌ Incorrect search → Red Tint & Reset Progress
                        self.assets["scan_fail"].play()
                        self.interaction_progress = 0
                        self.tint_color = (255, 0, 0)  # Red
                        self.take_damage(20)  # Reduce power by 5%

                        # Trigger Sparks at the bottom of the player when scanning incorrectly
                        self.create_sparks(self.x + self.sprite.get_width() // 2, self.y + self.sprite.get_height() - 10)

                    # Apply Tint
                    self.sprite = self.tint_sprite(self.tint_color)
                    self.is_tinted = True
                    self.tint_timer = pygame.time.get_ticks() + 1500  # Tint for 1.5 sec

                self.is_searching = False
                self.current_object = None

        # Remove Tint After Timer Expires
        if self.is_tinted and pygame.time.get_ticks() >= self.tint_timer:
            self.sprite = self.assets[self.sprite_direction]  # Restore correct sprite direction
            self.is_tinted = False

        # Get player's feet position for better collision accuracy
        player_feet_x = self.x + self.sprite.get_width() // 22  # Center bottom
        player_feet_y = self.y + self.sprite.get_height() - 20  # Lower part of sprite

        # Check if player is on a floor item
        for item in floor_items[:]:  
            if item.is_wear:
                continue  # Skip wear items (they are non-interactive)

            if not item.collected and abs(player_feet_x - item.x) < 15 and abs(player_feet_y - item.y) < 15:
                item.collect(self) 
                floor_items.remove(item) 

        if door.check_door_zone(self, collected_items):  
            if self.interaction_progress < len(self.interaction_order) and self.interaction_order[self.interaction_progress] == "game_over":
                return "game_over"

            level_number = int(current_level.split("_")[1])  
            next_level = f"level_{level_number + 1}"  

            if next_level in game_data:  
                return next_level  
            else:
                return "game_complete"
            
        # Update expanding green energy rings
        for wave in self.energy_waves:
            wave["radius"] += wave["growth_speed"]  # Expand outward
            wave["alpha"] -= wave["fade_speed"]   # Gradually fade out

        # Remove fully faded waves
        self.energy_waves = [wave for wave in self.energy_waves if wave["alpha"] > 0]

        return game_over


    def draw(self, screen):
        """Draw player and active particles."""
        screen.blit(self.sprite, (self.x, self.y))

        # Draw the sparks dynamically
        for particle in self.particles:
            pygame.draw.circle(screen, (252, 248, 131), (int(particle["x"]), int(particle["y"])), int(particle["size"]))

        # Draw damage message if needed
        if self.message:
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.message, True, (255, 255, 255))
            text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 5), pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 150))

            text_x = self.x + self.sprite.get_width() // 2 - text_surface.get_width() // 2
            text_y = self.y - 30

            screen.blit(text_bg, (text_x - 5, text_y - 5))
            screen.blit(text_surface, (text_x, text_y))