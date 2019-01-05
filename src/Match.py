from Helper import Helper


class Match:

    def matches(gamestate) -> bool:
        '''checks if there are any matches'''
        matched_cells = Helper._get_matched_cells(gamestate)
        if not matched_cells:
            return False
        return True

    def remove_matches(gamestate) -> None:
        '''removes match attribute for cells'''
        matched_cells = Helper._get_matched_cells(gamestate)
        for cell in matched_cells:
            cell.make_empty_cell()

    def match_cells(gamestate) -> None:
        '''matches all cells'''
        all_matched_cells = []
        matched_horizontally = Match._cells_matched_horizontally(gamestate)
        matched_vertically = Match._cells_matched_vertically(gamestate)
        matched_diagonally = Match._cells_matched_diagonally(gamestate)
        matched_anti_diagonally = Match._cells_matched_anti_diagonally(gamestate)
        all_matched_cells.append(matched_horizontally)
        all_matched_cells.append(matched_vertically)
        all_matched_cells.append(matched_diagonally)
        all_matched_cells.append(matched_anti_diagonally)
        for cells in all_matched_cells:
            for cell in cells:
                cell.make_matched_cell(cell._display)

    def _cells_matched_horizontally(gamestate) -> list:
        '''matches horizontal cells'''
        matched_cells = Match._matching_algorithm(gamestate, gamestate._board)
        return matched_cells

    def _cells_matched_anti_diagonally(gamestate) -> list:
        '''matches anti diagonal cells'''
        matched_cells = []
        h, w = len(gamestate._board), len(gamestate._board[0])
        diagonals = [[gamestate._board[p - q][q]
                     for q in range(max(p-h+1, 0),
                     min(p+1, w))]for p in range(h + w - 1)]
        diagonals_over_3 = []
        for diagonal in diagonals:
            if len(diagonal) >= 3:
                diagonals_over_3.append(diagonal)
        matched_cells = Match._matching_algorithm(gamestate, diagonals_over_3)
        return matched_cells

    def _cells_matched_diagonally(gamestate) -> list:
        '''matches diagonal cells'''
        matched_cells = []
        h, w = len(gamestate._board), len(gamestate._board[0])
        diagonals = [[gamestate._board[h - p + q - 1][q]
                     for q in range(max(p-h+1, 0),
                     min(p+1, w))]for p in range(h + w - 1)]
        diagonals_over_3 = []
        for diagonal in diagonals:
            if len(diagonal) >= 3:
                diagonals_over_3.append(diagonal)
        matched_cells = Match._matching_algorithm(gamestate, diagonals_over_3)
        return matched_cells

    def _matching_algorithm(gamestate, groups) -> list:
        '''gets matches in cell groups'''
        matched_cells = []
        for group in groups:
            j = len(group)
            while j != 2:
                num_shifts = abs(j-(len(group))) + 1
                for x in range(0, num_shifts):
                    subgroup = group[x:j+x]
                    subgroup_cells = ''
                    for cell in subgroup:
                        subgroup_cells += str(cell._display)
                    same_cells = str(group[x]._display) * j
                    if subgroup_cells == same_cells:
                        for cell in subgroup:
                            if not cell._empty:
                                matched_cells.append(cell)
                j -= 1
        return matched_cells

    def _cells_matched_vertically(gamestate) -> list:
        '''matches vertical cells'''
        matched_cells = []
        cols = []
        for c in range(0, gamestate._cols+1):
            col = []
            for r in range(0, gamestate._rows+1):
                cell = gamestate._board[r][c]
                col.append(cell)
            cols.append(col)
        matched_cells = Match._matching_algorithm(gamestate, cols)
        return matched_cells
