import pygame
from os import path
from settings import *

Vector = pygame.math.Vector2

class Background(object):
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(path.join(self.game.dir, "background.jpg")).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.stars = pygame.sprite.Group()
        self.stars.add(Stars(self))

    def update(self):
        self.stars.update()

    def draw(self):
        self.game.screen.blit(self.image, (0, 0, WIDTH, HEIGHT))
        self.stars.draw(self.game.screen)


class Stars(pygame.sprite.Sprite):
    def __init__(self, background):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.image = pygame.image.load(path.join(self.background.game.dir, "stars.png")).convert()
        self.image = pygame.transform.scale(self.image, (int(WIDTH * 1.5), int(HEIGHT * 1.5)))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.start_pos = (WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos

    def update(self):
        force_x = self.background.game.player.vel.x * 0.1
        force_y = self.background.game.player.vel.y * 0.1

        if force_x < 0:
            if self.rect.center[0] < WIDTH / 4:
                force_x = 0
        elif force_x > 0:
            if self.rect.center[0] > WIDTH * 0.75:
                force_x = 0
        if force_y < 0:
            if self.rect.center[1] < HEIGHT / 4:
                force_y = 0
        elif force_y > 0:
            if self.rect.center[1] > HEIGHT * 0.75:
                force_y = 0

        self.pos += (-force_x, -force_y)

        self.rect.center = self.pos
