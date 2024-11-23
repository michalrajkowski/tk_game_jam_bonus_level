from hero_manager import HeroManager, Hero, HeroStats
from decisions import Decision, Rest_Decision, GoNextRoom_Decision, HeroEnum
import random

class DecisionManager():
    def __init__(self):
        self.hero_manager : HeroManager = None
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

    def get_default_decisions(self):
        default_decisions = [
            Rest_Decision(),
            GoNextRoom_Decision(),
        ]
        return default_decisions
    def get_room_traits():
        pass
