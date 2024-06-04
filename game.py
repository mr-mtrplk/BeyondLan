import pygame, random, time
from datetime import datetime, timedelta
# TODO: install package

game = "story"
running = True
debug = False
# TODO: game saves
save = {
    'FinishedStory': False
}

# init
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Pizza Delivery')
clock = pygame.time.Clock()

# TODO: enemy shooting
class roadrage:
    def __init__(self):
        self.GameEnd = False
        self.GameTime = datetime.now() + timedelta(minutes=1)
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

        current_time = datetime.now()
        if current_time > self.GameTime:
            print('end game')
            self.GameEnd = True

        pygame.display.flip()

class Story:
    def __init__(self):
        self.GameEnd = False
        self.char_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 42)

        self.text_color = (0, 0, 0)
        self.space_delay = 0 
        self.afterspace_delay = 25

        self.bg = pygame.transform.scale(pygame.image.load('img/background.jpg'), (screen.get_width(), screen.get_height()))
        self.char = pygame.transform.scale(pygame.image.load('img/pizzabox.png'), (screen.get_height() // 3, screen.get_height() // 3))

        self.bg_rect = self.bg.get_rect()

        self.story_lines = [
            "Boss | Hey, newbie, got a new order for you.",
            "Newbie | Sure thing, boss! What's the order?",
            "Boss | It's a delivery to Mr. Smith. Here are the details.",
            "Newbie | Got it. Anything specific I need to know?",
            "Boss | Just make sure it gets there on time. He's a regular.",
            "Newbie | Will do, boss. I'll head out now.",
            "Boss | Great. Keep up the good work!",
        ]
        self.current_line = 0

    def main_loop(self):
        # display
        screen.fill("black")
        screen.blit(self.bg, (0, 0))
        screen.blit(self.char, (screen.get_width() // 10, screen.get_height() // 2))

        if self.current_line < len(self.story_lines):
            name, line = self.story_lines[self.current_line].split('|')
            
            char_name = self.char_font.render(name, True, self.text_color)
            screen.blit(char_name, (50, screen.get_height() - 130))

            char_line = self.text_font.render(line, True, self.text_color)
            screen.blit(char_line, (50, screen.get_height() - 100))

        # key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if 0 >= self.space_delay: 
                self.space_delay = self.afterspace_delay
                self.current_line += 1
                if self.current_line >= len(self.story_lines):
                    save['FinishedStory'] = True
                    self.GameEnd = True
        
        # tick
        if self.space_delay > 0:
            self.space_delay -= 1
        pygame.display.flip()


class Calculator:
    def __init__(self):
        self.GameEnd = False
        self.font = pygame.font.Font(None, 36)
        self.customer_money = random.randint(1, 100)
        self.items_cost = random.randint(1, 100)
        self.change_due = self.customer_money - self.items_cost
        self.user_input = ""
        self.message = "Calculate the change:"

    def main_loop(self):
        # Clear screen
        screen.fill("black")

        # Display the customer money and items cost
        customer_text = self.font.render(f"Customer Money: ${self.customer_money}", True, pygame.Color("white"))
        items_cost_text = self.font.render(f"Items Cost: ${self.items_cost}", True, pygame.Color("white"))
        message_text = self.font.render(self.message, True, pygame.Color("white"))
        user_input_text = self.font.render(f"Your Change: ${self.user_input}", True, pygame.Color("white"))

        # Render texts on screen
        screen.blit(customer_text, (50, 50))
        screen.blit(items_cost_text, (50, 100))
        screen.blit(message_text, (50, 150))
        screen.blit(user_input_text, (50, 200))

        # Update display
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GameEnd = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_change()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.unicode.isdigit():
                    self.user_input += event.unicode

    def check_change(self):
        try:
            user_change = int(self.user_input)
            if user_change == self.change_due:
                self.message = "Correct! Well done."
                self.GameEnd = True
            else:
                if random.choice([True, False]):  # Random chance customer forgets
                    self.message = "Incorrect, but the customer didn't notice."
                else:
                    self.message = "Incorrect! The customer noticed."
                self.GameEnd = True
        except ValueError:
            self.message = "Please enter a valid number."

        self.user_input = ""

RRGame, SGame, CGame = False, False, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game == False: 
        if not save['FinishedStory']:
            game = "story" 
        else:
            game = "roadrage"

    if game == "story":
        if not SGame:
            SGame = Story()
        else: 
            if SGame.GameEnd:
                game = False
                SGame = None

                continue
        SGame.main_loop()

    if game == "roadrage":
        if not RRGame:
            RRGame = roadrage()
        else:
            if RRGame.GameEnd:
                game = 'roadrage'
                RRGame = None

                continue
        RRGame.main_loop() 
        
    #if game == "calculate":
    #    if not CGame:
    #        CGame = Calculator()
    #    else:
    #        if CGame.GameEnd:
    #            game = False
    #            CGame = None
    #
    #            continue
    #    CGame.main_loop() 
    
    clock.tick(100)
pygame.quit()