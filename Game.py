#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:13:36 2018

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
    
    Input(integer):
    """
    def __init__(self):
        self.board = Board(3, 6)
        self.flame_count = 0
        self.ice_count = 0
        self.flight_count = 0
        self.powerup_count = 0
        self.bowser_count = 0
        self.bowserjr_count = 0
        self.exit = False
        self.card_position = {}
        self.R_TO_P_RATIO = 3.5
        self.SPECIALS_RATIO = 2/7
        self.POWERUP_RATIO = 1/7
        self.BOWSERS_RATIO = 0.5
        self.int_to_ascii_dict = {i: ascii_uppercase[i] for i in range(self.board.width)}
        self.ascii_to_int_dict = {v: k for k, v in self.int_to_ascii_dict.items()}
        
    def init_game(self):
        self.init_gamestate()
        self.place_deck(self.shuffle_deck(self.create_deck()),self.board)
        self.players = [Player(), Player()]
        self.ask_for_name()
        self.generate_pos()
        self.print_board()
    
    def ask_for_name(self):
        self.players[0].name = input('Please input name for Player 1 (Default is Mario): ') or 'Mario'
        self.players[0].turn = True
        self.players[1].name = input('Please input name for Player 2 (Default is Luigi): ') or 'Luigi'
        
    def init_gamestate(self):
        self.gamestate = {}
        for key in self.board.slots.keys():
            self.gamestate[key] = Card(None).flip
    
    def create_deck(self):
        """
        Input:
            size(integer): size of deck
            r_to_p_ratio(float): reward to penalty ratio in the deck
        Output:
            deck(list): a list consisting the contents of each card in the deck
        """
        self.num_penalty = int(self.board.size / (self.R_TO_P_RATIO + 1))
        self.num_rewards = self.board.size - self.num_penalty
        rewards = Counter({'flame'   : round(self.num_rewards * self.SPECIALS_RATIO),
                           'ice'     : round(self.num_rewards * self.SPECIALS_RATIO),
                           'flight'  : round(self.num_rewards * self.SPECIALS_RATIO),
                           'powerup' : round(self.num_rewards * self.POWERUP_RATIO)})
        penalties = Counter({'bowser'  : round(self.num_penalty * self.BOWSERS_RATIO),
                             'bowserjr': round(self.num_penalty * self.BOWSERS_RATIO)})
        all_items = rewards + penalties
        self.dead_by_bowser = penalties['bowser']
        self.dead_by_bowserjr = penalties['bowserjr']
        deck = []
        for key, value in all_items.items():
            for i in range(value):
                deck.append(Card(str(key)))
        return deck
    
    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck
    
    def place_deck(self, deck, board):
        keys = list(board.slots.keys())
        for count, key in enumerate(keys):
            self.card_position[key] = deck[count]
    
    def update_gamestate_and_rewards(self, pos):
        self.gamestate[pos] = True
        self.update_rewards(self.card_position[pos].word)
        self.update_bowsers(self.card_position[pos].word)
    
    def print_board(self):
        divider = '  +========+========+========+========+========+========+'
        printable_board = []
        printable_board.append('      A        B        C        D        E        F     ')
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
        for p in self.players:
            if p.turn:
                return p
            
    def change_current_player(self):
        for p in self.players:
            if p.turn:
                p.turn = False
            else:
                p.turn = True
    
    def ascii_to_int(self, upper_ascii):
        return self.ascii_to_int_dict[upper_ascii]
    
    def int_to_ascii(self, input_int):
        return self.int_to_ascii_dict[input_int]
    
    def generate_pos(self):
        self.pos_dict={}
        for i in range(self.board.height):
            for j in range(self.board.width):
                self.pos_dict[self.int_to_ascii(j) + str(i)] = (i, j)
        self.inv_pos_dict = {v: k for k, v in self.pos_dict.items()}
        
    def ask_for_pick(self):
        print('{}, Please pick a card!'.format(self.find_current_player().name))
        while True:
            if self.exit:
                break
            while True:
                player_input = input("Please pick a card (From {} to {}): ".format( \
                           list(self.pos_dict.keys())[0], list(self.pos_dict.keys())[self.board.size-1]))
                if player_input == "exit":
                    self.exit = True
                    break
                elif player_input == "rules":
                    self.print_rules()
                    continue
                if player_input not in self.pos_dict.keys():
                    print("Oops! Please enter a value between {} and {}.".format( \
                           list(self.pos_dict.keys())[0], list(self.pos_dict.keys())[self.board.size-1]))
                    continue
                else:
                    break
            if not self.exit:
                x = int(player_input[1])
                y = self.ascii_to_int(player_input[0])
                if self.gamestate[(x,y)]:
                    print("Card already picked, please pick again.")
                    continue
                else:
                    return (x,y)

    def display_pick(self, pick):
        print('{} picked {}, it revealed the card [{}]' \
              .format(self.find_current_player().name, self.inv_pos_dict[pick], self.card_position[pick].word))
            
    def update_rewards(self, word):
        if word == 'flame':
            self.flame_count += 1
        elif word == 'ice':
            self.ice_count += 1
        elif word == 'flight':
            self.flight_count += 1
        elif word == 'powerup':
            self.powerup_count += 1
            
    def update_bowsers(self, word):
        if word == 'bowser':
            self.bowser_count += 1
        elif word == 'bowserjr':
            self.bowserjr_count += 1
            
#     def update_record(self, player_name, word):
#         self.player[].record.append(word)
#         self.players[0].name
#         self.players = [Player(), Player()]
        
    def print_rules(self):
        print('Game Rules')
        
    def print_current_count(self):
        print('Current card counts are:')
        print('{}x Flame  Powerup Card(s) ÷2 = {}x Flame  Powerup(s)'.format(self.flame_count, self.flame_count//2))
        print('{}x Ice    Powerup Card(s) ÷2 = {}x Ice    Powerup(s)'.format(self.ice_count, self.ice_count//2))
        print('{}x Flight Powerup Card(s) ÷2 = {}x Flight Powerup(s)'.format(self.flight_count, self.flight_count//2))
        print('{}x Normal Powerup Card(s) ÷2 = {}x Normal Powerup(s)'.format(self.powerup_count, self.powerup_count//2))
        print('{}x Bowser         Card(s)'.format(self.bowser_count))
        print('{}x Bowser Jr.     Card(s)'.format(self.bowserjr_count))
        
    def print_results(self):
        print('Game Over!')
        if self.bowser_count >=2:
            print('You were kicked out by Bowser!')
        elif self.bowserjr_count >=2:
            print('You were kicked out by Bowser Jr.!')
        elif self.exit:
            print('Goodbye! See you next time!')
        else:
            print('Amazing! You gained all the rewards!')
        print('You have gained:') # use join
        print('{}x Flame  Powerup(s)'.format(self.flame_count//2))
        print('{}x Ice    Powerup(s)'.format(self.ice_count//2))
        print('{}x Flight Powerup(s)'.format(self.flight_count//2))
        print('{}x Normal Powerup(s)'.format(self.powerup_count//2))