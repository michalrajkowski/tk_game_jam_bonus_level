# (E) Player card system?
# - cards / actions on hand
# - hover on card to select it (it will slide up? (showing description?))
# - card has description what they do?
# - cards with targets or no targets?
# - for now basic actions (maybe they upgrade?)
import pyxel
import random
from decisions import HeroEnum, get_state
from game_manager import State
LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus eget ex ac purus scelerisque suscipit ac ut turpis. Quisque ut massa posuere, ultrices nunc quis, sagittis tortor. Cras ac leo enim. Pellentesque ut viverra augue, et maximus orci. Ut non mollis elit. Donec sed feugiat ligula, ut rhoncus turpis. Nulla elementum a dui accumsan vulputate. Praesent sem lacus, dignissim id eros vitae, ultricies volutpat quam. Etiam non vehicula ex. "
(CARD_W, CARD_H) = (60, 90)
MIN_W = 10
HIDDEN_H = 40
CARD_SHOW_TIME = 0.3
GRABBED_PLAY_H = 30
SHRINKED = 20

class CardManager():
    def __init__(self, game_manager):
        self.cards_in_hand : list[Card] = []
        self.card_show_timers :  list[float] = []
        self.hovered_card_index : int = None
        self.selected_card : Card = None
        self.grabbed_card : Card = None

        
        self.SCREEN_W = None
        self.SCREEN_H = None
        self.OBJECT_SLOTS = None
        self.PLAYER_SLOTS = None
        self.OBJECT_SIZE = None
        self.HERO_SIZE = None

        self.game_manager = game_manager
        self.hero_manager = None
        self.room_manager = None
        self.load_example_hand(3)
    
    def load_example_hand(self, number):
        for i in range(number):
            if (random.random() > 0.5):
                card : Card = NecroBoltCard()
            else:
                card : Card = NecroBoltCard()

            card.game_manager = self.game_manager
            card.card_manager = self
            self.cards_in_hand.append(card)
            self.card_show_timers.append(0.0)
    # Draw cards in hand.
    # draws them from middle
    def draw_ghastly_selects(self):
        animation_state = (int(self.game_manager.current_frame)%40)/2 - 10
        # Draws indicators around valid targets
        if self.selected_card.can_target_players:
            # Draw indicator around each player
            for i in range(len(self.PLAYER_SLOTS)):
                # Draw highlight around player:
                slot = self.PLAYER_SLOTS[i]
                pyxel.rectb(slot[0] - animation_state, slot[1]- animation_state, self.HERO_SIZE[0]+animation_state*2, self.HERO_SIZE[1]+animation_state*2, 7)
        if self.selected_card.can_target_objects:
            # Daw indicator around each object
            for i in range(len(self.OBJECT_SLOTS)):
                # Draw highlight around player:
                slot = self.OBJECT_SLOTS[i]
                pyxel.rectb(slot[0] - animation_state, slot[1]- animation_state, self.OBJECT_SIZE[0]+animation_state*2, self.OBJECT_SIZE[1]+animation_state*2, 7)
    def resolve_card(self):
        # Resolve card effect:
        self.selected_card.resolve_card()
    
    def select_card_target(self, index):
        if self.selected_card.can_target_players:
            self.selected_card.card_target_player = self.hero_manager.hero_list[get_state(index)]
            print("Assigned target")
            print(self.selected_card.card_target_player)
        if self.selected_card.can_target_objects:
            self.selected_card.card_target_object = self.room_manager.current_room.room_elements[index]
            print("Assigned target")
            print(self.selected_card.card_target_object)

    def is_mouse_in_space(self, x,y,space):
        if space[0]<= x <= space[0]+space[2] and space[1] <= y <= space[1] + space[3]:
            return True
        return False
    def is_valid_target(self):
        if self.selected_card.can_target_players:
            # Draw indicator around each player
            for i in range(len(self.PLAYER_SLOTS)):
                # Draw highlight around player:
                if (self.is_mouse_in_space(pyxel.mouse_x, pyxel.mouse_y, self.PLAYER_SLOTS[i])):
                    return True, i
                
        if self.selected_card.can_target_objects:
            # Daw indicator around each object
            # Draw indicator around each player
            for i in range(len(self.OBJECT_SLOTS)):
                # Draw highlight around player:
                if (self.is_mouse_in_space(pyxel.mouse_x, pyxel.mouse_y, self.OBJECT_SLOTS[i])):
                    return True, i
        return False
    def unselect_card(self, card):
        place_index = 0
        self.cards_in_hand.insert(place_index, card)
        self.card_show_timers.insert(place_index, CARD_SHOW_TIME)
        self.grabbed_card = None
        self.selected_card = None

    def draw_arrow(self):
        COLOR_OK = 11
        COLOR_NOT_OK = 8
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        color = COLOR_NOT_OK # RED
        if self.is_valid_target():
            color = COLOR_OK
        # Draw line with arrow between mouse and played card
        pyxel.line(int(self.SCREEN_W/2), self.SCREEN_H - CARD_H, mouse_x, mouse_y, color)

    def draw_cards(self, shrinked = False):
        total_cards = len(self.cards_in_hand)
        
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

        if card_spacing > 0:
            card_spacing = 2
        # Calculate the starting x position to center the cards
        start_draw_x = (self.SCREEN_W - (total_cards * CARD_W + (total_cards - 1) * card_spacing)) // 2
        
        # Draw each card
        (special_x, special_y, special_index) = (0,0,-1)
        for i, card in enumerate(self.cards_in_hand):
            if not shrinked:
                timer = self.card_show_timers[i] if i < len(self.card_show_timers) else 0
                lerp_percent = timer / CARD_SHOW_TIME  # Normalize the timer to a 0-1 range
                start_draw_y = self.SCREEN_H - (CARD_H)*(lerp_percent) - (HIDDEN_H)*(1.0 - 1.0*lerp_percent) 
                card_x = start_draw_x + i * (CARD_W + card_spacing)
                if (self.grabbed_card != None):
                    start_draw_y = self.SCREEN_H - HIDDEN_H
                self.draw_one_card(card_x, start_draw_y, self.cards_in_hand[i])
                if (self.card_show_timers[i] == CARD_SHOW_TIME):
                    (special_x, special_y, special_index) = (card_x, start_draw_y, i)
            else:
                card_x = start_draw_x + i * (CARD_W + card_spacing)
                self.draw_one_card(card_x, self.SCREEN_H - SHRINKED, self.cards_in_hand[i])
        
        # Draw special card for more readability:
        if not shrinked:
            if special_index != -1:
                self.draw_one_card(special_x, special_y, self.cards_in_hand[special_index])

            if self.grabbed_card != None:
                # Draw grabbed card:
                self.draw_one_card(pyxel.mouse_x, pyxel.mouse_y, self.grabbed_card)
                pass
        if self.selected_card != None:
            self.draw_one_card(int(self.SCREEN_W/2 - CARD_W/2), self.SCREEN_H - CARD_H, self.selected_card)


    def draw_one_card(self, card_x, card_y, card):
        card_border_color = 7
        if self.grabbed_card == card:
            card_y = max(card_y, self.SCREEN_H +  - GRABBED_PLAY_H - CARD_H)
            # Decide card border color:
            if card_y == self.SCREEN_H +  - GRABBED_PLAY_H - CARD_H:
                card_border_color = 11# GREEN
            else:
                card_border_color = 10 # YELLOW
        
        pyxel.rect(card_x, card_y, CARD_W, CARD_H, 0)
        pyxel.rectb(card_x, card_y, CARD_W, CARD_H, card_border_color)
        this_card : Card = card

        # Draw card name
        pyxel.text(card_x+2, card_y+2, this_card.name, 7)

        ART_H = 40
        # Draw card art
        pyxel.rect(card_x+1, card_y+2+7, CARD_W-2, ART_H, 4)

        # Draw card description
        pyxel.text(card_x+2, card_y+2+7+ART_H+1, this_card.description, 7)
        
    
    def simulate(self):
        self.hovered_card_index = None
        (mouse_x, mouse_y) = (pyxel.mouse_x, pyxel.mouse_y)
        # Find if any card is highlited?
        total_cards = len(self.cards_in_hand)
        
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
        
        if card_spacing > 0:
            card_spacing = 0
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
        
        if self.grabbed_card != None:
            print(mouse_y)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) == False:
                if mouse_y < self.SCREEN_H - CARD_H - GRABBED_PLAY_H:
                #play card
                    print("PLAY CARD")
                    self.selected_card = self.grabbed_card
                    self.selected_card.play_card()
                    self.grabbed_card = None
                    return
                else:
                    print("INSERT CARD")
                    place_index = self.hovered_card_index
                    if place_index == None:
                        if mouse_x < self.SCREEN_W / 2:
                            place_index = 0
                        else:
                            place_index = len(self.cards_in_hand)
                    self.cards_in_hand.insert(place_index, self.grabbed_card)
                    self.card_show_timers.insert(place_index, CARD_SHOW_TIME)
                    self.grabbed_card = None
                    return
            return
        if self.hovered_card_index == None:
            return
        
        self.card_show_timers[self.hovered_card_index] = CARD_SHOW_TIME
        # Test for card grab
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.grabbed_card = self.cards_in_hand[self.hovered_card_index]
            self.cards_in_hand.remove(self.grabbed_card)
            del self.card_show_timers[self.hovered_card_index]


class Card():
    def __init__(self, name : str = "", descript : str = LOREM):
        self.card_manager = None
        self.game_manager = None
        self.name : str = name 
        self.description = descript
        self.description = split_text_into_lines(self.description, CARD_W-4)
        
        # TARGETS
        self.choose_targets = False
        self.can_target_players = False
        self.can_target_objects = False
        self.card_target_object = None
        self.card_target_player = None

    def play_card(self):
        if self.choose_targets == True:
            self.game_manager.game_state =State.CARD_CHOOSING_TARGETS
        else:
            self.game_manager.game_state = State.CARD_PLAYED
    def resolve_card(self):
        print("Card Resolving:")
        print(self)

class DefaultCard(Card):
    def __init__(self):
        super().__init__()
        self.name = "Default Card"
        self.choose_targets = True
        self.can_target_players = True

class NecroBoltCard(Card):
    def __init__(self):
        super().__init__()
        self.name = "Necro Bolt"
        self.description = "Deal 1 Wound to a Hero."
        self.choose_targets = True
        self.can_target_players = True
        self.description = split_text_into_lines(self.description, CARD_W-4)
    
    def resolve_card(self):
        # Hero takes 1 wound
        # He speaks sth?
        self.card_target_player.get_wound()
        self.card_manager.selected_card = None
        
class SkipCard(Card):
    def __init__(self):
        super().__init__()
        self.name = "Skip Turn"
        self.description = "Skip your turn"
        self.description = split_text_into_lines(self.description, CARD_W-4)

    def resolve_card(self):
        pass
        # Hero takes 1 wound
        # He speaks sth?


def split_text_into_lines(text, card_w):
    current_line = []
    current_width = 0
    result_lines = []

    for char in text:
        # Calculate the width of the character plus a space (except for the last character on the line)
        char_width = 3
        space_width = 1 if len(current_line) > 0 else 0  # No space before the first character

        # Check if adding this character would exceed the line width
        if current_width + char_width + space_width <= card_w:
            current_line.append(char)
            current_width += char_width + space_width
        else:
            # If the current line is full, save it and start a new line
            result_lines.append(''.join(current_line))
            current_line = [char]
            current_width = char_width

    # Add the last line if there are any characters left
    if current_line:
        result_lines.append(''.join(current_line))

    # Join the lines with '\n' and return the result as a single string
    return '\n'.join(result_lines)    