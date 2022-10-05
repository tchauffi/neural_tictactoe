import numpy as np


class TicTacBoard:
    def __init__(self):
        self.board = np.zeros((3, 3)).astype(int)
        self.player1_turn = True
        self.winner = False
        self.plays = []

    def play_turn(self, i: int, j: int):
        if self._is_possible(i, j) and not self._is_finished():
            if self.player1_turn:
                self.board[i][j] = 1
            else:
                self.board[i][j] = -1

            self.draw_current_board_as_ascii()
            self._is_winning()

            self.player1_turn = not self.player1_turn
            self.plays.append((i, j))

        else:
            raise ValueError("Turn is not possible")

    def draw_current_board_as_ascii(self):
        board = ""
        for j in range(3):
            board = f"{board}\n{self._encode_game(self.board[0][j])}|" \
                    f"{self._encode_game(self.board[1][j])}|{self._encode_game(self.board[2][j])}"
        print(board)

    def _get_possibilities(self) -> list:
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def _is_possible(self, i: int, j: int) -> bool:
        if (i, j) in self._get_possibilities():
            return True
        else:
            return False

    def _player1_turn(self) -> bool:
        return self.player1_turn

    def _is_winning(self) -> bool:
        for j in range(3):
            if np.abs(np.sum(self.board[j])) == 3 or np.abs(np.sum(self.board.T[j])) == 3:
                if self.player1_turn:
                    print("Player 1 wins")
                else:
                    print("Player 2 wins")
                self.winner = True
                return True
        if np.abs(self.board[0][0] + self.board[1][1] + self.board[2][2]) == 3:
            if self.player1_turn:
                print("Player 1 wins")
            else:
                print("Player 2 wins")
            self.winner = True
            return True
        elif np.abs(self.board[0][2] + self.board[1][1] + self.board[2][0]) == 3:
            if self.player1_turn:
                print("Player 1 wins")
            else:
                print("Player 2 wins")
            self.winner = True
            return True
        else:
            return False

    def _is_finished(self) -> bool:
        if 0 in self.board.reshape(-1) and not self.winner:
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

    while not game._is_finished():
        truc = game._get_possibilities()[np.random.choice(range(len(game._get_possibilities())))]

        print(truc)
        game.play_turn(truc[0], truc[1])

