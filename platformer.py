import pygame
import sys
from pygame.locals import *
import random
import time
import pickle

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

background = pygame.image.load("background.png")
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
hiscore_file = "hiscore.txt"

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("snowman.png")
        self.rect = self.surf.get_rect()
 
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0
        self.dir = 'left'
        self.height_score = 0
        self.game_time = 40.0

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            if self.dir != 'left':
                self.surf = pygame.transform.flip(self.surf, True, False)
            self.dir = 'left'
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            if self.dir != 'right':
                self.surf = pygame.transform.flip(self.surf, True, False)
            self.dir = 'right'
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH + 15:
            self.pos.x = -15
        if self.pos.x < -15:
            self.pos.x = WIDTH + 15
            
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    
class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-20)))
        self.moving = True
        self.speed = random.randint(-1, 1)
        self.point = True

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
    
    def generateCoin(self):
        if (self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
 
        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()
 
        self.rect.topleft = pos
 
    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 10
            P1.height_score += 200
            P1.game_time += 3
            self.kill()

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

def plat_gen():
    while len(platforms) < 6 :
        width = random.randrange(50,100)
        p  = platform()
        C = True
        rep = 0

        while C and rep < 500:
            rep += 1
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                            random.randrange(-20, 0))
            C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)

def load_hiscore():
    f = open(hiscore_file, 'rb')
    hiscore = pickle.load(f)
    f.close()
    return hiscore

def save_hiscore(hiscores):
    f = open(hiscore_file, 'wb')
    pickle.dump(hiscores, f)
    f.close()

def print_scores(scores):
    print("\nHI SCORES:\n==========")
    for ind_s, scor in enumerate(scores):
        ind_s += 1
        print(ind_s, scor[0], str(scor[1]))

# UNCOMMENT TO RESET TO DEFAULT HISCORE TABLE
"""def_hiscores = []
for scr in range(10):
    def_hiscores.append(["DJ", 10])
save_hiscore(def_hiscores)
print (def_hiscores)"""

def record_hiscore(score):
    loaded_score = load_hiscore()
    for si, sc in enumerate(loaded_score):
        if sc[1] < score:
            print("\nNEW HI SCORE: " + str(score) + " POINTS!")
            name = input("Input name please: ")
            new_score = [name, score]
            loaded_score.insert(si, new_score)
            loaded_score = loaded_score[:10]
            print_scores(loaded_score)
            save_hiscore(loaded_score)
            break
    else:
        print("\nYou got: " + str(score) + " points")
        print_scores(loaded_score)

PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((200,50,50))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
coins = pygame.sprite.Group()
platforms = pygame.sprite.Group()

platforms.add(PT1)

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)

hiscore = load_hiscore()

try:
    while True:
        P1.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_SPACE:
                    P1.jump()
            if event.type == pygame.KEYUP:    
                if event.key == pygame.K_SPACE:
                    P1.cancel_jump() 

        if P1.rect.top <= HEIGHT / 3:
            P1.height_score += int(abs(P1.vel.y))
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            for coin in coins:
                coin.rect.y += abs(P1.vel.y)
                if coin.rect.top >= HEIGHT:
                    coin.kill()
        
        plat_gen()
        displaysurface.blit(background, (0, 0))
        f = pygame.font.SysFont("Verdana", 20)
        g  = f.render(str(P1.height_score), True, (255,255,255))
        displaysurface.blit(g, (WIDTH/2.5, 10)) 
        g2 = f.render(str("HI: " + str(hiscore[0][1])), True, (255,255,255))
        displaysurface.blit(g2, (WIDTH - 120, 10)) 
        g3 = f.render(str(int(P1.game_time)), True, (255,255,255))
        displaysurface.blit(g3, (20, 10))

        for coin in coins:
            displaysurface.blit(coin.image, coin.rect)
            coin.update()

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)
        P1.game_time -= 0.0167

        if P1.rect.top > HEIGHT or P1.game_time <= 0:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                f = pygame.font.SysFont("Verdana", 20)
                if P1.game_time <= 0:
                    go_text = "TIME OVER"
                else:
                    go_text = "GAME OVER"
                g  = f.render(go_text, True, (0,0,0))
                displaysurface.blit(g, (WIDTH/2 - 60, HEIGHT/2)) 
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                record_hiscore(P1.height_score)
                sys.exit()
except:
    raise