from Faller import Faller
from Match import Match
from Helper import Helper


NEXT = 0
FALLER = 1
MOVE_LEFT = 2
MOVE_RIGHT = 3
ROTATE = 4
QUIT = 5
EMPTY_CELL = ' '


class InvalidInput:
    pass


class InvalidNumCols:
    pass


class InvalidNumRows:
    pass


class GameState:
    def __init__(self, num_rows: int, num_cols: int):
        self._board = GameState._initialize_empty_board(self, num_rows, num_cols)
        self._displayed_board = self._board[3:]
        self._rows = len(self._board)-1
        self._cols = len(self._board[0])-1
        self._game_over = False
        self._faller = False
        self._last_faller_row = None
        self._faller_col = None
        self._started = False
        GameState.check_valid_board(self)

    def _initialize_empty_board(self, num_rows: int, num_cols: int) -> [list]:
        '''initialize board with cell displays valued as empty'''
        empty_board = []
        for r in range(0, num_rows+3):  # +3 to give space for fallers
            empty_row = []
            for c in range(0, num_cols):
                empty_cell = Cell(EMPTY_CELL, (r, c))
                empty_row.append(empty_cell)
            empty_board.append(empty_row)
        return empty_board

    def next_tick(self, move_list: list) -> None:
        '''gets move and handles event'''

        if Match.matches(self):
            Match.remove_matches(self)
            Helper.drop_cells(self)
            Helper.check_game_over(self)
            Match.match_cells(self)

        move = move_list[0]

        if move == NEXT:
            if self._faller:
                Faller.drop_faller(self)
        elif move == FALLER:
            if not self._faller:
                GameState.check_valid_col_faller(self, move_list[1])
                Faller.make_faller(self, move_list[1], move_list[2])
        elif move == MOVE_LEFT:
            if self._faller:
                Faller.move_faller(self, MOVE_LEFT)
        elif move == MOVE_RIGHT:
            if self._faller:
                Faller.move_faller(self, MOVE_RIGHT)
        elif move == ROTATE:
            if self._faller:
                Faller.rotate_faller(self)
        elif move == QUIT:
            self._game_over = True
        else:
            raise InvalidInput

    def check_valid_board(self):
        if self._cols < 2:
            raise InvalidNumCols
        if self._rows < 6:
            raise InvalidNumRows

    def check_valid_col_faller(self, col):
        if col > self._cols or col < 0:
            raise InvalidInput


class Cell:
    def __init__(self, display: str, pos: tuple):
        self._display = display
        self._faller = False
        self._landed = False
        self._matched = False
        self._empty = True
        self._row, self._col = pos

    def make_landed_cell(self, display: str):
        self._landed = True
        self._faller = True
        self._empty = False
        self._matched = False
        self._display = display

    def make_faller_cell(self, display: str):
        self._faller = True
        self._landed = False
        self._empty = False
        self._matched = False
        self._display = display

    def make_matched_cell(self, display: str):
        self._matched = True
        self._empty = False
        self._faller = False
        self._landed = False
        self._display = display

    def make_frozen_cell(self, display: str):
        self._empty = False
        self._faller = False
        self._landed = False
        self._matched = False
        self._display = display
        if display == ' ':
            Cell.make_empty_cell(self)

    def make_empty_cell(self):
        self._empty = True
        self._faller = False
        self._landed = False
        self._matched = False
        self._display = EMPTY_CELL
