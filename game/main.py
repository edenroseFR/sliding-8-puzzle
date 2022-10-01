import enum
import pygame
import random
import time
from .sprite import *
from .settings import *


class Game:
    def __init__(self, initial=[], solution=None) -> None:
        pygame.init()
        self.initial = initial
        self.solution = solution
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def create_game(self):
        """
        This function will create a 2D list that will hold all the grids
        """

        if self.initial:
            grid = [
                self.initial[:3],
                self.initial[3:6],
                self.initial[6:9]
            ]
        else:
            # Create a 2D grid
            grid = []
            tiles = [x+1 for x in range(GAME_SIZE**2)]
            for x in range(GAME_SIZE):
                row = tiles[(x)*GAME_SIZE:GAME_SIZE*(x+1)]
                grid.append(row)

            # Set the bottom right grid to zero
            grid[-1][-1] = 0

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
        print('tiles grid is ', self.tiles_grid)
        self.draw_tiles()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.execute_solution()
            self.update()
            self.draw()


    def update(self):
        self.all_sprites.update()


    def draw(self):
        """
        This is where all the graphics are coded
        """
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


    def move_tile(self, clicked_tile, row, col, s=None):
        """
        :param clicked_tile:
        :param row:
        :param col:
        :param s: the passed solution (computer-generated)
        """
        if (clicked_tile.right() and col-1 >= 0 and self.tiles_grid[row][col-1] == 0) \
            or s == 'R':

            self.tiles_grid[row][col-1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.left() and col+1 < GAME_SIZE and self.tiles_grid[row][col+1] == 0) \
            or s == 'L':

            self.tiles_grid[row][col+1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.up() and row+1 < GAME_SIZE and self.tiles_grid[row+1][col] == 0) \
            or s == 'U':

            self.tiles_grid[row+1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.down() and row-1 >= 0 and self.tiles_grid[row-1][col] == 0) \
            or s == 'D':

            self.tiles_grid[row-1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        else:
            print('Invalid move')


    def events(self):
        """
        This function is responsible for detecting events in the game.
        """
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


    def execute_solution(self):
        """
        This function will only get executed if the
        solution is passed as an argument to the game.
        """
        if self.solution:
            print(self.tiles)
            for s in self.solution:
                x = self.initial.index(0)
                row = int(x / 3)
                col = int(x % 3) + 1
                tile = self.tiles[row][col]
                self.move_tile(tile, row, col, s)
                self.solution.pop(0)


def start_game(initial_state=[], solution=[]):
    game = Game(initial_state, solution)

    while True:
        game.new()
        game.run()