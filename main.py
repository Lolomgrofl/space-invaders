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


class Ship:

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))


# ---- MAIN LOOP

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    ship = Ship(335, 650)

    main_font = pygame.font.SysFont("comicsans", size=50)

    clock = pygame.time.Clock()

    def refresh_redraw_window():
        WIN.blit(BG, (0, 0))
        # ---- drawing stuff
        lives_label = main_font.render(f'Lives: {lives}', True, (255, 255, 255))
        level_label = main_font.render(f'Level: {level}', True, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - lives_label.get_width() - 10, 10))
        ship.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        refresh_redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()  # dict of pressed keys
        if keys[pygame.K_a]:  # moving left
            ship.x -= 1


main()
