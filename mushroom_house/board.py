"""
This file consists of the Board class, in which stores the attributes of the
board as well as all functions related to the board.
@author: godinechan
"""
from string import ascii_uppercase

class Board:
    """
    Description: The Board class stores attributes such as the height, width, 
                 size and slots of the board.
    """
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.size = self.height * self.width
        self.slots = {(i, j): None for i in range(height) for j in range(width)}
        self.card_position = {}
        self.int_to_ascii_dict = \
                       {i: ascii_uppercase[i] for i in range(self.width)}
                       
    def generate_pos(self):
        """
        Description: Generate a dictionary that maps position on the board
                     to a grid, and vise versa.
        """
        self.pos_dict={}
        for i in range(self.height):
            for j in range(self.width):
                self.pos_dict[self.int_to_ascii_dict[j] + str(i)] = (i, j)
        self.inv_pos_dict = {v: k for k, v in self.pos_dict.items()}
        
    def place_deck(self, deck, board):
        """
        Description: Place deck on the board by building a dictionary as
                     an attribute of the game with position on the board as
                     keys and the cards as the values.
        Input:
            deck, (list) : a deck with contents defined on each card
            board, (Broad) : the game board
        """
        for count, key in enumerate(self.slots):
            self.card_position[key] = deck[count]
            
    def print_board(self, gamestate):
        """
        Description: Print game board with ascii charaters to terminal.
        """
        indent = '  '
        divider = indent + '+'
        column_index = indent
        for i in range(self.width):
            divider += '========+'
            column_index += '    ' + ascii_uppercase[i] + '    '
        printable_board = []
        printable_board.append(column_index)
        printable_board.append(divider)
        for i in range(self.height):
            row = str(i) + ' |'
            for j in range(self.width):
                if gamestate[(i,j)]:
                    display = self.card_position[(i,j)].word
                else:
                    display = 'pick me!'
                row = row + display.ljust(8) + '|'
            printable_board.append(row)
            printable_board.append(divider)
        for m in range(len(printable_board)):
            print(printable_board[m])
        print('')