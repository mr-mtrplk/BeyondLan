import pygame 
# todo: install package

pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - screen.get_height() / 15)
speed = 6

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    pygame.draw.circle(screen, "red", player_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player_pos.x > 0:
            player_pos.x -=  speed

    if keys[pygame.K_d]:
        if player_pos.x < screen.get_width():
            player_pos.x +=  speed

    pygame.display.flip()
    clock.tick(60)

pygame.quit()