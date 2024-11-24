from hero_manager import HeroManager, Hero, HeroStats
from decisions import Decision, Rest_Decision, GoNextRoom_Decision, HeroEnum
from animation_handler import AnimationHandler, TalkAnimation
from room_manager import RoomManager
import random

class DecisionManager():
    def __init__(self):
        self.hero_manager : HeroManager = None
        self.animation_handler : AnimationHandler = None
        self.room_manager : RoomManager = None
        self.PLAYER_SLOTS = None
        pass
    def make_decisions(self):
        # Get decision for each player?
        
        # For each hero:
        # MAKE DECISION:
        for key, value in self.hero_manager.hero_list.items():
            self.make_decision(value)    
    
    def make_decision(self, hero : Hero):
        decisions = []
        
        default_decisions = self.get_default_decisions()
        decisions+=default_decisions
        # Get traits from the room
        
        # Get traits from what is happening? / stats / preferences / default actions
        
        # Weighted decision what happens / actions
        # Create a list of weights corresponding to each decision
        weights = [decision.weigth for decision in decisions]
        
        # Select one decision randomly, considering the weights
        selected_decision = random.choices(decisions, weights=weights, k=1)[0]
        hero.set_decision(selected_decision)
        hero_pos = self.PLAYER_SLOTS[hero.hero_type.value]
        # Get random description:
        description = selected_decision.description_box[HeroEnum.DEFAULT][0]
        self.animation_handler.add_anim(TalkAnimation(4.0, hero_pos[0], hero_pos[1], hero_pos[2], description), True)


    def get_default_decisions(self):
        go_next_room = GoNextRoom_Decision()
        go_next_room.weigth = 5*self.room_manager.current_turn*self.room_manager.current_turn
        default_decisions = [
            Rest_Decision(),
            go_next_room,
        ]
        return default_decisions
    def get_room_traits():
        pass
