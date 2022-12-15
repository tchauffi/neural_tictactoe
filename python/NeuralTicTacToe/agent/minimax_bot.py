from .robot import Robot
import numpy as np
from board.board import TicTacBoard, GameStatus
import logging

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)


class MinimaxBot(Robot):
    def predict_best_turn(self, current_board_state: TicTacBoard):
        return self.minimax(current_board_state, max_player=True)

    def minimax(
        self,
        current_board_state: TicTacBoard,
        max_player: bool,
        depth=np.inf,
        alpha=-np.inf,
        beta=np.inf,
    ):
        if current_board_state.is_winning() != GameStatus.NO_WINNER or depth == 0:
            if current_board_state.is_winning == GameStatus.DRAW:
                return 0
            elif max_player:
                return 1
            else:
                return -1

        else:
            if max_player:
                value = -np.inf
                for possibility in current_board_state.get_possibilities():
                    current_board_state.play_turn(possibility)
                    score = self.minimax(
                        current_board_state.copy(),
                        not max_player,
                        depth - 1,
                        alpha,
                        beta,
                    )
                    if score > value:
                        best = possibility
                        value = score
                        if value >= beta:
                            return best
                        alpha = max(alpha, value)
                    current_board_state.undo()
                return best
            else:
                value = +np.inf
                for possibility in current_board_state.get_possibilities():
                    current_board_state.play_turn(possibility)
                    score = self.minimax(
                        current_board_state.copy(),
                        not max_player,
                        depth - 1,
                        alpha,
                        beta,
                    )
                    if score < value:
                        best = possibility
                        value = score
                        if alpha >= value:
                            return best
                        beta = min(beta, value)
                    current_board_state.undo()
                return best
