#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Areal', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

font2 = font.SysFont('Areal', 36)

img_hero = "rocket.png"
img_enemy = "ufo.png"
img_back = "galaxy.png"
img_bullet = "bullet.png"

score = 0
lost = 0
max_score = 20



class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (55, 55))
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)   
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y < 0:
            self.kill()  
                     


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 80, 20, 40, 10)

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 20, 40, randint(1,2))
    monsters.add(monster)

FPS = 60
finish = False
run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()


    if not finish:
        window.blit(background, (0, 0))

        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 20, 40, randint(1,2))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_score:
            finish = True
            window.blit(lose, (200, 200)) 

        if score >= max_score: 
            finish = True
            window.blit(win, (200, 200))        

    display.update()
    clock.tick(FPS)
    