import pygame
import math
from settings import *
from projectile import Projectile
from text import Text

Vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(8, 168, 48, 48)
        self.image = pygame.transform.rotate(self.image, 360 - 90)
        self.original_image = self.image
        self.original_rect = self.original_image.get_rect()
        self.rect = self.image.get_rect()
        self.game.all_sprites.add(self)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = Vector(self.rect.center)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.direction = 0
        self.rotation_speed = 2
        self.direction_vector = Vector(0, 0)
        self.direction_magnitude = 500
        self.force_vector = Vector(0, 0)
        self.time_since_fire = 0
        self.vel_x_text = Text(self.game, "X velocity: " + str(self.vel.x), WHITE, None, None, None, True)
        self.vel_y_text = Text(self.game, "Y velocity: " + str(self.vel.y), WHITE, None, None, None, True)
        self.dir_x_text = Text(self.game, "Dir x: " + str(self.direction_vector.x), WHITE, None, None, None, True)
        self.dir_y_text = Text(self.game, "Dir y: " + str(self.direction_vector.y), WHITE, None, None, None, True)
        self.pos_x_text = Text(self.game, "Pos x: " + str(self.pos.x), WHITE, None, None, None, True)
        self.pos_y_text = Text(self.game, "Pos y: " + str(self.pos.y), WHITE, None, None, None, True)
        self.projectile_count_text = Text(self.game, "Projectile count: " + str(len(self.game.all_projectiles)), WHITE, None, None, None, True)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, -self.direction)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = self.rect.center)
        #self.image.get_rect().center = self.original_rect.center
        self.original_rect.center = self.pos

        self.direction %= 360

        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
        #update hitbox and directional vector
        # first quadrant
        if self.direction >= 0 and self.direction < 90:
            self.hitbox = \
            pygame.Rect(self.rect.x, self.original_rect.y,
                        self.original_rect.width + (self.original_rect.x - self.rect.x),
                        self.original_rect.height + (self.original_rect.y - self.rect.y))
        if self.direction >= 90 and self.direction < 180:
            self.hitbox = \
            pygame.Rect(self.rect.x, self.rect.y,
                        self.original_rect.width + (self.original_rect.x - self.rect.x),
                        self.original_rect.height + (self.original_rect.y - self.rect.y))
        if self.direction >= 180 and self.direction < 270:
            self.hitbox = \
            pygame.Rect(self.original_rect.x, self.rect.y,
                        self.original_rect.width + (self.original_rect.x - self.rect.x),
                        self.original_rect.height + (self.original_rect.y - self.rect.y))
        if self.direction >= 270 and self.direction < 360:
            self.hitbox = \
            pygame.Rect(self.original_rect.x, self.original_rect.y,
                        self.original_rect.width + (self.original_rect.x - self.rect.x),
                        self.original_rect.height + (self.original_rect.y - self.rect.y))
        #self.rect = self.hitbox

        self.direction_vector = Vector(math.sin(math.radians(self.direction)), -(math.cos(math.radians(self.direction))))
        self.heading_point = Vector(self.rect.center[0] + (self.direction_magnitude * self.direction_vector.x),
                                    self.rect.center[1] + (self.direction_magnitude * self.direction_vector.y))

        deltaY = self.heading_point.y - self.rect.center[1]
        deltaX = self.heading_point.x - self.rect.center[0]
        self.force_vector = (deltaX * PLAYER_ACC, deltaY * PLAYER_ACC)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.direction += self.rotation_speed
        if keys[pygame.K_UP]:
            self.vel += self.force_vector
        if keys[pygame.K_DOWN]:
            self.acc = -PLAYER_ACC
        if keys[pygame.K_SPACE]:
            self.fire()

        # limit velocity
        if self.vel.x > PLAYER_MAX_VELOCITY:
            self.vel.x -= self.vel.x - PLAYER_MAX_VELOCITY
        if self.vel.x < -PLAYER_MAX_VELOCITY:
            self.vel.x -= self.vel.x + PLAYER_MAX_VELOCITY
        if self.vel.y > PLAYER_MAX_VELOCITY:
            self.vel.y -= self.vel.y - PLAYER_MAX_VELOCITY
        if self.vel.y < -PLAYER_MAX_VELOCITY:
            self.vel.y -= self.vel.y + PLAYER_MAX_VELOCITY

        self.pos += self.vel

        # calculations are made to pos, then rect.center is set to pos
        self.rect.center = self.pos
        self.acc *= PLAYER_ACC

        # update texts
        self.vel_x_text.update_text("X velocity: " + str(self.vel.x))
        self.vel_y_text.update_text("Y velocity: " + str(self.vel.y))
        self.dir_x_text.update_text("Dir x: " + str(self.direction_vector.x))
        self.dir_y_text.update_text("Dir y: " + str(self.direction_vector.y))
        self.pos_x_text.update_text("Pos x: " + str(self.pos.x))
        self.pos_y_text.update_text("Pos y: " + str(self.pos.y))
        self.projectile_count_text.update_text("Projectile count: " + str(len(self.game.all_projectiles)))

    def draw(self):
        if self.game.show_dev:
            pygame.draw.rect(self.game.screen, BLUE, self.original_rect, 0)
            pygame.draw.rect(self.game.screen, GREEN, self.rect, 2)
            pygame.draw.rect(self.game.screen, RED, self.hitbox, 1)
            pygame.draw.line(self.game.screen, WHITE, self.rect.center,
                            (self.rect.center[0] + (self.direction_magnitude * self.direction_vector.x),
                             self.rect.center[1] + (self.direction_magnitude * self.direction_vector.y)), 1)

    def fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_since_fire > 300:
            self.time_since_fire = current_time
            self.game.all_projectiles.add(Projectile(self.game, self, self.get_pos(), self.heading_point))

    def get_pos(self):
        pos = Vector(self.pos.x, self.pos.y)
        return pos
