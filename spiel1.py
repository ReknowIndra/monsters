# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:29:40 2024

@author: ReichelErwinWIVAP&G
"""

import pygame
import sys
import numpy as np
import random
import time

# Initialisierung von Pygame
pygame.init()

# Fenster erstellen
width, height = 1600, 1000
#width, height = 1600,1200

#screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
width,height = screen.get_size()
pygame.display.set_caption("Mein erstes Spiel")

# Spielvariablen

size = int(width/30)

player_x, player_y = width-2*size, size
player_speed =0.5

player2_x, player2_y = size, size
player2_speed =0.5

Nmonster = 3
monster_speed = 0.25

level = 0
cloneprob = 2000
maxMon = 32

score1 = 0
score2 = 0

horn_sound = pygame.mixer.Sound("horn.mp3")
car_sound = pygame.mixer.Sound("car.mp3")
shout_sound = pygame.mixer.Sound("shout.mp3")
plop_sound = pygame.mixer.Sound("plop.mp3")

im_won_mons = pygame.transform.scale(pygame.image.load("monsters.png"),(width/2,height/2))
im_won_human = pygame.transform.scale(pygame.image.load("humans.png"),(width/2,height/2))

im_mons = pygame.transform.scale(pygame.image.load("monster1.png"),(size,size))
im_monsi = pygame.transform.scale(pygame.image.load("monster1i.png"),(size,size))
im_monsd = []
deadC = 6
for d in range(deadC):
    im_monsd.append(pygame.transform.scale(pygame.image.load("monster1d{}.png".format(d)),(size,size)))

im_ghost = pygame.transform.scale(pygame.image.load("ghost.png"),(size,size))
im_p1 = pygame.transform.scale(pygame.image.load("player1.png"),(size,size))
im_p2 = pygame.transform.scale(pygame.image.load("player2.png"),(size,size))

#im_bk = pygame.transform.scale(pygame.image.load("bkhouse.png"),(width,height))
im_bk = pygame.transform.scale(pygame.image.load("quadrill.png"),(width,height))


im_car = pygame.image.load("car.png")
im_cari = pygame.image.load("cari.png")

sc = 5

level = 0

maxSpeed = 1.5

class monster:
    def __init__(self,x,y,speed=monster_speed,size=size,color=(0,255,0)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.speedx = self.speed*random.randrange(-1,2)
        self.speedy = self.speed*random.randrange(-1,2)
        self.jig = 2*self.size
        self.jcount = self.jig
        self.life = 1
        self.inv = 0
        self.reps = monster_speed*random.gauss(0.5,2)
        self.dead = deadC-1
        
    def draw(self,screen):
        #if self.inv == 0:
        #    self.color=(55+(self.life-1)*50,255,0)
        #else:
        #    self.color=(255,255,255)
        #    self.inv -= 1
        if self.dead < deadC-1:
            screen.blit(im_monsd[int(self.dead)], (self.x, self.y))
            return
        
        if self.inv > 0:
            self.inv -= 1
        
        if self.life > 1:
            #pygame.draw.rect(screen, self.color, (self.x-2, self.y-2, self.size+4, self.size+4))  # Monster
            if self.inv == 0:
                screen.blit(im_car, (self.x, self.y))
            else:
                screen.blit(im_cari, (self.x, self.y))
        else:
            if self.inv == 0:
                screen.blit(im_mons, (self.x, self.y))
            else:
                screen.blit(im_monsi, (self.x, self.y))


    def move(self):
        if self.dead < deadC-1:
            return
        
        self.x += self.speedx*sc
        self.y += self.speedy*sc

        if self.x < -size:
            self.x = width
        elif self.x > width:
            self.x = -size

        if self.y < -size:
            self.y = height
        elif self.y > height:
            self.y = -size

        self.jcount -= 1
        if self.jcount <= 0: 
            self.speedx = self.speed*random.randint(-1,1)
            self.speedy = self.speed*random.randint(-1,1)
            self.jcount = self.jig

    def repel(self,x,y):
        dx = self.x-x
        dy = self.y-y
        d = np.sqrt(dx**2+dy**2)
        if d<size:
            d = size
        if d < 5*size:
            self.speedx += self.reps*dx/d**2
            self.speedy += self.reps*dy/d**2
            self.speed = np.sqrt(self.speedx**2+self.speedy**2)
            if self.speed > maxSpeed:
                lim = maxSpeed/self.speed
                self.speed = maxSpeed
                self.speedx = self.speedx*lim
                self.speedy = self.speedx*lim
                
            #self.jcount = self.jig

    def touch(self,x,y):
        dx = self.x-x
        dy = self.y-y

        if (abs(dx) < size) and (abs(dy) < size):
            if self.inv > 0:
                self.inv -= 1
                if self.life > 1:
                    horn_sound.play()

            else:
                self.life -= 1
                self.inv = 150
                self.speedx = 0
                self.speedy = 0

            if self.life == 0:
                if self.dead > 0:
                    self.dead -= 0.25
                    shout_sound.play()
                else:
                    return True
        return False
    
class ghost (monster):
    def __init__(self):
        x = width/2
        y = height*0.7
        monster.__init__(self,x,y,level*0.02)
        self.reps = 0.5-0.2*level
        
    def draw(self,screen):        
        screen.blit(im_ghost, (self.x, self.y))
    
    def move(self):
        monster.move(self)
        if self.speed > 0:
            self.speed -= 0.001

    def touch(self,x,y):
        dx = self.x-x
        dy = self.y-y

        if (abs(dx) < size) and (abs(dy) < size):
                    return True
        return False
    
#%%
 
def sunrise(screen,stage=0):
    w,h = screen.get_size()

    screen.fill((stage*4,stage*4,stage*4,255))

    px = int(w/2)
    Nc = 50
    py = h*2.5-stage*h/20
    pyinc = h/(2*Nc)
    ri = w
    cinc = stage*8/Nc
    r = stage*4
    g = stage*4
    b = stage*4
    rdec = w/(1.8*Nc)

    for n in range(Nc):
        pygame.draw.circle(screen,(r,g,b),(px,py),ri)
        py -= pyinc
        ri -= rdec

        r += cinc
        g += cinc/2
        b += cinc/3

#bk = pygame.Surface((width, height))
#sunrise(bk,20)
#bk.set_alpha(128)
#pygame.draw.circle(bk,(0,0,255,255),(width/2,height/2),100)

#screen.blit(im_bk,(0,0))
#screen.blit(bk,(0,0))
#pygame.display.flip()    
#%%
monsters = []
for n in range(Nmonster):
    x = random.randint(0, width-size)
    y = random.randint(0, height-size)
    monsters.append(monster(x,y))
        
plop_sound.play()
    
level = 1
ghosts = [ghost()]

#sunrise(bk,level)
bk = pygame.Surface((width, height), pygame.SRCALPHA)

sunrise(bk,level)
#bk.set_alpha(128)
plop_sound.play()

bk.blit(im_bk,(0,0))
screen.blit(bk,(0,0))

pygame.mixer.music.load('Come, now is the time.wav')
pygame.mixer.music.play(-1)

# Spielhauptschleife
while True:
    tic = time.process_time_ns()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed *sc
    player_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed *sc

    player2_x += (keys[pygame.K_d] - keys[pygame.K_a]) * player2_speed *sc
    player2_y += (keys[pygame.K_s] - keys[pygame.K_w]) * player2_speed *sc

    # Spiellogik hier hinzufügen
    if player_x<0:
        player_x=0
    if player_y<0:
        player_y=0
    if player_x>width-size:
        player_x=width-size
    if player_y>height-size:
        player_y=height-size

    if player2_x<0:
        player2_x=0
    if player2_y<0:
        player2_y=0
    if player2_x>width-size:
        player2_x=width-size
    if player2_y>height-size:
        player2_y=height-size

 
    # Zeichne den Spieler
    #screen.fill((0, 0, 0))  # Hintergrundfarbe
    #screen.blit(im_bk,(0,0))
    screen.blit(bk,(0,0))
    
    for g in ghosts:
        g.repel(player_x,player_y)
        g.repel(player2_x,player2_y)
        g.move()
        g.draw(screen)
        if g.touch(player_x,player_y) and player_speed > 0.5:
            player_speed -= 0.001
        if g.touch(player2_x,player2_y) and player2_speed > 0.5:
            player2_speed -= 0.001
        
    for m in monsters:
        m.repel(player_x,player_y)
        m.repel(player2_x,player2_y)
        for m2 in monsters:
            m.repel(m2.x,m2.y)

        m.move()
        m.draw(screen)

        # CATCH monsters
        if m.touch(player_x,player_y):
            monsters.remove(m)
            score1 += level*10
            player_speed += 0.1*1/(2+level)
            print("p1: {}, p2: {}, {} monsters left".format(score1,score2,len(monsters)))
            continue
        
        if m.touch(player2_x,player2_y):
            monsters.remove(m)
            score2 += level*10
            player2_speed += 0.1*1/(2+level)
            print("p1: {}, p2: {}, {} monsters lefts".format(score1,score2,len(monsters)))
            continue
        
        # CLONE
        if random.randrange(0,cloneprob+len(monsters*300)) == 0 and len(monsters) < 50 and m.inv == 0:
            nmons = monster(m.x,m.y)
            nmons.speed = monster_speed
            nmons.jig = m.jig+m.size*random.gauss(0,0.5)
            nmons.reps = m.reps+random.gauss(0,0.1)

            monsters.append(nmons)
            plop_sound.play()

            if level > 12:
                car_sound.play()
                if level < 17:
                    monsters[-1].life = level-11
                else:
                    monsters[-1].life = 5

            print("now {} monsters!".format(len(monsters)))
        
    if not monsters:
        print("Level {} done!".format(level))
        level += 1
        
        sunrise(bk,level)
        #bk.set_alpha(128)
        plop_sound.play()
    
        bk.blit(im_bk,(0,0))
        screen.blit(bk,(0,0))
        
        #Nmonster *= 2
        cloneprob = cloneprob-100
        if cloneprob < 400:
            cloneprob = 400
        for n in range(Nmonster):
            x = random.randint(0, width-size)
            y = random.randint(0, height-size)
            #monster_speed = monster_speed+0.2
            monsters.append(monster(x,y,monster_speed))
            if level > 17:
                monsters[-1].life = level-17
            
        if level > 17:
            ghosts.append(ghost())
        
    if len(monsters) > maxMon:
        screen.blit(im_won_mons, (width/4, height/4))
        print("Monsters won!")
        break

    if level > 20:
        screen.blit(im_won_human, (width/4, height/4))
        print("Players won!")
        break

        
    pygame.draw.rect(screen, (255, 0, 0), (width-5, max(0,height*(1-player_speed)), width, height))  # Roter Spieler
    pygame.draw.rect(screen, (0, 0, 255), (0, max(0,height*(1-player2_speed)), 5, height))  # Roter Spieler
    pygame.draw.rect(screen, (0, 220, 50), (0, height-5, width/maxMon*len(monsters), 5))  # Monsterbalken
    pygame.draw.rect(screen, (255, 255, 0), (0, 0, width/20*level, 5))  # Monsterbalken

    #pygame.draw.rect(screen, (0, 0, 255), (player2_x, player2_y, size, size))  # Blauer Spieler
    screen.blit(im_p1, (player_x, player_y))
    screen.blit(im_p2, (player2_x, player2_y))

    pygame.display.flip()
    
    toc = time.process_time_ns()
    tw = 0.01-(toc-tic)/1e9
    if tw > 0:
        time.sleep(tw)

pygame.display.flip()

time.sleep(5)
pygame.quit()


