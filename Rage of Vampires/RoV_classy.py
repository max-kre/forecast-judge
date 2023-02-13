import pygame
# from pygame.locals import *
from pygame import mixer
from sys import exit
import random
from Flyer import Flyer
from Explosion import Explosion
from time import sleep

print(__name__)

DIFFICULTYSCALE = 5

class Button:
    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.screen = pygame.display.get_surface()

		# top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#000000'

		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'

        #text
        self.gui_font = gui_font = pygame.font.Font(None,30)
        self.text_surf = gui_font.render(text,True,'#cc0000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # show cursor
        pygame.mouse.set_visible(True)

		# elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        #screen = pygame.display.set_mode((500,500))
        pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#575757'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                return 1
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print('click')
                    self.pressed = False

        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#cccccc'


class RoV_Game:
    def __init__(self) -> None:
        print("init start")
        # game setup:
        pygame.init()
        self.screen = pygame.display.set_mode((1800,900))
        pygame.display.set_caption('Rage of Vampires 3 - Definitiv(ly not good) edition')
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.game_mode = 0
        self.run_game = True
        
        #intial parameters:
        self.hit_counter = 0
        self.life = 3
        
        #groups and class images
        self.vampireExplosions = pygame.sprite.Group()
        self.explosion = pygame.image.load('Graphics/explosion.png').convert_alpha()
        self.flyersprites = pygame.sprite.Group()
        # self.vamp = pygame.image.load('Graphics/bat_xs.png').convert_alpha()
        # self.pigeon = pygame.image.load('Graphics/pigeon_s.png').convert_alpha()
        # self.firefly = pygame.image.load('Graphics/Firefly.png').convert_alpha()
        self.heart = pygame.image.load('Graphics/heart_s.png').convert_alpha()
        self.heart_rect = self.heart.get_rect()
        self.bckdrop = pygame.image.load('Graphics/bck.jpg').convert()
        self.gui_font = pygame.font.Font(None, 50)
        self.crosshair = pygame.image.load('Graphics/crosshair.png').convert_alpha()

        self.bckdrop_menu = pygame.image.load('Graphics/menu-bck.jpg').convert()
        self.leftbar_bck = pygame.Surface((350,900))
        self.leftbar_bck.fill('black')
        self.leftbar_bck.set_alpha(180)
        self.button_quit_menu = Button('Quit',260,40,(45,800),5)
        self.button_options_menu= Button('Options',260,40,(45,260),5)
        self.button_highscore_menu = Button('Highscore',260,40,(45,170),5)
        self.button_newgame_menu = Button('New Game',260,40,(45,80),5)

        self.bckdrop_credits = pygame.image.load('Graphics/credits.png').convert()
        self.button_quit_credits = Button('Quit',300,50,(800,360),5)
        self.button_highscore_credits = Button('Highscore',300,50,(800,280),5)
        self.button_newgame_credits = Button('New Game',300,50,(800,200),5)

        #player shooting
        self.can_shoot = True
        self.shot_time = None
        self.reload_duration = 300

        #Flyer spawning
        self.can_spawn_bat = True
        self.spawn_time_bat = None
        self.spawn_cooldown_bat = 1000
        self.spawn_chance_bat = 100 #%
        self.can_spawn_pigeon = True
        self.spawn_time_pigeon = None
        self.spawn_cooldown_pigeon = 2000
        self.spawn_chance_pigeon = 10 #%
        self.can_spawn_firefly = True
        self.spawn_time_firefly = None
        self.spawn_cooldown_firefly = 2000
        self.spawn_chance_firefly = 10 #%

        #music
        mixer.init()
        mixer.music.load('Audio/spooky.wav')
        mixer.music.play(-1)

        print("init done")
      
    
    def update_ui(self):
        #counter oben rechts
        counter_surf = self.gui_font.render(str(self.hit_counter), False, "red")
        counter_rect = counter_surf.get_rect(midright=(1790,25))
        self.screen.blit(counter_surf, counter_rect)

        #crosshair
        mouse_pos = pygame.mouse.get_pos()
        ## rect from mouse-pos as center
        self.crosshair_rect = self.crosshair.get_rect(center = mouse_pos)
        self.screen.blit(self.crosshair, self.crosshair_rect)
        ##
        # self.screen.blit(self.crosshair, (mouse_pos[0]-60, mouse_pos[1]-60))
        
        # update HP
        if self.life > 0:
            self.screen.blit(self.heart,(10,820))
        if self.life > 1:
            self.screen.blit(self.heart,(70,820))
        if self.life > 2:
            self.screen.blit(self.heart,(130,820))
        if self.life == 0:
            print('killed again')
            # self.cred_state = True
            # self.credits()
            self.game_mode = 99
            return False
        return True

    def gamemode(self):
        while self.run_game:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         print("I wanna quit")
            #         self.run_game = False
            #         pygame.quit()
            #         exit()
            if self.game_mode == 0:
                self.menu()
            elif 0 < self.game_mode < 99:
                self.run()
            elif self.game_mode == 99:
                self.credits()
            else:
                self.run_game = False

    
    def run(self):
        in_gameloop = True
        pygame.mouse.set_visible(False)
        
        while in_gameloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("I wanna quit")
                    self.run_game = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.can_shoot:
                    self.can_shoot = False
                    self.shot_time = pygame.time.get_ticks()
                    for b in self.flyersprites.sprites():
                        if b.rect.collidepoint(event.pos):
                        #if b.rect.collidepoint(mouse_pos):
                        # if b.rect.colliderect(self.crosshair_rect):
                            b.got_hit()
                            print("collision")

            self.screen.blit(self.bckdrop,(0,0))
            self.spawn_flyer()

            # for event in pygame.event.get():
            
            if not self.can_shoot:
                if pygame.time.get_ticks() >= self.shot_time + self.reload_duration:
                    self.can_shoot = True

            self.change_gamemode()
            in_gameloop = self.update_game()

            self.clock.tick(60)
            

    def change_gamemode(self):
        self.game_mode = self.hit_counter//DIFFICULTYSCALE + 1
        
    def change_life(self, value):
        self.life += value
        if self.life > 3:
            self.life = 3

    def flyer_hit(self,pos,score_points):
        self.hit_counter += score_points
        Explosion(pos,self.explosion,[self.vampireExplosions])

    def spawn_flyer(self):
        tick_now = pygame.time.get_ticks()
        speed_multiplyer = 1 + self.game_mode/100
        if self.can_spawn_bat:
            if random.randrange(0,1000)/10 <= self.spawn_chance_bat:
                y_spawnheight = random.randrange(50,750)
                Flyer((1900,y_spawnheight),self.change_life, self.flyer_hit,[self.flyersprites],"bat",speed_multiplyer)
            self.can_spawn_bat = False
            self.spawn_time_bat = tick_now
        else:
            if tick_now > self.spawn_time_bat + self.spawn_cooldown_bat / (1 + self.game_mode / 50):
                self.can_spawn_bat = True
        if self.can_spawn_pigeon:
            if random.randrange(0,1000)/10 <= self.spawn_chance_pigeon * (1 + self.game_mode / 50):
                y_spawnheight = random.randrange(50,750)
                Flyer((1900,y_spawnheight),self.change_life, self.flyer_hit,[self.flyersprites],"pigeon",speed_multiplyer)
            self.can_spawn_pigeon = False
            self.spawn_time_pigeon = tick_now
        else:
            if tick_now > self.spawn_time_pigeon + self.spawn_cooldown_pigeon / (1 + self.game_mode / 50):
                self.can_spawn_pigeon = True
        if self.can_spawn_firefly:
            if random.randrange(0,1000)/10 <= self.spawn_chance_firefly / (1 + self.game_mode / 50):
                x_spawn = random.randrange(100,1700)
                y_spawnheight = random.randrange(50,750)
                Flyer((x_spawn,y_spawnheight),self.change_life, self.flyer_hit,[self.flyersprites],"firefly",speed_multiplyer)
            self.can_spawn_firefly = False
            self.spawn_time_firefly = tick_now
        else:
            if tick_now > self.spawn_time_firefly + self.spawn_cooldown_firefly * (1 + self.game_mode / 50):
                self.can_spawn_firefly = True
    
    def reset_game(self):
        self.vampireExplosions = pygame.sprite.Group()
        self.flyersprites = pygame.sprite.Group()
        self.game_mode = 1
        self.hit_counter = 0
        self.life = 3

    def credits(self):
        print("credits started")
        in_creditloop = True
        while in_creditloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("I wanna quit credits")
                    pygame.quit()
                    exit()
            self.screen.blit(self.bckdrop_credits, (0,0))
            self.button_newgame_credits.draw()
            self.button_highscore_credits.draw()
            self.button_quit_credits.draw()
            if self.button_quit_credits.check_click() == 1:
                print ("exiting")
                sleep(0.2)
                pygame.quit()
                exit()
            if self.button_newgame_credits.check_click() == 1:
                print ("new game")
                self.reset_game()
                in_creditloop = False
            pygame.display.update()
            self.clock.tick(60)

    ### new shit from Pichael, probably doesn't work
    def menu(self):
        
        print("menu started")
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("I wanna quit menu")
                    pygame.quit()
                    exit()
            self.screen.blit(self.bckdrop_menu, (0,0))
            self.screen.blit(self.leftbar_bck, (0,0))
            self.button_newgame_menu.draw()
            self.button_highscore_menu.draw()
            self.button_options_menu.draw()
            self.button_quit_menu.draw()
            if self.button_quit_menu.check_click() == 1:
                print ("exiting")
                sleep(0.2)
                pygame.quit()
                exit()
            if self.button_newgame_menu.check_click() == 1:
                print ("new game")
                self.reset_game()
                in_menu = False
            pygame.display.update()
            self.clock.tick(60)


    def update_game(self):
        #draw explosions
        #for e in self.vampireExplosions.sprites():
        #    e.timeout()
        self.vampireExplosions.update() #calls "update" function defined in each sprite
        self.vampireExplosions.draw(self.screen)
        
        #move bats
        # for b in self.flyersprites.sprites():
        #     b.move()
        self.flyersprites.update() #calls "update" function defined in each sprite
        self.flyersprites.draw(self.screen)
        
        #update UI
        self.update_ui()

        pygame.display.update()

if __name__ == "__main__":
    game = RoV_Game()
    game.gamemode()
