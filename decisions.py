# Decision of what he wants to do
from enum import Enum, auto
import random
from animation_handler import TalkAnimation

class HeroEnum(Enum):
    WIZARD = 0
    ROGUE = 1
    WARRIOR = 2
    DEFAULT = 3

def get_state(index):
    try:
        return HeroEnum(index)
    except ValueError:
        return None  # Return None or handle invalid index

class Decision():
    def __init__(self, weigth=5):
        from hero_manager import HeroEnum
        self.non_decision = False
        self.room_manager = None
        self.weigth = weigth
        self.description_short = "DEFAULT DECISION"
        self.description_box : dict[HeroEnum, list[str]] = {}
        self.initialize_weigth()

    def resolve(self, hero, hero_manager):
        # Gighlight this hero action?
        if (self.room_manager.too_late == True):
            return

    # Change it's weigth based on some conditions???
    def initialize_weigth(self):
        pass

    def __str__(self):
        return f"{self.description_short}"
    
class NoneDecision(Decision):
    def __init__(self):
        super().__init__()
        self.description_short = "EMPTY DECISION"
        self.non_decision = True 

class Rest_Decision(Decision):
    def __init__(self):
        from hero_manager import HeroEnum
        super().__init__()
        self.description_short = "Rest"
        self.description_box = {
            HeroEnum.DEFAULT: ["Maybe i could rest a bit..."]
        }

    def resolve(self, hero, hero_manager):
        return super().resolve(hero, hero_manager)
        if (self.room_manager.too_late == True):
            return
        # Regenerate some resource?

class GoNextRoom_Decision(Decision):
    def __init__(self):
        from hero_manager import HeroEnum
        super().__init__()
        self.description_short = "Escape"
        self.description_box = {
            HeroEnum.DEFAULT: ["I think we should keep going."]
        }
    
    def resolve(self, this_hero, hero_manager):
        super().resolve(this_hero, hero_manager)
        if (self.room_manager.too_late == True):
            return
        # If at least 2 other players want to go to the next room, go to the next room,
        # The remaining dude will get angry
        
        # If not the asker gets angry
        votes_yes = 0
        for new_hero in hero_manager.hero_list.values():
            if (isinstance(new_hero.decision, GoNextRoom_Decision)):
                votes_yes+=1
        if votes_yes == 1:
            # Asker gets angry / fear
            texts = [
                "Why you don't listen to me? I want to go!",
                "Guys, can we move. I dont like this place at all...",
                "Can we leave this place please?!"
            ]
            to_say = random.choice(texts)
            this_hero.say(to_say)
            this_hero.get_anger(1)
        else:
            texts = [
                "We voted to leave!",
                "The majority decided. We are leaving",
                "We are leaving."
            ]
            to_say = random.choice(texts)
            this_hero.say(to_say)
            for hero_2 in hero_manager.hero_list.values():
                if not (isinstance(hero_2.decision, GoNextRoom_Decision)):
                    # This one is about to get angry
                    texts = [
                        "What? I dont want to leave yet.",
                        "Why moving so fast???",
                        "That's nonsense. I want to stay!"
                    ]
                    to_say = random.choice(texts)
                    hero_2.say(to_say)
                    hero_2.get_anger(1)
            self.room_manager.go_to_next_room()