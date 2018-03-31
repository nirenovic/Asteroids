# game object
import pygame
import sys
from settings import *
from os import path
from player import Player
from spritesheet import Spritesheet
from asteroid import Asteroid
from text import Text

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
        self.min_asteroids = 5
        self.all_text = []
        self.dev_text = []
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    if not self.show_dev:
                        self.show_dev = True
                    else:
                        self.show_dev = False
                if event.key == pygame.K_q:
                    pygame.quit()
        # special keys
        # current_time = pygame.time.get_ticks()
        # keys = pygame.key.get_pressed()
        # if current_time - self.time_since_toggle > 500:
        #     self.time_since_toggle = current_time
        #     if keys[pygame.K_u]:
        #         if not self.show_dev:
        #             self.show_dev = True
        #         else:
        #             self.show_dev = False

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
        self.check_collisions()
        self.spawn_asteroids()

    def render(self):
        self.screen.fill(BLACK)
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
        self.score_text = Text(self, str(self.score), WHITE, 30, WIDTH / 2, 20, False, False)
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
        self.score_text = Text(self, str(self.score), WHITE, 30, WIDTH / 2, 20, False, False)

    def spawn_asteroids(self):
        while len(self.all_asteroids) < self.min_asteroids:
            self.all_asteroids.add(Asteroid(self))

    def check_collisions(self):
        for asteroid in self.all_asteroids:
            for projectile in self.all_projectiles:
                if pygame.sprite.collide_rect(asteroid, projectile):
                    asteroid.destroy()
                    projectile.kill()
                    self.update_score(10)
