import pygame, random, math
# todo: install package

pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()
running = True

player = pygame.transform.scale(pygame.image.load("img/player.png"), (40, 40))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - screen.get_height() / 15)
moving_speed = 6

bullets = []
shoot_delay = 0 #ticks
aftershoot_delay = 15
bullet_speed = 10
              
enemyMarker = pygame.transform.scale(pygame.image.load("img/enemy.png"), (40,40))
enemies = []
max_enemies = 1
spawn_delay = 200
afterspawn_delay = 120

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # discplay
    screen.fill("black")
    screen.blit(player, player_pos)
    
    for i in bullets:
        pygame.draw.circle(screen, 'white', i, 2)

    for i in enemies:
        screen.blit(enemyMarker, i)

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
            bullets.append(pygame.Vector2(player_pos.x, player_pos.y))
            shoot_delay = aftershoot_delay

    # tick
    if shoot_delay > 0:
        shoot_delay -= 1
    if spawn_delay > 0:
        spawn_delay -= 1

    for i in bullets:
        i.y -= bullet_speed
        
        if 0 > i.y:
            bullets.remove(i)

        #for j in enemies: 
        #    hitbox_x = 100
        #    hitbox_y = 100
        #    pygame.draw.circle(screen, 'white', (j.x + hitbox_x, j.y + hitbox_y), 1)
        #    pygame.draw.circle(screen, 'white', (j.x + hitbox_x, j.y - hitbox_y), 1)
        #    pygame.draw.circle(screen, 'white', (j.x - hitbox_x, j.y + hitbox_y), 1)
        #    pygame.draw.circle(screen, 'white', (j.x - hitbox_x, j.y - hitbox_y), 1)
        #    
        #    print(j.y - i.y, j.x - i.x)
        #    if hitbox_y > j.y - i.y > -hitbox_y and hitbox_x > j.x - i.x > -hitbox_x:
        #       
        #       enemies.remove(j)
    
    if 0 >= spawn_delay and max_enemies > len(enemies):
        if 1 == random.randint(1, 1):
            enemies.append(pygame.Vector2(random.randint(0, screen.get_width()),random.randint(0, round(screen.get_height()/3))))
            spawn_delay = afterspawn_delay

    pygame.display.flip()
    clock.tick(60)

pygame.quit()