import enum
import pygame
import random
import time
from sprite import *
from settings import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def create_game(self):
        '''

        This function will create a 2D list that will hold all the grids
        '''

        # Create a 2D grid
        grid = []
        tiles = [x+1 for x in range(GAME_SIZE**2)]
        for x in range(GAME_SIZE):
            row = tiles[(x)*GAME_SIZE:GAME_SIZE*(x+1)]
            grid.append(row)

        # Set the bottom right grid to zero
        grid[-1][-1] = 0

        # Return grid
        return grid


    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, 'empty'))


    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.grid_completed = self.create_game()
        self.draw_tiles()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        self.all_sprites.update()


    def draw(self):
        '''
        This is where all the graphics are coded
        '''

        # Set window background
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        pygame.display.flip()


    def draw_grid(self):
        # Draw the puzzle grid
        for  row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for  col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))


    def move_tile(self, clicked_tile, row, col):
        print(self.tiles_grid)
        if clicked_tile.right() and col-1 >= 0 and self.tiles_grid[row][col-1] == 0:

            self.tiles_grid[row][col-1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif clicked_tile.left() and col+1 < GAME_SIZE and self.tiles_grid[row][col+1] == 0:

            self.tiles_grid[row][col+1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif clicked_tile.up() and row+1 < GAME_SIZE and self.tiles_grid[row+1][col] == 0:

            self.tiles_grid[row+1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif clicked_tile.down() and row-1 >= 0 and self.tiles_grid[row-1][col] == 0:

            self.tiles_grid[row-1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        else:
            print('Invalid move')


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y) and \
                            tile.text != 'empty':
                            self.move_tile(tile, row, col)

game = Game()

while True:
    game.new()
    game.run()