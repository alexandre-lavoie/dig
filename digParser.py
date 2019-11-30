from enums import *
from exceptions import *
import string

def isHex(s):
    try:
        int(s, 16)
        return len(s) <= 2
    except ValueError:
        return False

def isNametag(s):
    return s[0] == '$'

def parse(file: str):
    code = []
    nametags = {}

    with open(file, 'r') as fp:
        lineNumber = 1
        codeLine = 0

        for line in fp:
            lineNumber += 1
            line = line.strip()

            if line and line[0] == '/':
                split = line.split()
                tokens = []

                if split[0][1:].upper() in [x.name for x in Command]:
                    command = Command[split[0][1:].upper()]
                    tokens.append(command)
                
                    if command == Command.WARP or command == Command.CLEAR:
                        if not split[1]:
                            raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                        elif not split[1].upper() in [x.name for x in BiomeType]:
                            raise SyntaxError(UNKNOWN_BIOME, (file, lineNumber, line.find(split[1]) + 1, line))
                        else:
                            tokens.append(BiomeType[split[1].upper()])
                    elif command == Command.NAMETAG:
                        if not split[1]:
                            raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                        elif not isNametag(split[1]):
                            # RAISE NOT NAMETAG
                            pass
                        nametags[split[1]] = codeLine
                        tokens.append(split[1])
                    elif command == Command.SAY:
                        if len(split) < 2:
                            raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                        elif not split[1].upper() in [x.name for x in IOMode]:
                            raise SyntaxError(UNKNOWN_IO, (file, lineNumber, line.find(split[1]) + 1, line))
                        else:
                            tokens.append(IOMode[split[1].upper()])
                    elif command == Command.MOVE or command == Command.SPAWNPOINT:
                        if len(split) < 3:
                            raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                        elif not split[1].upper() in [x.name for x in MoveType]:
                            # RAISE WRONG MOVETYPE
                            pass
                        elif not isHex(split[2].upper()):
                            # RAISE NUMBER NOT HEX
                            pass
                        else:
                            tokens.append(MoveType[split[1].upper()])
                            tokens.append(int(split[2], 16))
                    elif command == Command.TP:
                        if not split[1]:
                            raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                        elif split[1].upper() in [x.name for x in JumpCondition]:
                            if not split[2]:
                                raise SyntaxError(MISSING_ARGS, (file, lineNumber, line.find(split[0]) + 1, line))
                            else:
                                tokens.append(JumpType.CONDITIONAL)

                                tokens.append(JumpCondition[split[1].upper()])

                                if isNametag(split[2]):
                                    # WE SHOULD EVENTUALLY LOOK IF THE NAMETAG EXISTS
                                    tokens.append(ValueType.NAMETAG)
                                    tokens.append(split[2])
                                elif isHex(split[2]):
                                    tokens.append(ValueType.NUMBER)
                                    tokens.append(int(split[2], 16))
                                else:
                                    # RAISE INVALID TYPE
                                    pass
                        else:
                            tokens.append(JumpType.NORMAL)

                            if isNametag(split[1]):
                                # WE SHOULD EVENTUALLY LOOK IF THE NAMETAG EXISTS
                                tokens.append(ValueType.NAMETAG)
                                tokens.append(split[1])
                            elif isHex(split[1]):
                                tokens.append(ValueType.NUMBER)
                                tokens.append(int(split[1], 16))
                            else:
                                # RAISE INVALID TYPE
                                pass

                    codeLine += 1
                    code.append(tokens)
                else:
                    raise SyntaxError(UNKNOWN_COMMAND, (file, lineNumber, line.find(split[0]) + 1, line))
    
    if len(code) == 0:
        raise Exception(EMPTY_CODE)
    return code, nametags