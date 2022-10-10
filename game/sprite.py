import pygame
from .settings import *

pygame.font.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        """
        :param x: x coordinate of the tile
        :param y: y coordinate of the tile
        :param text:
        """
        pygame.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x = x + LEFT_MARGIN
        self.y = y + TOP_MARGIN
        self.text = text
        self.rect = self.image.get_rect()
        self.draw_rects()
        self.write_text()


    def draw_rects(self, r=20):
        """
        :param r: border_radius
        """
        pygame.draw.rect(
            self.image,
            BGCOLOR,
            (self.x - 10, self.y - 10, TILESIZE + 10, TILESIZE + 10)
        )
        pygame.draw.rect(
            self.image,
            TILE_COLOR,
            (self.x + 10, self.y + 10, TILESIZE - 15, TILESIZE - 15),
            border_radius=r
        )

    def write_text(self):
        if self.text != 'empty':
            self.font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
            font_surface = self.font.render(self.text, True, WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x + 7, draw_y + 5))
        else:
            self.image.fill(BGCOLOR)

    def highlight(self, selected):
        if selected:
            self.draw_rects(15)
        else:
            self.draw_rects()
        self.write_text()

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and \
            self.rect.top <= mouse_y <= self.rect.bottom

    def hover(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)

    def right(self):
        return self.rect.x - TILESIZE >= 0

    def left(self):
        return self.rect.x + TILESIZE <= (GAME_SIZE + LEFT_MARGIN)  * TILESIZE

    def up(self):
        return self.rect.y + TILESIZE <= (GAME_SIZE + TOP_MARGIN) * TILESIZE

    def down(self):
        return self.rect.y - TILESIZE >= 0


class UIElement:
    def __init__(self, x, y, text='', justify='center'):
        self.x, self.y = x, y
        self.text = text
        self.justify = justify


    def write_text(self, screen):
        font = pygame.font.SysFont(FONT_STYLE, 30)
        text = font.render(self.text, True, WHITE)
        if self.justify == 'center':
            w,h = font.size(self.text)
            self.x = int((WIDTH - w) / 2)
            self.y = int(HEIGHT - NAV_HEIGHT - h)
        pygame.draw.rect(
            screen,
            TILE_COLOR,
            (self.x, self.y, w+20, h+5),
            border_radius=10
        )
        screen.blit(
            text,
            (self.x + 10, self.y + 5)
        )

    def draw_nav(self, screen, color, w, h):
        pygame.draw.rect(screen, color, (self.x, self.y, w, h))


class Button:
    def __init__(
        self,
        x=0, y=0,
        width=10,
        height=10,
        text='Button',
        text_colour=DARKGREY,
        colour=WHITE,
        roundness=0
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.text_colour = text_colour
        self.roundness = roundness

    def draw_rect(self, screen):
        pygame.draw.rect(
            screen,
            self.colour,
            (self.x, self.y, self.width, self.height),
            border_radius=self.roundness
        )
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def draw_img(self, screen, img, rect, scale=None):
        img = pygame.transform.scale(img, scale) if scale else img
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        screen.blit(img, self.rect)

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.height

    def hover(self):
        """
        This function will return True if the cursor
        is on top of the Button object.
        False, otherwise.
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())
