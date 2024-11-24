from enum import Enum, auto
from decisions import Decision, NoneDecision, HeroEnum
from animation_handler import AnimationHandler, TalkAnimation, StatIncreaseAnimation
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
        hero_mage : Hero = Hero(HeroEnum.WIZARD, "Ruphus", 
                                {
                                    HeroStats.ANGER: 0,
                                    HeroStats.BLOOD: 2,
                                    HeroStats.FEAR: 4
                                },
                                {
                                    HeroStats.ANGER: 10,
                                    HeroStats.BLOOD: 10,
                                    HeroStats.FEAR: 10
                                })
        hero_rogue : Hero = Hero(HeroEnum.ROGUE, "Sylas", 
                                {
                                    HeroStats.ANGER: 1,
                                    HeroStats.BLOOD: 4,
                                    HeroStats.FEAR: 1
                                },
                                {
                                    HeroStats.ANGER: 10,
                                    HeroStats.BLOOD: 10,
                                    HeroStats.FEAR: 10
                                }) 
        hero_warrior : Hero = Hero(HeroEnum.WARRIOR, "Tharlic", 
                                {
                                    HeroStats.ANGER: 4,
                                    HeroStats.BLOOD: 2,
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
            if not hero.is_dead:
                hero.resolve_decisions(self)
    def alive_heroes_num(self):
        alive = 3
        for hero in self.hero_list.values(): 
            if hero.is_dead:
                alive -=1
        return alive
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
        self.is_dead = False
        

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
        print("Resolving decision")
        print(self.decision)
        self.decision.resolve(self, hero_handler)

    def set_decision(self, decision : Decision):
        self.decision = decision

    def get_wound(self, value=1):
        """
        Increases the BLOOD stat and triggers an animation with a message.
        """
        print("GET WOUND")
        print(self)
        
        # Update blood stat
        self.current_stats[HeroStats.BLOOD] += value
        
        # Description texts for blood wounds
        description_box = {
            HeroEnum.DEFAULT: ["Ouch! What was that?", "Oof, who hurt me??", "Argh! What the...."]
        }
        
        # Get hero position
        hero_pos = self.PLAYER_SLOTS[self.hero_type.value]
        
        # Select description
        description = random.choice(description_box[HeroEnum.DEFAULT])
        
        if self.current_stats[HeroStats.BLOOD] < 10:
            # Add animation
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], description),
                True
            )
            self.animation_handler.add_anim(
                StatIncreaseAnimation(1.5, hero_pos[0], hero_pos[1], f"+{value} Blood", 8),
                True
            )
        else:
        # I cant take it anymore
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], "It is so cold in here.... *starts closing eyes*"),
                True
            )
            self.is_dead = True

    def say(self, str, push = False):
        # Get hero position
        hero_pos = self.PLAYER_SLOTS[self.hero_type.value]
        
        # Select description
        description = str
        
        # Add animation
        if push == False:
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], description),
                True
            )
        else:
            self.animation_handler.push_front_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], description),
                True
            )

    def play_anim(self, animation, blocking=False):
        self.animation_handler.add_anim(
            animation,
            blocking)
    def get_anger(self, value=1):
        """
        Increases the ANGER stat and triggers an animation with a message.
        """
        print("GET ANGER")
        print(self)
        
        # Update anger stat
        self.current_stats[HeroStats.ANGER] += value
        
        # Description texts for anger
        description_box = {
            HeroEnum.DEFAULT: ["I'm so mad right now!", "This makes my blood boil!", "I'll get you for this!"]
        }
        
        # Get hero position
        hero_pos = self.PLAYER_SLOTS[self.hero_type.value]
        
        # Select description
        description = random.choice(description_box[HeroEnum.DEFAULT])
        
        # Add animation
        if self.current_stats[HeroStats.ANGER] < 10:
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], description),
                True
            )
            self.animation_handler.add_anim(
                StatIncreaseAnimation(1.5, hero_pos[0], hero_pos[1], f"+{value} Anger", 9),
                True
            )
        else:
        # I cant take it anymore
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], "I can't take it any longer... *heart starts to beat super fast*"),
                True
            )
            self.is_dead = True


    def get_fear(self, value=1):
        """
        Increases the FEAR stat and triggers an animation with a message.
        """
        print("GET FEAR")
        print(self)
        
        # Update fear stat
        self.current_stats[HeroStats.FEAR] += value
        
        # Description texts for fear
        description_box = {
            HeroEnum.DEFAULT: ["What was that? I'm scared!", "No, no, no! This isn't right!", "I can't handle this!"]
        }
        
        # Get hero position
        hero_pos = self.PLAYER_SLOTS[self.hero_type.value]
        
        # Select description
        description = random.choice(description_box[HeroEnum.DEFAULT])
        
        # Add animation
        if self.current_stats[HeroStats.FEAR] < 10:
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], description),
                True
            )
            self.animation_handler.add_anim(
                StatIncreaseAnimation(1.5, hero_pos[0], hero_pos[1], f"+{value} Fear", 2),
                True
            )
        else:
            # I cant take it anymore
            self.animation_handler.add_anim(
                TalkAnimation(1.0, hero_pos[0], hero_pos[1], hero_pos[2], "I can't take it any longer... *starts crying*"),
                True
            )
            self.is_dead = True