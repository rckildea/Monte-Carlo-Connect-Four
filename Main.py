import GameBoard
import Player
import random

'''
Author: Ryan Kildea
Date created: 02/14/19
Last modified: 02/14/19

This project implements a Monte Carlo Tree Search (MCTS) for two AI players
in a game of Connect Four.  The tree allows each player to estimate their best
move along each step of the way.
'''

player_x = Player.Player("\033[1;31mX\033[1;m")
player_o = Player.Player("\033[1;34mO\033[1;m")

current_player = None

num_games_played = 0
target_num_games = 1000


# This section allows for user input, but is not required for this project.
# def get_user_input():
#     col = None
#     while col is None:
#         try:
#             col = int(input("Player {p}, please choose a column (1-7): ".format(p=current_player.symbol)))
#             if not 1 <= col <= 7:
#                 col = None
#                 raise ValueError
#         except ValueError:
#             print("Please enter a number between 1 and 7.")
#     return col


while num_games_played < target_num_games:
    board = GameBoard.GameBoard()

    while not board.game_over:
        current_player = player_x if not current_player == player_x else player_o

        validity_check = board.place(current_player.symbol, random.randrange(1, 8)) # Denotes dropping a piece into the respective column.
        while not validity_check: # The method returned false, so the column selected by the RNG is full.  Try again.
            validity_check = board.place(current_player.symbol, random.randrange(1, 8))

        # Again, code for user input that is not necessary for this assignment
        # col = get_user_input()
        # while not board.place(current_symbol, col):
        #     print("That column is full.  Please enter a different column.")
        #     col = get_user_input()

    if board.board_full:
        # The board was full, so neither AI won.
        board.board_full = False
    else:
        current_player.total_wins += 1

    num_games_played += 1

    # Reset
    board.game_over = False
    current_player = None

draws = target_num_games - player_x.total_wins - player_o.total_wins

print("X wins: {x} ({xp}%)\nO wins: {o} ({op}%)\nDraws: {d} ({dp}%)".format(x=player_x.total_wins,
                                                                            xp=round(player_x.total_wins/target_num_games * 100, 2),
                                                                            o=player_o.total_wins,
                                                                            op=round(player_o.total_wins/target_num_games * 100, 2),
                                                                            d=draws,
                                                                            dp=round(draws/target_num_games * 100, 2)))


# Extra code that can be used to show the results of each game
# board.print_board()
# if board.board_full:
#     print("Draw!")
# else:
#     print("Player " + current_player.symbol + " won!")