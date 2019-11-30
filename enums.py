from enum import Enum

class MoveType(Enum):
    ABS = 0
    REL = 1

class BiomeType(Enum):
    ASCII = 0
    IO = 1
    STORAGE = 2

class BlockType(Enum):
    ZERO = 0

class IOMode(Enum):
    IN = 0
    OUT = 1

class JumpCondition(Enum):
    C = 0
    NC = 1
    NZ = 2
    Z = 3

class JumpType(Enum):
    NORMAL = 0
    CONDITIONAL = 1

class ValueType(Enum):
    NUMBER = 0
    NAMETAG = 1

class Command(Enum):
    CLEAR = 0
    KILL = 1
    MINE = 2
    MOVE = 3
    NAMETAG = 4
    PLACE = 5
    SAY = 6
    SPAWNPOINT = 7
    TP = 8
    WARP = 9
    
class RegisterType(Enum):
    CRAFT_REGISTER = int("0xCF", 16)
    DUPE_REGISTER = int("0xD0", 16)

class FlagType(Enum):
    CARRY_FLAG = int("0xCC", 16)
    ZERO_FLAG = int("0xC0", 16)
    NEGATIVE_FLAG = int("0xFF", 16)