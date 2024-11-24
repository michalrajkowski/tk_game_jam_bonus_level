# Decision of what he wants to do
from enum import Enum, auto

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
        self.weigth = weigth
        self.description_short = "DEFAULT DECISION"
        self.description_box : dict[HeroEnum, list[str]] = {}
        self.initialize_weigth()

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

class GoNextRoom_Decision(Decision):
    def __init__(self):
        from hero_manager import HeroEnum
        super().__init__()
        self.description_short = "Go to the next room"
        self.description_box = {
            HeroEnum.DEFAULT: ["I think we should keep going."]
        }