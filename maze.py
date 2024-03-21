from pygame import *
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 70))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect))

class Player(GameSprite):

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys_pressed[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

class Enemy(GameSprite):

    def update(self):
        if self.rect.x >= 620:
            self.direction = 'left' 
        
        if self.rect.x <= 400:
            self.direction = 'right'

        if self.direction == 'right':
            self.rect.x += self.speed

        if self.direction == 'left':
            self.rect.x -= self.speed

    def diagonal(self):
        if self.rect.x >= 400 and self.rect.y >= 300:
            self.direction = 'left_up' 
        
        if self.rect.x <= 150 and self.rect.y <= 400:
            self.direction = 'right_down'

        if self.direction == 'right_down':
            self.rect.x += self.speed
            self.rect.y += self.speed

        if self.direction == 'left_up':
            self.rect.x -= self.speed
            self.rect.y -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, r, g, b, w, h, x, y):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


window = display.set_mode((700, 500))
display.set_caption("Maze")
background = transform.scale(image.load("фон.jpg"), (700,500))
hero = Player("hero.png", 5, 420, 9)
cyborg = Enemy("cyborg.png", 400, 420, 5)
cyborg_2 = Enemy("cyborg.png", 400, 300, 5)
gold = GameSprite("treasure.png", 500, 420, 4)
wall_1 = Wall(0, 255, 0, 50, 350, 100, 150)
wall_2 = Wall(0, 255, 0, 200, 50, 200, 0)
wall_3 = Wall(0, 255, 0, 50, 200, 300, 300)
wall_4 = Wall(0, 255, 0, 200, 50, 500, 350)
wall_5 = Wall(0, 255, 0, 200, 50, 350, 200)

game = True
finish = False

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.SysFont('Arial', 70)
win = font.render('You win', True, (119, 119, 0))
lose = font.render('You lose', True, (255, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        hero.reset() 
        cyborg.reset()
        gold.reset()
        cyborg_2.reset()
        hero.update() 
        cyborg.update()
        cyborg_2.diagonal()
        if sprite.collide_rect(hero, gold):
            window.blit(win, (200, 200))
            finish = True
            money.play()


        if sprite.collide_rect(hero, cyborg) or sprite.collide_rect(hero, cyborg_2) or  sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2) or sprite.collide_rect(hero, wall_3) or sprite.collide_rect(hero, wall_4) or sprite.collide_rect(hero, wall_5):
            window.blit(lose, (200, 200))
            finish = True
            kick.play()
    display.update()
    time.delay(10)