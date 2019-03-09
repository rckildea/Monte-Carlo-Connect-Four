"""
Author: Ryan Kildea
Date created: 03/09/19
Last modified: 03/09/19
"""

class MonteCarloTree:
    """
    This is an implementation of a tree.
    Stores a given move and its estimated value at each node along the way.
    """

    def __init__(self, parent, move, value):
        self.move = move # The column number where a token is being dropped
        self.children = [] # No limit to how many children the tree may have
        self.parent = parent
        self.wld_value = value # Win-loss-draw value
        self.est_win_percent = 0

    def add_child(self, move, value):
        """
        Add a child node to the current node in our tree.
        :param move: The requested column number for the current move
        :param value: Win, loss, and draw each assigned relative values for measuring success
        :return: None
        """
        node = MonteCarloTree(self, move, value)
        self.children.append(node)

    def find_best_move(self):
        """
        Iterates through every child for a given node and calculates the most optimal move
        based on the list of all possible moves and their average WLD rate.
        :return: best_move (int stating which column should be played), est_win_percent (rough estimate of
             the likelihood of winning at a given point in time)
        """
        values = [[None, None], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] # [value, num trials] # (value, num trials)
        for child in self.children:
            values[child.move][0] += child.wld_value
            values[child.move][1] += 1

        best_move = 1

        for i in range(1, 8):
             if not values[i][1] == 0:
                 current_value = values[i][0]/values[i][1]
                 if max(self.est_win_percent, current_value) == current_value:
                    self.est_win_percent = current_value
                    best_move = i

        self.est_win_percent *= 100

        return best_move, self.est_win_percent
