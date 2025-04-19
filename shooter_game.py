from pygame import *
from random import randint

# инициализация Pygame
init()

# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
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
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(0, 635)
            self.rect.y = 0
            lost += 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y > win_height:
            self.rect.x = randint(0, 635)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed  
        if self.rect.y < 0:
            self.kill()


# сцена
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

score = 0
lost = 0
max_score = 100
max_lost = 30
life = 3

player = Player('rocket.png', 300, 430, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 635), randint(-100, -40), randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1):
    asteroid = Asteroid('asteroid.png', randint(0, 635), randint(-100,-40), randint(1 ,3))
    asteroids.add(asteroid)

finish = False
clock = time.Clock()
FPS = 60

run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        window.blit(background, (0, 0))

        font2 = font.Font('None', 48)
        
        # Отображение счета и жизней на экране
        text_score = font2.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        # Изменено: теперь жизней отображается в правом верхнем углу
        text_life = font2.render('Жизни: ' + str(life), True,(255 ,255 ,255))
        window.blit(text_life,(win_width -200 ,20)) 

        text_lose = font2.render('Пропущено: ' + str(lost), True,(255 ,255 ,255))
        window.blit(text_lose,(10 ,50))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        player.reset()
        
        monsters.draw(window)
        bullets.draw(window) 
        asteroids.draw(window)

        collided_monsters = sprite.groupcollide(monsters, bullets, True, True)
        collided_asteroids=sprite.spritecollide(player, asteroids, True)

        for asteroid in collided_asteroids:
            life -= 1 
            new_asteroid=Asteroid('asteroid.png',randint(0 ,win_width -65),randint(-100,-40),randint(1 ,3))
            asteroids.add(new_asteroid)

            if life <= 0 :
                finish = True 
                lose_text = font2.render('Туда его',True,(255 ,0 ,0))
                window.blit(lose_text,(300 ,200))

        for monster in collided_monsters:
            score += 1 
            monster_new = Enemy('ufo.png',randint(0 ,win_width -65),randint(-100 ,-40),randint(1 ,5))
            monsters.add(monster_new)

        if lost >= max_lost:
            finish = True 
            lose = font2.render('Туда его',True,(255 ,0 ,0))
            window.blit(lose,(300 ,200))

        if score >= max_score:
            finish = True 
            win = font2.render('Ура, победа',True,(0 ,255 ,0))
            window.blit(win,(300 ,200))

    display.update()
    clock.tick(FPS)