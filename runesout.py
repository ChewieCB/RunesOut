import random


class Board:
    def __init__(self, size: tuple, starting_values: list, debug: bool = False):
        self.size = size    # size of the grid (nxn)
        self.starting_values = starting_values  # matrix of starting values
        self.debug = debug  # debug mode

        if not len(starting_values) == size[0]:
            # if the size of the starting value matrix does not match size of the grid
            pass
            # TODO: add random starting value generation

        # create an empty list to store rune objects
        self.runes = [[] for _ in range(self.size[0])]  # access order: runes[col[row]]
        self.create_runes()     # create rune objects

    def create_runes(self):
        """Create an array of runes within the nxn grid."""
        if self.debug is False:
            print('\n')  # initial new line
            for j in range(self.size[0]):  # for each column of the grid
                for i in range(self.size[1]):   # for each row in the column
                    _rune = Rune(board=self, pos=(j, i))  # create a rune at position (j, i)
                    self.runes[j].append(_rune)     # append the rune to the board's list of runes
                    print(_rune.char, end='\t')  # print the rune's string character for testing
                print('\n')  # new line

    # ---------> OLD CODE <---------
    #
    # def create_runes_test(self):
    #     """Print the runes as 'x' to test placement."""
    #     print('\n')     # initial new line
    #     for j in range(self.size[0]):  # for each column of the grid
    #         for i in range(self.size[1]):   # for each row in the column
    #             _rune = Rune(board=self, pos=(j, i), state=None)
    #             self.runes[j].append(_rune)
    #             if _rune.state is True:
    #                 print('o', end='\t')    # print an o for each  activated rune
    #             else:
    #                 print('x', end='\t')    # print an x for each  deactivated rune
    #         print('\n')     # new line

    def rune_edit(self, _select: tuple = None):
        """Allow a user to input a tuple to toggle the corresponding rune."""
        if not _select:     # if a position has not been inputted
            _select_col = int(input('Col: '))   # user input for column
            _select_row = int(input('Row: '))   # user input for row
            _select = (_select_col, _select_row)    # combine col and row into a tuple

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
        if not state:
            self.state = bool(random.getrandbits(1))  # if an initial state is not given, generate a random one

        # assign a print variable for testing
        if self.state is True:
            self.char = 'o'
        else:
            self.char = 'x'

    def swap_state(self):
        """If the rune is activated, flip its state and the states of the runes around it."""
        self.state = not self.state     # flip the boolean state

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
        # FIXME: for _col in self.board.runes is not a viable way of looping through this, find a cleaner way
        for _col in range(self.board.size[1]):  # iterate through 1st layer of rune list (columns)
            for _row in self.board.runes[_col]:  # iterate through 2nd layer (rows)
                if _cell == _row.pos:   # if a Rune object has the same position as the input then it is valid
                    _row.state = not _row.state     # flip the state


_test = Board((3, 3), [0], debug=False)

while True:     # main game loop for testing
    _test.rune_edit()   # input rune position to flip
    _test.update()     # update the board
