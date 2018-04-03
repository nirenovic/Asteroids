# game object
import pygame
import sys
from settings import *
from os import path
from player import Player
from spritesheet import Spritesheet
from asteroid import Asteroid
from text import Text
from background import Background

class Game(object):
    def __init__(self):
        # first step is always to initialise pygame
        pygame.init()
        # the mixer handles the sound, this also needs to be initialised
        pygame.mixer.init()
        # a pygame screen object needs to be created
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Asteroids")
        # set up a clock for tracking time and drawing FPS correctly
        self.clock = pygame.time.Clock()
        self.running = True
        self.dir = path.dirname(__file__)
        self.load_data()
        self.background = Background(self)
        self.min_asteroids = 5
        self.show_dev = False

    def load_data(self):
        if getattr(sys, 'frozen', False):
            self.spritesheet = Spritesheet(path.join(sys._MEIPASS, 'spritesheet.png'))
        else:
            self.spritesheet = Spritesheet(path.join(self.dir, 'spritesheet.png'))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        # special keys
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if current_time - self.time_since_toggle > 500:
            self.time_since_toggle = current_time
            if keys[pygame.K_LCTRL] and keys[pygame.K_d]:
                if not self.show_dev:
                    self.show_dev = True
                else:
                    self.show_dev = False

    def update(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            # check for close window
            if event.type == pygame.QUIT:
                self.running = False
        # update all sprites
        self.all_sprites.update()
        self.all_projectiles.update()
        self.all_asteroids.update()
        self.background.update()
        self.check_collisions()
        self.spawn_asteroids()

    def render(self):
        self.screen.fill(BLACK)
        self.background.draw()
        self.all_asteroids.draw(self.screen)
        self.all_projectiles.draw(self.screen)
        self.player.draw()
        #self.draw_text("Angle: " + str(self.player.direction), WHITE, 16, 20, 20)
        #self.draw_text("Asteroid count: " + str(len(self.all_asteroids)), WHITE)
        self.draw_score()
        for text in self.all_text:
            if text in self.dev_text:
                if self.show_dev:
                    self.draw_text(text)
            else:
                self.draw_text(text)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def new(self):
        self.score = 0
        self.time_since_toggle = 0
        self.all_text = []
        self.dev_text = []
        self.score_text = Text(self, "Score: " + str(self.score), WHITE, 30, WIDTH / 2, 30, False, False)
        self.score_text.text_rect.center = (WIDTH / 2, 30)
        self.all_sprites = pygame.sprite.Group()
        self.all_projectiles = pygame.sprite.Group()
        self.all_asteroids = pygame.sprite.Group()
        self.spawn_asteroids()
        self.player = Player(self)
        self.playing = True
        self.run()

    def run(self):
        while(self.running):
            self.process_events()
            self.update()
            self.render()

    def draw_text(self, text_object):
        self.screen.blit(text_object.text_surface, text_object.text_rect)

    def draw_score(self):
        self.draw_text(self.score_text)

    def update_score(self, amount):
        self.score += amount
        self.score_text = Text(self, "Score: " + str(self.score), WHITE, 30, WIDTH / 2, 30, False, False)
        self.score_text.text_rect.center = (WIDTH / 2, 30)

    def spawn_asteroids(self):
        while len(self.all_asteroids) < self.min_asteroids:
            self.all_asteroids.add(Asteroid(self))

    def check_collisions(self):
        # create sprite that uses player's calculated hitbox to test for accurate collision
        player_hitbox = pygame.sprite.Sprite()
        player_hitbox.rect = self.player.hitbox

        for asteroid in self.all_asteroids:
            if pygame.sprite.collide_rect(asteroid, player_hitbox):
                if not self.show_dev:
                    self.new()
            for projectile in self.all_projectiles:
                if pygame.sprite.collide_rect(asteroid, projectile):
                    asteroid.take_damage()
                    projectile.kill()
                    self.update_score(10)
