import pygame
from .settings import *

pygame.font.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        '''

        :x - x coordinate of the tile
        :y - y coordinate of the tile
        :text - the numbers 0-8
        '''

        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != 'empty':
            self.font = pygame.font.SysFont('Consolas', 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGCOLOR)


    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and \
            self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x - TILESIZE >= 0

    def left(self):
        return self.rect.x + TILESIZE <= GAME_SIZE * TILESIZE

    def up(self):
        return self.rect.y + TILESIZE <= GAME_SIZE * TILESIZE


    def down(self):
        return self.rect.y - TILESIZE >= 0
