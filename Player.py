"""
Author: Ryan Kildea
Date created: 02/14/19
Last modified: 03/09/19
"""


class Player:
    """
    Defines a player or AI character for the game.
    """

    def __init__(self, char, color, num_nodes):
        """
        :param symbol: The character symbol that represents the player's game pieces
        """
        self.color = color
        self.char = char[0]
        self.color_num = self.get_color_num()
        self.total_wins = 0
        self.num_nodes_generated = num_nodes

    def get_color_num(self):
        """
        Get the number associated with text color for console output.
        :return: Value corresponding to a given color
        """
        if self.color == "red":
            return 31
        elif self.color == "green":
            return 32
        elif self.color == "yellow":
            return 33
        else:
            return 34

    def get_symbol(self, char="@"):
        """
        Just for fun, uses don't have to use X and O.  They can use their own symbol.
        :param char: The user's chosen character
        :return: Color-encoded symbol for the game
        """
        char = self.char if char == "@" else char
        return "\033[1;{col}m{c}\033[1;m".format(col=self.color_num, c=char)

    def color_percentage(self, num):
        """
         Format/color the win percentage to allow it to stand out more.
         :param num: The estimated win percentage
         :return: Color-formatted win percentage
         """
        return "\033[1;{col}m{num:.1f}\033[1;m".format(col=self.color_num, num=num)