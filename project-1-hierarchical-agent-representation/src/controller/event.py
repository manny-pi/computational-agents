from enum import Enum, auto

class Event(Enum):
    """
    An Enum type that represents the type of event that was fired.
    """
    
    SPRITE_INIT = 1 
    SPRITE_UPDATE = 2
