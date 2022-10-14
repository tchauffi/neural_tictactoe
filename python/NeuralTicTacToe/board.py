import numpy as np
from numpy.typing import NDArray
from typing import List
from enum import Enum


class GameStatus(Enum):
    NO_WINNER = -1
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    DRAW = 0


class TicTacBoard:
    def __init__(self):
        self.board: NDArray = np.zeros((3, 3)).astype(int)
        self.player1_turn: bool = True
        self.winner: GameStatus = GameStatus.NO_WINNER
        self.plays: List = []

    def play_turn(self, i: int, j: int) -> bool:
        """Play turn is possible and returns true if played else returns False"""
        if self.is_possible(i, j) and not self.is_finished():
            if self.player1_turn:
                self.board[i][j] = 1
            else:
                self.board[i][j] = -1

            self.draw_current_board_as_ascii()
            self.is_winning()

            self.player1_turn = not self.player1_turn
            self.plays.append((i, j))
            return True

        else:
            return False

    def draw_current_board_as_ascii(self):
        """Draw current board using ASCII + emoji"""
        board = ""
        for j in range(3):
            board = (
                f"{board}\n{self._encode_game(self.board[0][j])}|"
                f"{self._encode_game(self.board[1][j])}|{self._encode_game(self.board[2][j])}"
            )
        print(board)

    def get_possibilities(self) -> list:
        """Returns all possible possibilities from current board"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def is_possible(self, i: int, j: int) -> bool:
        """Check if combination is possible"""
        if (i, j) in self.get_possibilities():
            return True
        else:
            return False

    def is_player1_turn(self) -> bool:
        """Returns True if it is player 1 turns"""
        return self.player1_turn

    def define_winner(self):
        if self.player1_turn:
            print("Player 1 wins")
            self.winner = GameStatus.PLAYER_1_WIN
        else:
            print("Player 2 wins")
            self.winner = GameStatus.PLAYER_2_WIN

    def is_winning(self) -> bool:
        """Check if current state board is winning"""
        for j in range(3):
            if (
                np.abs(np.sum(self.board[j])) == 3
                or np.abs(np.sum(self.board.T[j])) == 3
            ):
                self.define_winner()
                return True
        if np.abs(self.board[0][0] + self.board[1][1] + self.board[2][2]) == 3:
            self.define_winner()
            return True
        elif np.abs(self.board[0][2] + self.board[1][1] + self.board[2][0]) == 3:
            self.define_winner()
            return True
        elif 0 not in self.board:
            print("It's a draw")
            self.winner = GameStatus.DRAW
            return False
        else:
            return False

    def is_finished(self) -> bool:
        if 0 in self.board.reshape(-1) and self.winner is GameStatus.NO_WINNER:
            return False
        else:
            return True

    @staticmethod
    def _encode_game(i):
        if i == 1:
            return "❌"
        elif i == 0:
            return "  "
        else:
            return "👌"


if __name__ == "__main__":
    # play game at random
    game = TicTacBoard()

    while not game.is_finished():
        turn = game.get_possibilities()[
            np.random.choice(range(len(game.get_possibilities())))
        ]

        print(turn)
        game.play_turn(turn[0], turn[1])
