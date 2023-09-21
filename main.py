import pygame
import sys

HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkey Idle")

# Create a Clock object to control the frame rate
clock = pygame.time.Clock()

# Desired frames per second (FPS)
fps = 30

# Common color variables
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
gray = (128, 128, 128)
brown = (139, 69, 19)  # RGB color for brown

# Initialize the banana count and upgrades
banana_count = 0
bananas_per_second = 0

class Upgrade:
    def __init__(self, name, base_cost, banana_per_second, description):
        self.name = name
        self.base_cost = base_cost
        self.banana_per_second = banana_per_second
        self.description = description
        self.owned = 0

    def calculate_cost(self):
        # Calculate the cost of the next upgrade with a 5% increase
        return round(self.base_cost * 1.05**self.owned)

    def buy_upgrade(self, banana_count):
        cost = self.calculate_cost()
        if banana_count >= cost:
            banana_count -= cost
            self.owned += 1
            return True  # Upgrade was purchased
        return False  # Upgrade purchase failed

    def get_banana_production(self):
        # Calculate the total banana production per second from this upgrade
        return self.banana_per_second * self.owned

# Create a list of upgrades
upgrades = [
    Upgrade("Recruit a Monkey", 20, 1, "Hire a monkey to collect bananas for you."),
    # Add more upgrades here as needed
]

# Initialize the font
pygame.font.init()
font = pygame.font.SysFont(None, 36)  # Using a built-in font

def calculate_monkey_cost(base_cost, owned):
    # Calculate the cost of the next monkey with a 5% increase
    return round(base_cost * 1.05**owned)

def is_upgrade_button_clicked(upgrade_button, event):
    return (
        event.type == pygame.MOUSEBUTTONDOWN
        and event.button == 1
        and upgrade_button.collidepoint(event.pos)
    )

def display_upgrades(screen, font, upgrades, banana_count, y_offset, event):
    for upgrade in upgrades:
        upgrade_cost = upgrade.calculate_cost()
        upgrade_text = font.render(
            f'{upgrade.name} - Cost: {upgrade_cost} Bananas', True, white)
        upgrade_rect = upgrade_text.get_rect()
        upgrade_rect.right = WIDTH - 20  # Position on the right side
        upgrade_rect.top = y_offset  # Position from the top
        screen.blit(upgrade_text, upgrade_rect)

        # Draw a smaller upgrade button underneath the upgrade description
        button_width = 100
        button_height = 30
        upgrade_button_rect = pygame.Rect(WIDTH - button_width - 20, y_offset + 40, button_width, button_height)
        pygame.draw.rect(screen, green, upgrade_button_rect)
        button_text = font.render("Buy", True, black)
        text_rect = button_text.get_rect()
        text_rect.center = upgrade_button_rect.center
        screen.blit(button_text, text_rect)

        # Check for click on the upgrade button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_upgrade_button_clicked(upgrade_button_rect, event) and banana_count >= upgrade_cost:
                banana_count -= upgrade_cost
                upgrade.buy_upgrade(banana_count)

        y_offset += 80



def main():
    global banana_count, bananas_per_second, upgrades  # Declare global variables
    pygame.init()
    running = True

    # Variable to track the last time the passive effect was applied
    last_passive_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse button click events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button (button == 1)
                # Check if the click occurred within the bounds of the banana
                banana_rect = pygame.Rect(100, 200, 50, 200)
                if banana_rect.collidepoint(event.pos):
                    # Increase the banana count when the banana is clicked
                    banana_count += 1

        # Call the display_upgrades function with the event parameter
        display_upgrades(screen, font, upgrades, banana_count, 100, event)  # Pass the event variable

        # Check and apply passive effects from upgrades
        current_time = pygame.time.get_ticks()
        if current_time - last_passive_time >= 1000:
            bananas_per_second = sum(upgrade.get_banana_production() for upgrade in upgrades)
            banana_count += bananas_per_second
            last_passive_time = current_time

        # Clear the screen
        screen.fill(black)  # Fill the screen with black

        # Draw a tall banana shape on the left side
        banana_rect = pygame.Rect(100, 200, 50, 200)  # Define the dimensions of the banana
        pygame.draw.ellipse(screen, yellow, banana_rect)  # Draw an ellipse with yellow color

        # Draw a brown stem on top of the banana (overlapping)
        stem_rect = pygame.Rect(115, 150, 20, 50)  # Define the dimensions of the stem
        pygame.draw.rect(screen, brown, stem_rect)  # Draw a brown rectangle for the stem

        # Display the bananas per second (BPS) text on the left side over the banana
        bps_text = font.render(f'BPS: {bananas_per_second}', True, white)
        bps_rect = bps_text.get_rect()
        bps_rect.left = 20  # Position on the left side
        bps_rect.top = 20  # Position from the top
        screen.blit(bps_text, bps_rect)

        # Display the banana count text on the right side
        text = font.render(f'Bananas: {banana_count}', True, white)
        text_rect = text.get_rect()
        text_rect.right = WIDTH - 20  # Position on the right side
        text_rect.top = 20  # Position from the top

        # Ensure text doesn't go outside of the screen
        if text_rect.right > WIDTH:
            text_rect.right = WIDTH
            text_rect.left -= 20  # Move it a little to the left

        screen.blit(text, text_rect)

        # Display upgrades
        display_upgrades(screen, font, upgrades, banana_count, 100, event)  # Pass the event variable

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
