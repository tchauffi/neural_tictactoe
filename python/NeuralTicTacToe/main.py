from board.board import TicTacBoard, GameStatus
from agent.random_bot import RandomBot
from agent.minimax_bot import MinimaxBot

import logging

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT)


logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
win_1 = 0
win_2 = 0
draw = 0
iter = 100

bot1 = RandomBot()
bot2 = MinimaxBot()
game = TicTacBoard()

for _ in range(iter):
    logger.info(f"turn {_}")
    # play game at random

    while not game.is_finished():
        if game.is_player1_turn():
            # player 1
            turn = bot1.predict_best_turn(game)
            logger.info(turn)
            game.play_turn(turn)
        else:
            # player 2
            turn = bot2.predict_best_turn(game)
            logger.info(turn)
            game.play_turn(turn)
        logger.info(game.draw_current_board_as_ascii())

    if game.is_winning() == GameStatus.PLAYER_1_WIN:
        logger.info("Player 1 win")
        win_1 += 1
    elif game.is_winning() == GameStatus.PLAYER_2_WIN:
        logger.info("Player 2 win")
        win_2 += 1
    elif game.is_winning() == GameStatus.DRAW:
        logger.info("Draw")
        draw += 1

    game.reset()

logger.info(f"{win_1 / iter}, {win_2 / iter}, {draw / iter}")
