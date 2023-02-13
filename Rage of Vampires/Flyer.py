import pygame
from math import sin,cos
import random

#move_RL-stat range
SPEED = [3,8]
YWAVELENGTH = [100, 300]
YAMP = [10, 50]
FLOATSPEED = 100
FLOATRADIUS = 10
FIREFLYLIFETIME = 2000

#flyer-types
# FLYER_TYPES = {
#     "bat" : {"can_cause_damage" : True, "move_type" : "RL", "score_points" : 1,"life_when_shot" : 0,"image" : pygame.image.load('Graphics/bat_xs.png').convert_alpha()},
#     "pigeon" : {"can_cause_damage" : False, "move_type" : "RL", "score_points" : 0,"life_when_shot" : -1, "image": pygame.image.load('Graphics/pigeon_s.png').convert_alpha()},
#     "firefly" : {"can_cause_damage" : False, "move_type" : "float", "score_points" : 0,"life_when_shot" : 1, "image" : pygame.image.load('Graphics/Firefly.png').convert_alpha()},
# }

class Flyer(pygame.sprite.Sprite):
    def __init__(self, pos, change_life, hitcounter, groups, flyer_type, speed_multiplyer) -> None:
        super().__init__(groups)
        # self.pos = pos
        self.FLYER_TYPES = {
            "bat" : {"can_cause_damage" : True, "move_type" : "RL", "score_points" : 1,"life_when_shot" : 0,"image" : pygame.image.load('Graphics/bat_xs.png').convert_alpha()},
            "pigeon" : {"can_cause_damage" : False, "move_type" : "RL", "score_points" : 0,"life_when_shot" : -1, "image": pygame.image.load('Graphics/pigeon_s.png').convert_alpha()},
            "firefly" : {"can_cause_damage" : False, "move_type" : "float", "score_points" : 0,"life_when_shot" : 1, "image" : pygame.image.load('Graphics/Firefly.png').convert_alpha()},
        }
        self.startpos = pos
        self.type = flyer_type
        # self.y_baseline = pos[1]
        self.image = self.FLYER_TYPES[flyer_type]["image"]
        self.rect = self.image.get_rect(center=pos)
        self.change_life = change_life
        self.roll_stats(speed_multiplyer)
        if self.type == "firefly":
            #einmal ausführen, um firefly an den gerollten offset zu bewegen
            self.move_float()
        self.hitcounter = hitcounter
        self.spawn_time = pygame.time.get_ticks()
        
        #from FLYER_TYPES
        self.can_cause_damage = self.FLYER_TYPES[flyer_type]["can_cause_damage"]
        if self.FLYER_TYPES[flyer_type]["move_type"] == "RL":
            self.movement = self.move_RL
        elif self.FLYER_TYPES[flyer_type]["move_type"] == "float":
            self.movement = self.move_float
        self.score_points = self.FLYER_TYPES[flyer_type]["score_points"]
        self.life_when_shot = self.FLYER_TYPES[flyer_type]["life_when_shot"]
    
    def roll_stats(self,speed_multiplyer):
        self.ywavelength = random.randrange(YWAVELENGTH[0], YWAVELENGTH[1])
        self.yamp = random.randrange(YAMP[0], YAMP[1])
        self.speed = speed_multiplyer * random.randrange(SPEED[0], SPEED[1])
        self.float_offset = [random.randrange(0,250), random.randrange(0,250)]

    def move_RL(self):
        self.rect.x -= self.speed
        self.rect.y = self.startpos[1] + self.yamp*sin(self.rect.x/self.ywavelength)
        if self.rect.right <= 0:
            self.got_through()

    def move_float(self):
        now_tick = pygame.time.get_ticks()
        self.rect.x = self.startpos[0] + FLOATRADIUS*sin((now_tick+self.float_offset[0])/FLOATSPEED)
        self.rect.y = self.startpos[1] + FLOATRADIUS*sin((now_tick+self.float_offset[1])/FLOATSPEED)

    def got_hit(self):
        self.hitcounter(self.rect.center,self.score_points)
        if self.life_when_shot != 0:
            self.change_life(self.life_when_shot)
        self.kill()

    def got_through(self):
        if self.can_cause_damage:
            self.change_life(-1)
        self.kill()

    def update(self):
        self.movement()
        if self.type == 'firefly':
            self.blink()
            self.check_end_of_life()

    def blink(self):
        blink_rate = 60
        now_tick = pygame.time.get_ticks()
        alpha = 255*(1+sin(now_tick/blink_rate))
        self.image.set_alpha(alpha)
        # darken = int(abs(10*sin(now_tick)))
        # self.image.fill((darken, darken, darken), special_flags=pygame.BLEND_RGB_SUB)
        # brighten = int(10*abs(cos(now_tick)))
        # self.image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)

    def check_end_of_life(self):
        if pygame.time.get_ticks() > self.spawn_time + FIREFLYLIFETIME:
            self.kill()
