# title: Lich Dungeon
# author: michalrajkowski
# desc: Game jam entry for TK Game Jam 2024 : The bonus level
# site: https://github.com/michalrajkowski/tk_game_jam_bonus_level
# license: MIT
# version: 1.0

import pyxel
from enum import Enum, auto
from decision_manager import DecisionManager, HeroEnum
from hero_manager import HeroManager
from room_manager import RoomManager, Room
from card_manager import CardManager
from game_manager import State

# CONSTANTS:
# Box - x, y, w, h

HUD_ZONE_H = 50
OBJECT_ZONE_H = 80 
PLAYERS_ZONE_H = 110

SCREEN_W, SCREEN_H = (300, 300)
HERO_SIZE = (40, 80)
HERO_SLOTS = []
hero_start_draw_y= HUD_ZONE_H+OBJECT_ZONE_H+PLAYERS_ZONE_H - HERO_SIZE[1]
for i in range(3):
    x_draw = 25+ i*int((SCREEN_W - 50)/3) + int((SCREEN_W - 50)/12)
    hero_slot = (x_draw, hero_start_draw_y, HERO_SIZE[0], HERO_SIZE[1])
    HERO_SLOTS.append(hero_slot)

OBJECT_SIZE = (60, 60)
object_start_Draw_y = HUD_ZONE_H+OBJECT_ZONE_H - OBJECT_SIZE[1]
OBJECT_SLOTS = []
for i in range(3):
    x_draw = 8+ i*int((SCREEN_W - 30)/3) + int((SCREEN_W - 30)/12)
    object_slot = (x_draw, object_start_Draw_y, OBJECT_SIZE[0], OBJECT_SIZE[1])
    OBJECT_SLOTS.append(object_slot)

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Lich Game")
        pyxel.mouse(True)
        pyxel.load("assets/assets.pyxres")

        self.game_state = State.HEROES_THINK
        self.decision_manager : DecisionManager = DecisionManager()
        self.hero_manager : HeroManager = HeroManager()
        self.room_manager : RoomManager = RoomManager()
        self.card_manager : CardManager = CardManager(self)

        self.decision_manager.hero_manager = self.hero_manager
        self.card_manager.SCREEN_W = SCREEN_W
        self.card_manager.SCREEN_H = SCREEN_H

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.simulate_turn()
        # Simulate the turn?
        # - 

    def draw(self):
        pyxel.cls(0)
        
        # Draw hud
        self.draw_hud()
        # Draw players zone
        self.draw_players_zone()
        # draw objects zone
        self.draw_objects_zone()

        if (self.game_state == State.CARD_CHOOSING_TARGETS):
            self.card_manager.draw_arrow()

        if (self.game_state == State.PLAYERS_ACT):
            self.draw_player_cards()
        else:
            self.card_manager.draw_cards(shrinked=True)
        # Load Heroes on screen

    def draw_heroes(self):
                
        # Draw individual heroes inside it
        pyxel.rect(HERO_SLOTS[0][0], HERO_SLOTS[0][1], HERO_SIZE[0], HERO_SIZE[1], 5)
        pyxel.rect(HERO_SLOTS[1][0], HERO_SLOTS[1][1], HERO_SIZE[0], HERO_SIZE[1], 3)
        pyxel.rect(HERO_SLOTS[2][0], HERO_SLOTS[2][1], HERO_SIZE[0], HERO_SIZE[1], 8)

        # Draw heroes decisions (later icons might be used for this as well?)
        hero_manager = self.hero_manager
        pyxel.text(HERO_SLOTS[0][0], HERO_SLOTS[0][1] - 5, hero_manager.hero_list[HeroEnum.WIZARD].decision.description_short, 7)
        pyxel.text(HERO_SLOTS[1][0], HERO_SLOTS[1][1] - 5, hero_manager.hero_list[HeroEnum.ROGUE].decision.description_short, 7)
        pyxel.text(HERO_SLOTS[2][0], HERO_SLOTS[2][1] - 5, hero_manager.hero_list[HeroEnum.WARRIOR].decision.description_short, 7)
        decision_decscription = hero_manager.hero_list[HeroEnum.WIZARD].decision.description_short
        pyxel.text(0, 0, decision_decscription, 7)

    def draw_hud(self):
        # DRAW HUD BOX
        pyxel.rectb(0,0,SCREEN_W, HUD_ZONE_H, 1)
        # DRAW ROOMS STUFF
        self.draw_rooms_left()
    # Draw players zone
        # draw objects zone
    def draw_players_zone(self):
        pyxel.rectb(0,HUD_ZONE_H,SCREEN_W, OBJECT_ZONE_H, 2)
        self.draw_heroes()

    def draw_objects_zone(self):
        pyxel.rectb(0,HUD_ZONE_H+OBJECT_ZONE_H,SCREEN_W, PLAYERS_ZONE_H, 3)
        self.draw_objects()

    def draw_objects(self):
        # Draw individual heroes inside it
        pyxel.rect(OBJECT_SLOTS[0][0], OBJECT_SLOTS[0][1], OBJECT_SIZE[0], OBJECT_SIZE[1], 5)
        pyxel.rect(OBJECT_SLOTS[1][0], OBJECT_SLOTS[1][1], OBJECT_SIZE[0], OBJECT_SIZE[1], 3)
        pyxel.rect(OBJECT_SLOTS[2][0], OBJECT_SLOTS[2][1], OBJECT_SIZE[0], OBJECT_SIZE[1], 8)

    def draw_rooms_left(self):
        # Draw on top?
        number_of_rooms = self.room_manager.max_rooms
        room_w = 16
        # Calculate start draw x:
        start_x = int((SCREEN_W - number_of_rooms*(room_w +1)) / 2)
        # Actualy draw them with 1 px left between
        for i in range(number_of_rooms):
            # Draw one room:
            this_room : Room = self.room_manager.rooms_list[i]
            (u, v, w, h) = (this_room.room_icon[0], this_room.room_icon[1], this_room.room_icon[2], this_room.room_icon[3])
            pyxel.blt(start_x + i*(room_w +1), 1, 0, u, v, w, h, 0)
        # Draw mark on current room
        current_room = self.room_manager.current_room_index
        pyxel.rectb(start_x + current_room*(room_w +1)-1, 0, 18, 18, 8)

    def draw_player_cards(self):
        pyxel.rectb(0, SCREEN_H - 50, SCREEN_W, 50, 7)
        self.card_manager.draw_cards()

    def simulate_turn(self):
        # Enum turn step?
        # Additional thing for anims?
        if (self.game_state == State.HEROES_THINK):
            self.decision_manager.make_decisions()
            self.game_state = State.PLAYERS_ACT
            return

        if (self.game_state == State.PLAYERS_ACT):
            self.card_manager.simulate()    
            return
        
        if (self.game_state == State.CARD_CHOOSING_TARGETS):
            # Choose target for our card
            # Draw choice target arrow
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.card_manager.is_valid_target():
                    pass
                else:
                # If mouse released on non valid target:
                # - unselect card
                # - go back to card selection
                    self.card_manager.unselect_card(self.card_manager.selected_card)
                    self.game_state = State.PLAYERS_ACT
                    return
            print("CHOOSING TARGETS")
            return
        
        if (self.game_state == State.CARD_PLAYED):
            print("CARD PLAYED")
            return
        # Heroes decide what to do

        # (Skipable animations?)

        # Player can do sth

        # Resolving action?

        # Skipable animation?

App()