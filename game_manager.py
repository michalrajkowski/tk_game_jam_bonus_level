from enum import Enum, auto

class State(Enum):
    HEROES_THINK = auto()
    PLAYERS_ACT = auto()
    CARD_PLAYED = auto()
    CARD_CHOOSING_TARGETS = auto()
    POST_PLAYED_ANIMS = auto()
    ANIMATIONS_RESOLVING = auto()
    RESOLVING_HERO_ACTIONS = auto()