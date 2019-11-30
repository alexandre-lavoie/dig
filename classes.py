from enums import *
from constants import *
from exceptions import *

class Block():
    def __init__(self, id):
        self.id = id.value if isinstance(id, BlockType) else id

    def getId(self) -> int:
        return self.id

    def __str__(self):
        return str(chr(self.getId()))

class Point():
    def __init__(self, x: int):
        self.x = x

    def getX(self):
        return self.x

    def __str__(self):
        return hex(self.x)

    def __eq__(self, other):
        return isinstance(other, Point) and other.getX() == self.getX()

    def __str__(self):
        return hex(self.x)

    def __add__(self, other):
        return self.x + other.value

    def __sub__(self, other):
        return self.getX - other.value

    def __radd__(self, other):
        return self.x + other

    def __rsub__(self, other):
        return self.x - other

class Player():
    def __init__(self):
        self.inventory = []
        self.biome = BiomeType.ASCII
        self.position = Point(DEFAULT_BIOME_SPAWN)

    def __str__(self):
        return "Player: " + str(self.getPosition()) + ", Inventory: " + str([str(x) for x in self.inventory])

    def getBiome(self) -> BiomeType:
        return self.biome

    def addToInventory(self, block: Block):
        if len(self.inventory) <= 36:
            self.inventory.append(block)
        else:
            raise Exception(INVENTORY_FULL)

    def popInventory(self):
        if len(self.inventory) > 0:
            return Block(self.inventory.pop().getId())
        else:
            raise Exception(INVENTORY_EMPTY)

    def warp(self, biomeType: BiomeType, spawn: Point):
        self.biome = biomeType
        self.position = Point(spawn.getX())

    def getPosition(self):
        return Point(self.position.getX())

    def move(self, position: Point):
        self.position = Point(position.getX())

class Biome():
    def __init__(self, biomeType: BiomeType, world):
        self.world = world
        self.spawnPoint = Point(DEFAULT_BIOME_SPAWN)
        self.biomeType = biomeType
        self.clear()

    def __str__(self):
        return str([str(b) for b in self.chunk])

    def getSpawnPoint(self):
        return Point(self.spawnPoint.getX())

    def setSpawnPoint(self, position: Point):
        self.spawnPoint = Point(position.getX())

    def getBlock(self, position: Point) -> Block:
        return Block(self.chunk[position.getX()].getId())

    def setBlock(self, block: Block, position: Point):
        self.chunk[position.getX()] = Block(block.getId())

    def clear(self):
        if self.biomeType == BiomeType.ASCII:
            self.chunk = [Block(i) for i in range(CHUNK_SIZE * CHUNK_SIZE)]
        elif self.biomeType == BiomeType.STORAGE:
            self.chunk = [Block(BlockType.ZERO) for _ in range(CHUNK_SIZE * CHUNK_SIZE)]
            self.chunk[FlagType.ZERO_FLAG.value] = Block(1)
        else:
            self.chunk = [Block(BlockType.ZERO) for _ in range(CHUNK_SIZE * CHUNK_SIZE)]

    def read(self):
        string = ""

        for i in self.chunk:
            if i.getId() == 0:
                break
            else:
                string += str(i)

        return string

    def write(self, input: str):
        self.clear()

        for i, e in enumerate(input):
            self.setBlock(Block(ord(e)), Point(i))

    def place(self, block: Block, position: Point):
        if self.biomeType == BiomeType.ASCII:
            raise Exception(NO_PLACE)
        elif self.biomeType == BiomeType.STORAGE:
            if position.getX() == RegisterType.CRAFT_REGISTER.value:
                self.world.setCarryFlag(False)
                self.world.setZeroFlag(False)

                if self.world.isNegative():
                    self.setBlock(Block(self.getBlock(position).getId() - block.getId()), position)

                    if self.getBlock(Point(RegisterType.CRAFT_REGISTER.value)).getId() < BlockType.ZERO.value:
                        self.world.setZeroFlag(True)
                        self.setBlock(Block(BlockType.ZERO), position)
                else:
                    self.setBlock(Block(self.getBlock(position).getId() + block.getId()), position)

                    while self.getBlock(position).getId() >= self.world.MAX_SIZE: 
                        self.world.setCarryFlag(True)
                        self.setBlock(Block(self.getBlock(position).getId() - self.world.MAX_SIZE), position)

                    if self.getBlock(Point(RegisterType.CRAFT_REGISTER.value)).getId() == BlockType.ZERO.value:
                        self.world.setZeroFlag(True)
            elif position.getX() == RegisterType.DUPE_REGISTER.value:
                self.setBlock(block, position)
            elif position.getX() == FlagType.NEGATIVE_FLAG.value:
                if block.getId() < 2:
                    self.setBlock(block, position)
                else:
                    raise Exception(NOT_BINARY)
            elif position.getX() in [x for x in FlagType]:
                raise Exception(NO_PLACE)
            else:
                self.setBlock(block, position)
        else:       
            self.setBlock(block, position)


    def mine(self, position: Point):
        if self.biomeType == BiomeType.ASCII:
            return self.getBlock(position)
        elif self.biomeType == BiomeType.STORAGE:
            if position.getX() in [x.value for x in RegisterType] or position.getX() in [x.value for x in FlagType]:
                return self.getBlock(position)
            else:
                block = self.getBlock(position)
                self.place(Block(0), position)
                return block
        else:
            block = self.getBlock(position)
            self.place(Block(0), position)
            return block

class World():
    biomes = {}

    def __init__(self):
        self.player = Player()
        self.biomes = {}
        self.MAX_SIZE = CHUNK_SIZE * CHUNK_SIZE

        for biomeType in BiomeType:
            self.biomes[biomeType] = Biome(biomeType, self)
    
    def __str__(self):
        return "Biome: " + str(self.getPlayer().getBiome().name) + '\n\n' + str(self.getBiome(self.getPlayer().getBiome())) + "\n\n" + str(self.getPlayer()) + '\n'

    def move(self, moveType: MoveType, position: int):
        if moveType == MoveType.REL:
            change = position
            if position >= 128:
                change = 127 - position
            nextPoint = Point(self.getPlayer().getPosition().getX() + change)
        else:
            nextPoint = Point(position)
        
        if nextPoint.getX() >= CHUNK_SIZE * CHUNK_SIZE or nextPoint.getX() < 0:
            raise Exception(FAR_LANDS)
        else:
            self.getPlayer().move(nextPoint)

    def warp(self, biomeType: BiomeType):
        self.getPlayer().warp(biomeType, self.getBiome(biomeType).getSpawnPoint())

    def place(self):
        player = self.getPlayer()
        block = player.popInventory()
        self.getBiome(player.getBiome()).place(block, player.getPosition())

    def mine(self):
        player = self.getPlayer()
        block = self.getBiome(player.getBiome()).mine(player.getPosition())
        player.addToInventory(block)

    def clear(self, biomeType: BiomeType):
        self.getBiome(biomeType).clear()

    def setSpawnPoint(self, moveType: MoveType, position: int):
        if moveType == MoveType.REL:
            change = position
            if position >= 128:
                change = 127 - position
            nextPoint = Point(self.getPlayer().getPosition().getX() + change)
        else:
            nextPoint = Point(position)
        
        if nextPoint.getX() >= CHUNK_SIZE * CHUNK_SIZE or nextPoint.getX() < 0:
            raise Exception(FAR_LANDS)
        else:
            self.getBiome(self.getPlayer().getBiome()).setSpawnPoint(nextPoint)

    def say(self, ioType: IOMode):
        if ioType == IOMode.IN:
            user = input("Enter Value: ")
            self.getBiome(BiomeType.IO).write(user)
        else:
            print(self.getBiome(BiomeType.IO).read())

    def getPlayer(self) -> Player:
        return self.player

    def getBiome(self, biomeType: BiomeType) -> Biome:
        return self.biomes[biomeType]

    def isNegative(self):
        return self.getBiome(BiomeType.STORAGE).getBlock(Point(FlagType.NEGATIVE_FLAG.value)).getId() == 1
    
    def setCarryFlag(self, state: bool):
        self.getBiome(BiomeType.STORAGE).setBlock(Block(1 if state else 0), Point(FlagType.CARRY_FLAG.value))

    def isCarry(self):
        return self.getBiome(BiomeType.STORAGE).getBlock(Point(FlagType.CARRY_FLAG.value)).getId() == 1

    def setZeroFlag(self, state: bool = True):
        self.getBiome(BiomeType.STORAGE).setBlock(Block(1 if state else 0), Point(FlagType.ZERO_FLAG.value))

    def isZero(self):
        return self.getBiome(BiomeType.STORAGE).getBlock(Point(FlagType.ZERO_FLAG.value)).getId() == 1