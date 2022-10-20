import pygame
from . import store
from .sprite import *
from .settings import *
from .widget import create_button
from time import sleep
from solver.main import randomize_move, solve_puzzle


class Game:
    def __init__(self, initial=[]):
        """
        :param initial: the shuffled state
        """
        pygame.init()
        self.initial = initial or [1,2,3,4,5,6,7,8,0]
        self.move = ''
        self.key_moves = ''

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
        self.initial = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, 'empty'))

                try:
                    self.initial.append(int(tile))
                except ValueError:
                    self.initial.append(0)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.grid_completed = [1,2,3,4,5,6,7,8,0]
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.draw()
            self.update()
            self.events()

    def update(self):
        self.all_sprites.update()

        if store.start_shuffle:
            prev_move = self.move if self.move  else ''
            self.move = randomize_move(self.initial, prev_move)
            self.execute_move()
            store.shuffle_times += 1
            if store.shuffle_times > 10:
                store.start_shuffle = False
                store.shuffle_times = 0

        if self.initial == self.grid_completed:
            store.puzzle_solved = True
            store.show_clicked  = False
            self.move = ''

        if len(self.key_moves) > 0 and store.solving:
            self.move = self.key_moves[0]
            self.execute_move()

        if len(self.key_moves) == 0:
            store.solving = False

    def draw(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_UI()
        pygame.display.flip()

    def draw_UI(self):
        # Navbar
        self.nav_rect = UIElement(0, 0)
        self.nav_rect.draw_nav(self.screen, BGCOLOR, WIDTH, NAV_HEIGHT+30)
        self.nav_rect.draw_nav(self.screen, TILE_COLOR, WIDTH, NAV_HEIGHT)

        # Buttons
        img, rect = Game.get_img_info(LOGO)
        self.logo = create_button(self.screen, img, rect, 'logo')

        img, rect = Game.get_img_info(SHUFFLE_BTN)
        self.shuffle = create_button(self.screen, img, rect, 'shuffle', 'hand')


        if store.show_clicked:
            img, rect = Game.get_img_info(SOLVE_BTN)
        elif store.puzzle_solved:
            img, rect = Game.get_img_info(SOLVED_BTN)
        else:
            img, rect = Game.get_img_info(SHOW_BTN)
        self.solve = create_button(self.screen, img, rect, 'solve')
        if self.solve.hover() and not store.puzzle_solved:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Answer Key
        self.key = UIElement(self.solve.x, self.solve.y, ' '.join(self.key_moves))
        self.key.write_text(self.screen)

        img, rect = Game.get_img_info(HELP_BTN)
        self.help_btn = create_button(self.screen, img, rect, 'help-btn')

        if self.help_btn.hover():
            img, rect = Game.get_img_info(HELP_TEXT)
            self.help_text = create_button(self.screen, img, rect, 'help-text')

        for algo, state in store.algorithms.items():
            img_file = STATIC + algo + '-' + state + '.png'
            img, rect = Game.get_img_info(img_file)
            # Create a global variable for each algorithm,
            # so that it becomes accessible by other methods
            globals()[algo] = create_button(self.screen, img, rect, algo, 'hand')


    @staticmethod
    def get_img_info(img):
        btn = pygame.image.load(img)
        rect = btn.get_rect()
        return btn, rect

    def move_tile(self, clicked_tile, row, col, s=False):
        """
        :param clicked_tile:
        :param row:
        :param col:
        :param s: the passed solution (computer-generated)
        :param k: the key pressed
        """
        if s == 'R'\
            or (clicked_tile.right() and col-1 >= 0 and self.tiles_grid[row][col-1] == 0):

            self.tiles_grid[row][col-1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.update_key_moves('R')

        elif s == 'L'\
            or (clicked_tile.left() and col+1 < GAME_SIZE and self.tiles_grid[row][col+1] == 0):

            self.tiles_grid[row][col+1] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.update_key_moves('L')

        elif s == 'U'\
            or (clicked_tile.up() and row+1 < GAME_SIZE and self.tiles_grid[row+1][col] == 0):

            self.tiles_grid[row+1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.update_key_moves('U')

        elif s == 'D'\
            or (clicked_tile.down() and row-1 >= 0 and self.tiles_grid[row-1][col] == 0):

            self.tiles_grid[row-1][col] = int(clicked_tile.text)
            self.tiles_grid[row][col] = 0
            self.update_key_moves('D')

        else:
            print('Invalid move')


    def update_key_moves(self, action):
        if len(self.key_moves) > 0 and self.key_moves[0] == action:
            self.key_moves = self.key_moves[2:]


    def events(self):
        """
        This function is responsible for detecting events in the game.
        """
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y) and \
                            tile.text != 'empty':
                            self.move_tile(tile, row, col)
                            self.draw_tiles()

                if self.shuffle.click(mouse_x, mouse_y):
                    self.key_moves = ''
                    store.show_clicked = False
                    store.start_shuffle = True
                    store.puzzle_solved = False

                if self.solve.click(mouse_x, mouse_y):
                    if not store.puzzle_solved:
                        if store.show_clicked:
                            store.show_clicked = False
                            store.solve_clicked = True
                        else:
                            store.show_clicked = True
                            store.solve_clicked = False
                        key = solve_puzzle(self.initial, store.active_algo)
                        print('Solution found!')
                        self.key_moves = ' '.join(key)

                if store.solve_clicked:
                    store.solving = True

                if astar.click(mouse_x, mouse_y):
                    store.active_algo = 'astar'
                    store.update_algorithms('astar')

                if bfs.click(mouse_x, mouse_y):
                    store.active_algo = 'bfs'
                    store.update_algorithms('bfs')

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.execute_move()

            # Handle tile hover
            for row, tiles in enumerate(self.tiles):
                for col, tile in enumerate(tiles):
                    if tile.hover(mouse_x, mouse_y):
                        tile.highlight(True)
                    else:
                        tile.highlight(False)

    def execute_move(self):
        if self.move:
            # search_solution(self.initial)
            x = self.initial.index(0)

            if self.move == 'U':
                row = int(x / 3) - 1
            elif self.move == 'D':
                row = int(x / 3) + 1
            else:
                row = int(x / 3)
            if self.move == 'R':
                col = int(x % 3) + 1
            elif self.move == 'L':
                col = int(x % 3) - 1
            else:
                col = int(x % 3)

            tile = self.tiles[row][col]
            self.move_tile(tile, row, col, self.move)
            sleep(100/1000)
            self.draw_tiles()



def start_game(initial_state=[]):
    game = Game(initial_state)

    while True:
        pygame.time.delay(1500)
        game.new()
        game.run()