import pygame
import random

pygame.init()

# Display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Obstacle Course")

player_color = (0, 255, 0)  # Green
obstacle_color = (255, 0, 0)  # Red
background_color = (0, 0, 0)  # Black
text_color = (255, 255, 255)  # White

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 74) 

# Player
player_width, player_height = 50, 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5


time_limit = 30
start_time = pygame.time.get_ticks()
difficulty = 'easy'  # default difficulty
obstacle_count = 5  # default obstacle count

# Game Over screen
def show_game_over():
    screen.fill(background_color)
    game_over_text = font.render("Game Over!", True, text_color)
    restart_text = small_font.render("Press R to Restart", True, text_color)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 10))
    pygame.display.flip()
    wait_for_restart()

# Win screen
def show_great_job():
    screen.fill(background_color)
    great_job_text = font.render("Great Job!", True, text_color)
    restart_text = small_font.render("Press R to Restart", True, text_color)
    screen.blit(great_job_text, (width // 2 - great_job_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 10))
    pygame.display.flip()
    wait_for_restart()

# wait for user input to restart
def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart
                    main()  # Call the main function to restart the game
                    waiting = False

# Display timer
def display_timer(elapsed_time):
    timer_text = small_font.render(f"Time Left: {int(time_limit - elapsed_time)}", True, text_color)
    screen.blit(timer_text, (10, 10))  # Position at the top left of the screen

def main():
    global player_x, player_y, obstacle_count, start_time

    # Reset player position and start time
    player_x = width // 2 - player_width // 2
    player_y = height - player_height - 10
    start_time = pygame.time.get_ticks()  # Reset start time

    # obstacles
    obstacles = []
    for _ in range(obstacle_count):
        obstacle_x = random.randint(0, width - player_width)
        obstacle_y = random.randint(-height, -50)  # Spawn above the screen
        obstacles.append((obstacle_x, obstacle_y))

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed

        # Move obstacles
        for i in range(len(obstacles)):
            obstacle_x, obstacle_y = obstacles[i]
            obstacle_y += 5  # Move down the obstacle
            if obstacle_y > height:
                obstacle_y = random.randint(-height, -50)  # Reset position above the screen
                obstacle_x = random.randint(0, width - player_width)
            obstacles[i] = (obstacle_x, obstacle_y)

        # Collision detection
        for obstacle_x, obstacle_y in obstacles:
            if (obstacle_x < player_x < obstacle_x + player_width or
                obstacle_x < player_x + player_width < obstacle_x + player_width) and \
                (obstacle_y < player_y < obstacle_y + player_height or
                 obstacle_y < player_y + player_height < obstacle_y + player_height):
                show_game_over() 

        # Check time limit
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
        if elapsed_time > time_limit:
            show_great_job()

        # Fill the background
        screen.fill(background_color)

        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

        # Draw the obstacles
        for obstacle_x, obstacle_y in obstacles:
            pygame.draw.rect(screen, obstacle_color, (obstacle_x, obstacle_y, player_width, player_height))

        # Display timer
        display_timer(elapsed_time)

        # Update display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(30)

# Difficulty selection
def select_difficulty():
    global obstacle_count
    screen.fill(background_color)
    welcome_text = big_font.render("Welcome!", True, text_color)
    easy_text = small_font.render("Press 1 for Easy", True, text_color)
    medium_text = small_font.render("Press 2 for Medium", True, text_color)
    hard_text = small_font.render("Press 3 for Hard", True, text_color)

    screen.blit(welcome_text, (width // 2 - welcome_text.get_width() // 2, height // 2 - 80))
    screen.blit(easy_text, (width // 2 - easy_text.get_width() // 2, height // 2))
    screen.blit(medium_text, (width // 2 - medium_text.get_width() // 2, height // 2 + 40))
    screen.blit(hard_text, (width // 2 - hard_text.get_width() // 2, height // 2 + 80))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    obstacle_count = 5
                    waiting = False
                elif event.key == pygame.K_2:  # Medium
                    obstacle_count = 7
                    waiting = False
                elif event.key == pygame.K_3:  # Hard
                    obstacle_count = 10
                    waiting = False

# Start the game
select_difficulty()
main()
pygame.quit()
