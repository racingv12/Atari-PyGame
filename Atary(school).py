

from tkinter import *



window = Tk()

window.configure(bg="#000011")

running = False # contrlled by Tkinter(only beging when the player click start)

# Constants for the colours in hexadecimal
GREEN = "#006A4E"
RED = "#FF0000"
WHITE = "#FFFFFF"
BLUE = "#000011"


def start():
    global running, score,spaceship, bullets, asteroids
    running = True
    play_btn.configure(state="disabled")
    window.destroy() # Close Tkinter to start the game



play_btn = Button(window, text="CLICK HERE TO PLAY!", command = start, bg = BLUE, fg = RED)
play_btn.grid(row=4,column=3,rowspan=1, columnspan=4)

intro_txt = Label(window, text=f"SPACE INVADERS ",fg=RED,bg=BLUE)
intro_txt.grid(row=1,column=3,columnspan=4)

guide_txt = Label(window, text=f"USE ARROW KEYS TO NAVIGATE THE SPACE SHIP AND SPACE TO SHOOT", fg = WHITE, bg= BLUE , font = ("Helvetica", 9,"bold"))
guide_txt.grid(row=2,column=4,columnspan=4)

 # makes z , x , c Bolded
cosmetic_txt = Label(window, 
                        text="Press ", fg=WHITE, bg=BLUE, font=("Helvetica", 9))
cosmetic_txt.grid(row=3, column=4, columnspan=2)

zxc_txt = Label(window, 
                   text="z, x, or c", fg=WHITE, bg=BLUE, font=("Helvetica", 9, "bold"))
zxc_txt.grid(row=3, column=4, columnspan=3)

cosmetic_txt2 = Label(window, 
                         text=" to switch between JETS", fg=WHITE, bg=BLUE, font=("Helvetica", 9 ))
cosmetic_txt2.grid(row=3, column=5, columnspan=4)

# hit text 
hint_txt = Label(window, text = " Hint : The blue asteroids give you 50 points ..", fg = WHITE , bg = BLUE)
hint_txt.grid(row = 5 , column = 3, columnspan = 4)

# Complete this section

mainloop()




import pygame as pg
import random




pg.init()
#pg.mixer.init()



WIDTH = 400
HEIGHT = 300

screen = pg.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
BLACK = (0,0,40)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# space ship, Astroid,and bullet sizing

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 40
BULLET_WIDTH = 5
BULLET_HEIGHT = 5
BIGBULLET_HEIGHT = 10
BIGBULLET_WIDTH = 100
ASTEROID_HEIGHT = 30
ASTEROID_WIDTH = 20

#Speed system

SPACESHIP_SPEED = 3
BULLET_SPEED = 10
ASTEROID_SPEED = 1

#fonts


font = pg.font.SysFont('Times',20)

# loading space ships

spshp1 = "spaceship.png"
spshp2 = "spaceship2.png"
spshp3 = "spaceship3.png"

shown = spshp1

spaceship_img = pg.image.load(shown)
spaceship_img = pg.transform.scale(spaceship_img, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))

# Initializing Spaceship

spaceship = pg.Rect(WIDTH / 2 - SPACESHIP_WIDTH / 2, HEIGHT - 60,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)



#list of bullets

bullets = []

#list of asteroids

asteroids = []

# Big asteroids

big_asteroids = []

#score and high score 

score = 0



clock = pg.time.Clock()

#laser_sfx = pg.mixer.Sound("laser.mp3")
#laser_sfx.set_volume(1.0)  # Set to max volume

def create_asteroid():
    x = random.randint(0, WIDTH - ASTEROID_WIDTH)
    y = -ASTEROID_WIDTH # asteroids start coming down from the top of the screen
    return pg.Rect(x, y, ASTEROID_WIDTH, ASTEROID_HEIGHT)



def create_big_asteroid():
    x = random.randint(0, WIDTH - ASTEROID_WIDTH)
    y = -ASTEROID_WIDTH
    return pg.Rect(x, y, ASTEROID_WIDTH+10, ASTEROID_HEIGHT+10)

# system for the ultimate bility that is avaible every 10 seconds
biglaser_cooldown = 10000 # 10 seconds in millisecods
biglaser_avb = False # when the laser is avaible
biglaser_start = 0 # when the laser starts firing
biglaser_duration = 1000
last_time_used = 0


# Keeping track of High_score 

highscore = 0

while True:


    while running:
        
        
        current_time = pg.time.get_ticks() # gives us current time
        events = pg.event.get()
        keys = pg.key.get_pressed()
        
        
        
        
        
        #movement of space ship and shooting
        if keys[pg.K_a]  and spaceship.left > 0: # moving left (a )
            spaceship.x -= SPACESHIP_SPEED
        if keys[pg.K_LEFT]  and spaceship.left > 0: # moving left (<--)
            spaceship.x -= SPACESHIP_SPEED
        
        
        if keys[pg.K_d]  and spaceship.right < WIDTH: # moving right (d)
            spaceship.x += SPACESHIP_SPEED
        if keys[pg.K_RIGHT]  and spaceship.right < WIDTH: # moving right (-->)
            spaceship.x += SPACESHIP_SPEED
        
        
        
        
        if keys[pg.K_w]  and spaceship.bottom > 0: # moving up (w)
            spaceship.y -= SPACESHIP_SPEED
        if keys[pg.K_UP]  and spaceship.bottom > 0: # moving right ( up arrow )
            spaceship.y -= SPACESHIP_SPEED
        
        if keys[pg.K_s]  and spaceship.bottom < HEIGHT: # moving down (s)
            spaceship.y += SPACESHIP_SPEED
        if keys[pg.K_DOWN]  and spaceship.bottom < HEIGHT: # moving right ( down arrow )
            spaceship.y += SPACESHIP_SPEED
        
        
        
        
        # switches the looks of the spaceship based on the button you press
        if keys[pg.K_z]  and spaceship.right < WIDTH:
            shown = spshp2
            spaceship_img = pg.image.load(shown)
            spaceship_img = pg.transform.scale(spaceship_img, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
    
        if keys[pg.K_x]  and spaceship.right < WIDTH:
            shown = spshp1
            spaceship_img = pg.image.load(shown)
            spaceship_img = pg.transform.scale(spaceship_img, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
        if keys[pg.K_c]:
            shown = spshp3
            spaceship_img = pg.image.load(shown)
            spaceship_img = pg.transform.scale(spaceship_img, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
    
        
        
        
        
        # Activates ultimate ability in a proper manner
        if keys[pg.K_b] and not biglaser_avb and current_time - last_time_used  >= biglaser_cooldown:
            biglaser_avb = True
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top -30 ,BIGBULLET_WIDTH,BIGBULLET_HEIGHT)) # It sends 7 rays of the ultimate ability evty time you press it 
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top - 10 ,BIGBULLET_WIDTH,BIGBULLET_HEIGHT)) 
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 10 ,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 30 ,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 50 ,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 70,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 90,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
            bullets.append(pg.Rect(spaceship.centerx - BIGBULLET_WIDTH/2 , spaceship.top + 110,BIGBULLET_WIDTH,BIGBULLET_HEIGHT))
    
    
    
            biglaser_start = current_time # record when the laser starts 
            last_time_used = current_time # Update last time used
            
            
        if biglaser_avb and current_time - biglaser_start >= biglaser_duration:
            biglaser_avb = False
            
        
        can_fire = True
        
        for event in events:
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and can_fire:
                    # it fires three bullets every time you click space 
                    bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top - 20, BULLET_WIDTH, BULLET_HEIGHT))  # Top bullet
                    bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top, BULLET_WIDTH, BULLET_HEIGHT))  # Middle bullet
                    bullets.append(pg.Rect(spaceship.centerx - BULLET_WIDTH // 2, spaceship.top + 20, BULLET_WIDTH, BULLET_HEIGHT))  # Bottom bullet
                    can_fire = False  # Disable firing until key is released
                
        
            
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    can_fire = True
                
            
        
        
        
        
        
        #bullets moving
        for bullet in bullets[:]: 
            bullet.y -= BULLET_SPEED
            if bullet.bottom < 0: # removes the bullet from the list to avoid lag
                bullets.remove(bullet)
        
        screen.fill(BLACK)
        screen.blit(spaceship_img, (spaceship.x,spaceship.y))
        
        for bullet in bullets:
            pg.draw.rect(screen,GREEN, bullet)
        
        
        
            
        
        
        for big_asteroid in big_asteroids[:]:
            
            big_asteroid.y += ASTEROID_SPEED
            if big_asteroid.top > HEIGHT:
                big_asteroids.remove(big_asteroid)
            
            #checking for hits, and colision with the spaceship
            for bullet in bullets[:]:
                if big_asteroid.colliderect(bullet): # uses colliderect to check for bullet hitting the asteroid
                    big_asteroids.remove(big_asteroid)
                    bullets.remove(bullet)
                    score += 50
            
                    break
                
            if spaceship.colliderect(big_asteroid):
                running = False # ends game once asteroid hits the space ship
                
                if score > highscore:
                    highscore = score
                
        
        
        for asteroid in asteroids[:]:
            asteroid.y += ASTEROID_SPEED
            if asteroid.top > HEIGHT:
                asteroids.remove(asteroid)
            
            #checking for hits, and colision with the spaceship
            for bullet in bullets[:]:
                if asteroid.colliderect(bullet): # uses colliderect to check for bullet hitting the asteroid
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    score += 10
                    break
                
            if spaceship.colliderect(asteroid):
                
                running = False # ends game once asteroid hits the space ship 
                if score > highscore:
                    highscore = score
        
        
        
        # changes the odds of asteroid spawning based on your score
        
        diff = min(1 + score // 200 , 50) 
        
        
        if random.randint(1,100) <= diff: #the ods of asteriods spawning
            asteroids.append(create_asteroid())
        
        for asteroid in asteroids:
            pg.draw.rect(screen,RED, asteroid)
           
        
        diff_r = min(0.01 + score // 400 , 50) 
        
        if random.randint(1,100) <= diff_r: #the ods of asteriods spawning
            big_asteroids.append(create_big_asteroid())
        for big_asteroid in big_asteroids:
            pg.draw.ellipse(screen, BLUE, big_asteroid)
           
           
        # prints Score   
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        #Shows when the ultimate ability is avaible
        if biglaser_avb:
            cooldown_text = font.render("Ultimate Active!", True, GREEN)
        elif current_time - last_time_used < biglaser_cooldown:
            remaining_cooldown = (biglaser_cooldown - (current_time - last_time_used)) // 1000
            cooldown_text = font.render(f"Cooldown: {remaining_cooldown}s", True, WHITE)
        else:
            cooldown_text = font.render("Ultimate Ready! Press 'B'", True, GREEN)
        screen.blit(cooldown_text, (10, 30))
        
        pg.display.update()
        
        clock.tick(60)

    # game over screen
    
    
    gameover_txt = font.render(f"YOU GOT HIT! SCORE: {score}",True, WHITE)
    highscore_txt = font.render(f"HIGH SCORE : {highscore}", True, WHITE )
    worldr_txt = font.render(f"WORLD RECORD: 7350",True, WHITE)
    replay_txt = font.render("Press R to play again", True, WHITE)
    screen.fill(BLACK)
    screen.blit(gameover_txt, (WIDTH // 2 - gameover_txt.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(highscore_txt, (WIDTH // 2 - gameover_txt.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(worldr_txt, (WIDTH // 2 - gameover_txt.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(replay_txt, (WIDTH // 2 - gameover_txt.get_width() // 2, HEIGHT // 2 - 90))
    pg.display.update()
    keys = pg.key.get_pressed()
    
    
    replay = False 
    
    # reseting everything if you want to play again
    while not replay and running == False  :
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        
        for event in pg.event.get():
            
            
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                replay = True 
                running = True
                screen.fill(BLACK)
                score = 0
                asteroids = []
                big_asteroids = []
                bullets = []
                spaceship.x = WIDTH / 2 - SPACESHIP_WIDTH/2
                spaceship.y = HEIGHT - 60
                
                # system for the ultimate bility that is avaible every 10 seconds
                current_time = pg.time.get_ticks() # gives us current time
                biglaser_cooldown = 10000 # 10 seconds in millisecods
                biglaser_avb = False # when the laser is avaible
                biglaser_start = 0 # when the laser starts firing
                biglaser_duration = 1000
                last_time_used = 0
                
                biglaser_start = current_time # record when the laser starts 
                last_time_used = current_time # Update last time used
            
