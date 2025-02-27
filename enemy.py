import pygame
import random
from walls import is_within_iso_bounds  # Ensure movement stays in bounds

# Define movement boundaries (same as player)
TOP_WALL_Y = 545
RIGHT_WALL_Y = -250
BOTTOM_WALL_Y = 820
LEFT_WALL_Y = 357

class SentryBot:
    def __init__(self, x, y, speed, assets):
        """Initialize sentry bot with bouncing movement."""
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = random.choice([-1, 1]) * max(speed, 0.4)  # Ensure at least 0.4 speed
        self.dy = random.choice([-1, 1]) * max(speed, 0.4)  # Prevent zero movement
        self.image = assets["sentry_bot"]

        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

        # Debug Log (Now without patrol range)


    def update(self):
        """Move the sentry bot with controlled randomness and bounce off walls."""
        
        # Introduce occasional direction changes (every 1.5 - 3 sec)
        if not hasattr(self, "next_turn_time"):
            self.next_turn_time = pygame.time.get_ticks() + random.randint(1500, 3000)

        if pygame.time.get_ticks() > self.next_turn_time:
            if random.random() < 0.5:  # 50% chance to change X or Y direction
                self.dx = random.choice([-1, 1]) * self.speed
            if random.random() < 0.5:
                self.dy = random.choice([-1, 1]) * self.speed
            self.next_turn_time = pygame.time.get_ticks() + random.randint(1500, 3000)  # Reset timer

        # Apply brief speed bursts, but reset after
        if not hasattr(self, "speed_boost_end"):
            self.speed_boost_end = 0

        if random.random() < 0.01 and pygame.time.get_ticks() > self.speed_boost_end:  # 1% chance per frame
            self.dx *= 1.5  # Temporary speed boost
            self.dy *= 1.5
            self.speed_boost_end = pygame.time.get_ticks() + random.randint(500, 1000)  # Lasts 0.5 - 1 sec

        # Reset speed after burst ends
        if pygame.time.get_ticks() > self.speed_boost_end:
            if self.dx != 0:
                self.dx = self.dx / abs(self.dx) * self.speed  # Reset X speed if nonzero
            else:
                self.dx = random.choice([-1, 1]) * self.speed  # Reset if stuck

            if self.dy != 0:
                self.dy = self.dy / abs(self.dy) * self.speed  # Reset Y speed if nonzero
            else:
                self.dy = random.choice([-1, 1]) * self.speed  # Reset if stuck

        # Slight drift to break predictability
        if random.random() < 0.1:  # 10% chance per frame
            self.dx += random.choice([-0.2, 0.2])
            self.dy += random.choice([-0.2, 0.2])

        # Calculate new position
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Check wall collisions and bounce
        hit_x = not is_within_iso_bounds(new_x, self.y, TOP_WALL_Y, RIGHT_WALL_Y, BOTTOM_WALL_Y, LEFT_WALL_Y)
        hit_y = not is_within_iso_bounds(self.x, new_y, TOP_WALL_Y, RIGHT_WALL_Y, BOTTOM_WALL_Y, LEFT_WALL_Y)

        if hit_x and hit_y:
            self.dx *= -1
            self.dy *= -1
        elif hit_x:
            self.dx *= -1
        elif hit_y:
            self.dy *= -1

        # Apply movement
        self.x += self.dx
        self.y += self.dy


    def check_collision(self, player):
        """Checks if the sentry bot collides with the player's lower body (feet), deals damage, and bounces off."""
        sentry_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        # Adjust player collision box to only include feet area
        player_feet_x = player.x
        player_feet_y = player.y + (player.sprite.get_height() * 0.7)  # Only bottom 30% of sprite
        player_feet_rect = pygame.Rect(player_feet_x, player_feet_y, player.sprite.get_width(), player.sprite.get_height() * 0.3)

        if sentry_rect.colliderect(player_feet_rect):  # Now only detects hits near feet
            if pygame.time.get_ticks() > player.invincible_timer:  # Prevent rapid damage
                player.take_damage(45)  # Reduce power
                player.invincible_timer = pygame.time.get_ticks() + 1000  # 1 second invincibility
                player.assets["enemy_hit"].play()

                # Reflect bot in opposite direction
                self.dx *= -1  
                self.dy *= -1  

    def draw(self, screen):
        """Draw sentry bot."""
        screen.blit(self.image, (self.x, self.y))
