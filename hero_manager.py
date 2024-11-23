from enum import Enum, auto
from decisions import Decision, NoneDecision, HeroEnum

class HeroStats(Enum):
    ANGER = auto()
    FEAR = auto()
    BLOOD = auto()

class HeroManager():
    def __init__(self):
        # Generate Heroes
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
        self.hero_list[HeroEnum.WARRIOR] = hero_warrior
        self.hero_list[HeroEnum.WIZARD] = hero_mage
        self.hero_list[HeroEnum.ROGUE] = hero_rogue
        
class Hero():
    def __init__(self, hero_type : HeroEnum,name : str, current_stats : dict[HeroStats, int], max_stats : dict[HeroStats, int]):
        print("INIT HERO")
        self.hero_type : HeroEnum = hero_type
        self.name :str = name
        self.current_stats : dict[HeroStats, int] = current_stats
        self.max_stats : dict[HeroStats, int] = max_stats
        self.decision : Decision = None
        self.set_decision(NoneDecision())
        

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
    
    def set_decision(self, decision : Decision):
        print("SETTING DECISION : ")
        self.decision = decision