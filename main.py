import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()
# loop
loop = 0
# create screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('space.jpg')
# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("Rodolfo Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('rodolfo.png')
playerImg1 = pygame.image.load('rodolfo.png')
playerImg2 = pygame.image.load('rodolfo2.png')
playerImg3 = pygame.image.load('rodolfo3.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien2.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(40)
# Bullet
bulletImg = pygame.image.load('fireball.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# GameOver text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    playerImg = playerImg3
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (int(x), int(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x + 16), int(y + 10)))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # if keystroke is pressed check whether is right or left
    if event.type == pygame.KEYDOWN:
        # print("A keystroke has been pressed")
        if event.key == pygame.K_LEFT:
            # print("Left arrow is pressed")
            playerX_change = -7.5
        if event.key == pygame.K_RIGHT:
            #   print("Right arrow is pressed")
            playerX_change = 7.5
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                playerImg = playerImg2
                bulletX = playerX
                fire_bullet(playerX, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #  print("Keystroke has been released")
            playerX_change = 0

        # RGB colors
    screen.fill((0, 0, 0))
    # add background
    screen.blit(background, (0, 0))
    # movement
    playerX += playerX_change
    # No out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            if loop == 0:
                pygame.mixer.music.stop()
                over_Sound = mixer.Sound('over.wav')
                over_Sound.play()
                loop = +1
            playerImg = playerImg3
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        # No out of bounds
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            playerImg = playerImg1
            explosion_Sound = mixer.Sound('clap.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        playerImg = playerImg1
    if bullet_state == "fire":
        fire_bullet(int(bulletX), int(bulletY))
        bulletY -= bulletY_change

    # Update Screen
    player(int(playerX), int(playerY))
    show_score(textX, textY)
    pygame.display.update()
