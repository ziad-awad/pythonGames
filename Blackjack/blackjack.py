# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or stand"
score = {'player':0 , 'Dealer':0}

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

def string_list_join(string_list):
    ans = ""
    for i in range(len(string_list)):
        ans += string_list[i]
        ans += ' '
    return ans

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards_obj = []

    def __str__(self):
        Massage =['Hand contains']
        for card in self.cards_obj:
            Massage.append(card.get_suit() + card.get_rank())
        return string_list_join(Massage)
          
    def add_card(self, card):
        self.cards_obj.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        have_a = False
        for card in self.cards_obj:
            r = card.get_rank()
            if r == 'A'and not have_a:
                total += 10
                have_a = True
            if r == 'K' and  have_a:
                continue                
            total += VALUES[r]
        return total
            
    def draw(self, canvas, pos):
            for card in self.cards_obj:
                card.draw(canvas , pos)
                pos[0] += 80
    
    
# define deck class 
class Deck:
    def __init__(self):
        self.Deck_cards = []
        for s in SUITS:
            for r in RANKS:
                c = Card(s,r)
                self.Deck_cards.append(c)
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.Deck_cards)

    def deal_card(self):
        # deal a card from the list
        return self.Deck_cards.pop(-1)
          
    def __str__(self):
        # return a string representing the deck
        message = ['Deck contains']
        for card in self.Deck_cards:
            message.append(card.get_suit() + card.get_rank())
        return string_list_join(message)


#define event handlers for buttons
def deal():
    global outcome, in_play , player_hand , dealer_hand , deck_copy
    # your code goes here
    if not in_play:
        player_hand = Hand()
        dealer_hand = Hand()
        deck_copy = Deck()
        deck_copy.shuffle()
        player_hand.add_card(deck_copy.deal_card())
        player_hand.add_card(deck_copy.deal_card())
        dealer_hand.add_card(deck_copy.deal_card())
        dealer_hand.add_card(deck_copy.deal_card())
        print dealer_hand
        print player_hand
    else:
        outcome = 'Player lose ! becase of re-deal'
        score['Dealer'] += 1
        
    in_play = True

def hit():
    global outcome , in_play
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck_copy.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            outcome = 'You have busted'
            print outcome

            
def stand():   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global score , outcome , in_play , dealer_hand
    if in_play == False:
        outcome = 'Dealer Win !!!'
        score['Dealer'] += 1
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck_copy.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted."
            print "Dealer is busted. Player wins."
            score['player'] += 1
            in_play = False
        else:
            if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
                print "Dealer wins"
                outcome = "Dealer wins. New deal?"
                score['Dealer'] += 1
                in_play = False
            else:
                print "Player wins. New deal?"
                outcome = "Player wins"
                score['player'] += 1
                in_play = False
  

# draw handler    
def draw(canvas):
    # player and dealer hands
    
    canvas.draw_text('Player Hand' , [50 , 390] , 20 , 'white')
    player_hand.draw(canvas ,[50 , 400] )
    canvas.draw_text('Dealer Hand' , [50 , 240] , 20 , 'white')
    dealer_hand.draw(canvas ,[50 , 250] )
    # print the name of the game and the global message
    canvas.draw_text('Blackjack' , [250 , 25] , 30 , 'white')
    canvas.draw_text(outcome , [50 , 150] , 25 , 'yellow')
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (85,298), CARD_BACK_SIZE)


    # print the score
    str_score = 'Player : '+str(score['player'])+'           Dealer : '+str(score['Dealer'])
    canvas.draw_text(str_score , [200 , 75] , 20 , 'white')

    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
