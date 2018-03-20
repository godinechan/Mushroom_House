"""
@author: godinechan
"""
class Player:
    """
    Description: The Player class stores attributes such as the name of the player, the player number and
                 record the card selections of the players throughout the game.
    """
    def __init__(self):
        self.name = None      #Player name
        self.player_num = 0   #Player number
        self.record = []      #Record of the player's card selection