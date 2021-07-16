import os
import pygame
import random
import time

pygame.font.init()

# ---- PYGAME WINDOW SETUP
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders 1.0")

# ---- LOADING IMAGES ----
# ---- ENEMY SHIPS
RED_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
BLUE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")
GREEN_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")

# ---- PLAYER SHIP
PLAYER_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

# ---- LASERS
RED_LASER = pygame.image.load("assets/pixel_laser_red.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

# ---- BACKGROUND
BG = pygame.transform.scale(pygame.image.load("assets/background-black.png"), (WIDTH, HEIGHT))


# ---- LASERS
class Laser:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, speed):
        self.y += speed

    def off_screen(self, height):
        return not(height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):  # ---- we are checking collision between 2 objects(their masks)
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None  # is obj1 overlapping obj2 with the given
    # offsets ( offset: distance between top-left angle of object masks)


# ---- SHIPS

class Ship:
    COOLDOWN_FIRE = 30  # 0.5 sec

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def cooldown(self):  # shooting cd
        if self.cool_down_counter >= self.COOLDOWN_FIRE:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, speed, obj):  # ---- checking if enemy laser hits the player
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):  # ---- if hit, reduce hp
                obj.health -= 10
                self.lasers.remove(laser)


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, speed, objs):  # ---- checking if our laser hits enemy
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

class EnemyShip(Ship):
    COLOR_MAP = {
        'red': (RED_SPACE_SHIP, RED_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed


# ---- MAIN LOOP

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    lost = False
    lost_counter = 0
    player = Player(335, 650)
    player_speed = 5
    main_font = pygame.font.SysFont("comicsans", size=50)

    # ---- Enemies params
    enemies = []
    wave_length = 5
    enemy_speed = 1
    laser_speed = 3

    clock = pygame.time.Clock()

    def refresh_redraw_window():  # ---- rendering stuff on screen
        WIN.blit(BG, (0, 0))

        # ---- drawing
        lives_label = main_font.render(f'Lives: {lives}', True, (255, 255, 255))
        level_label = main_font.render(f'Level: {level}', True, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - lives_label.get_width() - 10, 10))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = main_font.render(f'You Lost on LVL {level}! Nice try!', True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        refresh_redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_counter += 1

        if lost:
            if lost_counter > FPS * 3:  # msg time on screen control, we wait 3 sec and then close game
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3
            for i in range(wave_length):  # ---- spawning enemies
                enemy = EnemyShip(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                  random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        # ---- SHIP MOVEMENT
        keys = pygame.key.get_pressed()  # dict of pressed keys
        if keys[pygame.K_a] and player.x - player_speed > 0:  # moving left
            player.x -= player_speed
        if keys[pygame.K_d] and player.x + player_speed + player.get_width() < WIDTH:  # moving right
            player.x += player_speed
        if keys[pygame.K_w] and player.y - player_speed > 0:  # moving up
            player.y -= player_speed
        if keys[pygame.K_s] and player.y + player_speed + player.get_height() < HEIGHT:  # moving down
            player.y += player_speed
        if keys[pygame.K_SPACE]:
            player.shoot()
        for enemy in enemies[:]:  # ---- enemy movements ( copy of enemies list)
            enemy.move(enemy_speed)
            enemy.move_lasers(laser_speed, player)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(laser_speed, enemies)


main()
