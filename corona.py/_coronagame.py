import pygame
from pygame import mixer
import random
import math
pygame.init()

fps = pygame.time.Clock()
FPS = 60

mixer.music.load('bgm.wav')
mixer.music.play(-1)

window = pygame.display.set_mode((800,600))
bg = pygame.image.load('room.jpg')



pygame.display.set_caption("GO CORONA GO")
playerimg = pygame.image.load('cutie.jpeg')
playerX = 370
playerY = 480
playerX_change = 0


enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyCount = 6

for i in range(enemyCount):
   enemyimg.append(pygame.image.load('virus.jpg'))
   enemyX.append(random.randint(0,735))
   enemyY.append(random.randint(50,150))
   enemyX_change.append(4)
   enemyY_change.append(40)

bulletimg = pygame.image.load('shield.jpg')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
status = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Vanished Coronas:"+ str(score_value),True,(255,0,255))
    window.blit(score,(x,y)) 

def game_over_text():
    over_text = over_font.render("GO TO HOSPITAL",True,(0,0,0))
    window.blit(over_text,(100,250)) 


def player(x,y):
    window.blit(playerimg,(x,y))

def enemy(x,y,i):
    window.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global status
    status = "fire"
    window.blit(bulletimg,(x+16,y+10))   

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False   




running = True
while running:
    window.fill((0,0,0))
    window.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                
            if event.key == pygame.K_SPACE:
                if status is "ready":
                    bullet_sound = mixer.Sound('laserru.wav')
                    bullet_sound.play()
                    bulletX = playerX
                fire_bullet(bulletX,bulletY)



        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736 


    for i in range(enemyCount):

        if enemyY[i] > 420:
            for j in range(enemyCount):
                enemyY[j] = 2000
            mixer.music.stop()
            gameover_sound = mixer.Sound('laserru.wav')
            gameover_sound.play()
            game_over_text()
            break    
    




        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
          enemyX_change[i] = 4
          enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
           enemyX_change[i] = -4
           enemyY[i] += enemyY_change[i] 

        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY) 
        if collision:
          exp_sound = mixer.Sound('explosion.wav')
          exp_sound.play()
          bulletY = 480
          status = "ready"  
          score_value += 1
           
          enemyX[i] = random.randint(0,735)

          enemyY[i]= random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)






    if bulletY <= 0:
        bulletY = 480
        status = "ready"

    if status is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= 10  

    
    player(playerX,playerY)

    fps.tick(FPS)
   
    show_score(textX,textY)
    pygame.display.update()