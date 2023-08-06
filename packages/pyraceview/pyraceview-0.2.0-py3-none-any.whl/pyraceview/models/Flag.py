from enum import IntEnum


# Use IntEnum instead of Enum to allow for JSON serialization
class Flag(IntEnum):
    UNDEFINED = -1
    PRE_RACE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3
    WHITE = 4
    CHECKERED = 5
