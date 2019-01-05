# Nathan Costa 55997860

import pygame
from Columns import GameState
from Helper import Helper
from Match import Match
import random

ROWS = 13
COLS = 6
BOARD_WIDTH = 700
BOARD_HEIGHT = 750

BOARD_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (253, 253, 90)
GRID_COLOR = (64, 64, 64)
GREEN_COLOR = (110, 255, 51)
RED_COLOR = (255, 66, 51)
BLUE_COLOR = (51, 119, 255)
ORANGE_COLOR = (255, 165, 51)
PURPLE_COLOR = (134, 51, 255)
TURQUOISE_COLOR = (51, 255, 178)
PINK_COLOR = (255, 51, 147)

NEXT = 0
FALLER = 1
MOVE_LEFT = 2
MOVE_RIGHT = 3
ROTATE = 4
QUIT = 5
EMPTY_CELL = ' '

COLORS = {
    0: GREEN_COLOR,
    1: RED_COLOR,
    2: BLUE_COLOR,
    3: ORANGE_COLOR,
    4: PURPLE_COLOR,
    5: TURQUOISE_COLOR,
    6: PINK_COLOR
}


class ColumnsGame:
    def __init__(self):
        self._running = True
        self._state = GameState(ROWS, COLS)
        self._clock_tick = 16
        self._fall_tick_ratio = .2
        self._ticks = 0
        self._next_jewels = None
        self._next_col = None
        self._get_random_col()
        self._get_random_jewels()
        self._score = 0

    def run(self) -> None:
        pygame.init()
        self._match_sound = pygame.mixer.Sound('match.wav')
        self._landed_sound = pygame.mixer.Sound('landed.wav')
        self._my_score_font = pygame.font.SysFont("Times New Roman", 50)
        self._my_title_font = pygame.font.SysFont("Times New Roman", 70)
        self._resize_surface((BOARD_WIDTH, BOARD_HEIGHT))

        clock = pygame.time.Clock()

        while self._running:
            clock.tick(self._clock_tick)
            self._handle_events()
            self._redraw()
        pygame.quit()

    def _handle_events(self) -> None:
        '''Handles all events'''
        self._check_end_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._state.next_tick([MOVE_RIGHT])
                if event.key == pygame.K_LEFT:
                    self._state.next_tick([MOVE_LEFT])
                if event.key == pygame.K_SPACE:
                    self._state.next_tick([ROTATE])
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self._fall_tick_ratio = .8
            else:
                self._fall_tick_ratio = .2

        if not self._state._faller and not Match.matches(self._state):
            self._state.next_tick([FALLER, self._next_col, self._next_jewels])
            self._get_random_col()
            self._get_random_jewels()

        if self._ticks * self._fall_tick_ratio > 1.6:
            self._ticks = 0
            self._state.next_tick([NEXT])
        self._ticks += 1

    def _draw_title(self):
        surface = pygame.display.get_surface()
        title = self._my_title_font.render("COLUMNS", 1, (0, 0, 0))
        titlerotated = pygame.transform.rotate(title, 90)
        surface.blit(titlerotated, (600, 200))

    def _draw_next_jewels(self):
        '''draw next jewels to be dropped'''
        surface = pygame.display.get_surface()
        starting_x = 153
        starting_y = 103
        i = 0
        for jewel in self._next_jewels:
            pygame.draw.rect(surface, COLORS[jewel], (starting_x, starting_y + (i * 50), 44, 44))
            i += 1

    def _draw_score_board(self):
        '''draw score board'''
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, (0, 0, 0), (50, 350, 150, 50))
        scoreLabel = self._my_score_font.render("SCORE:", 1, (0, 0, 0))
        scoreDisplay = self._my_score_font.render(str(self._score), 1, (250, 250, 250))
        surface.blit(scoreLabel, (50, 300))
        surface.blit(scoreDisplay, (50, 350))

    def _get_random_col(self):
        '''returns random col from 0 to 5'''
        self._next_col = random.randrange(0, 6, 1)

    def _get_random_jewels(self):
        '''returns a list of 3 random jewel numbers 0 to 6'''
        random_list = []
        for i in range(0, 3):
            random_list.append(random.randrange(0, 7, 1))
        self._next_jewels = random_list

    def _draw_grid(self) -> None:
        '''draw grid for cells'''
        surface = pygame.display.get_surface()
        for x in range(250, 600, 50):
            pygame.draw.line(surface, GRID_COLOR, (x, 50), (x, 700), 3)
        for y in range(50, 750, 50):
            pygame.draw.line(surface, GRID_COLOR, (250, y), (550, y), 3)

    def _draw_cells(self) -> None:
        '''draw all cells in grid'''
        self._draw_faller_cells()
        self._draw_active_cells()

    def _draw_active_cells(self):
        '''draws active cells and checks for matched/landed cells'''
        active_cells = Helper._get_active_cells(self._state)
        landed_cells = Helper._get_landed_cells(self._state)
        matched_cells = Helper._get_matched_cells(self._state)

        if landed_cells and self._ticks * self._fall_tick_ratio > 1.6:
            self._landed_sound.play()
        if matched_cells and self._ticks * self._fall_tick_ratio > 1.6:
            self._match_sound.play()
            for cell in matched_cells:
                self._score += 10
        for cell in active_cells:
            self._place_cell_in_board(cell)

    def _place_cell_in_board(self, cell):
        '''put cells in board'''
        surface = pygame.display.get_surface()
        starting_x = 253
        starting_y = 53
        if cell._row > 2:
            displayed_row = cell._row - 3
            col = cell._col
            pygame.draw.rect(surface, COLORS[cell._display], (starting_x + (col*50), starting_y + (displayed_row*50), 44, 44))
            if cell._landed:
                pygame.draw.rect(surface, (250, 250, 250), (starting_x + (col*50), starting_y + (displayed_row*50), 44, 44), 3)
            if cell._matched:
                pygame.draw.rect(surface, (250, 250, 250), (starting_x + (col*50), starting_y + (displayed_row*50), 44, 44))

    def _draw_faller_cells(self) -> None:
        '''draws all faller cells'''
        faller_cells = Helper._get_faller_cells(self._state)
        for cell in faller_cells:
            self._place_cell_in_board(cell)

    def _draw_board(self) -> None:
        '''draw board'''
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, BOARD_COLOR, (250, 50, 300, 650))
        pygame.draw.rect(surface, BOARD_COLOR, (150, 100, 50, 150))

    def _redraw(self) -> None:
        '''redraw after each tick'''
        surface = pygame.display.get_surface()
        surface.fill(BACKGROUND_COLOR)
        self._draw_board()
        self._draw_title()
        self._draw_next_jewels()
        self._draw_grid()
        self._draw_score_board()
        self._draw_cells()
        pygame.display.flip()

    def _end_game(self) -> None:
        self._running = False

    def _check_end_game(self) -> None:
        if self._state._game_over:
            self._end_game()

    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)


if __name__ == '__main__':
    ColumnsGame().run()
