import pygame
import random
from settings import *

Vector = pygame.math.Vector2

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.spritesheet.get_image(218, 146, 28, 29)
        self.rect = self.image.get_rect()
        random_scale = random.randint(1,3)
        self.image = pygame.transform.scale(self.image, (self.rect.width * random_scale, self.rect.height * random_scale))
        self.rect = self.image.get_rect()
        self.pos = Vector(-100, -100)
        self.vel = Vector(0, 0)
        self.rect.center = self.pos
        self.entered_screen = False
        self.destroyed = False
        self.spawn()

    def update(self):
        if self.destroyed == True:
            self.destroy()
        self.pos += self.vel
        self.rect.center = self.pos

        if self.pos.x > 0 and self.pos.x < WIDTH:
            if self.pos.y > 0 and self.pos.y < HEIGHT:
                self.entered_screen = True

        # wrap after asteroid has entered screen
        if self.entered_screen:
            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = WIDTH
            if self.pos.y < 0:
                self.pos.y = HEIGHT
            if self.pos.y > HEIGHT:
                self.pos.y = 0

    def spawn(self):
        # random number between 1-4 for spawn location
        location = random.randint(1, 4)

        # top side of screen
        if location == 1:
            self.pos.x = random.randint(0, WIDTH)
            self.pos.y = 0 - self.rect.height
        # right side
        elif location == 2:
            self.pos.x = WIDTH + self.rect.width
            self.pos.y = random.randint(0, HEIGHT)
        # bottom
        elif location == 3:
            self.pos.x = random.randint(0, WIDTH)
            self.pos.y = HEIGHT + self.rect.height
        # left
        elif location == 4:
            self.pos.x = 0 - self.rect.width
            self.pos.y = random.randint(0, HEIGHT)

        #self.pos = Vector(WIDTH / 2, HEIGHT / 2)

        # generate heading direction
        heading_point = Vector(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        deltaX = heading_point.x - self.pos.x
        deltaY = heading_point.y - self.pos.y
        self.vel = Vector(deltaX * 0.002, deltaY * 0.002)

    def destroy(self):
        self.kill()
