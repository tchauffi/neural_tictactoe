from abc import ABC, abstractmethod
from board.board import TicTacBoard


class Robot(ABC):
    @abstractmethod
    def predict_best_turn(self, current_board_state: TicTacBoard):
        pass

