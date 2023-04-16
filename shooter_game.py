#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!',True,(255,255,255))
lose = font1.render('YOU LOSE!',True,(180,0,0))
font2 = font.SysFont('Arial', 36)

img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'

score = 0 #килы
goal = 100 #килы для победы
lost = 0 #пропуски врагов
max_lost = 3 #пропуски врагов для проигрыша
life = 4 #жизни

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 50:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0 

class Bullet(GameSprite):
   #движение пули
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

ship = Player(img_hero,300,win_height - 50,40,50,10)

monsters = sprite.Group()
for i in range(1,7):
    monster = Enemy(img_enemy, randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_ast, randint(80,win_width-80),-40,80,50,randint(3,5))  
    asteroids.add(asteroid)
    
bullets = sprite.Group()

game = True
finish = False
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
                
    if not finish:
        window.blit(background,(0,0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False):
            sprite.spritecollide(ship,monsters,True)
            life -= 1

        if sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,asteroids,True)
            life -= 1
            asteroid = Asteroid(img_ast, randint(80,win_width-80),-40,80,50,randint(3,5))  
            asteroids.add(asteroid)
            
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        text = font2.render('Счет: '+str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render('Пропущено: '+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)

        text_life = font1.render('ХП:'+str(life),1,life_color)
        window.blit(text_life,(570,10))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,7):
            monster = Enemy(img_enemy, randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Asteroid(img_ast, randint(80,win_width-80),-40,80,50,randint(3,5))  
            asteroids.add(asteroid)

    time.delay(30)
