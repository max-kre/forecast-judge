import pygame
from pygame.locals import *
from pygame import mixer
from sys import exit
import random


pygame.init()

#To DO:
# - learn how to use sprites and use it here.

# game setup:
screen = pygame.display.set_mode((1800,900))
pygame.display.set_caption('Rage of Vampires 3 - Definitiv(ly not good) edition')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

#intial parameters:
hit_counter = 0
life = 3
vamp_gravity = 0
vamp_hit = 0

# loading fonts and images:
counter_font = pygame.font.Font(None, 50)

bckdrop = pygame.image.load('Graphics/bck.jpg').convert()
vamp = pygame.image.load('Graphics/bat_xs.png').convert_alpha()
vamp_rect = vamp.get_rect(midbottom = (1000,300))
heart = pygame.image.load('Graphics/heart_s.png').convert_alpha()
heart_rect = heart.get_rect()
explosion = pygame.image.load('Graphics/explosion.png').convert_alpha()
explosion_rect = explosion.get_rect()
crosshair = pygame.image.load('Graphics/crosshair.png').convert_alpha()

# setting music:
mixer.init()
mixer.music.load('Audio/spooky.wav')
mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #initial setup
    screen.blit(bckdrop,(0,0))
    counter_surf = counter_font.render(str(hit_counter), False, "red")
    counter_rect = counter_surf.get_rect(midright=(1790,25))
    screen.blit(counter_surf, counter_rect)

    #vampire movement
    screen.blit(vamp, vamp_rect)
    vamp_rect.x -= 5
    if vamp_rect.right == 0:
        vamp_rect.right = 1800
        vamp_rect.bottom = random.randrange(50,800)
        life -=1

    # cursor and shooting
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(crosshair, (mouse_pos[0]-60, mouse_pos[1]-60))
    if event.type == pygame.MOUSEBUTTONDOWN and vamp_rect.collidepoint(event.pos):
#        mouse_presses = pygame.mouse.get_pressed()
#        if mouse_presses[0]:     
            print("collision")
            collision_pos = event.pos
            vamp_hit = 1
            hit_counter += 1

    #vampire hit effect
    if vamp_hit ==1:
        start_time = pygame.time.get_ticks()
        screen.blit(explosion,(500,500))                                                                           # needs work
        if pygame.time.get_ticks() > start_time + 2000:                                                            # that shit also doesn't work
            vamp_hit = 0
    
    # lifes
    if life == 3:
        screen.blit(heart,(10,820))
        screen.blit(heart,(70,820))
        screen.blit(heart,(130,820))
    if life == 2:
        screen.blit(heart,(10,820))
        screen.blit(heart,(70,820))
    if life == 1:
        screen.blit(heart,(10,820))
    if life == 0:
        print('killed again')

    
    pygame.display.update()
    clock.tick(60)