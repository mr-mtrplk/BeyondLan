import pygame, random, time
from datetime import datetime, timedelta

save = {'FinishedStory': False}
running = True

# init
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Calculator:
    def __init__(self):
        self.GameEnd = False
        self.player_pos = [540, 360]  # Initial position of the player (center of the screen)
        self.player_speed = 5
        self.pizzas = []
        self.spawn_pizza()

    def spawn_pizza(self):
        # Spawn a pizza at a random position
        pizza_pos = [random.randint(0, 1080), random.randint(0, 720)]
        self.pizzas.append(pizza_pos)

    def main_loop(self):
        screen.fill(BLACK)
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed
        if keys[pygame.K_UP]:
            self.player_pos[1] -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_pos[1] += self.player_speed

        # Draw player
        pygame.draw.circle(screen, WHITE, self.player_pos, 20)

        # Draw pizzas
        for pizza_pos in self.pizzas:
            pygame.draw.circle(screen, (255, 0, 0), pizza_pos, 10)

        pygame.display.flip()

CGame = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not CGame:
        CGame = Calculator()
    else:
        if CGame.GameEnd:
            game = False
            CGame = None
            continue
        CGame.main_loop() 
    
    clock.tick(100)

pygame.quit()
