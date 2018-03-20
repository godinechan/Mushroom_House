"""
Description: Main program for the Mushroom House minigame
@author: godinechan
"""
from Game import Game

def main():
    """
    Description: Main program in running the Mushroom House minigame
    """
    mygame = Game()    #Create game
    mygame.init_game() #Initialize game
    #Continue the game until reaching conditions to end game or exiting
    while (    mygame.bowser_count   < mygame.PAIR
           and mygame.bowserjr_count < mygame.PAIR
           and not mygame.exit):
        pick = mygame.ask_for_pick()       #ask player to pick a card
        if not mygame.exit:
            mygame.display_pick(pick)      #display the pick and the result
            mygame.update_gamestate_and_rewards(pick) #perform updates in game
            mygame.print_board()           #print game board on terminal
            mygame.print_current_count()   #print current card counts
            mygame.change_current_player() #switch players
    mygame.print_results()                 #print results at the end
    
if __name__ == '__main__':
    main()