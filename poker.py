# MIT License
# 
# Copyright (c) 2017 JadingTsunami
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random

NUM_RANKS = 13
NUM_SUITS = 4

class Card:

    # Suits
    HEARTS   = 1
    DIAMONDS = 2
    SPADES   = 3
    CLUBS    = 4

    SUIT_STRINGS = {HEARTS:"Hearts",DIAMONDS:"Diamonds",SPADES:"Spades",CLUBS:"Clubs"}

    # Ranks
    NO_CARD = 0

    # Special ranks, else refer to by number
    ACE = 1
    JACK = 11
    QUEEN = 12
    KING = 13

    RANK_STRINGS = {
        NO_CARD:"No Card",
        ACE:"Ace",
        2:"Two",
        3:"Three",
        4:"Four",
        5:"Five",
        6:"Six",
        7:"Seven",
        8:"Eight",
        9:"Nine",
        10:"Ten",
        JACK:"Jack",
        QUEEN:"Queen",
        KING:"King"
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def str(self):
        return str(Card.RANK_STRINGS[self.rank] + " of " + Card.SUIT_STRINGS[self.suit])
        

class Deck:
    
    CARDS_PER_DECK = 52

    def __init__(self, num_decks):
        self.cards = []

        for i in range(0,num_decks):
            for suit in range(1,NUM_SUITS+1):
                for rank in range(1,NUM_RANKS+1):
                    self.cards.append(Card(rank,suit))

    def deal_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)
        
    def shuffle(self):
        random.shuffle(self.cards)

    def print_deck(self):
        for card in self.cards:
            print card.str()



class Poker:

    NO_CARD         = 0
    HIGH_CARD       = 1
    PAIR            = 2
    TWO_PAIR        = 3
    THREE_OF_A_KIND = 4
    STRAIGHT        = 5
    FLUSH           = 6
    FULL_HOUSE      = 7
    FOUR_OF_A_KIND  = 8
    STRAIGHT_FLUSH  = 9
    ROYAL_FLUSH     = 10

    HAND_STRINGS = {
        HIGH_CARD:"High Card",
        PAIR:"Pair",
        TWO_PAIR:"Two Pair",
        THREE_OF_A_KIND:"Three of a Kind",
        STRAIGHT:"Straight",
        FLUSH:"Flush",
        FULL_HOUSE:"Full House",
        FOUR_OF_A_KIND:"Four of a Kind",
        STRAIGHT_FLUSH:"Straight Flush",
        ROYAL_FLUSH:"Royal Flush"
    }

    POKER_HAND_LENGTH = 5

    @staticmethod
    def find_high_card(cards):
        rank = Poker.get_ranks(cards)

        # ACE is special.
        if rank[Card.ACE] >= 1:
            return Card.ACE

        for i in range(len(rank)-1,1, -1):
            if rank[i] >= 1:
                return i

        return Poker.NO_CARD

    @staticmethod
    def get_ranks(cards):
        rank = [0] * 14
        for card in cards:
            rank[card.rank] += 1
        return rank
        
    @staticmethod
    def get_suits(cards):
        suit = [0] * 5
        
        for card in cards:
            suit[card.suit] += 1

        return suit

    @staticmethod
    def sort_cards(cards):
        return sorted(cards, key=lambda x: (x.suit, x.rank))

    @staticmethod
    def find_card(cards, rank, suit):
        for card in cards:
            if card.rank == rank and card.suit == suit:
             return True
        return False
        

    @staticmethod
    def find_poker_hand(cards):
        # with an array of cards, find the poker hand it contains
        # (if any)
        ranks = Poker.get_ranks(cards)
        suits = Poker.get_suits(cards)

        # detect flush
        flush = False

        for suit in suits:
            if suit >= Poker.POKER_HAND_LENGTH:
                flush = True
                break

        # detect straight
        straight = False
        largest_set = 0
        second_largest_set = 0

        run = 0
        run_high_card = Card.NO_CARD
        prevrank = -1
        has_ace = (ranks[Card.ACE] > 0)

        for i, rank in reversed(list(enumerate(ranks))):

            if rank >= 1 and not straight:
                if prevrank == -1:
                    run_high_card = i
                    run = 1
                    if i == Card.KING and has_ace:
                        run += 1
                        run_high_card = Card.ACE
                elif prevrank == i+1:
                    run += 1

                if run == Poker.POKER_HAND_LENGTH:
                    straight = True
                prevrank = i
            else:
                run = 0
                prevrank = -1

            if rank >= largest_set:
                second_largest_set = largest_set
                largest_set = rank

        # detect straight and royal flushes
        straightflush = False
        royalflush = False

        if straight and flush:
            sorted_cards = reversed(Poker.sort_cards(cards))
            current_suit = -1
            prev_rank = -1
            straightflush_length = 0

            for card in sorted_cards:
                if card.rank == (prev_rank - 1) and card.suit == current_suit:
                    straightflush_length += 1
                    prev_rank = card.rank
                    if straightflush_length == Poker.POKER_HAND_LENGTH-1 and Poker.find_card(cards, Card.ACE, current_suit) and card.rank == 10:
                        royalflush = True
                    elif straightflush_length == Poker.POKER_HAND_LENGTH:
                        straightflush = True
                        break
                else:
                    prev_rank = card.rank
                    current_suit = card.suit
                    straightflush_length = 1
                    
                    

    
        if royalflush:
            return Poker.ROYAL_FLUSH
        elif straightflush:
            return Poker.STRAIGHT_FLUSH
        elif largest_set == 4:
            return Poker.FOUR_OF_A_KIND
        elif largest_set == 3 and second_largest_set == 2:
            return Poker.FULL_HOUSE
        elif flush:
            return Poker.FLUSH
        elif straight:
            return Poker.STRAIGHT
        elif largest_set == 3:
            return Poker.THREE_OF_A_KIND
        elif largest_set == 2 and second_largest_set == 2:
            return Poker.TWO_PAIR
        elif largest_set == 2:
            return Poker.PAIR
        else:
            return Poker.HIGH_CARD


# Example Code
deck = Deck(10)
deck.shuffle()

while len(deck.cards) >= 15:
    hand = []
    for i in range(0,15):
        dealt = deck.deal_card()
        print str(dealt.str())
        hand.append(dealt)
    print "This hand is a: " + str(Poker.HAND_STRINGS[Poker.find_poker_hand(hand)])
    print "High card: " + str(Card.RANK_STRINGS[Poker.find_high_card(hand)])
    print "\n"
    
hand = []
