import random
import pygame


class Board:
    def __init__(self, size: tuple, starting_values: list = None, debug: bool = False):
        self.size = size    # size of the grid (nxn)
        for item in size:
            if not isinstance(item, int):
                raise ValueError('Size must be (nxn) integer tuples only!')
        self.starting_values = starting_values  # matrix of starting values
        self.debug = debug  # debug mode

        if not starting_values:
            # if the size of the starting value matrix does not match size of the grid
            # generate a nxn matrix of random binary digits
            self.starting_values = [[bool(random.randint(0, 1)) for b in range(size[0])] for b in range(size[1])]

        else:
            for e in range(len(self.starting_values)):  # FIXME: these nested loops are messy, cleanup if possible
                for item in self.starting_values[e]:  # check starting values are bool
                    if not isinstance(item, bool):
                        raise ValueError('Start values must be bool!')

        # create an empty list to store rune objects
        self.runes = [[] for _ in range(self.size[0])]  # access order: runes[col[row]]
        self.rune_states = [[] for _ in range(self.size[0])]    # for accessing just states in testing
        self.create_runes()     # create rune objects

    def create_runes(self):
        """Create an array of runes within the nxn grid."""
        if self.debug is False:
            print('\n')  # initial new line
            k = 1   # id iterable
            for j in range(self.size[0]):  # for each column of the grid
                for i in range(self.size[1]):   # for each row in the column
                    if self.starting_values:    # create runes with states dictated by starting values
                        try:
                            # create a rune at position (j, i) with state starting_values[j][i]
                            _rune = Rune(board=self, pos=(j, i), state=bool(self.starting_values[j][i]))
                        except ValueError:
                            raise ValueError('Starting values must be bool values!')

                    else:   # create runes with random states
                        _rune = Rune(board=self, pos=(j, i))  # create a rune at position (j, i)

                    _rune.id = f'Rune: {k}'
                    self.runes[j].append(_rune)     # append the rune to the board's list of runes
                    self.rune_states[j].append(_rune.state)
                    print(_rune.char, end='\t')  # print the rune's string character for testing
                    k += 1  # iterate k
                print('\n')  # new line

    def rune_edit(self, _select: tuple = None):
        """Allow a user to input a tuple to toggle the corresponding rune."""
        if not _select:     # if a position has not been inputted
            _select_col = int(input('Col: '))   # user input for column
            _select_row = int(input('Row: '))   # user input for row
            _select = (_select_row, _select_col)    # combine col and row into a tuple

        for _col in range(self.size[0]):  # iterate through 1st layer of rune list (columns)
            for _cell in self.runes[_col]:  # iterate through 2nd layer (rows)
                if _select == _cell.pos:  # if a Rune object has the same position as the input
                    _cell.swap_state()   # activate the swap state function

    def update(self):
        """Refresh display after runes have been activated/deactivated."""
        print('\n')     # initial new line
        for _col in range(self.size[0]):  # iterate through 1st layer of rune list (columns)
            for _cell in self.runes[_col]:  # iterate through 2nd layer (rows)
                print(_cell.char, end='\t')  # print the rune's string character for testing
            print('\n')  # new line


class Rune:
    def __init__(self, board: Board, pos: tuple, state: bool = None):
        self.board = board  # assign the rune to a board
        self.pos = pos  # assign position as a tuple
        self.col, self.row = pos[0], pos[1]  # break up position into vertical and horizontal components (col, row)

        self.state = state  # assign initial state (on or off)
        if self.state is None:
            self.state = bool(random.getrandbits(1))  # if an initial state is not given, generate a random one
        self.char = self.print_char()   # identifying character (x or o)

        # V redundant code - causes pytest to fail V
        # self.img = rune_on_img if self.state is True else rune_off_img  # images for on/off states

        self.sprite = None      # variable to store pygame sprite object
        self.sprite_pos = None      # variable to store sprite position once drawn

        self.id = None  # string ID for debugging

    def print_char(self):
        """assign a print variable for testing"""
        if self.state is True:
            char = 'o'
        else:
            char = 'x'
        return char

    def swap_state(self):
        """If the rune is activated, flip its state and the states of the runes around it."""
        self.state = not self.state     # flip the boolean state

        self.char = self.print_char()

        # Check for valid cells around the rune
        # get the position of each cell
        _above = (self.col, self.row - 1)
        _below = (self.col, self.row + 1)
        _left = (self.col - 1, self.row)
        _right = (self.col + 1, self.row)

        _neighbors = [_above, _below, _left, _right]    # store the neighboring cell positions in a list

        for item in _neighbors:     # iterate through the list, checking to see if they are valid positions
            self.validate_cell(item)

    def validate_cell(self, _cell: tuple):
        """Check if a given cell exists on the board, then flip it if it does."""
        # FIXME: find a cleaner way to loop through this
        for _col in range(self.board.size[0]):  # iterate through 1st layer of rune list (columns)
            for _row in self.board.runes[_col]:  # iterate through 2nd layer (rows)
                if _cell == _row.pos:   # if a Rune object has the same position as the input then it is valid
                    _row.state = not _row.state     # flip the state
                    _row.char = _row.print_char()   # change the print character of the rune to match the new state
                    break    # skip the rest of the loop once the matchine rune for this column has been found

    def display_sprite(self, x, y):
        """Update and redraw the sprite."""
        if self.state is True:
            self.img = rune_on_img   # images for on/off states
        else:
            self.img = rune_off_img

        self.sprite = game_display.blit(self.img, (x, y))
        return self.sprite


def draw_sprites(board):
    """Draw/redraw sprites onto pygame surface."""
    for x in range(board.size[0]):  # iterate through 1st layer of rune list (columns)
        for y in range(board.size[1]):  # iterate through 2nd layer (rows)
            board.runes[x][y].display_sprite(x*200, y*200)  # display the sprite
            board.runes[x][y].sprite_pos = (x*200, y*200)   # store the sprite's position within the Rune object


if __name__ == "__main__":     # main game loop for testing
    # import images
    background_img = pygame.image.load('resources/stone_floor.jpg')    # stone floor background
    rune_off_img = pygame.image.load('resources/rune_deactivated.png')      # off state sprite
    rune_on_img = pygame.image.load('resources/rune_activated.png')     # on state sprite

    box_off_img = pygame.image.load('resources/end_box_off.png')    # win box
    box_hover_img = pygame.image.load('resources/end_box_hover.png')    # win box when hovered over
    box_click_img = pygame.image.load('resources/end_box_click.png')    # win box when clicked

    # setup board
    _test = Board((3, 3))

    # setup win state
    win_state = [[True for b in range(_test.size[0])] for b in range(_test.size[1])]        # nxn matrix of 1s

    # setup pygame
    pygame.init()   # initialise pygame module
    display_width, display_height = _test.size[0]*200, _test.size[0]*200    # set display dimensions
    game_display = pygame.display.set_mode((display_width, display_width))  # setup display
    pygame.display.set_caption('RuneOut')   # set title

    black = (0, 0, 0)
    white = (255, 255, 255)

    clock = pygame.time.Clock()     # game clock

    crashed = False     # initial crash value
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:    # when the user clicks their mouse
                for y in range(_test.size[0]):  # iterate through 1st layer of rune list (columns)
                    for x in range(_test.size[1]):  # iterate through 2nd layer (rows)
                        if _test.runes[x][y].sprite:    # if the rune has a sprite
                            if _test.runes[x][y].sprite.collidepoint(pygame.mouse.get_pos()):
                                # if the mouse is over the sprite
                                _test.runes[x][y].swap_state()      # swap the state
                                draw_sprites(_test)     # redraw the sprites

            print(event)

        game_display.fill(black)

        game_display.blit(background_img, (0, 0))

        draw_sprites(_test)

        pygame.display.update()
        clock.tick(60)

        if _test.runes == win_state:  # check for the win state
            pass
            # TODO: add win condition textbox
            win_box_off = game_display.blit(box_off_img,
                                            (_test.size[0] * 200 - 400, _test.size[0] * 200 - 200))  # display win box
            if win_box_off.collidepoint(pygame.mouse.get_pos()):  # if the mouse is over the sprite
                win_box_off = None
                win_box_hover = game_display.blit(box_hover_img, (_test.size[0] * 200 - 400, _test.size[0] * 200 - 200))
                # display win box hover

    pygame.quit()
    quit()

    # _test = Board((3, 3))
    # while True:
    #     _test.rune_edit()   # input rune position to flip
    #     _test.update()     # update the board

# FIXME: cols and row for console printed version and GUI version are swapped
