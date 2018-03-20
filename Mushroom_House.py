#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:08:46 2018

@author: godinechan
"""
from Game import Game

def main():
    mygame = Game()
    mygame.init_game()
    while (mygame.bowser_count < mygame.dead_by_bowser
          and mygame.bowserjr_count < mygame.dead_by_bowserjr
          and not mygame.exit):
        pick = mygame.ask_for_pick()
        if not mygame.exit:
            mygame.display_pick(pick)
            mygame.change_current_player()
            mygame.update_gamestate_and_rewards(pick)
            mygame.print_board()
            mygame.print_current_count()
    mygame.print_results()
    
if __name__ == '__main__':
    main()