import pygame
from settings import *

Vector = pygame.math.Vector2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, src, pos, dest):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.src = src
        self.dest = dest
        self.image = self.game.spritesheet.get_image(217, 72, 6, 6)
        self.rect = self.image.get_rect()
        # self.game.all_sprites.add(self)
        self.pos = pos
        self.dest = dest
        self.acc = Vector(0, 0)
        self.rect.center = self.pos
        deltaY = self.dest.y - self.rect.center[1]
        deltaX = self.dest.x - self.rect.center[0]
        self.vel = Vector(0, 0)
        self.force_vector = (deltaX * 0.01, deltaY * 0.01)
        self.vel = self.force_vector

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        if self.pos[0] > WIDTH or\
           self.pos[0] < 0 or\
           self.pos[1] > HEIGHT or\
           self.pos[1] < 0:
            self.kill()
