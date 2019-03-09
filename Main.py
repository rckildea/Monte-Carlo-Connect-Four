import GameBoard
import Player
import random
import MonteCarloTree
import copy

"""
Author: Ryan Kildea
Date created: 02/14/19
Last modified: 03/09/19

This project implements a Monte Carlo Tree Search (MCTS) for two AI players
in a game of Connect Four.  The tree allows each player to estimate their best
move along each step of the way.

Please note that at lower values for tree search depth (num_nodes_generated) the estimated win
percentage is highly inaccurate (1-100).  At higher values (100+) it starts performing very well.
"""

p1 = Player.Player("O", "red", 1000)
p2 = Player.Player("O", "yellow", 2000)
best_move_dict = {}  # board: (move, est_win_percentage)
TARGET_NUM_GAMES = 10 # Number of games to play


def make_move(player, node, board):
    """
    Validate the AI's requested move and store it in our MCST
    :param player: The current player
    :param node: The current point in our MCST
    :param board: A GameBoard object
    :return: None
    """
    win_value = 1.0
    draw_value = 0.01
    loss_value = 0.0

    the_player = player

    current_board = copy.deepcopy(board)

    validity_check = False

    # Make first move and remember position
    if not current_board.game_over:
        while not validity_check:  # Keep trying until we find a valid move
            move_position = random.randrange(1, 8)
            validity_check = current_board.place(the_player.get_symbol(), move_position)
        validity_check = False

    # Make a random move
    # Generate random move from opponent
    # Repeat until board over
    while not current_board.game_over:
        the_player = p1 if not the_player == p1 else p2
        while not validity_check:
            validity_check = current_board.place(the_player.get_symbol(), random.randrange(1, 8))
        validity_check = False

    if current_board.board_full:
        node.add_child(move_position, draw_value)
    else:
        if the_player == player:
            node.add_child(move_position, win_value)
        else:
            node.add_child(move_position, loss_value)


def find_best_move(current_player, current_node, board):
    """
    For the given layout, find what the best move is and update the hash table of visited states.
    :param current_player: The current player
    :param current_node: The current point in our MCST
    :param board: A GameBoard object
    :return: best_move (int stating which column should be played), est_win_percent (rough estimate of
             the likelihood of winning at a given point in time)
    """
    for move in range(0, current_player.num_nodes_generated):
        make_move(current_player, current_node, board)

    best_move, est_win_percent = current_node.find_best_move()

    if not board.board_empty:
        regular_board = str(board.board)
        inverse_board = str(board.get_inverse_board(p1.get_symbol(), p2.get_symbol()))
        best_move_dict.update(
            {regular_board: (best_move, est_win_percent), inverse_board: (best_move, est_win_percent)})

    return best_move, est_win_percent


def main():
    num_games_played = 0

    while num_games_played < TARGET_NUM_GAMES:

        print("-" * 60)
        print("GAME {current} of {total}".format(current=num_games_played+1, total=TARGET_NUM_GAMES))
        print("-" * 60)

        current_player = p1 if random.randrange(1, 3) == 1 else p2
        board = GameBoard.GameBoard()
        final_tree = MonteCarloTree.MonteCarloTree(None, None, None)
        est_win_percent = 0

        while not board.game_over:

            current_player = p1 if not current_player == p1 else p2
            current_node = MonteCarloTree.MonteCarloTree(None, None, None)

            print("Player {symbol}:     ".format(symbol=current_player.get_symbol()), end='')

            # If the previous player has < 50% chance of winning, stick with known methods
            if str(board.board) in best_move_dict.keys() and best_move_dict.get(str(board.board))[1] >= 50:
                best_move, est_win_percent = best_move_dict.get(str(board.board))
                print("Best move: {move}        Est. Win Chance: {ewc}%     *PREVIOUS STATE FOUND".format(move=best_move, ewc=current_player.color_percentage(est_win_percent)))
            else:
                best_move, est_win_percent = find_best_move(current_player, current_node, board)
                print("Best move: {move}        Est. Win Chance: {ewc}%".format(move=best_move, ewc=current_player.color_percentage(est_win_percent)))

            board.place(current_player.get_symbol(), best_move)
            final_tree = MonteCarloTree.MonteCarloTree(final_tree, best_move, current_node.wld_value)

        if not board.board_full:
            current_player.total_wins += 1

        board.print_board()
        num_games_played += 1

    draws = num_games_played - p1.total_wins - p2.total_wins

    print("\n{p1} wins: {x} ({xp}%)\n{p2} wins: {o} ({op}%)\nDraws: {d} ({dp}%)".format(p1=p1.get_symbol(),
                                                                                        x=p1.total_wins,
                                                                                        xp=p1.color_percentage(p1.total_wins / num_games_played * 100),
                                                                                        p2=p2.get_symbol(),
                                                                                        o=p2.total_wins,
                                                                                        op=p2.color_percentage(p2.total_wins / num_games_played * 100),
                                                                                        d=draws,
                                                                                        dp=round(draws/num_games_played * 100, 1)))

main()
