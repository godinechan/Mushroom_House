"""
This file consists of the Game class, in which stores the attributes of the
game as well as all functions required for the game.
@author: godinechan
"""
import random
from collections import Counter
from string import ascii_uppercase
from board import Board
from card import Card
from player import Player
import constants

class Game:
    """
    Description: The Game class stores all attributes of the current game
                 instance, including variables, as well as all functions
                 required to run the game.
    """
    def __init__(self):
        """Constructor for the game which initializes variables"""
        #Initialization of game objects
        self.board = Board(constants.BOARD_HEIGHT, constants.BOARD_WIDTH)
        self.exit = False
        #initialization of variables
        self.current_player_num = 0
        self.counts = {
            'flame': 0,
            'ice': 0,
            'flight': 0,
            'powerup': 0,
            'bowser': 0,
            'bowserjr': 0,
        }
        #reference dictionaries
        self.ascii_to_int_dict = \
                       {ascii_uppercase[i]: i for i in range(self.board.width)}
                       
    def init_game(self):
        """
        Description: Game initialization function.
        """
        self.print_welcome()             #print welcome message and rules
        self.init_gamestate()            #initialize game state
        self.board.generate_pos()        #map position on the board with a grid
        #create a deck, shuffle it and place it on the board
        self.board.place_deck(self.shuffle_deck(self.create_deck()),self.board)
        self.players = [Player(), Player()]    # initialize 2 players
        self.ask_for_name()                    #inquire players for their names
        self.board.print_board(self.gamestate) #print game board
        
    def playgame(self):
        """
        Description: Function which plays the game until it ends.
        """
        while (self.counts['bowser']   < constants.PAIR
           and self.counts['bowserjr'] < constants.PAIR
           and not self.exit):
            pick = self.ask_for_pick()       #ask player to pick a card
            if not self.exit:
                self.display_pick(pick)      #display the pick and the result
                self.update_gamestate_and_rewards(pick) #perform updates
                self.board.print_board(self.gamestate)  #print game board
                self.print_current_count()   #print current card counts
                self.change_current_player() #switch players

    def init_gamestate(self):
        """
        Description: Initialize game state with all cards being not flipped.
        """
        self.gamestate = {}
        for key in self.board.slots:
            self.gamestate[key] = Card(None).flip
    
    def create_deck(self):
        """
        Description: Create a deck of the size of the board for the game.
        Output:
            deck, (list) : a list consisting the contents of each card in the
                           deck
        """
        self.num_penalty = int(self.board.size / (constants.R_TO_P_RATIO + 1))
        self.num_rewards = self.board.size - self.num_penalty
        rewards   = Counter({'flame'   : round(self.num_rewards * \
                                                    constants.SPECIALS_RATIO),
                             'ice'     : round(self.num_rewards * \
                                                    constants.SPECIALS_RATIO),
                             'flight'  : round(self.num_rewards * \
                                                    constants.SPECIALS_RATIO),
                             'powerup' : round(self.num_rewards * \
                                                    constants.POWERUP_RATIO)})
        penalties = Counter({'bowser'  : round(self.num_penalty * \
                                                    constants.BOWSERS_RATIO),
                             'bowserjr': round(self.num_penalty * \
                                                    constants.BOWSERS_RATIO)})
        all_items = rewards + penalties
        deck = []
        for key, value in all_items.items():
            for i in range(value):
                deck.append(Card(str(key)))
        return deck
    
    def shuffle_deck(self, deck):
        """
        Description: Helper function to shuffle the deck.
        Input:
            deck, (list) : a deck with contents defined on each card
        Output:
            deck, (list) : the shuffled deck
        """
        random.shuffle(deck)
        return deck
    
    def ask_for_name(self):
        """
        Description: Inquire names from players.
                     As a two-player game, define default players as
                     Mario and Luigi.
        """
        default = ['Mario', 'Luigi']
        for i in range(constants.PAIR):
            self.players[i].player_num = i + 1
            self.players[i].name = \
                 input('Please input name for Player {} (Default is {}): ' \
                          .format(self.players[i].player_num, default[i])) \
                          or default[i]
    
    def ask_for_pick(self):
        """
        Description: Ask players for their pick of the card on the game board.
                     Limit players to pick only cards that are not flipped
                         and within bounds on the board.
                     Takes input "exit" to quite the game.
                     Takes input "rules" to print game rules
                     Takes input "board" to print game board
                     Takes input "count" to print current card count
        Output:
            (x,y), (tuple) : The position of the card selected by the player
        """
        #Tell the current player to pick a card
        print('{}, Please pick a card!'\
                                      .format(self.find_current_player().name))
        while True:
            if self.exit: #Exit the game if "exit" was typed
                break
            while True:
                #Ask for input
                player_input = input("Please pick a card (From {} to {}): "\
                              .format('A0',ascii_uppercase[self.board.width-1]\
                              + str(self.board.height-1)))
                if player_input == "exit":
                    self.exit = True #Exit the game if "exit" was typed
                    break
                elif player_input == "rules":
                    self.print_rules() #Print game rules
                    continue
                elif player_input == "board":
                    self.board.print_board(self.gamestate) #Print game board
                    continue
                elif player_input == "count":
                    self.print_current_count() #Print card count
                    continue
                player_input = player_input.upper()
                #Ask for input again if out of bounds
                if player_input not in self.board.pos_dict: 
                    print("Oops! Please enter a value between {} and {}.\n"\
                          .format('A0',ascii_uppercase[self.board.width-1]\
                          + str(self.board.height-1)))
                    continue
                else:
                    break
            if not self.exit:
                x = int(player_input[1])
                y = self.ascii_to_int_dict[player_input[0]]
                #If card was already revealed, ask for input again
                if self.gamestate[(x,y)]: 
                    print("Card already picked, please pick again.\n")
                    continue
                else:
                    return (x,y) #return position of the selected card

    def find_current_player(self):
        """Helper function to locate current player with the player number."""
        return self.players[self.current_player_num]
            
    def change_current_player(self):
        """Helper function to flip current player number."""
        if self.current_player_num == 0:
            self.current_player_num = 1
        elif self.current_player_num == 1:
            self.current_player_num = 0
    
    def display_pick(self, pick):
        """Helper function to print the selected position and the card."""
        print('{} picked {}, it revealed the card [{}]\n' \
               .format(self.find_current_player().name, \
           self.board.inv_pos_dict[pick], self.board.card_position[pick].word))
    
    def update_gamestate_and_rewards(self, pos):
        """
        Description: Taking the position selected as input, update the
                     game state as well as the rewards and penalties accrued.
                     Also record the moves of the players.
        Input:
            pos, (tuple) : position selected on the board as (m, n)
        """
        #update game state by flipping the card at the selected position
        self.gamestate[pos] = True
        #updated accumulated rewards or penalties
        self.update_count(self.board.card_position[pos].word)
        #updated player records
        self.update_record(self.board.card_position[pos].word)  
        
    def update_count(self, word):
        """
        Description: Update the count according to the card revealed
        Input:
            word, (string) : The content on the selected card
        """
        self.counts[word] += 1
        
    def update_record(self, word):
        """Helper function to record the players' selection in the game."""
        self.players[self.current_player_num].record.append(word)
        
    def print_welcome(self):
        """Helper function to print the welcome message of the game."""
        print('/////////////Welcome to the Mushroom House!\\\\\\\\\\\\\\\\\\\\\
\\\\\\\\')
        self.print_rules()
        
    def print_rules(self):
        """Helper function to print the rules of the game."""
        print('*********************************************************')
        print('* Game Rules:                                           *')
        print('* This is a team game in which two players - Mario and  *')
        print('* Luigi, take turns picking cards from the game board   *')
        print('* in order to collect powerups from the mushroom house. *')
        print('* The card will stays in the players\' collection once   *')
        print('* they are revealed. Collect a pair of powerups to earn *')
        print('* them as rewards. However, beware of Bowser and        *')
        print('* Bowser Jr.! The game ends when a pair of Bowser or    *')
        print('* Bowser Jr. cards are revealed!                        *')
        print('* - Type in the position on the grid to flip a card.    *')
        print('* - Type "board" to print the game board.               *')
        print('* - Type "count" to display current card count.         *')
        print('* - Type "exit" anytime to quit the game.               *')
        print('* - Revisit the rules anytime by typing "rules".        *')
        print('*********************************************************\n')

    def print_current_count(self):
        """Helper function to print the current accrued cards in the game."""
        print('Current card counts are:')
        print('{}x Flame  Powerup Card(s) ÷2 = {}x Flame  Powerup(s)'.format(\
              self.counts['flame']   , self.counts['flame']    // constants.PAIR))
        print('{}x Ice    Powerup Card(s) ÷2 = {}x Ice    Powerup(s)'.format(\
              self.counts['ice']     , self.counts['ice']      // constants.PAIR))
        print('{}x Flight Powerup Card(s) ÷2 = {}x Flight Powerup(s)'.format(\
              self.counts['flight']  , self.counts['flight']   // constants.PAIR))
        print('{}x Normal Powerup Card(s) ÷2 = {}x Normal Powerup(s)'.format(\
              self.counts['powerup'], self.counts['powerup'] // constants.PAIR))
        print('{}x Bowser         Card(s)'.format(self.counts['bowser']))
        print('{}x Bowser Jr.     Card(s)\n'.format(self.counts['bowserjr']))
        
    def print_results(self):
        """Helper function to print the results at the end of the game."""
        print('Game Over!')
        if self.counts['bowser'] >= constants.PAIR:
            print('You were kicked out by Bowser!')
        elif self.counts['bowserjr'] >= constants.PAIR:
            print('You were kicked out by Bowser Jr.!')
        elif self.exit:
            print('Goodbye! See you next time!')
        else:
            print('Amazing! You gained all the rewards!')
        print('You have gained:')
        print('{}x Flame  Powerup(s)'.format(self.counts['flame']   // constants.PAIR))
        print('{}x Ice    Powerup(s)'.format(self.counts['ice']     // constants.PAIR))
        print('{}x Flight Powerup(s)'.format(self.counts['flight']  // constants.PAIR))
        print('{}x Normal Powerup(s)'.format(self.counts['powerup'] // constants.PAIR))