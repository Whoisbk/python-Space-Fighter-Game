import pygame
import pygame.freetype
import os
pygame.font.init()
pygame.init()


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("space_fighter")
FPS = 60

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
BULLET_SPEED = 8
MAX_BULLETS = 5
counter = 60

#COLORS
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#FONTS
font = pygame.font.SysFont("comicsans",50)
winner_font = pygame.font.SysFont("comicsans",80)

#Background Image
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(SCREEN_WIDTH,SCREEN_HEIGHT))
#SPACESHIPS
class ships():
    def __init__(self,x,y,name,rotate,hp,max_hp):
        self.y = y
        self.x = x 
        self.hp = max_hp
        self.max_hp = max_hp
        self.height = 40
        self.width = 55
        self.alive = True
        self.name = name
        self.speed = 5
        self.rotate = rotate
        self.flip = False
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("Assets",f"spaceship_{self.name}.png")),(self.width,self.height))
        self.image = pygame.transform.rotate(self.img,self.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def draw(self):
        WIN.blit(self.image,self.rect)
    
    def attack(self,target):
        demage = 3
        target.hp -= demage

        if target.hp < -3:
            target.alive = False

def draw_win(yellow_bullets,red_bullets,timer):
    WIN.blit(BG,(0,0))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    WIN.blit(timer,(SCREEN_WIDTH//2 , 10))

class health_bar():
    def __init__(self,x,y,hp,max_hp):
        self.y = y
        self.x = x 
        self.hp = max_hp
        self.max_hp = max_hp
        self.height = 40
        self.width = 100
    
    def draw(self,hp):
        #red healthbar
        #update with new health 
        self.hp = hp
        #calculate health ratio
        ratio = self.hp /self.max_hp#when you have full health the ratio will be 1 and if its half its 0.5
        pygame.draw.rect(WIN,WHITE,(self.x,self.y,150,20),4)
        pygame.draw.rect(WIN,GREEN,(self.x,self.y,150*ratio,20))

#INSTANCES
yellow_ship = ships(100,250,"yellow",90,20,20)
red_ship = ships(800,250,"red",270,20,20)
red_ship.flip = True

health_bar_P1 = health_bar(10,10,yellow_ship.hp,yellow_ship.max_hp)
health_bar_P2 = health_bar(SCREEN_WIDTH-180,10,red_ship.hp,red_ship.max_hp)

yellow_bullets = []
red_bullets = []
winner = ""
start_time = 60000
clock = pygame.time.Clock()
run = True
while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(yellow_ship.rect.centerx,yellow_ship.rect.centery,20,5)
                yellow_bullets.append(bullet)
            
            if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red_ship.rect.centerx,red_ship.rect.centery,20,5)
                red_bullets.append(bullet)
    
    #KEY_INPUT YELLOW
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w] and yellow_ship.rect.top > 0:
        yellow_ship.rect.y -= yellow_ship.speed
    if key_pressed[pygame.K_s] and yellow_ship.rect.bottom < SCREEN_HEIGHT:
        yellow_ship.rect.y += yellow_ship.speed
    if key_pressed[pygame.K_a] and yellow_ship.rect.left > 0:
        yellow_ship.rect.x -= yellow_ship.speed
    if key_pressed[pygame.K_d] and yellow_ship.rect.right < SCREEN_WIDTH//2:
        yellow_ship.rect.x += yellow_ship.speed
    #KEY_INPUT RED
    if key_pressed[pygame.K_UP] and red_ship.rect.top > 0:
        red_ship.rect.y -= red_ship.speed
    if key_pressed[pygame.K_DOWN] and red_ship.rect.bottom < SCREEN_HEIGHT:
        red_ship.rect.y += red_ship.speed
    if key_pressed[pygame.K_LEFT] and red_ship.rect.left > SCREEN_WIDTH//2:
        red_ship.rect.x -= red_ship.speed
    if key_pressed[pygame.K_RIGHT] and red_ship.rect.right < SCREEN_WIDTH:
        red_ship.rect.x += red_ship.speed

    #COLLISION
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red_ship.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_ship.attack(red_ship) 
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow_ship.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_ship.attack(yellow_ship) 
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
    current_time = pygame.time.get_ticks()
    delta_time_sec = (start_time - current_time) // 1000
    
    text = font.render(str(delta_time_sec),1,WHITE)
    if delta_time_sec < 10:
        text = font.render(str(delta_time_sec),1,RED)
    
    if yellow_ship.alive == False or red_ship.alive == False or delta_time_sec == 0:
        if yellow_ship.hp > red_ship.hp:
            winner = winner_font.render("Yellow Wins!",10,YELLOW)
            WIN.blit(winner,(SCREEN_WIDTH//2 - 100 , SCREEN_HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(3000)
        elif red_ship.hp > yellow_ship.hp:
            winner = winner_font.render("Red Wins!",10,RED)
            WIN.blit(winner,(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(3000)
        else:
            winner = winner_font.render("DRAW!",10,WHITE)
            WIN.blit(winner,(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(3000)

        break
            

    #DRAW WINDOW
    draw_win(yellow_bullets,red_bullets,text)
    #DRAW PLAYERS
    health_bar_P1.draw(yellow_ship.hp)
    health_bar_P2.draw(red_ship.hp)
    yellow_ship.draw()
    red_ship.draw()
    


    pygame.display.update()
pygame.quit()    



