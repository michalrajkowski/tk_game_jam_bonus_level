# Decision of what he wants to do
class Decision():
    def __init__(self, weigth=5):
        from hero_manager import HeroEnum
        self.weigth = weigth
        self.description_short = ""
        self.description_box : dict[HeroEnum, list[str]] = {}

    def __str__(self):
        return f"{self.description_short}"
        
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