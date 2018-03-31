import pygame

class Text(object):
    def __init__(self, game, text, color, size = None, x = None, y = None, is_dev = False, add_to_all = True):
        self.game = game
        self.text = text
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.is_dev = is_dev

        if self.size is None:
            self.size = 16
        if self.x is None:
            if len(self.game.all_text) > 0:
                self.x = self.game.all_text[len(self.game.all_text) - 1].x
            else:
                self.x = 20
        if y is None:
            if len(self.game.all_text) > 0:
                self.y = self.game.all_text[len(self.game.all_text) - 1].y + 20
            else:
                self.y = 20
        self.font = pygame.font.SysFont('arial', self.size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y

        if add_to_all:
            self.game.all_text.append(self)
        if is_dev:
            self.game.dev_text.append(self)

    def update_text(self, text):
        self.text_surface = self.font.render(text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y
