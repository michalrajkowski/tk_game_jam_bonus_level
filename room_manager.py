# holds current room
# holds max rooms
# Information about each room and their content / elements?

import random

class RoomManager():
    def __init__(self):
        self.current_room_index = -1
        self.current_room : Room = None
        self.max_rooms = 6
        self.rooms_list : list[Room] = []
        self.initialize_rooms()
        self.go_to_next_room()

    def go_to_next_room(self):
        self.current_room_index += 1
        self.current_room = self.rooms_list[self.current_room_index]

    def initialize_rooms(self):
        for i in range(self.max_rooms):
            possible_rooms = [MysteryRoom(), TreasureRoom()]
            new_room = random.choice(possible_rooms)
            self.rooms_list.append(new_room)

# Room elements
# Room number??
# ICON?
# ELEMENTS
class Room():
    def __init__(self, room_name : str = "room name", room_icon = (0,0,16,16)):
        self.room_name : str = room_name
        self.room_icon = room_icon
        self.room_elements : list[RoomElement] = []
        pass

class MysteryRoom(Room):
    def __init__(self, room_name = "Mystery Room", room_icon=(0, 0, 16, 16)):
        super().__init__(room_name, room_icon)
        self.room_icon = (0,0,16,16)

class TreasureRoom(Room):
    def __init__(self, room_name = "Treasure Room", room_icon=(16, 0, 16, 16)):
        super().__init__(room_name, room_icon)
        self.room_icon = (0,0,16,16)

class RoomElement():
    def __init__(self):
        pass