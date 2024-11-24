# holds current room
# holds max rooms
# Information about each room and their content / elements?

import random
from enum import Enum, auto
from game_manager import ObjectEnum

class RoomManager():
    def __init__(self, animation_handler, game_manager):
        self.animation_handler = animation_handler
        self.animation_handler.room_manager = self
        self.game_manager = game_manager
        self.too_late = False
        self.current_room_index = -1
        self.current_room : Room = None
        self.max_rooms = 5
        self.rooms_list : list[Room] = []
        self.current_turn = 0
        self.initialize_rooms()
        self.go_to_next_room()

    def go_to_next_room(self):
        if self.too_late:
            return
        self.too_late = True
        self.animation_handler.end_room_anim()
        # Add anim that will load next room content 
        

    def load_next_room_content(self):
        self.too_late = False
        self.current_turn = 0
        self.current_room_index += 1
        if self.current_room_index >= self.max_rooms:
            self.current_room_index = 0
            self.game_manager.end_game()
            return
        self.current_room = self.rooms_list[self.current_room_index]

    def initialize_rooms(self):
        for i in range(self.max_rooms):
            
            new_room = Room()
            new_room.generate_this_room()
            self.rooms_list.append(new_room)

# Room elements
# Room number??
# ICON?
# ELEMENTS

# Random room elements?
# Generate room elements graphics

class Room():
    def __init__(self, room_name : str = "room name", room_icon = (0,0,16,16)):
        self.room_name : str = room_name
        self.room_icon = room_icon
        self.room_elements : dict[int, RoomElement] = {0: None, 1: None, 2: None}
        self.generate_this_room()
    
    def generate_this_room(self):
        # Create random enums for room elements
        for i in range(3):
            if random.random() < 0.5:
                continue
            room_elements_basic = [
                RoomElement(ObjectEnum.FURNITURE_1),
                RoomElement(ObjectEnum.MONSTER_1)
            ]
            random_element = random.choice(room_elements_basic)
            self.room_elements[i] = random_element


class MysteryRoom(Room):
    def __init__(self, room_name = "Mystery Room", room_icon=(0, 0, 16, 16)):
        super().__init__(room_name, room_icon)
        self.room_icon = (0,0,16,16)

class TreasureRoom(Room):
    def __init__(self, room_name = "Treasure Room", room_icon=(16, 0, 16, 16)):
        super().__init__(room_name, room_icon)
        self.room_icon = (16,0,16,16)

class RoomElement():
    def __init__(self, object_enum :ObjectEnum, hp : int = 1):
        self.enum = object_enum
        self.hp = 1