import pygame, random, math
from datetime import datetime, timedelta
# todo: install package

debug = False
running = True

# prep
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()

# icon
player = pygame.transform.scale(pygame.image.load("img/player.png"), (100, 100))
enemyMarker = pygame.transform.scale(pygame.image.load("img/enemy.png"), (80, 80))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - screen.get_height() / 10)

DFont = pygame.font.SysFont("monospace", 15)

enemy_rect = enemyMarker.get_rect()
player_rect = player.get_rect()

labels = []
bullets = []
enemies = []

moving_speed = 6
shoot_delay = 0 
aftershoot_delay = 1
bullet_speed = 10
max_enemies = 5
spawn_delay = 200
afterspawn_delay = 120

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # discplay
    screen.fill("black")
    screen.blit(player, player_rect)
    player_rect.center = player_pos
    
    for i in bullets:
        pygame.draw.circle(screen, 'white', i, 2)

    for i in enemies:
        screen.blit(enemyMarker, enemy_rect)
        enemy_rect.center = i['pos']
    
    for i in labels:
        current_time = datetime.now()
        if current_time > i['TTL']:
            labels.remove(i)
        label = DFont.render(i['label'], 1, (255,255,0))
        i['pos'] += i['added']
        screen.blit(label, i['pos'])

    # key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player_pos.x > 0:
            player_pos.x -=  moving_speed

    if keys[pygame.K_d]:
        if player_pos.x < screen.get_width():
            player_pos.x += moving_speed
    
    if keys[pygame.K_SPACE]:
        if 0 >= shoot_delay: 
            bullets.append(pygame.Vector2(player_pos.x, player_pos.y - 20))
            shoot_delay = aftershoot_delay

    # tick
    if shoot_delay > 0:
        shoot_delay -= 1
    if spawn_delay > 0:
        spawn_delay -= 1

    for i in bullets:
        i.y -= bullet_speed
        
        if -2 > i.y:
            bullets.remove(i)

        for j in enemies: 
            hitbox = 40
            if debug:
                pygame.draw.circle(screen, 'white', (j.x + hitbox, j.y + hitbox), 1)
                pygame.draw.circle(screen, 'white', (j.x + hitbox, j.y - hitbox), 1)
                pygame.draw.circle(screen, 'white', (j.x - hitbox, j.y + hitbox), 1)
                pygame.draw.circle(screen, 'white', (j.x - hitbox, j.y - hitbox), 1)
            
            if hitbox > j['pos'].y - i.y > -hitbox and hitbox > j['pos'].x - i.x > -hitbox and i in bullets:
                bullets.remove(i)
                if random.randint(1, 20) == 1: 
                   damage = random.randint(1, 20)
                else:
                    damage = random.randint(20, 80)
                j['health'] -= damage
                labels.append({
                    'pos': pygame.Vector2(j['pos'].x, j['pos'].y), 
                    'label': str(damage), 
                    'TTL': datetime.now() + timedelta(seconds=2),
                    'added': pygame.Vector2(random.randint(-3,3), random.randint(-3,3))
                })
                
                if 0 >= j['health']:
                    enemies.remove(j)
                    
    
    if 0 >= spawn_delay and max_enemies > len(enemies):
        if 1 == random.randint(1, 100):
            enemies.append({
                'pos': pygame.Vector2(random.randint(20, screen.get_width()-20),
                                      random.randint(20, round(screen.get_height()/3)-20)),
                'health': 250
            })
            spawn_delay = afterspawn_delay

    pygame.display.flip()
    clock.tick(60)

pygame.quit()