import math
import random
import pygame

stars=[[random.randint(0,800),random.randint(0,600)]for i in range(100)]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')

playerImg = pygame.image.load('spaceship.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))

bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (32, 32))

enemyImg = pygame.image.load('enemy.png')
enemyImg = pygame.transform.scale(enemyImg, (32, 32))

bossImg = pygame.image.load('boss.png')
bossImg = pygame.transform.scale(bossImg, (128, 128))

exposionSound=pygame.mixer.Sound('explosion.mp3')
winningSound=pygame.mixer.Sound('winning.mp3')
backgroundSound=pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

playerX = 370
playerY = 520
playerSpeed = 1

bulletX = 0
bulletY = playerY
bulletSpeed = 3
bulletState = "ready"

bossX=random.randint(0,800)
bossY=random.randint(0,600)
bossActive=False
bossHealth=50
bossDamagemultiplier=2
bossDirection=1
bossSpeed=2

# Enemy setup
enemyX = random.randint(0, 768)
enemyY = random.randint(0, 150)
enemyYspeed = 0.5  # vertical movement speed

# Score
score = 0
high_score = 0

# Load/save high score
def load_high_score():
    global high_score
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0

def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

# UI Screens
def show_start_screen():
    font = pygame.font.Font(None, 64)
    text = font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (200, 250))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_score(x, y):
    font = pygame.font.Font(None, 32)
    text = font.render(f"Score: {score}  High Score: {high_score}", True, (255, 255, 255))
    screen.blit(text, (x, y))

def show_win_screen():
    font = pygame.font.Font(None, 64)
    text = font.render("New High Score!", True, (255, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (200, 250))
    pygame.display.update()
    pygame.time.wait(3000)

# Drawing functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 16, y))

def enemySpawn(x, y):
    screen.blit(enemyImg, (x, y))

def bossSpawn(x,y):
    screen.blit(bossImg,(x,y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    return distance < 40

# Load high score and show start screen
load_high_score()
show_start_screen()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    for star in stars:
        star[1]+=1
        if star[1]>600:
            star[0]=random.randint( 0,800)
            star[1]=0
        pygame.draw.circle(screen,(255,255,255),star,2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Boss Spawn
    if((score%500==0)and (score!=0) and (not bossActive)):
        bossActive = True
        bossHealth = 50 * bossDamagemultiplier
        bossX = random.randint(0, 672)
        bossY = 100
        
    #Boss Chaloa
    if(bossActive):
        bossX+= bossDirection*bossSpeed
        if bossX <= 0 or bossX >= 672:
            bossDirection *= -1
        bossSpawn(bossX,bossY)

    #Boss Collision
    if isCollision(bossX, bossY, bulletX, bulletY) and bulletState == 'fire':
        bulletState = 'ready'
        bulletY = playerY
        bossHealth -= 10
        if bossHealth <= 0:
            score += 50
            exposionSound.play()
            bossActive = False 
            bossDamagemultiplier *= 2
            winningSound.play()  


    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT]:
        playerX += playerSpeed

    # Keep player within bounds
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Fire bullet on space hold
    if keys[pygame.K_SPACE] and bulletState == "ready":
        bulletX = playerX
        bulletY = playerY
        bulletState = "fire"

    # Bullet movement
    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletSpeed
        if bulletY <= 0:
            bulletState = "ready"

    # Collision detection
    if isCollision(enemyX, enemyY, bulletX, bulletY) and bulletState == 'fire':
        bulletState = 'ready'
        bulletY = playerY
        score += 10
        if score > high_score:
            high_score = score
        enemyX = random.randint(0, 768)
        enemyY = random.randint(0, 150)
        exposionSound.play()

    # Enemy vertical movement
    enemyY += enemyYspeed
    if enemyY > 600:  # off the bottom
        enemyX = random.randint(0, 768)
        enemyY = random.randint(0, 150)

    # Game over if enemy reaches player
    if enemyY >= playerY:
        running = False

    # Draw everything
    enemySpawn(enemyX, enemyY)
    player(playerX, playerY)
    show_score(10, 10)
    pygame.display.update()

# End of game
save_high_score()
if score == high_score and score != 0:
    show_win_screen()

pygame.quit()
