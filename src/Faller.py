from Match import Match
from Helper import Helper

NEXT = 0
FALLER = 1
MOVE_LEFT = 2
MOVE_RIGHT = 3
ROTATE = 4
QUIT = 5
EMPTY_CELL = ' '


class Faller:

    def move_faller(gamestate, direction: int) -> None:
        '''moves faller left or right'''
        faller_cells = Helper._get_faller_cells(gamestate)
        bot_cell = faller_cells[2]
        if Faller._faller_can_move(gamestate, bot_cell, direction):
            if direction == MOVE_RIGHT:
                gamestate._faller_col += 1
            else:
                gamestate._faller_col -= 1
            for cell in faller_cells[::-1]:
                gamestate._board[cell._row][gamestate._faller_col].make_faller_cell(cell._display)
                cell.make_empty_cell()
            if Faller._landed(gamestate):
                Faller._assert_landed_cells(gamestate)

    def make_faller(gamestate, col: int, jewels: list) -> None:
        '''creates a faller and places it in col above board'''
        if not gamestate._board[3][col]._empty:
            gamestate._game_over = True
            return
        for i in range(1, 4):
            gamestate._board[i][col].make_faller_cell(jewels[i-1])
        gamestate._faller_col = col
        gamestate._faller = True
        gamestate._last_faller_row = 0
        if Faller._landed(gamestate):
            Faller._assert_landed_cells(gamestate)

    def _faller_can_move(gamestate, cell, direction: int) -> bool:
        '''returns true if faller can move'''
        if direction == MOVE_RIGHT:
            if gamestate._faller_col == gamestate._cols:
                return False
            else:
                cell_to_right = gamestate._board[cell._row][cell._col+1]
                if cell_to_right._empty:
                    return True
                else:
                    return False
        else:
            if gamestate._faller_col == 0:
                return False
            else:
                cell_to_left = gamestate._board[cell._row][cell._col-1]
                if cell_to_left._empty:
                    return True
                else:
                    return False

    def rotate_faller(gamestate) -> None:
        '''rotates the faller in place'''
        faller_cells = Helper._get_faller_cells(gamestate)
        top_cell_color = faller_cells[0]._display
        top_cell_row = faller_cells[0]._row
        mid_cell_row = faller_cells[1]._row
        mid_cell_color = faller_cells[1]._display
        bot_cell_color = faller_cells[2]._display
        bot_cell_row = faller_cells[2]._row
        if Faller._landed(gamestate):
            gamestate._board[bot_cell_row][gamestate._faller_col].make_landed_cell(top_cell_color)
            gamestate._board[mid_cell_row][gamestate._faller_col].make_landed_cell(bot_cell_color)
            gamestate._board[top_cell_row][gamestate._faller_col].make_landed_cell(mid_cell_color)
        else:
            gamestate._board[bot_cell_row][gamestate._faller_col].make_faller_cell(top_cell_color)
            gamestate._board[mid_cell_row][gamestate._faller_col].make_faller_cell(bot_cell_color)
            gamestate._board[top_cell_row][gamestate._faller_col].make_faller_cell(mid_cell_color)

    def drop_faller(gamestate) -> None:
        '''drops faller one row if row is empty, faller landed if empty under new faller, else freeze faller'''
        faller_cells = Helper._get_faller_cells(gamestate)
        last_faller_cell = faller_cells[2]
        if Helper._empty_under_cell(gamestate, last_faller_cell):
            gamestate._last_faller_row += 1
            for cell in faller_cells[::-1]:
                gamestate._board[cell._row+1][cell._col].make_faller_cell(cell._display)
                cell.make_empty_cell()
            if Faller._landed(gamestate):
                Faller._assert_landed_cells(gamestate)
        else:
            Faller._freeze_faller(gamestate)

    def _landed(gamestate) -> bool:
        '''returns true if faller landed'''
        new_last_faller_cell = Helper._get_faller_cells(gamestate)[2]
        empty_under_cell = Helper._empty_under_cell(gamestate, new_last_faller_cell)
        return not empty_under_cell

    def _assert_landed_cells(gamestate) -> None:
        '''changes cell attributes to landed'''
        faller_cells = Helper._get_faller_cells(gamestate)
        for cell in faller_cells:
            cell.make_landed_cell(cell._display)

    def _freeze_faller(gamestate) -> None:
        '''freezes faller, changes cell attributes and checks gameover'''
        faller_cells = Helper._get_faller_cells(gamestate)
        for cell in faller_cells:
            cell.make_frozen_cell(cell._display)
        Match.match_cells(gamestate)
        if not Match.matches(gamestate):
            Helper.check_game_over(gamestate)
        Faller._faller_gone(gamestate)

    def _faller_gone(gamestate) -> None:
        '''changes all faller attributes when gone'''
        gamestate._faller_col = None
        gamestate._faller = False
        gamestate._last_faller_row = None
