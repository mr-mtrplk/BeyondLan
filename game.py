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

class roadrage:
    def __init__(self):
      
        # icon
        self.player = pygame.transform.scale(pygame.image.load("img/player.png"), (100, 100))
        self.enemyMarker = pygame.transform.scale(pygame.image.load("img/enemy.png"), (80, 80))
        self.bg = pygame.image.load("img/bg-road.png")

        self.bg_pos = pygame.Vector2(0, 0)
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - screen.get_height() / 10)

        self.bg_rect = self.bg.get_rect()
        self.enemy_rect = self.enemyMarker.get_rect()
        self.player_rect = self.player.get_rect()

        self.DFont = pygame.font.SysFont("monospace", 15)

        self.labels = []
        self.bullets = []
        self.enemies = []

        # CFG
        self.moving_speed = 4
        self.shoot_delay = 0 
        self.aftershoot_delay = 10
        self.bullet_speed = 75
        self.max_enemies = 5
        self.spawn_delay = 200
        self.afterspawn_delay = 120

    def main_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # discplay
        screen.fill("black")
        screen.blit(self.bg, self.bg_pos)
        self.bg_rect.center = self.bg_pos
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
                        self.enemies.remove(j)

        if 0 >= self.spawn_delay and self.max_enemies > len(self.enemies):
            if 1 == random.randint(1, 100):
                self.enemies.append({
                    'pos': pygame.Vector2(random.randint(20, screen.get_width()-20),
                                          random.randint(20, round(screen.get_height()/3)-20)),
                    'health': 250
                })
                self.spawn_delay = self.afterspawn_delay

        pygame.display.flip()
        clock.tick(100)

class story():
    def __init__(self):
        print("story")

RRGame = False
while running:
    if game == False: 
        game = "story" 

    if game == "roadrage":
        if not RRGame:
            RRGame = roadrage()
        RRGame.main_loop()

pygame.quit()