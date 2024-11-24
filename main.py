# title: Lich Dungeon
# author: michalrajkowski
# desc: Game jam entry for TK Game Jam 2024 : The bonus level
# site: https://github.com/michalrajkowski/tk_game_jam_bonus_level
# license: MIT
# version: 1.0

import pyxel
from enum import Enum, auto
from decision_manager import DecisionManager, HeroEnum
from hero_manager import HeroManager, HeroStats
from room_manager import RoomManager, Room, RoomElement
from card_manager import CardManager
from game_manager import State, ObjectEnum
from animation_handler import AnimationHandler, BoxAnimation


# CONSTANTS:
# Box - x, y, w, h
ROOM_ELEMENTS_ARTS = {}
WIZARD_IMAGES = []
WARIOR_IMAGE = []
ROGUE_IMAGES = []
DUNGEON_BACKGROUND = []
DEAD_PLAYER = []

HUD_ZONE_H = 50
OBJECT_ZONE_H = 80 
PLAYERS_ZONE_H = 100

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

        self.initialize_game()

        pyxel.run(self.update, self.draw)
    
    def initialize_game(self):
        print("INITIALIZE")
        self.load_hero_sprites()
        self.load_objects_sprites()
        self.current_frame = 0.0
        self.force_game_end = False
        self.game_state = State.HEROES_THINK
        self.decision_manager : DecisionManager = DecisionManager(self)
        self.card_manager : CardManager = CardManager(self)
        self.animation_handler : AnimationHandler = AnimationHandler()
        self.room_manager : RoomManager = RoomManager(self.animation_handler, self)
        self.hero_manager : HeroManager = HeroManager(self.animation_handler, PLAYER_SLOTS=HERO_SLOTS)


        self.decision_manager.hero_manager = self.hero_manager
        self.card_manager.SCREEN_W = SCREEN_W
        self.card_manager.SCREEN_H = SCREEN_H
        self.card_manager.OBJECT_SLOTS = OBJECT_SLOTS
        self.card_manager.PLAYER_SLOTS = HERO_SLOTS
        self.card_manager.OBJECT_SIZE = OBJECT_SIZE
        self.card_manager.HERO_SIZE = HERO_SIZE
        self.card_manager.hero_manager = self.hero_manager
        self.card_manager.room_manager = self.room_manager
        self.animation_handler.game_manager = self
        self.decision_manager.animation_handler = self.animation_handler
        self.decision_manager.PLAYER_SLOTS = HERO_SLOTS    
        self.hero_manager.animation_handler = self.animation_handler
        self.decision_manager.room_manager = self.room_manager
        # self.animation_handler.room_manager = self.room_manager
        self.room_manager.animation_handler = self.animation_handler

        self.game_state = State.ANIMATIONS_RESOLVING
        self.animation_handler.go_back_to_state_after_blocking = State.HEROES_THINK
    
    def end_game(self):
        self.force_game_end = True
        self.game_state = State.GAME_ENDED
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.KEY_R):
            self.initialize_game()
        if self.force_game_end == True:
            self.game_state = State.GAME_ENDED

        if self.game_state== State.GAME_ENDED:
            return
        self.current_frame += 1.0
        self.animation_handler.do_one_frame()
        self.simulate_turn() 

    def draw(self):
        pyxel.cls(0)
        # Draw animations        # Draw hud
        if self.game_state == State.GAME_ENDED:
            self.draw_end_screen()
            return
        self.draw_dev_opstions()
        self.draw_hud()
        # Draw players zone
        self.draw_players_zone()
        # draw objects zone
        self.draw_objects_zone()

        if (self.game_state == State.CARD_CHOOSING_TARGETS):
            self.card_manager.draw_arrow()
            self.card_manager.draw_ghastly_selects()

        if (self.game_state == State.PLAYERS_ACT):
            self.draw_player_cards()
        else:
            self.card_manager.draw_cards(shrinked=True)
        # Load Heroes on screen

        self.animation_handler.draw_animations()
    def draw_big_text(self, x, y, text, color, scale=3):
            # Draw small text at the bottom of the screen (hidden area)
        pyxel.text(0, pyxel.height - 10, text, color)
        
        # Iterate over the text's pixel area
        for i in range(len(text) * 6):  # 6 pixels wide per character
            for j in range(8):  # Characters are 8 pixels tall
                pixel_color = pyxel.pget(i, pyxel.height - 10 + j)  # Read pixel color
                if pixel_color == color:
                    # Draw a scaled version of the pixel
                    pyxel.rect(x + i * scale, y + j * scale, scale, scale, color)
    def draw_dev_opstions(self):
        pyxel.text(0,2,"- DEV OPTIONS -", 3)
        pyxel.text(0,9,"[Q] : Quit game", 3)
        pyxel.text(0,9+8,"[R] : Restart game", 3)
        pyxel.text(0,9+16,"[T] : Go to next room", 3)
        pyxel.text(0,9+24,"[SPACE] : Skip animation", 3)
    def draw_end_screen(self):
        alive_heroes = self.hero_manager.alive_heroes_num()
        text = ""
        if alive_heroes == 0:
            # TOTAL DEMISE
            pyxel.images[2].load(0, 0, "assets/pixelized_images/ending_3.png")
            pyxel.blt(300,300, 2, 0, 0, 300, 300, scale=3)  
            text = "Total Demise"
        elif alive_heroes == 3:
            # Epic fail:
            pyxel.images[2].load(0, 0, "assets/pixelized_images/ending_1.png")
            pyxel.blt(300,300, 2, 0, 0, 300, 300, scale=3)
            text = "Heroes Escaped"
        else:
            # Parial victory
            pyxel.images[2].load(0, 0, "assets/pixelized_images/ending_2.png")
            pyxel.blt(300,300, 2, 0, 0, 300, 300, scale=3)
            text = "Partial Demise"

        pyxel.rect(0, 0, 300, 30, 0)
        self.draw_big_text(0,0,text, 7 ,5)
        pyxel.rect(0, 290, 100, 100, 0)
        pyxel.rect(0, 260, 300, 40, 0)
        self.draw_big_text(0,260,"R to Restart", 7 ,5)

    def load_hero_sprites(self):
        # load images for each character
        pyxel.images[2].load(0, 0, "assets/pixelized_images/wizard_01.png")
        WIZARD_IMAGES.append((0,0,HERO_SIZE[0], HERO_SIZE[1]))

        pyxel.images[2].load(0, 80, "assets/pixelized_images/rogue_01.png")
        ROGUE_IMAGES.append((0,80,HERO_SIZE[0], HERO_SIZE[1]))

        pyxel.images[2].load(0, 160, "assets/pixelized_images/warrior_01.png")
        WARIOR_IMAGE.append((0,160,HERO_SIZE[0], HERO_SIZE[1]))

        pyxel.images[1].load(0, 0, "assets/pixelized_images/dng_wall.png")
        DUNGEON_BACKGROUND.append((0,0,150,20))

        pyxel.images[2].load(40, 0, "assets/pixelized_images/dead_player.png")
        DEAD_PLAYER.append((40,0,40, 60))
    def load_objects_sprites(self):
        pyxel.images[1].load(0, 180, "assets/pixelized_images/library.png")
        ROOM_ELEMENTS_ARTS[ObjectEnum.FURNITURE_1] = (0,180,60,60)

        pyxel.images[1].load(60, 180, "assets/pixelized_images/drake.png")
        ROOM_ELEMENTS_ARTS[ObjectEnum.MONSTER_1] = (60,180,60,60)

    def draw_heroes(self):
        # Draw individual heroes inside it
        #pyxel.rect(HERO_SLOTS[0][0], HERO_SLOTS[0][1], HERO_SIZE[0], HERO_SIZE[1], 5)

        # LOAD DUNGEON BACKGROUND
        dungeon_background = DUNGEON_BACKGROUND[0]
        pyxel.blt(75, HUD_ZONE_H+OBJECT_ZONE_H+PLAYERS_ZONE_H+10
                  , 1, dungeon_background[0],dungeon_background[1],dungeon_background[2],dungeon_background[3], 0, scale=2.0)

        # Simple resize anim?
        if self.hero_manager.hero_list[HeroEnum.WIZARD].is_dead == True:
            wizard_sprite = DEAD_PLAYER[0]
            pyxel.blt(HERO_SLOTS[0][0], HERO_SLOTS[0][1]+20, 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
        else:
            wizard_sprite = WIZARD_IMAGES[0]
            pyxel.blt(HERO_SLOTS[0][0], HERO_SLOTS[0][1], 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
            # pyxel.blt(HERO_SLOTS[1][0], HERO_SLOTS[1][1], 0, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3])
         # Simple resize anim?
        
        if self.hero_manager.hero_list[HeroEnum.ROGUE].is_dead == True:
            wizard_sprite = DEAD_PLAYER[0]
            pyxel.blt(HERO_SLOTS[1][0], HERO_SLOTS[1][1]+20, 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
        else:
            wizard_sprite = ROGUE_IMAGES[0]
            pyxel.blt(HERO_SLOTS[1][0], HERO_SLOTS[1][1], 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
            # pyxel.blt(HERO_SLOTS[1][0], HERO_SLOTS[1][1], 0, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3])
         # Simple resize anim?
        
        if self.hero_manager.hero_list[HeroEnum.WARRIOR].is_dead == True:
            wizard_sprite = DEAD_PLAYER[0]
            pyxel.blt(HERO_SLOTS[2][0], HERO_SLOTS[2][1]+20, 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
        else:
            wizard_sprite = WARIOR_IMAGE[0]
            pyxel.blt(HERO_SLOTS[2][0], HERO_SLOTS[2][1], 2, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3], 0)
            # pyxel.blt(HERO_SLOTS[1][0], HERO_SLOTS[1][1], 0, wizard_sprite[0],wizard_sprite[1],wizard_sprite[2],wizard_sprite[3])

        hero_manager = self.hero_manager
        # Draw hero stats:
        self.draw_hero_stats(HERO_SLOTS[0][0]+40, HERO_SLOTS[0][1]+10, hero_manager.hero_list[HeroEnum.WIZARD])
        self.draw_hero_stats(HERO_SLOTS[1][0]+40, HERO_SLOTS[1][1]+10, hero_manager.hero_list[HeroEnum.ROGUE])
        self.draw_hero_stats(HERO_SLOTS[2][0]+40, HERO_SLOTS[2][1]+10, hero_manager.hero_list[HeroEnum.WARRIOR])

        # Draw heroes decisions (later icons might be used for this as well?)
        pyxel.text(HERO_SLOTS[0][0], HERO_SLOTS[0][1] - 5, "Plan:" + hero_manager.hero_list[HeroEnum.WIZARD].decision.description_short, 13)
        pyxel.text(HERO_SLOTS[1][0], HERO_SLOTS[1][1] - 5, "Plan:" + hero_manager.hero_list[HeroEnum.ROGUE].decision.description_short, 13)
        pyxel.text(HERO_SLOTS[2][0], HERO_SLOTS[2][1] - 5, "Plan:" + hero_manager.hero_list[HeroEnum.WARRIOR].decision.description_short, 13)

    def draw_hero_stats(self, x, y, hero):
        # Draw name, and 3 atributes?
        pyxel.text(x,y,hero.name, 5)
        blood_value = 1
        fear_value = 1
        anger_value = 1
        pyxel.text(x+2,y+8,"Blood", 1)
        pyxel.rect(x+3, y+14, hero.max_stats[HeroStats.BLOOD]*3, 2, 1)
        pyxel.rect(x+3, y+14, hero.current_stats[HeroStats.BLOOD]*3, 2, 8)
        pyxel.text(x+2,y+20,"Fear", 1)
        pyxel.rect(x+3, y+26, hero.max_stats[HeroStats.FEAR]*3, 2, 1)
        pyxel.rect(x+3, y+26, hero.current_stats[HeroStats.FEAR]*3, 2, 2)
        pyxel.text(x+2,y+32,"Anger", 1)
        pyxel.rect(x+3, y+38, hero.max_stats[HeroStats.ANGER]*3 , 2, 1)
        pyxel.rect(x+3, y+38, hero.current_stats[HeroStats.ANGER]*3 , 2, 9)


    def draw_hud(self):
        # DRAW HUD BOX
        pyxel.rectb(0,0,SCREEN_W, HUD_ZONE_H, 1)
        # DRAW ROOMS STUFF
        self.draw_rooms_left()
    # Draw players zone
        # draw objects zone
    def draw_players_zone(self):
        # pyxel.rectb(0,HUD_ZONE_H,SCREEN_W, OBJECT_ZONE_H, 2)
        self.draw_heroes()

    def draw_objects_zone(self):
        # pyxel.rectb(0,HUD_ZONE_H+OBJECT_ZONE_H,SCREEN_W, PLAYERS_ZONE_H, 3)
        self.draw_objects()

    def draw_objects(self):
        # Draw individual heroes inside it
        for i in range(3):
            room_element : RoomElement = self.room_manager.rooms_list[self.room_manager.current_room_index].room_elements[i]
            if room_element == None:
                continue
            # Draw proper room element texture?
            (u,v,w,h) = ROOM_ELEMENTS_ARTS[room_element.enum]
            pyxel.blt(OBJECT_SLOTS[i][0], OBJECT_SLOTS[i][1],1,u,v,w,h,0)
            #pyxel.rect(OBJECT_SLOTS[i][0], OBJECT_SLOTS[i][1], OBJECT_SIZE[0], OBJECT_SIZE[1], 5)

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
        if (self.game_state == State.ANIMATIONS_RESOLVING):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.animation_handler.skip_current()


        if (self.animation_handler.has_block_anims() and self.game_state != State.ANIMATIONS_RESOLVING):
            self.animation_handler.go_back_to_state_after_blocking = self.game_state
            self.game_state = State.ANIMATIONS_RESOLVING
            return

        if (self.game_state == State.HEROES_THINK):
            self.decision_manager.make_decisions()
            self.game_state = State.PLAYERS_ACT
            self.animation_handler.go_back_to_state_after_blocking = self.game_state
            self.game_state = State.ANIMATIONS_RESOLVING
            self.card_manager.first_tick = True
            return

        if (self.game_state == State.PLAYERS_ACT):
            self.card_manager.simulate()    
            return
        
        if (self.game_state == State.CARD_CHOOSING_TARGETS):
            # Choose target for our card
            # Draw choice target arrow
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                valid_target, index = self.card_manager.is_valid_target()
                if valid_target:
                    # Set target for card
                    # move to play phase
                    self.card_manager.select_card_target(index)
                    self.game_state = State.CARD_PLAYED
                else:
                # If mouse released on non valid target:
                # - unselect card
                # - go back to card selection
                    self.card_manager.unselect_card(self.card_manager.selected_card)
                    self.game_state = State.PLAYERS_ACT
                    return
            return
        
        if (self.game_state == State.CARD_PLAYED):
            # resolve card effect
            # Wait for animations et
            self.card_manager.resolve_card()
            self.game_state = State.ANIMATIONS_RESOLVING
            self.animation_handler.go_back_to_state_after_blocking = State.RESOLVING_HERO_ACTIONS
            return
        
        if (self.game_state == State.RESOLVING_HERO_ACTIONS):
            self.room_manager.current_turn+=1
            self.animation_handler.go_back_to_state_after_blocking = State.HEROES_THINK
            self.game_state = State.ANIMATIONS_RESOLVING
            self.hero_manager.resolve_decisions()

        # Heroes decide what to do

        # (Skipable animations?)

        # Player can do sth

        # Resolving action?

        # Skipable animation?

App()