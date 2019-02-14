'''
Author: Ryan Kildea
Date created: 02/14/19
Last modified: 02/14/19
'''

class Player:
    '''
    Defines a player or AI character for the game.
    '''
    def __init__(self, symbol):
        '''
        :param symbol: The character symbol that represents the player's game pieces
        '''
        self.symbol = symbol
        self.total_wins = 0