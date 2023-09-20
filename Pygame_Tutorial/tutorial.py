import pygame
from sys import exit
from random import randint
from pathlib import Path

def display_score():
    curtime = pygame.time.get_ticks()//1000 - start_time
    score_surf = test_font.render('Score: ' + f'{curtime}', False, (62,62,62))
    score_rect = score_surf.get_rect(center = (WIDTH/2,50))
    screen.blit(score_surf,score_rect)
    return curtime

def obstacle_movement(obs_list):
    for rect in obs_list:
        rect.x -= 5
        if rect.bottom == 300:
            screen.blit(snail_surf,rect)
        elif rect.bottom == 210:
            screen.blit(fly_surf,rect)
    obs_list = [obs for obs in obs_list if obs.x > -100]
    return obs_list

def player_collision(player, obs_list):
    for rect in obs_list:
        if player.colliderect(rect):
            return False
    return True

pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0 

PROJECT_ROOT = Path(__file__).parent

#test_surface = pygame.Surface((100,200))
#test_surface.fill('Red')
sky_surf = pygame.image.load(PROJECT_ROOT/"graphics/sky.png").convert() 
grd_surf = pygame.image.load(PROJECT_ROOT/'graphics/ground.png').convert()

test_font = pygame.font.Font(PROJECT_ROOT/'font/Pixeltype.ttf', 50)
# txt_surf = test_font.render('Score:', False, (62,62,62))
# txt_rect = txt_surf.get_rect(midtop = (WIDTH/2, 30))

#-----------------------------Obstacles-----------------------------#
snail_surf = pygame.image.load(PROJECT_ROOT/'graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load(PROJECT_ROOT/'graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []

#------------------------------Player-------------------------------#
player_surf = pygame.image.load(PROJECT_ROOT/'graphics/player/player_walk_1.png').convert_alpha()
#player_rect = pygame.Rect(left,top,width,height)
player_rect = player_surf.get_rect(midbottom = (100,300))
player_gravity = 0

#------------------------Introduction Screen------------------------#
player_stand = pygame.image.load(PROJECT_ROOT/'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (WIDTH/2, HEIGHT/2))

gametitle_surf = test_font.render('Pixel Runner', False, 'White')
gametitle_rect = gametitle_surf.get_rect(center = (WIDTH/2, 70))

gamemessage = test_font.render('Press Space to Start', False, 'White')
gamemessage_rect = gamemessage.get_rect(center = (WIDTH/2, HEIGHT-70))

#-------------------------------Timer-------------------------------#
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -15
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -15
            if event.type == obstacle_timer:
                if randint(0,1):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))
                    
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_rect.bottom = 300
                start_time = pygame.time.get_ticks()//1000
                game_active = True
        
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rec.collidepoint(event.pos): print('collision')
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print('mouse up')
    
    if game_active:
        #Background
        screen.blit(sky_surf, (0,0))
        screen.blit(grd_surf, (0,300))

        # pygame.draw.rect(screen, 'Light Blue', txt_rect)
        # pygame.draw.rect(screen, 'Light Blue', txt_rect, 10)
        #screen.blit(txt_surf, txt_rect)

        #Player
        player_gravity += 0.8
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = player_collision(player_rect, obstacle_rect_list)
        
        #snail collision
        # if player_rect.colliderect(snail_rect):
        #     game_active = False

        score = display_score()

        #KEYBOARD INPUT
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('space')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rec.collidepoint(mouse_pos):
        #     print('collision')
        # if player_rec.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())
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
        obstacle_rect_list.clear()
        player_rect.midbottom = (100,300)
        player_gravity = 0

    pygame.display.update()
    clock.tick(60)