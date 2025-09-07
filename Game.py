import os

import pygame, sys, random

#mixer
pygame.mixer.init()

#load file
paddle_hit_sound = pygame.mixer.Sound("108737__branrainey__boing.wav")


def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, player_score, player_2_score

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 7
    if start:
        ball_speed_x = speed * random.choice([-2, 2])  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
          # Increase player score
            ball_speed_y *= -1 # Reverse ball's vertical direction
            paddle_hit_sound.play()
    if ball.colliderect(player_2):
        if abs(ball.top - player_2.bottom) < 10:
            ball_speed_y *= -1
            paddle_hit_sound.play()
            # TODO Task 6: Add sound effects HERE




    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom >= screen_height:
        player_2_score += 1
        restart()  # Reset the game
    if ball.top <= 0:
        player_score += 1
        restart()

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def player_2_movement():
    """Handles the movement of player 2 paddle, keeping it within the screen boundaries."""
    player_2.x += player_2_speed
    if player_2.left <= 0:
        player_2.left = 0
    if player_2.right >= screen_width:
        player_2.right = screen_width


def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global player_score, player_2_score, ball_speed_x, ball_speed_y, start

    # Reset scores
    score = 0

    # Reset paddles
    player.centerx = screen_width / 2
    player_2.centerx = screen_width / 2

    # Reset ball
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = 0, 0
    start = False

def reset_game():
    """
    Completely resets the game (scores, ball, paddles).
    """
    global player_score, player_2_score, ball_speed_x, ball_speed_y, start

    # Reset scores
    player_score = 0
    player_2_score = 0

    # Reset paddles
    player.centerx = screen_width / 2
    player_2.centerx = screen_width / 2

    # Reset ball
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = 0, 0
    start = False


def game_over_screen(winner):
    """
    Displays the winner and waits for the player to press a key to restart.
    """
    global player_score, player_2_score, ball_speed_x, ball_speed_y, start

    # Clear the screen
    screen.fill(pygame.Color('black'))

    # Display winner text
    winner_text = basic_font.render(f"{winner} Wins!", True, pygame.Color('white'))
    restart_text = basic_font.render("Press R to Restart", True, pygame.Color('white'))

    # Center the texts
    screen.blit(winner_text, (screen_width / 2 - winner_text.get_width() / 2, screen_height / 2 - 50))
    screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, screen_height / 2 + 10))

    pygame.display.flip()

    # Wait for R key to reset
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()  # Reset scores, ball, paddles


# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Ask for framerate
try:
    framerate = int(input("Default framerate (30, 60, 120): "))
except ValueError:
    framerate = 60
print(f"Default framerate: {framerate} fps")


# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('purple')
green = pygame.Color('green')
light_grey = pygame.Color('grey83')
red = pygame.Color('red')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player 1 paddle
player_2 = pygame.Rect(screen_width/2 - player_width/2, 5, player_width, player_height)     # Player 2 paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
player_2_speed = 0
player_score = 0 # Player 1 (Bottom)
player_2_score = 0 # Player 2 (Top)

# Score Text setup
score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Fabian Vilaro"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
           # Player 1
            if event.key == pygame.K_LEFT:
                player_speed = -6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed = 6  # Move paddle right
            # Player 2
            if event.key == pygame.K_a:
                player_2_speed -= 6  # Move paddle left
            if event.key == pygame.K_d:
                player_2_speed += 6  # Move paddle right

            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            # Player 1
            if event.key == pygame.K_LEFT:
                player_speed = 0  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed = 0  # Stop moving right
            # Player 2
            if event.key == pygame.K_a:
                player_2_speed = -6  # Stop moving left
            if event.key == pygame.K_d:
                player_2_speed = 6  # Stop moving right
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_2_speed = 0
            if player_score >= 10 or player_2_score >= 10:
                reset_game()


    # Game Logic
    ball_movement()
    player_movement()
    player_2_movement()

    # See who won
    if player_score >= 10:
        game_over_screen("Player 1")
    elif player_2_score >= 10:
        game_over_screen("Player 2")

    # Visuals
    screen.fill(bg_color)  # Clear screen with background color
    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    pygame.draw.rect(screen, red, player_2) # Draw player 2 paddle
    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, green, ball)  # Draw ball
    player_text =  basic_font.render(f'{player_score}', True, light_grey)  # Render player 1 score
    screen.blit(player_text, (screen_width/2 - 200, screen_height/2))  # Display player 1 score on screen
    player_text_2 = basic_font.render(f'{player_2_score}', True, light_grey)
    screen.blit(player_text_2, (screen_width/2 + 200, screen_height/2))

    # Update display
    pygame.display.flip()
    clock.tick(framerate)  # Maintain framerate that is chosen by user