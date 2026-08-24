from tkinter import *
import pygame as pg
import random

# Initialize Tkinter
window = Tk()

window.configure(bg="#0000FF")

running = False # contrlled by Tkinter(only beging when the player click start)

# Constants for the colours in hexadecimal
GREEN = "#006A4E"
RED = "#FF0000"
WHITE = "#FFFFFF"
BLUE = "#0000FF"


def start():
    global running, score,spaceship, bullets, asteroids
    running = True
    play_btn.configure(state="disabled")
    window.destroy() # Close Tkinter to start the game



play_btn = Button(window, text="CLICK HERE TO PLAY!", command = start, bg = BLUE, fg = RED)
play_btn.grid(row=4,column=3,rowspan=1, columnspan=4)

start_txt = Label(window, text=f"SPACE INVADERS ",fg=RED,bg=BLUE)
start_txt.grid(row=1,column=3,columnspan=4)

start_txt = Label(window, text=f"USE ARROW KEYS TO NAVIGATE THE SPACE SHIP AND SPACE TO SHOOT", fg = WHITE, bg= BLUE)
start_txt.grid(row=2,column=4,columnspan=4)

start_txt = Label(window, text=f"Press j or k to switch between JETS", fg = WHITE, bg= BLUE)
start_txt.grid(row=3,column=3,columnspan=4)



# Complete this section

mainloop()


# Initialize pygame
pg.init()
pg.mixer.init()  # Initialize the mixer for sound effects

# Load sound effects
laser_sfx = pg.mixer.Sound("laser.mp3")
laser_sfx.set_volume(1.0)  # Set to max volume for firing sound
biglaser_sfx = pg.mixer.Sound("biglaser.mp3")
biglaser_sfx.set_volume(1.0)  # Set to max volume for ultimate ability sound

# Set the screen to fullscreen and get the screen size
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pg.display.set_caption("Space Shooter - Atari Style")  # Set the window caption

WHITE = (255, 255, 255)
BLACK = (0, 0, 40)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Ultimate bullet color

SPACESHIP_WIDTH = 140
SPACESHIP_HEIGHT = 140
BULLET_WIDTH = 5
BULLET_HEIGHT = 5
BIGBULLET_WIDTH = 300
BIGBULLET_HEIGHT = 20
ASTEROID_HEIGHT = 130
ASTEROID_WIDTH = 120

SPACESHIP_SPEED = 10
BULLET_SPEED = 30
ASTEROID_SPEED = 7

# Ultimate ability settings
BIGLASER_COOLDOWN = 10000  # 10 seconds
BIGLASER_DURATION = 1000  # 1 second
biglaser_available = False
biglaser_start_time = 0
last_biglaser_time = 0

font = pg.font.SysFont("Times", 50)

spaceship_img = pg.image.load("spaceship.png")
spaceship_img = pg.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship = pg.Rect(WIDTH / 2 - SPACESHIP_WIDTH / 2, HEIGHT - 130, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

bullets = []
asteroids = []
score = 0
can_fire = True  # Track firing cooldown
clock = pg.time.Clock()


def create_asteroid():
    x = random.randint(0, WIDTH - ASTEROID_WIDTH)
    y = -ASTEROID_WIDTH
    return pg.Rect(x, y, ASTEROID_WIDTH, ASTEROID_HEIGHT)


while running:
    events = pg.event.get()
    keys = pg.key.get_pressed()
    current_time = pg.time.get_ticks()

    # Movement controls
    if keys[pg.K_a] and spaceship.left > 0:
        spaceship.x -= SPACESHIP_SPEED
    if keys[pg.K_LEFT] and spaceship.left > 0:
        spaceship.x -= SPACESHIP_SPEED
    if keys[pg.K_d] and spaceship.right < WIDTH:
        spaceship.x += SPACESHIP_SPEED
    if keys[pg.K_RIGHT] and spaceship.right < WIDTH:
        spaceship.x += SPACESHIP_SPEED

    # Activate ultimate ability
    if keys[pg.K_b] and not biglaser_available and current_time - last_biglaser_time >= BIGLASER_COOLDOWN:
        biglaser_available = True
        biglaser_start_time = current_time
        last_biglaser_time = current_time

        # Fire multiple beams
        for offset in range(-60, 80):
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH // 2, spaceship.top + offset, BIGBULLET_WIDTH, BIGBULLET_HEIGHT))

        biglaser_sfx.play()

    # Deactivate ultimate ability after duration
    if biglaser_available and current_time - biglaser_start_time >= BIGLASER_DURATION:
        biglaser_available = False

    # Event processing
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and can_fire:
                # Fire bullets in a column
                bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top - 20, BULLET_WIDTH, BULLET_HEIGHT))
                bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top, BULLET_WIDTH, BULLET_HEIGHT))
                bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top + 20, BULLET_WIDTH, BULLET_HEIGHT))

                # Play laser sound
                laser_sfx.play()

                can_fire = False

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                can_fire = True

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move asteroids
    for asteroid in asteroids[:]:
        asteroid.y += ASTEROID_SPEED
        if asteroid.top > HEIGHT:
            asteroids.remove(asteroid)

        # Check for collisions
        for bullet in bullets[:]:
            if asteroid.colliderect(bullet):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score += 10
                break
        if spaceship.colliderect(asteroid):
            running = False

    # Spawn asteroids based on score
    diff = min(1 + score // 200, 50)
    if random.randint(1, 100) <= diff:
        asteroids.append(create_asteroid())

    # Render
    screen.fill(BLACK)
    screen.blit(spaceship_img, (spaceship.x, spaceship.y))
    for bullet in bullets:
        pg.draw.rect(screen, YELLOW if bullet.width > 50 else GREEN, bullet)
    for asteroid in asteroids:
        pg.draw.rect(screen, RED, asteroid)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display ultimate cooldown
    if biglaser_available:
        cooldown_text = font.render("Ultimate Active!", True, GREEN)
    elif current_time - last_biglaser_time < BIGLASER_COOLDOWN:
        remaining_cooldown = (BIGLASER_COOLDOWN - (current_time - last_biglaser_time)) // 1000
        cooldown_text = font.render(f"Cooldown: {remaining_cooldown}s", True, WHITE)
    else:
        cooldown_text = font.render("Ultimate Ready! Press 'B'", True, GREEN)
    screen.blit(cooldown_text, (10, 50))

    pg.display.update()
    clock.tick(60)

# Game over screen
gameover_txt = font.render(f"YOU GOT HIT! SCORE: {score}", True, WHITE)
screen.fill(BLACK)
screen.blit(gameover_txt, (WIDTH // 2 - gameover_txt.get_width() // 2, HEIGHT // 2 - 30))
pg.display.update()
pg.time.wait(3000)


replay = False

# Replay loop
while not replay:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            replay = True

# Reset game state
score = 0
asteroids = []
big_asteroids = []
bullets = []
spaceship.x = WIDTH / 2 - SPACESHIP_WIDTH / 2
spaceship.y = HEIGHT - 60

# Restart main game loop
running = True