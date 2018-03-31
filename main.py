import pygame
from game import Game

game = Game()

while game.running:
    game.new()

pygame.quit()
