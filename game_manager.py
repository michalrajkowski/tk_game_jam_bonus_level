from enum import Enum, auto

class State(Enum):
    HEROES_THINK = auto()
    PLAYERS_ACT = auto()
    CARD_PLAYED = auto()
    CARD_CHOOSING_TARGETS = auto()
    ANIMATIONS_RESOLVING = auto()