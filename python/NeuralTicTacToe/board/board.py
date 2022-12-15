import numpy as np
from numpy.typing import NDArray
from typing import List
from enum import Enum

import logging

logger = logging.getLogger("board")
logger.setLevel(logging.INFO)


class GameStatus(Enum):
    NO_WINNER = -1
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    DRAW = 0


def is_even(i):
    if i % 2 == 0:
        return True
    else:
        return False


class TicTacBoard:
    def __init__(self, plays: List = [], winner: GameStatus = GameStatus.NO_WINNER):
        self.winner = winner
        self.plays = plays

    def copy(self):
        return type(self)(self.plays, self.winner)

    def compute_board(self):
        board = np.zeros(9)
        for i, item in enumerate(self.plays):
            if is_even(i):
                board[item] = 1
            else:
                board[item] = -1
        return board.reshape((3, 3))

    def play_turn(self, i: int) -> bool:
        """Play turn is possible and returns true if played else returns False"""
        if self.is_possible(i) and not self.is_finished():
            self.plays.append(i)
            self.is_winning()
            return True
        else:
            return False

    def draw_current_board_as_ascii(self):
        """Draw current board using ASCII + emoji"""
        board_ascii = ""
        board = self.compute_board()
        for j in range(3):
            board_ascii = (
                f"{board_ascii}\n{self._encode_game(board[0][j])}|"
                f"{self._encode_game(board[1][j])}|{self._encode_game(board[2][j])}"
            )
        return board_ascii

    def get_possibilities(self) -> list:
        """Returns all possible possibilities from current board"""
        return [i for i in range(9) if i not in self.plays]

    def is_possible(self, i: int) -> bool:
        """Check if combination is possible"""
        if i in self.plays or i not in list(range(9)):
            return False
        else:
            return True

    def is_player1_turn(self) -> bool:
        """Returns True if it is player 1 turns"""
        return not is_even(len(self.plays))

    def define_winner(self):
        if self.is_player1_turn():
            self.winner = GameStatus.PLAYER_1_WIN
        else:
            self.winner = GameStatus.PLAYER_2_WIN

    def is_winning(self) -> bool:
        """Check if current state board is winning"""
        board = self.compute_board()
        for j in range(3):
            if np.abs(np.sum(board[j])) == 3 or np.abs(np.sum(board.T[j])) == 3:
                self.define_winner()
                return True
        if np.abs(board[0][0] + board[1][1] + board[2][2]) == 3:
            self.define_winner()
            return True
        elif np.abs(board[0][2] + board[1][1] + board[2][0]) == 3:
            self.define_winner()
            return True
        elif 0 not in board:
            self.winner = GameStatus.DRAW
            return False
        else:
            return False

    def is_finished(self) -> bool:
        if len(self.plays) < 9 and self.winner is GameStatus.NO_WINNER:
            return False
        else:
            return True

    def reset(self):
        self.winner = GameStatus.NO_WINNER
        self.plays = []

    @staticmethod
    def _encode_game(i):
        if i == 1:
            return "❌"
        elif i == 0:
            return "  "
        else:
            return "👌"
