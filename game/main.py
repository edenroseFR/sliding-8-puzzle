import enum
import pygame
import random
import time
from .sprite import *
from .settings import *
from solver.main import randomize_puzzle, get_solution


class Game:
    def __init__(self, actions=[], initial=[], solution=None):
        """
        :param actions: actions taken to shuffle the puzzle
        :param initial: the shuffled state
        :param solution: action to take in order to solve the puzzle
        """
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
            return [
                self.initial[:3],
                self.initial[3:6],
                self.initial[6:9]
            ]

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
        """
        This is where all the graphics are drawn
        """
        # Set window background
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_UI()
        pygame.display.flip()


    def draw_UI(self):
        # Navbar
        self.nav_rect = UIElement(0, 0)
        self.nav_rect.draw_nav(self.screen, TILE_COLOR, WIDTH, NAV_HEIGHT)


        # Buttons
        img, rect = Game.get_img_info(LOGO)
        w,h = rect.width, rect.height
        rect.x = 10
        rect.y = (NAV_HEIGHT - h) / 2
        self.logo = Button()
        self.logo.draw_img(self.screen, img, rect)

        img, rect = Game.get_img_info(SHUFFLE_BTN)
        w,h = rect.width, rect.height
        rect.x = WIDTH - w - 10
        rect.y = (NAV_HEIGHT - h) / 2
        self.shuffle = Button()
        self.shuffle.draw_img(self.screen, img, rect)

        img, rect = Game.get_img_info(SOLVE_BTN)
        w,h = rect.width, rect.height
        rect.x = (WIDTH - w) / 2
        rect.y = HEIGHT - NAV_HEIGHT - (TILESIZE*GAME_SIZE) - (TOP_MARGIN * 100 - 100)
        self.solve = Button()
        self.solve.draw_img(self.screen, img, rect)

        img, rect = Game.get_img_info(HELP_BTN)
        w,h = rect.width, rect.height
        rect.x = WIDTH - w - 20
        rect.y = HEIGHT - h - 20
        self.help = Button()
        self.help.draw_img(self.screen, img, rect)


    @staticmethod
    def get_img_info(img):
        btn = pygame.image.load(img)
        rect = btn.get_rect()
        return btn, rect



    def draw_grid(self):
        # Draw the puzzle grid
        for  row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, BGCOLOR, (row, 0), (row, GAME_SIZE * TILESIZE))
        for  col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, BGCOLOR, (0, col), (GAME_SIZE * TILESIZE, col))


    def move_tile(self, clicked_tile, row, col, s=None, k=None):
        """
        :param clicked_tile:
        :param row:
        :param col:
        :param s: the passed solution (computer-generated)
        :param k: the key pressed
        """
        if (clicked_tile.right() and col-1 >= 0 and self.tiles_grid[row][col-1] == 0) \
            or s == 'R' or (k and k == pygame.k_RIGHT):

            self.tiles_grid[row][col-1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.left() and col+1 < GAME_SIZE and self.tiles_grid[row][col+1] == 0) \
            or s == 'L' or (k and k == pygame.k_LEFT):

            self.tiles_grid[row][col+1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.up() and row+1 < GAME_SIZE and self.tiles_grid[row+1][col] == 0) \
            or s == 'U' or (k and k == pygame.k_UP):

            self.tiles_grid[row+1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        elif (clicked_tile.down() and row-1 >= 0 and self.tiles_grid[row-1][col] == 0) \
            or s == 'D' or (k and k == pygame.k_DOWN):

            self.tiles_grid[row-1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.draw_tiles()

        else:
            print('Invalid move')

        if self.initial:
            self.initial = []
            for row in self.tiles_grid:
                for tile in row:
                    self.initial.append(tile)


    def events(self):
        """
        This function is responsible for detecting events in the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y) and \
                            tile.text != 'empty':
                            self.move_tile(tile, row, col)

                if self.shuffle.click(mouse_x, mouse_y):
                    actions, random_state = randomize_puzzle()
                    self.initial = random_state
                    self.solution = actions
                    print('sol ', self.solution)
                    self.new()

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.get_solution()



    def get_solution(self):
        """
        This function will execute the list of
        actions in the self.solution array.
        """
        print('sol ', self.solution)
        if self.solution:
            # search_solution(self.initial)
            for action in self.solution:
                x = self.initial.index(0)
                if action == 'U':
                    row = int(x / 3) - 1
                elif action == 'D':
                    row = int(x / 3) + 1
                else:
                    row = int(x / 3)
                if action == 'R':
                    col = int(x % 3) + 1
                elif action == 'L':
                    col = int(x % 3) - 1
                else:
                    col = int(x % 3)
                tile = self.tiles[row][col]
                self.move_tile(tile, row, col, self.solution[0])
                time.sleep(1)


def start_game(actions=[], initial_state=[], solution=[]):
    game = Game(actions, initial_state, solution)

    while True:
        game.new()
        game.run()