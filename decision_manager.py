from hero_manager import HeroManager, Hero, HeroStats, HeroEnum
from decisions import Decision, Rest_Decision, GoNextRoom_Decision

class DecisionManager():
    def __init__(self):
        pass
    def make_decisions(self):
        print("MAKING DECISION")
        # Get decision for each player?
        
        # For each hero:
        # MAKE DECISION:
        for key, value in HeroManager().hero_list.items():
            self.make_decision(value)    
    
    def make_decision(self, hero : Hero):
        decisions = []
        
        default_decisions = self.get_default_decisions()
        decisions+=default_decisions
        # Get traits from the room
        
        # Get traits from what is happening? / stats / preferences / default actions
        
        # Weighted decision what happens / actions
        print(decisions)

        pass
    def get_default_decisions(self):
        default_decisions = [
            Rest_Decision(),
            GoNextRoom_Decision(),
        ]
        return default_decisions
    def get_room_traits():

        pass
