class Helper:

    def _get_matched_cells(gamestate):
        '''gets all matched cells'''
        active_cells = Helper._get_active_cells(gamestate)
        matched_cells = []
        for cell in active_cells:
            if cell._matched:
                matched_cells.append(cell)
        return matched_cells

    def _get_landed_cells(gamestate) -> list:
        '''returns all cells with attributes of landed'''
        landed_cells = []
        for row in gamestate._board:
            for cell in row:
                if cell._landed:
                    landed_cells.append(cell)
        return landed_cells

    def _get_faller_cells(gamestate) -> list:
        '''returns all cells with attributes of faller'''
        faller_list = []
        for row in gamestate._board:
            for cell in row:
                if cell._faller:
                    faller_list.append(cell)
        return faller_list

    def _get_active_cells(gamestate) -> list:
        '''returns all active cells on board not including faller or landed'''
        cell_list = []
        for row in gamestate._board:
            for cell in row:
                if not cell._empty and not cell._faller and not cell._landed:
                    cell_list.append(cell)
        return cell_list

    def check_game_over(gamestate) -> None:
        '''checks if game is over'''
        if gamestate._last_faller_row is None:
            return
        if gamestate._last_faller_row < 2:
            gamestate._game_over = True

    def drop_cells(gamestate) -> None:
        '''drops all cells into empty spaces'''
        still_dropping = True
        while still_dropping:
            active_cells = Helper._get_active_cells(gamestate)
            still_dropping = False
            for cell in active_cells:
                if Helper._empty_under_cell(gamestate, cell):
                    gamestate._board[cell._row+1][cell._col].make_frozen_cell(cell._display)
                    cell.make_empty_cell()
                    still_dropping = True

    def _empty_under_cell(gamestate, cell) -> bool:
        '''returns true if space is empty under current cell'''
        bottom = (gamestate._rows)
        if cell._row != bottom:
            cell_below = gamestate._board[cell._row + 1][cell._col]
            if cell_below._empty:
                return True
        return False
