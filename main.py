import pygame
import os
import random
from os import path
from pygame.locals import *
import threading
game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')
zombie_folder = os.path.join(img_folder, 'zombie/attack')
dead_zombie = os.path.join(img_folder, 'zombie/die')

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
hit_num =1
last_update = pygame.time.get_ticks()
score = 0
miss = 0
pos=0
hit = False
# ! cao đao
countdown1 = 30
countdown=countdown1
current_frame = 0
current_frame1=0
frame_rate= 50
frame_rate1 = 50
last_countdown = pygame.time.get_ticks()
old_rect=pygame.Rect(0, 0, 0, 0)  
dead_last_frame = pygame.time.get_ticks()
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

attack_images = []
for i in range(12):  
    img_path = os.path.join(zombie_folder, f"Attacking_{i:03}.png")
    attack_images.append(pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (100, 100)))
dead_images = []
for i in range(15): 
    img_path = os.path.join(dead_zombie, f"Dying_{i:03}.png")
    dead_images.append(pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (100, 100)))

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

value=0
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False  
        if event.type == MOUSEBUTTONDOWN and hit_num == 0:
            if event.button == 1 and not gameOver:
                if mole_rect.collidepoint(mouse_pos):
                    bonk.play()
                    score += 1
                    hit=True
                    old_rect = mole_rect.copy()
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
                countdown = countdown1
                gameOver = False
                pos=random_mole()
                last_countdown = pygame.time.get_ticks()
                # print("restart") 
        mouse_pos=pygame.mouse.get_pos()
        hammer_rect.center=(mouse_pos[0],mouse_pos[1])
    if hit:
        now = pygame.time.get_ticks()
        if now - dead_last_frame > 50:
            dead_last_frame=now
            value+=1
            if value>=len(dead_images):
                value=0
                hit=False
            
        image = dead_images[value]
        screen.blit(image, old_rect)   
            # time.sleep(1)  
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
        # Trick lỏ
        if not gameOver:
            screen.blit(attack_images[current_frame],mole_rect)
            if frame_rate > 0:
                frame_rate -=1
            else:
                current_frame = (current_frame + 1) % len(attack_images)
                frame_rate=40
            
            # time.sleep(frame_rate)
            
            # time.sleep(1)
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