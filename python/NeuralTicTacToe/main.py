from board.board import TicTacBoard
from agent.random_bot import RandomBot

import logging

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT)


logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# play game at random
game = TicTacBoard()
bot = RandomBot()

while not game.is_finished():
    turn = bot.predict_best_turn(game)

    logger.info(turn)
    game.play_turn(turn[0], turn[1])
