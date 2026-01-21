from enum import IntEnum


class Tag(IntEnum):
    STRESS = 1
    WORKOUT = 2
    SLEEP = 3
    FOCUS = 4
    MENTAL_HEALTH = 5


class Role(IntEnum):
    USER = 1
    TRAINER = 2
    ADMIN = 3
    SUPER_ADMIN = 4
