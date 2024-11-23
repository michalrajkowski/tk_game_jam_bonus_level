# (E) Player card system?
# - cards / actions on hand
# - hover on card to select it (it will slide up? (showing description?))
# - card has description what they do?
# - cards with targets or no targets?
# - for now basic actions (maybe they upgrade?)
import pyxel

(CARD_W, CARD_H) = (60, 90)
MIN_W = 10
HIDDEN_H = 40
CARD_SHOW_TIME = 0.3
class CardManager():
    def __init__(self):
        self.cards_in_hand : list[Card] = []
        self.card_show_timers :  list[float] = []
        self.hovered_card_index : int = None
        self.selected_card : Card = None
        self.SCREEN_W = None
        self.SCREEN_H = None
        self.load_example_hand(10)
    
    def load_example_hand(self, number):
        for i in range(number):
            card : Card = DefaultCard()
            self.cards_in_hand.append(card)
            self.card_show_timers.append(0.0)
    # Draw cards in hand.
    # draws them from middle
    def draw_cards(self):
        total_cards = len(self.cards_in_hand)
        if total_cards == 0:
            return
        
        # Calculate the total width required for the cards without overlap
        total_cards_width = total_cards * CARD_W

        # Calculate how much space is available for spreading cards horizontally
        available_space = self.SCREEN_W - total_cards_width

        # If there's not enough space, calculate the overlap (cards should never shrink below MIN_W width)
        if available_space < 0:
            overlap = min(-available_space, (total_cards - 1) * (CARD_W - MIN_W))
            card_spacing = -overlap // (total_cards - 1) if total_cards > 1 else 0
        else:
            # If there's enough space, spread them out
            card_spacing = available_space // (total_cards - 1) if total_cards > 1 else 0
        
        # Calculate the starting x position to center the cards
        start_draw_x = (self.SCREEN_W - (total_cards * CARD_W + (total_cards - 1) * card_spacing)) // 2
        
        # Draw each card
        (special_x, special_y, special_index) = (0,0,-1)
        for i, card in enumerate(self.cards_in_hand):
            timer = self.card_show_timers[i] if i < len(self.card_show_timers) else 0
            lerp_percent = timer / CARD_SHOW_TIME  # Normalize the timer to a 0-1 range
            start_draw_y = self.SCREEN_H - (CARD_H)*(lerp_percent) - (HIDDEN_H)*(1.0 - 1.0*lerp_percent) 
            card_x = start_draw_x + i * (CARD_W + card_spacing)
            self.draw_one_card(card_x, start_draw_y, i)
            if (self.card_show_timers[i] == CARD_SHOW_TIME):
                (special_x, special_y, special_index) = (card_x, start_draw_y, i)
        # Draw special card for more readability:
        if special_index != -1:
            self.draw_one_card(special_x, special_y, special_index)


    def draw_one_card(self, card_x, card_y, card_index):
        pyxel.rect(card_x, card_y, CARD_W, CARD_H, 0)
        pyxel.rectb(card_x, card_y, CARD_W, CARD_H, 7)

        

        
    
    def simulate(self):
        self.hovered_card_index = None
        (mouse_x, mouse_y) = (pyxel.mouse_x, pyxel.mouse_y)
        # Find if any card is highlited?
        total_cards = len(self.cards_in_hand)
        if total_cards == 0:
            return
        
        # Calculate the total width required for the cards without overlap
        total_cards_width = total_cards * CARD_W

        # Calculate how much space is available for spreading cards horizontally
        available_space = self.SCREEN_W - total_cards_width

        # If there's not enough space, calculate the overlap (cards should never shrink below MIN_W width)
        if available_space < 0:
            overlap = min(-available_space, (total_cards - 1) * (CARD_W - MIN_W))
            card_spacing = -overlap // (total_cards - 1) if total_cards > 1 else 0
        else:
            # If there's enough space, spread them out
            card_spacing = available_space // (total_cards - 1) if total_cards > 1 else 0
        
        # Calculate the starting x position to center the cards
        start_draw_x = (self.SCREEN_W - (total_cards * CARD_W + (total_cards - 1) * card_spacing)) // 2
        start_draw_y = self.SCREEN_H - HIDDEN_H
        
        for i, card in enumerate(self.cards_in_hand):
            card_y = start_draw_y
            if self.card_show_timers[i] == CARD_SHOW_TIME:
                card_y = self.SCREEN_H - CARD_H
            card_x = start_draw_x + i * (CARD_W + card_spacing)
            if card_x <= mouse_x <= card_x + CARD_W and card_y <= mouse_y:
                    self.hovered_card_index = i  # Mouse is within this card's area

        # decrese card show timers
        for i in range(len(self.card_show_timers)):
            self.card_show_timers[i] -= 1/30
            if self.card_show_timers[i] <= 0.0:
                self.card_show_timers[i] = 0.0
        
        if self.hovered_card_index != None:
            self.card_show_timers[self.hovered_card_index] = CARD_SHOW_TIME

class Card():
    def __init__(self, name : str = ""):
        self.name : str = name 
        pass

class DefaultCard(Card):
    def __init__(self):
        super().__init__()
        self.name = "Default Card"
        
class SkipCard(Card):
    def __init__(self):
        super().__init__()
        self.name = "Skip Turn"
    