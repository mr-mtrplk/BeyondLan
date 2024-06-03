import pygame, random, math
from datetime import datetime, timedelta
# todo: install package
game = "roadrage"
running = True
debug = False

# init
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()

# TODO: enemy shooting
class roadrage:
    def __init__(self):
      
        # icon
        self.player = pygame.transform.scale(pygame.image.load("img/player.png"), (100, 100))
        self.enemyMarker = pygame.transform.scale(pygame.image.load("img/enemy.png"), (80, 80))
        self.bg = pygame.image.load("img/bg_city.png")

        # TODO: random map
        
        self.bg_rect = self.bg.get_rect()
        self.enemy_rect = self.enemyMarker.get_rect()
        self.player_rect = self.player.get_rect()

        self.bg_pos, self.labels, self.bullets, self.enemies, self.bgmax_pos = [], [], [], [], []
        self.bg_pos.append(pygame.Vector2(screen.get_width() / 2, 120)) # TODO: better representation of "the bottom of the image"
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        self.Dbgpos = self.bg_pos[0].y
        self.CBG = 0
        self.bgmax_pos.append(self.Dbgpos + self.bg_rect.y)

        # CFG
        self.DFont = pygame.font.SysFont("monospace", 15)
        self.moving_speed = 4
        self.shoot_delay = 0 
        self.aftershoot_delay = 10
        self.bullet_speed = 75
        self.max_enemies = 5
        self.spawn_delay = 200
        self.afterspawn_delay = 120

    def main_loop(self):
        # display
        screen.fill("black")
        for i, d in enumerate(self.bg_pos):
            screen.blit(self.bg, self.bg_rect)
            self.bg_rect.center = d

        screen.blit(self.player, self.player_rect)
        self.player_rect.center = self.player_pos
        
        for i in self.bullets:
            pygame.draw.circle(screen, 'white', i, 2)

        for i in self.enemies:
            screen.blit(self.enemyMarker, self.enemy_rect)
            self.enemy_rect.center = i['pos']

        for i in self.labels:
            current_time = datetime.now()
            if current_time > i['TTL']:
                self.labels.remove(i)

            label = self.DFont.render(i['label'], 1, (255,255,0))
            i['pos'] += i['added']
            screen.blit(label, i['pos'])

        # key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.player_pos.x > 0:
                self.player_pos.x -=  self.moving_speed

        if keys[pygame.K_d]:
            if self.player_pos.x < screen.get_width():
                self.player_pos.x += self.moving_speed

        if keys[pygame.K_SPACE]:
            if 0 >= self.shoot_delay: 
                self.bullets.append(pygame.Vector2(self.player_pos.x, self.player_pos.y - 20))
                self.shoot_delay = self.aftershoot_delay

        # tick
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
        if self.spawn_delay > 0:
            self.spawn_delay -= 1

        for i in self.bullets:
            i.y -= self.bullet_speed

            if -2 > i.y:
                self.bullets.remove(i)

            for j in self.enemies: 
                hitbox = 40
                if debug:
                    pygame.draw.circle(screen, 'white', (j['pos'].x + hitbox, j['pos'].y + hitbox), 1)
                    pygame.draw.circle(screen, 'white', (j['pos'].x + hitbox, j['pos'].y - hitbox), 1)
                    pygame.draw.circle(screen, 'white', (j['pos'].x - hitbox, j['pos'].y + hitbox), 1)
                    pygame.draw.circle(screen, 'white', (j['pos'].x - hitbox, j['pos'].y - hitbox), 1)

                if hitbox > j['pos'].y - i.y > -hitbox and hitbox > j['pos'].x - i.x > -hitbox and i in self.bullets:
                    self.bullets.remove(i)
                    if random.randint(1, 20) == 1: 
                       damage = random.randint(1, 20)
                    else:
                        damage = random.randint(20, 80)
                    j['health'] -= damage
                    self.labels.append({
                        'pos': pygame.Vector2(j['pos'].x, j['pos'].y), 
                        'label': str(damage), 
                        'TTL': datetime.now() + timedelta(seconds=2),
                        'added': pygame.Vector2(random.randint(-3,3), random.randint(-3,3))
                    })

                    if 0 >= j['health']:
                        # TODO: explosion
                        self.enemies.remove(j)

        if 0 >= self.spawn_delay and self.max_enemies > len(self.enemies):
            if 1 == random.randint(1, 100):
                self.enemies.append({
                    'pos': pygame.Vector2(random.randint(20, screen.get_width()-20),
                                          random.randint(20, round(screen.get_height()/3)-20)),
                    'health': 250
                })
                self.spawn_delay = self.afterspawn_delay
                
        if self.CBG > 2:
            self.bg_pos.remove(self.bg_pos[0])
            self.bgmax_pos.remove(self.bgmax_pos[0])
            self.CBG -= 1

        for i in self.bg_pos:
            i.y += 5
    
        if self.bg_pos[self.CBG].y > self.bgmax_pos[self.CBG]:
            if debug:
                print(self.bg_pos[self.CBG].y, self.bgmax_pos[self.CBG])
                print(self.Dbgpos, self.bg_rect.y, self.Dbgpos - self.bg_rect.y)
                print("added map snippet")
            self.bg_pos.append(pygame.Vector2(screen.get_width() / 2, self.bg_rect.y))
            self.bgmax_pos.append(self.bgmax_pos[self.CBG] - self.bg_rect.y)
            self.CBG += 1

        pygame.display.flip()
        clock.tick(100)

class story():
    def __init__(self):
        print("story")

    def main_loop(self):
        # TODO: STORY
        print('work in progresses')

RRGame, SGame = False, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game == False: 
        game = "story" 

    if game == "story":
        if not SGame:
            SGame = roadrage()
        SGame.main_loop()

    if game == "roadrage":
        if not RRGame:
            RRGame = roadrage()
        RRGame.main_loop()

pygame.quit()