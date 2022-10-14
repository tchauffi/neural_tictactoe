from board.board import TicTacBoard
from bot.random_bot import RandomBot

# play game at random
game = TicTacBoard()
bot = RandomBot()

while not game.is_finished():
    turn = bot.predict_best_turn(game)

    print(turn)
    game.play_turn(turn[0], turn[1])