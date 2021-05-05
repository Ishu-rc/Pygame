
import random
import math

import pygame
from pygame import mixer


# Initialize pygame
from pygame.font import Font

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space In vaders")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('rocket.png')
playerX = 370
playerY = 430
playerX_change = 0

# Enemy
enemyImg=[]
enemyX =[]
enemyY = []
enemyX_change =[]
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('tank.png'))
    enemyX.append( random.randint(0, 735))
    enemyY.append( random.randint(50, 100))
    enemyX_change.append( 0.3 )
    enemyY_change.append( 40 )

# Bullet

# Ready = can't see the bullet on screen
# Fire = the bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 430
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

#score
score_value = 0
font: Font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 128)

def show_score(x,y):
    score = font.render("score :" + str(score_value), True , (0,250,0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render('Game Over : ' + str(score_value), True, (250, 0 , 100))
    screen.blit(over_text, (250, 300))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y - 20))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((50, 50, 100))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = +0.3
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # checking for boundaries

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720

    # Enemy movement

    for i in range(num_of_enemies):

        # GAme Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 720:
            enemyX_change[i] = -0.25
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480

            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX , textY)
    pygame.display.update()
