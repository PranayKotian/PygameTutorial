import pygame
import sys 
from random import randint, choice
from pathlib import Path

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load(PROJECT_ROOT/'graphics/player/player_walk_1.png').convert_alpha()
        walk2 = pygame.image.load(PROJECT_ROOT/'graphics/player/player_walk_2.png').convert_alpha()
        self.walk_frames = [walk1, walk2]
        self.index = 0
        self.jump = pygame.image.load(PROJECT_ROOT/'graphics/player/jump.png').convert_alpha()

        self.image = self.walk_frames[self.index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0

        #self.jumpSound = pygame.mixer.Sound(PROJECT_ROOT/'audio/jump.mp3')
        # self.jumpSound.set_volume(0.5) 

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # self.jumpSound.play()
            self.gravity = -15
    
    def apply_gravity(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
        if game_active == False:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk_frames): self.index = 0
            self.image = self.walk_frames[int(self.index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load(PROJECT_ROOT/'graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load(PROJECT_ROOT/'graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else: #type == 'snail':
            snail_1 = pygame.image.load(PROJECT_ROOT/'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(PROJECT_ROOT/'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (1000, y_pos))

    def animate(self):
        if type == 'fly':
            val = 0.15
        else: #type == 'snail':
            val = 0.1
        self.index += val
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.destroy()
        self.animate()
        self.rect.x -= 5
    
    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

def display_score():
    curtime = pygame.time.get_ticks()//1000 - start_time
    score_surf = test_font.render('Score: ' + f'{curtime}', False, (62,62,62))
    score_rect = score_surf.get_rect(center = (WIDTH/2,50))
    screen.blit(score_surf,score_rect)
    return curtime

def collision_spirte():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True




pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0 

# bg_music = pygame.mixer.Sound(PROJECT_ROOT/"audio/music.wav")
# bg_music.play(loops = -1)

PROJECT_ROOT = Path(__file__).parent

sky_surf = pygame.image.load(PROJECT_ROOT/"graphics/sky.png").convert() 
grd_surf = pygame.image.load(PROJECT_ROOT/'graphics/ground.png').convert()

test_font = pygame.font.Font(PROJECT_ROOT/'font/Pixeltype.ttf', 50)

#------------------------------Groups-------------------------------#
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#------------------------Introduction Screen------------------------#
player_stand = pygame.image.load(PROJECT_ROOT/'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (WIDTH/2, HEIGHT/2))

gametitle_surf = test_font.render('Pixel Runner', False, 'White')
gametitle_rect = gametitle_surf.get_rect(center = (WIDTH/2, 70))

gamemessage = test_font.render('Press Space to Start', False, 'White')
gamemessage_rect = gamemessage.get_rect(center = (WIDTH/2, HEIGHT-70))

#-------------------------------Timers------------------------------#
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


#-------------------------------Evolutionary Algorithm------------------------------#

#Random instructions / best instructions
#Run game
#Capture best score (w/ best instructions)
#Feed instructions back to beginning

# instructions = []
# spaceEvent = pygame.event.Event(pygame.locals.KEYDOWN, key=pygame.K_SPACE) #create the event

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()//1000
                game_active = True
    
    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(grd_surf, (0,300))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = display_score()
        game_active = collision_spirte()
    else:
        #------------------------Inro/Game Over Screen------------------------#
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(gametitle_surf, gametitle_rect)

        score_surf = test_font.render(f'Score: {score}', False, 'White')
        score_surf_rect = score_surf.get_rect(center = (WIDTH/2, HEIGHT-70))
        if score == 0: screen.blit(gamemessage, gamemessage_rect)
        else: screen.blit(score_surf, score_surf_rect) 

        #--------------------------Reset Game State--------------------------#
        

    pygame.display.update()
    clock.tick(60)