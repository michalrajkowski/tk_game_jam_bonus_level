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

# CONSTANTS:
# Box - x, y, w, h
SCREEN_W, SCREEN_H = (300, 300)
HERO_BOX = (0, 200, SCREEN_W, 50)

HERO_SIZE = (20, 40)
HERO_SLOTS = []
for i in range(3):
    HERO_ONE_BOX = (i*int(HERO_BOX[2]/3) + int(HERO_BOX[2]/12), HERO_BOX[1])
    HERO_SLOTS.append(HERO_ONE_BOX)

class State(Enum):
    HEROES_THINK = auto()
    PLAYERS_ACT = auto()
    ANIMATIONS_RESOLVING = auto()

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Lich Game")
        pyxel.mouse(True)
        pyxel.load("assets/assets.pyxres")

        self.game_state = State.HEROES_THINK
        self.decision_manager : DecisionManager = DecisionManager()
        self.hero_manager : HeroManager = HeroManager()
        self.room_manager : RoomManager = RoomManager()
        self.card_manager : CardManager = CardManager()

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
        
        self.draw_heroes()
        self.draw_rooms_left()
        self.draw_player_cards()
        # Load Heroes on screen

    def draw_heroes(self):
        
        # Hero box?
        pyxel.rectb(HERO_BOX[0], HERO_BOX[1], HERO_BOX[2], HERO_BOX[3], 7)
        
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
        self.card_manager.simulate()
        # Enum turn step?
        # Additional thing for anims?
        if (self.game_state == State.HEROES_THINK):
            self.decision_manager.make_decisions()
            self.game_state = State.PLAYERS_ACT
            return
        # Heroes decide what to do

        # (Skipable animations?)

        # Player can do sth

        # Resolving action?

        # Skipable animation?

App()