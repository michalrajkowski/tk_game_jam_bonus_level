from enum import Enum, auto
from decisions import Decision, NoneDecision, HeroEnum
from animation_handler import AnimationHandler, TalkAnimation
import random 

class HeroStats(Enum):
    ANGER = auto()
    FEAR = auto()
    BLOOD = auto()

class HeroManager():
    def __init__(self, animation_handler, PLAYER_SLOTS):
        # Generate Heroes
        self.animation_handler : AnimationHandler = animation_handler
        self.PLAYER_SLOTS = PLAYER_SLOTS
        self.hero_list : dict[HeroEnum, Hero] = {}
        hero_mage : Hero = Hero(HeroEnum.WIZARD, "Wizard", 
                                {
                                    HeroStats.ANGER: 0,
                                    HeroStats.BLOOD: 0,
                                    HeroStats.FEAR: 0
                                },
                                {
                                    HeroStats.ANGER: 10,
                                    HeroStats.BLOOD: 10,
                                    HeroStats.FEAR: 10
                                })
        hero_rogue : Hero = Hero(HeroEnum.ROGUE, "Rogue", 
                                {
                                    HeroStats.ANGER: 0,
                                    HeroStats.BLOOD: 0,
                                    HeroStats.FEAR: 0
                                },
                                {
                                    HeroStats.ANGER: 10,
                                    HeroStats.BLOOD: 10,
                                    HeroStats.FEAR: 10
                                }) 
        hero_warrior : Hero = Hero(HeroEnum.WARRIOR, "Warrior", 
                                {
                                    HeroStats.ANGER: 0,
                                    HeroStats.BLOOD: 0,
                                    HeroStats.FEAR: 0
                                },
                                {
                                    HeroStats.ANGER: 10,
                                    HeroStats.BLOOD: 10,
                                    HeroStats.FEAR: 10
                                }) 
        hero_warrior.animation_handler = self.animation_handler
        hero_rogue.animation_handler = self.animation_handler
        hero_mage.animation_handler = self.animation_handler
        hero_warrior.PLAYER_SLOTS = self.PLAYER_SLOTS
        hero_rogue.PLAYER_SLOTS = self.PLAYER_SLOTS
        hero_mage.PLAYER_SLOTS = self.PLAYER_SLOTS
        self.hero_list[HeroEnum.WARRIOR] = hero_warrior
        self.hero_list[HeroEnum.WIZARD] = hero_mage
        self.hero_list[HeroEnum.ROGUE] = hero_rogue
        
    def resolve_decisions(self):
        for hero in self.hero_list.values():
            hero.resolve_decisions(self)
class Hero():
    def __init__(self, hero_type : HeroEnum,name : str, current_stats : dict[HeroStats, int], max_stats : dict[HeroStats, int]):
        self.animation_handler : AnimationHandler = None
        self.hero_type : HeroEnum = hero_type
        self.name :str = name
        self.current_stats : dict[HeroStats, int] = current_stats
        self.max_stats : dict[HeroStats, int] = max_stats
        self.decision : Decision = None
        self.set_decision(NoneDecision())
        self.PLAYER_SLOTS = None
        

    def __str__(self):
        # Format stats for better readability
        current_stats_str = ", ".join(f"{stat.name}: {value}" for stat, value in self.current_stats.items())
        max_stats_str = ", ".join(f"{stat.name}: {value}" for stat, value in self.max_stats.items())

        return (
            f"Hero: {self.name}\n"
            f"Type: {self.hero_type.name}\n"
            f"Current Stats: {current_stats_str}\n"
            f"Max Stats: {max_stats_str}"
        )
    
    def resolve_decisions(self, hero_handler):
        self.decision.resolve(self, hero_handler)

    def set_decision(self, decision : Decision):
        self.decision = decision

    def get_wound(self):
        print("GET WOUND")
        print(self)
        self.current_stats[HeroStats.BLOOD] += 1
        description_box = {
            HeroEnum.DEFAULT: ["Ouch! What was that?", "Oof, who hurt me??", "Argh! What the...."]
        }
        print(self.PLAYER_SLOTS)
        hero_pos = self.PLAYER_SLOTS[self.hero_type.value]
        descritpion = random.choice(description_box[HeroEnum.DEFAULT])
        self.animation_handler.add_anim(TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], descritpion), True)
        