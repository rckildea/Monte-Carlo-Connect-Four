"""
Author: Ryan Kildea
Date created: 02/14/19
Last modified: 03/09/19
"""

class GameBoard:
    """
    Defines a standard Connect Four board with nxm columns and rows.
    Allows for pieces to be placed and checks the current state of the board to see
    if a winner has been found.
    """
    def __init__(self):

        # The actual columns and rows to be displayed and played with
        self.num_playable_columns = 7
        self.num_playable_rows = 6

        self.array_offset = 2  # Very ugly -> necessary for indexing errors when checking to see if someone won

        self.playable_column_range = (2, 9)
        self.playable_row_range = (2, 8)

        # The actual amount of columns and rows used by the program
        self.total_columns = self.num_playable_columns + 2 * self.array_offset
        self.total_rows = self.num_playable_rows + 2 * self.array_offset

        self.board_empty = True
        self.board_full = False
        self.game_over = False
        self.turns = 0  # Once turns = 42, game over

        self.board = []  # 2D array that represents the current board state
        for i in range(self.total_rows):  # board[rows][cols]
            self.board.append([" "] * self.total_columns)

    def print_board(self):
        """
        Prints out an easy-to-read display of the current game board.
        :return: None
        """
        print(" 1   2   3   4   5   6   7")
        for row in range(self.playable_row_range[0], self.playable_row_range[1]):
            for col in range(self.playable_column_range[0], self.playable_column_range[1]):
                print("[{piece}]".format(piece=self.board[row][col]), end=" ")
            print('\n', end="")
        print("\n")

    def get_inverse_board(self, symbol1, symbol2):
        """
        When tracking visited states, a state with one arragement of Xs and Os is exactly the same as
        that same arrangement where the Os and Xs are swapped.  This function is to account for that.
        :param symbol1: Player 1's game piece character
        :param symbol2: Player 2's game piece character
        :return: Inverted copy of the board
        """
        new_board = GameBoard()
        for row in range(self.playable_row_range[0], self.playable_row_range[1]):
            for col in range(self.playable_column_range[0], self.playable_column_range[1]):
                if not self.board[row][col] == " ":
                    new_board.board[row][col] = symbol1 if self.board[row][col] == symbol2 else symbol2
        return new_board.board


    def place(self, symbol, col):
        """
        Places a game piece onto the board, or finds that the requested column is already full.
        :param symbol: The player's game piece character
        :param col: The requested column the AI wants to drop their piece into
        :return: Boolean stating whether the move was legal (True) or the column was full (False)
        """
        col += self.array_offset - 1
        self.board_empty = False

        for row in range(self.playable_row_range[1] - 1, self.playable_row_range[0] - 1, -1):
            if self.board[row][col] == " ":
                self.board[row][col] = symbol
                self.turns += 1
                self.check_game_over(row, col)
                return True
        return False

    def check_game_over(self, row, col):

        """
        Checks to see if the game is over.  This occurs if a player has four pieces in a row, or if the board is full.
        :param row: The row number of the most recently played game piece
        :param col: The column number of the most recently played game piece
        :return: None
        """
        player_symbol = self.board[row][col]

        # Top Right: Row -1 Col 1
        # Bottom Left: Row 1 Col -1
        self.check_four_in_a_row(player_symbol, row, col, -1, 1, 1, -1)

        # Top Left: Row -1 Col -1
        # Bottom Right Row 1 Col 1
        self.check_four_in_a_row(player_symbol, row, col, -1, -1, 1, 1)

        # Horizontal: Row 0 Col 1, Row 0 Col -1
        self.check_four_in_a_row(player_symbol, row, col, 0, 1, 0, -1)

        # Vertical: Row 1 Col 0, Row -1 Col 0
        self.check_four_in_a_row(player_symbol, row, col, 1, 0, -1, 0)

        if self.turns >= self.num_playable_rows * self.num_playable_columns:
            self.game_over = True
            self.board_full = True

    def check_four_in_a_row(self, player_symbol, row, col, step_row_1, step_col_1, step_row_2, step_col_2):
        """
        Checks to see if there are four matching pieces in a row, either vertically, horizontally, or diagonally.
        If a chain of four is found, sets the game state to finished.
        :param player_symbol: The player's game piece (X or O)
        :param row: The row number of the most recently played game piece
        :param col: The column number of the most recently played game piece
        :param step_row_1: The amount to move first in the Y direction
        :param step_col_1: The amount to move first in the X direction
        :param step_row_2: The amount to move second in the Y direction
        :param step_col_2: The amount to move second in the X direction
        :return: None
        """
        num_connected = 1 # Tally of how many game pieces were found matching thus far

        def increment_connected(step_row, step_col):
            """
            Checks to see if the game is over.  This occurs if a player has four pieces in a row, or if the board is full.
            :param step_row: The amount to move in the Y direction
            :param step_col: The amount to move in the X direction
            :return: The number of adjacent matching tiles found by the function
            """
            connected = 0
            current_row = row + step_row
            current_col = col + step_col

            while self.board[current_row][current_col] == player_symbol:
                connected += 1
                current_row += step_row
                current_col += step_col

            return connected

        num_connected += increment_connected(step_row_1, step_col_1)
        num_connected += increment_connected(step_row_2, step_col_2)

        if num_connected >= 4:
            self.game_over = True
