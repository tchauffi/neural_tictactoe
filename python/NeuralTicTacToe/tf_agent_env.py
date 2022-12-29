import numpy as np
import copy
from tf_agents.environments import PyEnvironment
from tf_agents.specs import BoundedArraySpec
from tf_agents.trajectories.time_step import StepType
from tf_agents.trajectories.time_step import TimeStep

from board.board import TicTacBoard, GameStatus
from agent.random_bot import RandomBot


class TicTacEnv(PyEnvironment):
    REWARD_WIN = np.asarray(1.0, dtype=np.float32)
    REWARD_LOSS = np.asarray(-1.0, dtype=np.float32)
    REWARD_DRAW_OR_NOT_FINAL = np.asarray(0.0, dtype=np.float32)
    # A very small number such that it does not affect the value calculation.
    REWARD_ILLEGAL_MOVE = np.asarray(-0.001, dtype=np.float32)

    def __init__(self, rng: np.random.RandomState = None, discount=1.0):
        super(TicTacEnv, self).__init__(handle_auto_reset=True)
        self.opponent = RandomBot()
        self.board = TicTacBoard()
        self.rng = rng
        self._discount = np.asarray(discount, dtype=np.float32)
        self._states = None

    def current_time_step(self):
        return self._states

    def observation_spec(self):
        """Return observation_spec."""
        return BoundedArraySpec((3, 3), np.int32, minimum=-1, maximum=1)

    def action_spec(self):
        """Return action_spec."""
        return BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=8)

    def get_state(self) -> TimeStep:
        # Returning an unmodifiable copy of the state.
        return copy.deepcopy(self._current_time_step)

    def set_state(self, time_step: TimeStep):
        self._current_time_step = time_step
        self._states = time_step.observation

    def _reset(self):
        """Return initial_time_step."""
        self.board.reset()
        self._states = self.board.compute_board()
        return TimeStep(
            StepType.FIRST,
            np.asarray(0.0, dtype=np.float32),
            self._discount,
            self._states,
        )

    def _step(self, action):
        """Apply action and return new time_step."""
        if not self.board.play_turn(action):
            return TimeStep(
                StepType.LAST, self.REWARD_ILLEGAL_MOVE, self._discount, self._states
            )
        self._states = self.board.compute_board()

        if (
            self.board.is_winning() == GameStatus.PLAYER_1_WIN
            or self.board.is_winning() == GameStatus.PLAYER_2_WIN
        ):
            return TimeStep(
                StepType.LAST, self.REWARD_WIN, self._discount, self._states
            )

        elif self.board.is_winning() == GameStatus.DRAW:
            return TimeStep(
                StepType.LAST,
                self.REWARD_DRAW_OR_NOT_FINAL,
                self._discount,
                self._states,
            )

        oppo_play = self.opponent.predict_best_turn(self.board)

        self.board.play_turn(oppo_play)

        self._states = self.board.compute_board()

        if (
            self.board.is_winning() == GameStatus.PLAYER_1_WIN
            or self.board.is_winning() == GameStatus.PLAYER_2_WIN
        ):
            return TimeStep(
                StepType.LAST, self.REWARD_LOSS, self._discount, self._states
            )

        elif self.board.is_winning() == GameStatus.DRAW:
            return TimeStep(
                StepType.LAST,
                self.REWARD_DRAW_OR_NOT_FINAL,
                self._discount,
                self._states,
            )

        else:
            return TimeStep(
                StepType.MID,
                self.REWARD_DRAW_OR_NOT_FINAL,
                self._discount,
                self._states,
            )
