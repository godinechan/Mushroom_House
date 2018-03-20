"""
This file consists of the Game class, in which stores the attributes of the
game as well as all functions required for the game.
@author: godinechan
"""
import random
from collections import Counter
from string import ascii_uppercase
from Board import Board
from Card import Card
from Player import Player

class Game:
    """
    Description: The Game class stores all attributes of the current game
                 instance, including constants, variables, as well as all
                 functions required to run the game.
    """
    def __init__(self):
        """Constructor for the game which define constants and
           initializate variables"""
        #Initialization of game objects
        self.board = Board(3, 6)
        self.card_position = {}
        self.exit = False
        #Constants
        self.R_TO_P_RATIO   = 3.5
        self.SPECIALS_RATIO = 2/7
        self.POWERUP_RATIO  = 1/7
        self.BOWSERS_RATIO  = 0.5
        self.PAIR           = 2
        #initialziation of variables
        self.current_player_num = 0
        self.flame_count        = 0
        self.ice_count          = 0
        self.flight_count       = 0
        self.powerup_count      = 0
        self.bowser_count       = 0
        self.bowserjr_count     = 0
        #reference dictionaries
        self.int_to_ascii_dict = \
                       {i: ascii_uppercase[i] for i in range(self.board.width)}
        self.ascii_to_int_dict = \
                       {v: k for k, v in self.int_to_ascii_dict.items()}
        
    def init_game(self):
        """
        Description: Game initialization function.
        """
        self.print_welcome()             #print welcome message and rules
        self.init_gamestate()            #initializate game state
        #create a deck, shuffle it and place it on the board
        self.place_deck(self.shuffle_deck(self.create_deck()),self.board)
        self.players = [Player(), Player()] #initializate 2 players
        self.ask_for_name()              #inquire players for their names
        self.generate_pos()              #map position on the board with a grid
        self.print_board()               #print game board
    
    def ask_for_name(self):
        """
        Description: Inquire names from players.
                     As a two-player game, define default players as
                     Mario and Luigi.
        """
        default = ['Mario', 'Luigi']
        for i in range(2):
            self.players[i].player_num = i + 1
            self.players[i].name = \
                 input('Please input name for Player {} (Default is {}): ' \
                          .format(self.players[i].player_num, default[i])) \
                          or default[i]
        
    def init_gamestate(self):
        """
        Description: Initializate game state as all cards being not flipped.
        """
        self.gamestate = {}
        for key in self.board.slots.keys():
            self.gamestate[key] = Card(None).flip
    
    def create_deck(self):
        """
        Description: Create a deck of the size of the board for the game.
        Output:
            deck, (list) : a list consisting the contents of each card in the
                           deck
        """
        self.num_penalty = int(self.board.size / (self.R_TO_P_RATIO + 1))
        self.num_rewards = self.board.size - self.num_penalty
        rewards   = Counter({'flame'   : round(self.num_rewards * \
                                                    self.SPECIALS_RATIO),
                             'ice'     : round(self.num_rewards * \
                                                    self.SPECIALS_RATIO),
                             'flight'  : round(self.num_rewards * \
                                                    self.SPECIALS_RATIO),
                             'powerup' : round(self.num_rewards * \
                                                    self.POWERUP_RATIO)})
        penalties = Counter({'bowser'  : round(self.num_penalty * \
                                                    self.BOWSERS_RATIO),
                             'bowserjr': round(self.num_penalty * \
                                                    self.BOWSERS_RATIO)})
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
    
    def place_deck(self, deck, board):
        """
        Description: Place deck on the board by building a dictionary as
                     an attribute of the game with position on the board as
                     keys and the cards as the values.
        Input:
            deck, (list) : a deck with contents defined on each card
            board, (Broad) : the game board
        """
        keys = list(self.board.slots.keys())
        for count, key in enumerate(keys):
            self.card_position[key] = deck[count]
    
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
        #updated accumulated rewards
        self.update_rewards(self.card_position[pos].word)
        #updated accumulated penalties
        self.update_penalties(self.card_position[pos].word)
        #updated player records
        self.update_record(self.card_position[pos].word)    
            
    def print_board(self):
        """
        Description: Print game board with ascii charaters to terminal.
        """
        indent = '  '
        divider = indent + '+'
        column_index = indent
        for i in range(self.board.width):
            divider += '========+'
            column_index += '    ' + ascii_uppercase[i] + '    '
        printable_board = []
        printable_board.append(column_index)
        printable_board.append(divider)
        for i in range(self.board.height):
            row = str(i) + ' |'
            for j in range(self.board.width):
                if self.gamestate[(i,j)]:
                    display = self.card_position[(i,j)].word
                else:
                    display = 'pick me!'
                row = row + display.ljust(8) + '|'
            printable_board.append(row)
            printable_board.append(divider)
        for m in range(len(printable_board)):
            print(printable_board[m])
    
    def find_current_player(self):
        """Helper function to locate current player with player number."""
        return self.players[self.current_player_num]
            
    def change_current_player(self):
        """Helper function to flip current player number."""
        if self.current_player_num == 0:
            self.current_player_num = 1
        elif self.current_player_num == 1:
            self.current_player_num = 0
    
    def ascii_to_int(self, upper_ascii):
        """Helper function to change ascii character (uppercase) to integer."""
        return self.ascii_to_int_dict[upper_ascii]
    
    def int_to_ascii(self, input_int):
        """Helper function to change integer to ascii character (uppercase)."""
        return self.int_to_ascii_dict[input_int]
    
    def generate_pos(self):
        """
        Description: Generate a dictionary that maps position on the board
                     to a grid, and vise versa.
        """
        self.pos_dict={}
        for i in range(self.board.height):
            for j in range(self.board.width):
                self.pos_dict[self.int_to_ascii(j) + str(i)] = (i, j)
        self.inv_pos_dict = {v: k for k, v in self.pos_dict.items()}
        
    def ask_for_pick(self):
        """
        Description: Ask players for their pick of the card on the game board.
                     Limit players to pick only cards that are not flipped
                         and within bounds on the board.
                     Takes input "exit" to quite the game.
                     Takes input "rules" to print game rules
        Output:
            (x,y), (tuple) : The position of the card that selected by player
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
                                     .format(list(self.pos_dict.keys())[0],\
                                list(self.pos_dict.keys())[self.board.size-1]))
                if player_input == "exit":
                    self.exit = True #Exit the game if "exit" was typed
                    break
                elif player_input == "rules":
                    self.print_rules() #Print game rules
                    continue
                #Ask for input again if out of bounds
                if player_input not in self.pos_dict.keys(): 
                    print("Oops! Please enter a value between {} and {}."\
                          .format(list(self.pos_dict.keys())[0], \
                                list(self.pos_dict.keys())[self.board.size-1]))
                    continue
                else:
                    break
            if not self.exit:
                x = int(player_input[1])
                y = self.ascii_to_int(player_input[0])
                #If card was already reveals, ask for input again
                if self.gamestate[(x,y)]: 
                    print("Card already picked, please pick again.")
                    continue
                else:
                    return (x,y) #return position of the selected card

    def display_pick(self, pick):
        """Helper function to print the selection and result of the player."""
        print('{} picked {}, it revealed the card [{}]' \
              .format(self.find_current_player().name, \
                      self.inv_pos_dict[pick], self.card_position[pick].word))
            
    def update_rewards(self, word):
        """
        Description: Update the count of rewards according the card revealed
        Input:
            word, (string) : The content on the selected card
        """
        if word == 'flame':
            self.flame_count += 1
        elif word == 'ice':
            self.ice_count += 1
        elif word == 'flight':
            self.flight_count += 1
        elif word == 'powerup':
            self.powerup_count += 1
            
    def update_penalties(self, word):
        """
        Description: Update the count of penalties according the card revealed
        Input:
            word, (string) : The content on the selected card
        """
        if word == 'bowser':
            self.bowser_count += 1
        elif word == 'bowserjr':
            self.bowserjr_count += 1
            
    def update_record(self, word):
        """Helper function to record the players selection in the game."""
        self.players[self.current_player_num].record.append(word)
        
    def print_welcome(self):
        """Helper function to print the welcome message of the game."""
        print('Welcome to the Mushroom House!')
        self.print_rules()
        
    def print_rules(self):
        """Helper function to print the rules of the game."""
        print('Game Rules:')
        print('Game Rules')
        print('Game Rules')
        
    def print_current_count(self):
        """Helper function to print the current accured cards in the game."""
        print('Current card counts are:')
        print('{}x Flame  Powerup Card(s) ÷2 = {}x Flame  Powerup(s)'\
              .format(self.flame_count  , self.flame_count  // self.PAIR))
        print('{}x Ice    Powerup Card(s) ÷2 = {}x Ice    Powerup(s)'\
              .format(self.ice_count    , self.ice_count    // self.PAIR))
        print('{}x Flight Powerup Card(s) ÷2 = {}x Flight Powerup(s)'\
              .format(self.flight_count , self.flight_count // self.PAIR))
        print('{}x Normal Powerup Card(s) ÷2 = {}x Normal Powerup(s)'\
              .format(self.powerup_count, self.powerup_count// self.PAIR))
        print('{}x Bowser         Card(s)'.format(self.bowser_count))
        print('{}x Bowser Jr.     Card(s)'.format(self.bowserjr_count))
        
    def print_results(self):
        """Helper function to print the results at the end of the game."""
        print('Game Over!')
        if self.bowser_count >= self.PAIR:
            print('You were kicked out by Bowser!')
        elif self.bowserjr_count >= self.PAIR:
            print('You were kicked out by Bowser Jr.!')
        elif self.exit:
            print('Goodbye! See you next time!')
        else:
            print('Amazing! You gained all the rewards!')
        print('You have gained:')
        print('{}x Flame  Powerup(s)'.format(self.flame_count   // self.PAIR))
        print('{}x Ice    Powerup(s)'.format(self.ice_count     // self.PAIR))
        print('{}x Flight Powerup(s)'.format(self.flight_count  // self.PAIR))
        print('{}x Normal Powerup(s)'.format(self.powerup_count // self.PAIR))