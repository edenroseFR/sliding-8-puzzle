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
        self.x, self.y = x+LEFT_MARGIN, y+TOP_MARGIN
        pygame.draw.rect(self.image, BGCOLOR, (self.x - 10, self.y - 10, TILESIZE + 10, TILESIZE + 10))
        pygame.draw.rect(self.image, TILE_COLOR, (self.x + 10, self.y + 10, TILESIZE - 15, TILESIZE - 15), border_radius=30)
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != 'empty':
            self.font = pygame.font.SysFont('Fugaz One', 50)
            font_surface = self.font.render(self.text, True, WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x + 5, draw_y + 5))
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
        return self.rect.x + TILESIZE <= (GAME_SIZE + LEFT_MARGIN)  * TILESIZE

    def up(self):
        return self.rect.y + TILESIZE <= (GAME_SIZE + TOP_MARGIN) * TILESIZE


    def down(self):
        return self.rect.y - TILESIZE >= 0

class UIElement:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def write_text(self, screen, text):
        font = pygame.font.SysFont(FONT_STYLE, 30)
        text = font.render(text, True, DARKGREY)
        screen.blit(text, (self.x, self.y))

    def draw_nav(self, screen, color, w, h):
        pygame.draw.rect(screen, color, (self.x, self.y, w, h))



class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour, roundness=0):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text
        self.roundness = roundness

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), border_radius=self.roundness)
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height