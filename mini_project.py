"""Tic Tac Toe with a Minimax-powered AI opponent."""

from __future__ import annotations

import random
import sys
from typing import List, Optional, Tuple

import pygame

WIDTH = 600
HEIGHT = 600
ROWS = 3
COLS = 3
CELL_SIZE = WIDTH // COLS

BACKGROUND_COLOR = "#343434"
GRID_COLOR = "#ffde57"
MARK_COLOR = "#646464"
WIN_LINE_COLOR = "#4584b6"

LINE_WIDTH = 15
CROSS_WIDTH = 20
CIRCLE_WIDTH = 15
OFFSET = 50
FPS = 60

EMPTY = 0
HUMAN = 1
AI_PLAYER = 2
AI_LEVEL = 1


class Board:
    def __init__(self) -> None:
        self.squares = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.marked_squares = 0

    def clone(self) -> Board:
        clone = Board()
        clone.squares = [row[:] for row in self.squares]
        clone.marked_squares = self.marked_squares
        return clone

    def reset(self) -> None:
        self.__init__()

    def place_mark(self, row: int, col: int, player: int) -> None:
        if not self.is_empty(row, col):
            raise ValueError("Square is already occupied.")
        self.squares[row][col] = player
        self.marked_squares += 1

    def is_empty(self, row: int, col: int) -> bool:
        return self.squares[row][col] == EMPTY

    def available_moves(self) -> List[Tuple[int, int]]:
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_empty(row, col):
                    moves.append((row, col))
        return moves

    def is_full(self) -> bool:
        return self.marked_squares == ROWS * COLS

    def winner(self, surface: Optional[pygame.Surface] = None) -> int:
        for col in range(COLS):
            player = self.squares[0][col]
            if player != EMPTY and all(self.squares[row][col] == player for row in range(ROWS)):
                if surface is not None:
                    start = (col * CELL_SIZE + CELL_SIZE // 2, 20)
                    end = (col * CELL_SIZE + CELL_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(surface, WIN_LINE_COLOR, start, end, LINE_WIDTH)
                return player

        for row in range(ROWS):
            player = self.squares[row][0]
            if player != EMPTY and all(self.squares[row][col] == player for col in range(COLS)):
                if surface is not None:
                    start = (20, row * CELL_SIZE + CELL_SIZE // 2)
                    end = (WIDTH - 20, row * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.line(surface, WIN_LINE_COLOR, start, end, LINE_WIDTH)
                return player

        player = self.squares[0][0]
        if player != EMPTY and all(self.squares[index][index] == player for index in range(ROWS)):
            if surface is not None:
                pygame.draw.line(surface, WIN_LINE_COLOR, (20, 20), (WIDTH - 20, HEIGHT - 20), LINE_WIDTH)
            return player

        player = self.squares[ROWS - 1][0]
        if player != EMPTY and all(self.squares[ROWS - 1 - index][index] == player for index in range(ROWS)):
            if surface is not None:
                pygame.draw.line(surface, WIN_LINE_COLOR, (20, HEIGHT - 20), (WIDTH - 20, 20), LINE_WIDTH)
            return player

        return EMPTY


class AI:
    def __init__(self, level: int = 1, player: int = AI_PLAYER) -> None:
        self.level = level
        self.player = player
        self.opponent = HUMAN if player == AI_PLAYER else AI_PLAYER

    def random_move(self, board: Board) -> Optional[Tuple[int, int]]:
        moves = board.available_moves()
        if not moves:
            return None
        return random.choice(moves)

    def minimax(self, board: Board, maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
        winner = board.winner()
        if winner == self.player:
            return 1, None
        if winner == self.opponent:
            return -1, None
        if board.is_full():
            return 0, None

        if maximizing:
            best_eval = -10
            best_move = None
            for row, col in board.available_moves():
                next_board = board.clone()
                next_board.place_mark(row, col, self.player)
                evaluation, _ = self.minimax(next_board, False)
                if evaluation > best_eval:
                    best_eval = evaluation
                    best_move = (row, col)
            return best_eval, best_move

        best_eval = 10
        best_move = None
        for row, col in board.available_moves():
            next_board = board.clone()
            next_board.place_mark(row, col, self.opponent)
            evaluation, _ = self.minimax(next_board, True)
            if evaluation < best_eval:
                best_eval = evaluation
                best_move = (row, col)
        return best_eval, best_move

    def choose_move(self, board: Board) -> Optional[Tuple[int, int]]:
        if self.level == 0:
            return self.random_move(board)
        _, move = self.minimax(board, True)
        return move


class TicTacToeGame:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.board = Board()
        self.ai = AI(level=AI_LEVEL)
        self.current_player = HUMAN
        self.running = True
        self.draw_board()

    def reset(self) -> None:
        self.board.reset()
        self.current_player = HUMAN
        self.running = True
        self.draw_board()

    def draw_board(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        for index in range(1, COLS):
            position = index * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, (position, 0), (position, HEIGHT), LINE_WIDTH)
            pygame.draw.line(self.screen, GRID_COLOR, (0, position), (WIDTH, position), LINE_WIDTH)

    def draw_mark(self, row: int, col: int, player: int) -> None:
        if player == HUMAN:
            start_desc = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + OFFSET)
            end_desc = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
            pygame.draw.line(self.screen, MARK_COLOR, start_desc, end_desc, CROSS_WIDTH)
            start_asc = (col * CELL_SIZE + OFFSET, row * CELL_SIZE + CELL_SIZE - OFFSET)
            end_asc = (col * CELL_SIZE + CELL_SIZE - OFFSET, row * CELL_SIZE + OFFSET)
            pygame.draw.line(self.screen, MARK_COLOR, start_asc, end_asc, CROSS_WIDTH)
        else:
            center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, MARK_COLOR, center, CELL_SIZE // 4, CIRCLE_WIDTH)

    def make_move(self, row: int, col: int) -> None:
        self.board.place_mark(row, col, self.current_player)
        self.draw_mark(row, col, self.current_player)
        self.current_player = AI_PLAYER if self.current_player == HUMAN else HUMAN

    def check_game_state(self) -> bool:
        if self.board.winner(self.screen) != EMPTY:
            self.running = False
            return True
        if self.board.is_full():
            self.running = False
            return True
        return False

    def handle_human_move(self, position: Tuple[int, int]) -> None:
        if not self.running or self.current_player != HUMAN:
            return

        row = position[1] // CELL_SIZE
        col = position[0] // CELL_SIZE

        if self.board.is_empty(row, col):
            self.make_move(row, col)
            self.check_game_state()

    def play_ai_turn(self) -> None:
        if not self.running or self.current_player != AI_PLAYER:
            return

        move = self.ai.choose_move(self.board)
        if move is None:
            self.running = False
            return

        row, col = move
        self.make_move(row, col)
        self.check_game_state()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe AI")
    clock = pygame.time.Clock()
    game = TicTacToeGame(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_human_move(event.pos)

        game.play_ai_turn()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
