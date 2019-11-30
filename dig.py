from classes import World
import digParser
from enums import *
import sys

def main(code, nametags, gui = False):
    world = World()
    pointer = 0

    if gui:
        print(world)

    while pointer < len(code):
        line = code[pointer]

        # Clear: (CLEAR, BIOME)
        # Kill: (KILL)
        # SpawnPoint: (MOVE, TYPE, VALUE)
        # Mine: (MINE)
        # Place: (PLACE)
        # Say: (SAY, IOType)
        # SpawnPoint: (SPAWN_POINT, TYPE, VALUE)
        # Teleport: (TP, JUMP_TYPE, [CONDITION], VALUE_TYPE, VALUE)
        # Warp: (WARP, BIOME)

        if line[0] == Command.CLEAR:
            world.clear(line[1])
        elif line[0] == Command.KILL:
            break
        elif line[0] == Command.MOVE:
            world.move(line[1], line[2])
        elif line[0] == Command.MINE:
            world.mine()
            if gui:
                print(world)
        elif line[0] == Command.PLACE:
            world.place()
            if gui:
                print(world)
        elif line[0] == Command.SAY:
            world.say(line[1])
        elif line[0] == Command.SPAWNPOINT:
            world.setSpawnPoint(line[1], line[2])
        elif line[0] == Command.TP:
            if line[1] == JumpType.NORMAL:
                if line[2] == ValueType.NUMBER:
                    pointer += line[3]
                elif line[2] == ValueType.NAMETAG:
                    pointer = nametags[line[3]]
            elif line[1] == JumpType.CONDITIONAL:
                conditions = [JumpCondition.C, JumpCondition.NC, JumpCondition.Z, JumpCondition.NZ]
                state = [world.isCarry(), not world.isCarry(), world.isZero(), not world.isZero()]

                for jumpCondition, conditionState in zip(conditions, state):
                    if line[2] == jumpCondition and conditionState:
                        if line[3] == ValueType.NUMBER:
                            pointer += line[4]
                        elif line[3] == ValueType.NAMETAG:
                            pointer = nametags[line[4]]
                        break
            if gui:
                print(world)
        elif line[0] == Command.WARP:
            world.warp(line[1])
            if gui:
                print(world)

        pointer += 1

if __name__ == "__main__":
    code, nametags = digParser.parse(len(sys.argv) >= 2 and sys.argv[1])
    gui = len(sys.argv) >= 3 and sys.argv[2] == "gui"
    main(code, nametags, gui)
