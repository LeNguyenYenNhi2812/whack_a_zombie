import pygame
import os
import random
from os import path
from pygame.locals import *

game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')


WIDTH = 800
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BG = (17,166,41)

COL =3
ROW =3

pygame.init()

pygame.mixer.init()




screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Whack A Zombie!")
# screen.fill(WHITE)
clock = pygame.time.Clock()

#mouse
mouse_pos = (0,0)
pygame.mouse.set_visible(False)
hit_num = 3
last_update = pygame.time.get_ticks()
score = 0
miss = 0
pos=0
countdown = 3

last_countdown = pygame.time.get_ticks()
gameOver = False
# sound
bonk = pygame.mixer.Sound(os.path.join(img_folder, 'bonk.mp3'))
miss_sound = pygame.mixer.Sound(os.path.join(img_folder, 'miss.mp3'))
BGmusic = pygame.mixer.Sound(os.path.join(img_folder, 'BGmusic.mp3'))
#img

mound = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'mound.png')).convert_alpha(),(150, 150))
mound_list_rect = []
hammer = []
hammer.append(pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'hammer1.png')).convert_alpha(),(100, 100)))
hammer.append(pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'hammer2.png')).convert_alpha(),(100, 100)))
hammer_img=hammer[0]
hammer_rect=hammer_img.get_rect()

mole = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'mole.png')).convert_alpha(),(100, 100))
mole_rect=mole.get_rect()

def draw_mound():
    x,y=0,0
    for row in range(ROW):
        x=0
        for col in range(COL):
           screen.blit(mound, (x*200+140, y*200+100)) 
           pygame.draw.rect(screen, BG, (x*200+140, y*200+200,150,70))
           rect = pygame.Rect(x*200+140, y*200+130, 150, 70)
        #    pygame.draw.rect(screen, RED, rect, 1)  # draw rectangle around mounds
           mound_list_rect.append(rect)
           x+=1
        y+=1

def random_mole():
    random_mound = random.choice(mound_list_rect)
    mole_rect.midtop=random_mound.midbottom
    return random_mound[1]-70

def draw_text(text, font_size, font_color, x,y):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, font_color)
    screen.blit(text_surface, (x, y))

def draw_countdown():
    global countdown, last_countdown
    now = pygame.time.get_ticks()
    if now - last_countdown > 1000:
        last_countdown = now
        countdown -= 1
    draw_text(f'Time: {countdown}', 50, WHITE, WIDTH//2, 20)

run = True


BGmusic.play(-1)
BGmusic.set_volume(0.1) 



while run:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and hit_num == 0:
            if event.button == 1 and not gameOver:
                if mole_rect.collidepoint(mouse_pos):
                    bonk.play()
                    score += 1
                    pos=random_mole()
                else:
                    miss_sound.play()
                    miss += 1
                    # print("miss")
                
                hammer_img=hammer[1]
                
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                hammer_img=hammer[0]
        if event.type == KEYUP:
            if event.key == K_r and gameOver:
                hit_num = 3
                score = 0
                miss = 0
                countdown = 3
                gameOver = False
                pos=random_mole()
                last_countdown = pygame.time.get_ticks()
                # print("restart") 
        mouse_pos=pygame.mouse.get_pos()
        hammer_rect.center=(mouse_pos[0],mouse_pos[1])
    pygame.display.flip()


    now = pygame.time.get_ticks()
    if now - last_update > 1000 and hit_num > 0:
        last_update = now
        hit_num -= 1
        pos=random_mole()

    mole_rect.y -=1
    if mole_rect.y <= pos:
        # pos=random_mole()
        mole_rect.y = pos
    screen.fill(BG)
    
    if hit_num >0:
        draw_text(f'Start: {hit_num}', 50, WHITE, WIDTH//2-30, HEIGHT//2-90)
    else:
        screen.blit(mole,mole_rect)
        if not gameOver:
            draw_countdown()
            draw_text(f'Score: {score}', 50, WHITE, 15, 20)
            draw_text(f'Miss: {miss}', 50, WHITE, 15, 70)
    draw_mound()
    if countdown == 0:
        gameOver = True

        overlay = pygame.Surface((500, 500))  
        overlay.set_alpha(180)  # Độ trong suốt (0 = trong suốt, 255 = đục hoàn toàn)
        overlay.fill(WHITE)  
        screen.blit(overlay, (150, 150))

        draw_text('Game Over', 80, RED, WIDTH//2-200, HEIGHT//2-180)
        draw_text(f'Final Score: {score}', 50, BLUE, WIDTH//2-200, HEIGHT//2-70)
        if score + miss > 0:
            hit_rate = score / (score + miss)
        else:
            hit_rate = 0  # Tránh lỗi chia 0
        draw_text(f'Hit Rate: {hit_rate:.2%}', 50, BLUE, WIDTH//2-200, HEIGHT//2)
        draw_text('Press R to restart', 30, WHITE, WIDTH//2-200, HEIGHT//2+80)
    
    screen.blit(hammer_img,hammer_rect)

pygame.quit()