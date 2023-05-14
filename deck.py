#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from random import shuffle
import logging
import card_dark as cb
import card as c
from card import Card
from card_dark import Card_Black
from errors import DeckEmptyError


class Deck(object):
    """ This class represents a deck of cards """

    def __init__(self):
        self.cards = list()
        self.graveyard = list()
        self.logger = logging.getLogger(__name__)

        self.logger.debug(self.cards)

    def shuffle(self):
        """Shuffles the deck"""
        self.logger.debug("Shuffling Deck")
        shuffle(self.cards)

    def draw(self):
        """Draws a card from this deck"""
        try:
            card = self.cards.pop()
            self.logger.debug("Беру 1 карту." + str(card))
            return card
        except IndexError:
            if len(self.graveyard):
                while len(self.graveyard):
                    self.cards.append(self.graveyard.pop())
                self.shuffle()
                return self.draw()
            else:
                raise DeckEmptyError()

    def dismiss(self, card):
        """Returns a card to the deck"""
        if card.special:
            card.color = None
        self.graveyard.append(card)


    def _fill_classic_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.VALUES:
                    self.cards.append(Card(color, value))
                    if not value == c.ZERO:
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in c.COLORS:
                for value in c.VALUES:
                    self.cards.append(Card(color, value))
                    if not value == c.ZERO:
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
            
    def _fill_big_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
                        if not value == c.ZERO:
                            self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in c.COLORS:
                for value in c.VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
                        if not value == c.ZERO:
                            self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()




    def _fill_big_wild_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in c.COLORS:
                for value in c.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()


    def _fill_wild_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in c.COLORS:
                for value in c.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()


    def _fill_super_wild_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.SUPER_WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in c.COLORS:
                for value in c.SUPER_WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()

    def _fill_number_(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in c.COLORS:
                for value in c.NUMBER_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()
        else:    
            self.cards.clear()
            for color in c.COLORS:
                for value in c.NUMBER_VALUES:
                    for _ in range(4):
                        self.cards.append(Card(color, value))
            for special in c.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card(None, None, special=special))
            self.shuffle()

# блек карты


    def _fill_classic_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.VALUES:
                    self.cards.append(Card_Black(color, value))
                    if not value == cb.ZERO:
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.VALUES:
                    self.cards.append(Card_Black(color, value))
                    if not value == cb.ZERO:
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        
    
    def _fill_big_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
                        if not value == c.ZERO:
                            self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
                        if not value == c.ZERO:
                            self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()

    def _fill_big_wild_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else: 
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()


    def _fill_wild_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else:
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()





    def _fill_super_wild_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.SUPER_WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else:   
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.SUPER_WILD_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(8):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()

    def _fill_number_black(self, game_color):
        if game_color == "flip":
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.NUMBER_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS_FLIP:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
        else:    
            self.cards.clear()
            for color in cb.COLORS:
                for value in cb.NUMBER_VALUES:
                    for _ in range(4):
                        self.cards.append(Card_Black(color, value))
            for special in cb.SPECIALS:
                for _ in range(4):
                    self.cards.append(Card_Black(None, None, special=special))
            self.shuffle()
