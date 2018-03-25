import pygame
from game import Game

game = Game()

while game.running:
    game.run()

pygame.quit()
