from .robot import Robot
import numpy as np
from board.board import TicTacBoard
from typing import Tuple, Optional


class RandomBot(Robot):

    def __init__(self, seed: Optional[int] = None):
        self.random_seed = seed

    def predict_best_turn(self, current_board_state: TicTacBoard) -> Tuple:
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        return current_board_state.get_possibilities()[
            np.random.choice(range(len(current_board_state.get_possibilities())))
        ]




