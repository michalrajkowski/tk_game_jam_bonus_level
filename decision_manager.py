from hero_manager import HeroManager, Hero, HeroStats
from decisions import Decision, Rest_Decision, GoNextRoom_Decision, HeroEnum, Inspect_Decision, Shakespear_Decision, Attack_Decision, Defend_Decision
from animation_handler import AnimationHandler, TalkAnimation
from room_manager import RoomManager, RoomElement
import random
from game_manager import ObjectEnum


class DecisionManager():
    def __init__(self, game_manager):
        self.hero_manager : HeroManager = None
        self.animation_handler : AnimationHandler = None
        self.room_manager : RoomManager = None
        self.PLAYER_SLOTS = None
        self.game_manager = game_manager
        pass

    def make_decisions(self):
        # Get decision for each player?
        self.room_manager.too_late = False
        
        # For each hero:
        # MAKE DECISION:
        dead_count = 0
        for key, value in self.hero_manager.hero_list.items():
            if value.is_dead:
                dead_count+=1
            else:
                self.make_decision(value)    
        if dead_count == 3:
            # end game
            self.game_manager.end_game()
    def make_decision(self, hero : Hero):
        decisions = []
        
        default_decisions = self.get_default_decisions()
        room_decision = self.get_room_decisions(hero)
        decisions+=default_decisions
        decisions+=room_decision
        # Get traits from the room
        
        # Get traits from what is happening? / stats / preferences / default actions
        
        # Weighted decision what happens / actions
        # Create a list of weights corresponding to each decision
        weights = [decision.weigth for decision in decisions]
        
        # Select one decision randomly, considering the weights
        selected_decision = random.choices(decisions, weights=weights, k=1)[0]
        selected_decision.room_manager = self.room_manager
        hero.set_decision(selected_decision)
        hero_pos = self.PLAYER_SLOTS[hero.hero_type.value]
        # Get random description:
        description = selected_decision.description_box[HeroEnum.DEFAULT][0]
        self.animation_handler.add_anim(TalkAnimation(4.0, hero_pos[0], hero_pos[1], hero_pos[2], description), True)


    def get_default_decisions(self):
        go_next_room = GoNextRoom_Decision()
        go_next_room.weigth = 5*self.room_manager.current_turn*self.room_manager.current_turn
        shakespear : Decision = Shakespear_Decision()
        shakespear.weigth = 1
        default_decisions = [
            Rest_Decision(),
            go_next_room,
            shakespear
        ]
        return default_decisions
    def get_room_decisions(self, hero:Hero):
        # self room element
        []
        room_elements = self.room_manager.rooms_list[self.room_manager.current_room_index].room_elements
        # iterate over elements and add correct handling for decisions tied to them?
        decisions_pack = []
        for i in range(3):
            room_element : RoomElement = room_elements[i]
            if room_element == None:
                continue
            object_enum =  room_element.enum
            if object_enum == ObjectEnum.FURNITURE_1: # Library
                # check library
                inspect = Inspect_Decision(room_element)
                inspect.weigth = 5
                # if mage change is muuuch higher
                if hero.hero_type == HeroEnum.WIZARD:
                    inspect.weigth = 15
                decisions_pack.append(inspect)
                pass
            elif object_enum == ObjectEnum.MONSTER_1:
                attack_decision = Attack_Decision(room_element)
                defence_decision = Defend_Decision(room_element)
                if hero.hero_type == HeroEnum.WIZARD:
                    attack_decision.weigth = 5
                    defence_decision.weigth = 20
                if hero.hero_type == HeroEnum.WARRIOR:
                    attack_decision.weigth = 20
                    defence_decision.weigth = 20
                if hero.hero_type == HeroEnum.ROGUE:
                    attack_decision.weigth = 20
                    defence_decision.weigth = 5
                decisions_pack.append(attack_decision)
                decisions_pack.append(defence_decision)

        return decisions_pack
