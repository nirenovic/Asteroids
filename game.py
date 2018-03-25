# game object
import pygame
import sys
from settings import *
from os import path
from player import Player
from spritesheet import Spritesheet

class Game(object):
    def __init__(self):
        # first step is always to initialise pygame
        pygame.init()
        # the mixer handles the sound, this also needs to be initialised
        pygame.mixer.init()
        # a pygame screen object needs to be created
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # set up a clock for tracking time and drawing FPS correctly
        self.clock = pygame.time.Clock()
        self.running = True
        self.dir = path.dirname(__file__)
        print(str(self.dir))
        self.load_data()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.playing = True
        self.all_text = []

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

    def update(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            # check for close window
            if event.type == pygame.QUIT:
                self.running = False
        # update all sprites
        self.all_sprites.update()

    def render(self):
        self.screen.fill(BLACK)
        self.player.draw()
        self.draw_text("Angle: " + str(self.player.direction), WHITE, 16, 20, 20)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while(self.running):
            self.process_events()
            self.update()
            self.render()

    def draw_text(self, text, color, size = None, x = None, y = None):
        if size is None:
            size = 16
        if x is None:
            if len(self.all_text) > 0:
                x = self.all_text[len(self.all_text) - 1].x
            else:
                x = 20
        if y is None:
            if len(self.all_text) > 0:
                y = self.all_text[len(self.all_text) - 1].y + 20
            else:
                y = 20
        self.font = pygame.font.SysFont('arial', size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        self.all_text.append(text_rect)
        self.screen.blit(text_surface, text_rect)
