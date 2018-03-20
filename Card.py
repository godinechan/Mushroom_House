"""
@author: godinechan
"""
class Card:
    """
    Description: The Card class stores attributes such as the word on the card and its status as flipped/not flipped.
    """
    def __init__(self, word):
        """
        Description: Constructor for the card which define the contents(word) and flip status
        Input:
            word, (string) : the content on the face of the card
        """
        self.word = word   #words are taken as strings for the card
        self.flip = False  #the cards are defaulted to be not flipped