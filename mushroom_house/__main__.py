"""
Description: Main program for the Mushroom House minigame
@author: godinechan
"""
from game import Game

def main():
    """
    Description: Main program in running the Mushroom House minigame
    """
    mygame = Game()          #Create game
    mygame.init_game()       #Initialize game
    #Continue the game until reaching conditions to end game or exiting
    mygame.playgame()
    mygame.print_results()   #print results at the end
    
if __name__ == '__main__':
    main()