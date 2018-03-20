"""
@author: godinechan
"""
class Board:
    """
    Description: The Board class stores attributes such as the height, width, size and slots of the board.
    """
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.size = self.height * self.width
        self.slots = {(i, j): None for i in range(height) for j in range(width)}