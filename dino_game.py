import pygame
import random
import sys

# Initialize pygame without the mixer to avoid audio issues
pygame.init()
# Uncomment the line below to initialize the mixer only if audio is needed
# try:
#     pygame.mixer.init()
# except Exception as e:
#     print("Audio system not initialized. Continuing without audio.")

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (100, 150, 255)
DARK_GREEN = (0, 150, 0)
DINO_GREEN = (50, 205, 50)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 36)

# Dinosaur properties
dino_x, dino_y = 50, HEIGHT - 120
dino_width, dino_height = 60, 70
ground_y = HEIGHT - 50

# Jump settings
is_jumping = False
jump_velocity = 15
velocity_y = 0

# Obstacle properties
obstacles = []
obstacle_speed = 5
obstacle_timer = 0  # Time tracker for spawning obstacles

# Score
score = 0


def draw_dinosaur(x, y):
    """Draws a stylized dinosaur using pygame shapes."""
    # Body
    pygame.draw.ellipse(screen, DINO_GREEN, (x, y + 20, 50, 30))  # Body ellipse
    pygame.draw.rect(screen, DINO_GREEN, (x + 10, y + 10, 30, 40))  # Neck rectangle
    pygame.draw.circle(screen, DINO_GREEN, (x + 25, y), 15)  # Head circle

    # Tail
    pygame.draw.polygon(screen, DINO_GREEN, [(x, y + 35), (x - 20, y + 45), (x, y + 45)])

    # Eye
    pygame.draw.circle(screen, BLACK, (x + 30, y - 5), 3)  # Small black eye

    # Mouth
    pygame.draw.line(screen, BLACK, (x + 20, y + 5), (x + 30, y + 5), 2)  # Smile line

    # Legs
    pygame.draw.rect(screen, DARK_GREEN, (x + 10, y + 50, 8, 20))  # Front leg
    pygame.draw.rect(screen, DARK_GREEN, (x + 30, y + 50, 8, 20))  # Back leg


# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling for jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        velocity_y = -jump_velocity

    # Gravity and jump mechanics
    if is_jumping:
        dino_y += velocity_y
        velocity_y += 1  # Gravity effect

        # Stop jumping when dinosaur lands on the ground
        if dino_y >= ground_y - dino_height:
            dino_y = ground_y - dino_height
            is_jumping = False

    # Obstacle spawning
    obstacle_timer += 1
    if obstacle_timer > 60:  # Spawn an obstacle every 60 frames
        obstacle_width = random.randint(20, 40)
        obstacle_height = random.randint(30, 60)
        obstacle_x = WIDTH
        obstacle_y = ground_y - obstacle_height
        obstacles.append([obstacle_x, obstacle_y, obstacle_width, obstacle_height])
        obstacle_timer = 0

    # Move and remove obstacles
    for obstacle in obstacles[:]:
        obstacle[0] -= obstacle_speed  # Move obstacle left
        if obstacle[0] + obstacle[2] < 0:  # Remove if off-screen
            obstacles.remove(obstacle)

    # Collision detection
    for obstacle in obstacles:
        if (
            dino_x < obstacle[0] + obstacle[2]
            and dino_x + dino_width > obstacle[0]
            and dino_y < obstacle[1] + obstacle[3]
            and dino_y + dino_height > obstacle[1]
        ):
            running = False  # End game on collision

    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 50))

    # Draw dinosaur
    draw_dinosaur(dino_x, dino_y)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Update and display score
    score += 1  # Increment score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Display final score
screen.fill(WHITE)
final_score_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
screen.blit(final_score_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
pygame.display.flip()
pygame.time.wait(3000)

# Quit pygame
pygame.quit()
sys.exit()
