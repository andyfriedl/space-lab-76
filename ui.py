import pygame
import random





class UI:
    def __init__(self, title_font):
        """Initialize the UI system."""
        pygame.font.init()
        self.font = pygame.font.Font("fonts/Retro Floral.otf", 18)  # Regular UI font
        self.hint_font = pygame.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 20)  # Hint font
        self.start_font = pygame.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 40)  # Hint font
        self.title_font = title_font
        self.last_search_time = " ---" 
        

    def draw_title(self, screen):
        """Draws the game title at the top-left of the screen with '76' in red & blue."""
        space_lab_text = self.title_font.render("Space Lab ", True, (255, 255, 255))
        seven_text = self.title_font.render("7", True, (255, 44, 44))  # Red
        six_text = self.title_font.render("6", True, (62, 133, 198))  # Blue

        x_offset = 20
        screen.blit(space_lab_text, (x_offset, 10))
        x_offset += space_lab_text.get_width() + 5
        screen.blit(seven_text, (x_offset, 10))
        x_offset += seven_text.get_width()
        screen.blit(six_text, (x_offset, 10))
    
    def draw_power_bar(self, screen, player):
        """Draws a power-style energy bar (0-100 scale)."""
        bar_width = 200  
        bar_height = 20
        x, y = 10, 200  # Position of the power bar 

        # Calculate remaining power bar width
        current_width = (player.power / 100) * bar_width

        # Determine color based on power level
        if player.power > 65:
            color = (0, 255, 0)  # Green
        elif player.power > 20:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        # Display "Power" text
        text_surface = self.font.render(f"Battery: {round(player.power, 1)}%", True, (255, 255, 255))
        screen.blit(text_surface, (x, y - 35)) # Above the power bar
        
        # Draw power bar background
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height), 2)

        # Draw the current power level
        if player.power > 0:
            pygame.draw.rect(screen, color, (x, y, current_width, bar_height))

    def draw_hint(self, screen, player):
        """Draws the hint message above VOX (centered) with multi-line support."""
        if player.hint_message and pygame.time.get_ticks() < player.hint_timer:
            lines = player.hint_message.split("\n")  # Support multi-line hints
            max_width = max(self.hint_font.size(line)[0] for line in lines)  # Find widest line
            line_height = self.hint_font.get_height()
            
            text_x = player.x + (player.sprite.get_width() // 2) - (max_width // 2)
            text_y = player.y - (20 + (line_height * len(lines)))  # Adjust height for multiple lines

            # Draw semi-transparent background
            bg_rect = pygame.Rect(text_x - 5, text_y - 5, max_width + 10, (line_height * len(lines)) + 10)
            # Create a semi-transparent surface
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((1, 46, 1, 170))  # Green with transparency (RGBA)

            # Blit the transparent surface onto the screen
            screen.blit(bg_surface, (bg_rect.x, bg_rect.y))

            # Render and draw each line separately
            for i, line in enumerate(lines):
                text_surface = self.hint_font.render(line, True, (51, 255, 51))  # Green text
                screen.blit(text_surface, (text_x, text_y + (i * line_height)))  # Position each line correctly

    def draw_start_screen(self, screen):
        """Draws the start screen with title and instructions."""
        screen.fill((0, 0, 0))  # Black background

        # Stylized "Space Lab 76" Title
        space_lab_text = self.title_font.render("Space Lab ", True, (255, 255, 255))
        seven_text = self.title_font.render("7", True, (255, 44, 44))  # Red
        six_text = self.title_font.render("6", True, (62, 133, 198))  # Blue

        title_x = screen.get_width() // 2 - (space_lab_text.get_width() + seven_text.get_width() + six_text.get_width()) // 2
        screen.blit(space_lab_text, (title_x, 100))
        screen.blit(seven_text, (title_x + space_lab_text.get_width(), 100))
        screen.blit(six_text, (title_x + space_lab_text.get_width() + seven_text.get_width(), 100))

        # Instructions (Centered Block but Left-Aligned Text)
        instructions = [
            "• Use Arrow Keys to Move",
            "• Press SPACE to Scan Wall Objects",
            "• Collect Floor Items for Power & Hints",
            "• Unlock the Door by Scanning in Order",
            "• Avoid Enemy Drones!",
        ]

        font = pygame.font.Font(None, 28)  # Adjusted font size for readability

        # Find the widest text line for proper centering
        max_width = max(font.render(line, True, (255, 255, 255)).get_width() for line in instructions)
        instruction_x = screen.get_width() // 2 - max_width // 2  # Centered Block
        y_offset = 200

        for line in instructions:
            text_surface = font.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (instruction_x, y_offset))
            y_offset += 30

        # "Press Any Key to Start" Prompt (Centered)
        prompt_surface = self.start_font.render("Press Any Key to Start", True, (51, 255, 51))
        screen.blit(prompt_surface, (screen.get_width() // 2 - prompt_surface.get_width() // 2, y_offset + 40))

        pygame.display.flip()  # Refresh screen


    def draw_glitch_effect(screen, intensity, shake_offset):
        """Creates scanline and distortion glitch effects."""
        width, height = screen.get_size()
        
        # Apply scanline effect
        for i in range(0, height, 4):  # Spaced scanlines
            if random.random() < 0.5:  # Randomly flicker lines
                pygame.draw.line(screen, (0, 0, 0), (0, i), (width, i), 1)
        
        # Apply pixel shift distortion
        for _ in range(intensity):
            y = random.randint(0, height - 10)
            slice_height = random.randint(2, 10)
            shift = random.randint(-10, 10)
            screen.blit(screen, (shift, y), (0, y, width, slice_height))
        
        # Apply screen shake
        screen_offset_x = random.randint(-shake_offset, shake_offset)
        screen_offset_y = random.randint(-shake_offset, shake_offset)
        
        return screen_offset_x, screen_offset_y
    
    
    
    
    def draw_game_over(self, screen):
        """Display Game Over screen with centered text."""
        screen.fill((0, 0, 0))  # Black screen
        
        text = self.title_font.render("GAME OVER", True, (255, 44, 44))  # Red Text
        instruction = self.start_font.render("Press Any Key to Restart", True, (51, 255, 51))  

        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 3))
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, screen.get_height() // 2))
        
        pygame.display.flip()  # Make sure it's drawn




    def draw(self, screen, player, door):
        """Draw UI elements on the screen with better spacing and correct ordering."""
        
        self.draw_power_bar(screen, player)
        
        ui_elements = []

        # Show Interaction Progress
        progress_text = f"Progress: {player.interaction_progress}/{len(player.interaction_order) - 1}"
        ui_elements.append((progress_text, (255, 255, 255)))

        # Door Status
        door_label = "Door:  "
        door_status = " Unlocked" if door.is_open else " Locked"
        door_color = (0, 255, 0) if door.is_open else (255, 0, 0)  # Green for unlocked, Red for locked

        # Show remaining search time with milliseconds
        if player.is_searching:
            remaining_time_ms = max(1, player.search_timer - pygame.time.get_ticks())  # Never go below 1ms
            remaining_time_sec = remaining_time_ms / 1000.0  # Convert to seconds
            self.last_search_time = f"{remaining_time_sec:.2f}s"  # Format as 2 decimal places
        searching_text = f"Scanning: {self.last_search_time}"  # Always on screen

        # Draw UI text
        y_offset = 90  # Start lower to avoid overlapping title
        line_spacing = 35

        # Draw "Door: " in white and status in red/green
        door_label_surface = self.font.render(door_label, True, (255, 255, 255))  # White
        door_status_surface = self.font.render(door_status, True, door_color)  # Red/Green

        screen.blit(door_label_surface, (20, y_offset))
        screen.blit(door_status_surface, (10 + door_label_surface.get_width(), y_offset))
        y_offset += line_spacing

        # "Searching..." always on screen, updates only value
        searching_surface = self.font.render(searching_text, True, (255, 255, 255))
        screen.blit(searching_surface, (20, y_offset))
    
    
