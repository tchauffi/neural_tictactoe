from .robot import Robot
import numpy as np


class MinimaxBot(Robot):

    def __init__(self):
        self.depth: int = np.inf

    def predict_best_turn(self, current_board_state):
        raise NotImplementedError()
