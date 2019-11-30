# Dig
Dig is an Esoteric Programming Language based on Minecraft.

## Exceptions

```
INVENTORY_FULL: Player attempted to add an item to a full inventory.

NO_BREAK: Player attempted to break an unbreakable block.

NO_PLACE: Player attempted to place a block a static block.

FAR_LANDS: A position pointer is set out of bound.
```

## Commands

### Clear
```
/clear <biome>
```

Description: Clear the content of biome.

biome: One of [io | storage]

### Kill
```
/kill
```

Description: Stops code execution.

### Mine
```
/mine
```

Description: Remove block under the player and add block to the top of the inventory stack.

Can throw INVENTORY_FULL, NO_BREAK.

### Move
```
/move [abs | rel] <pos>
```

Description: Moves the player pointer relatively or absolutely to a position.

abs: The player position is set to pos [00, FF].

rel: pos [00, 7F] is a positive shift and pos (7F, FF] is negative shift.

pos: A position/shift in [00, FF].

Can throw FAR_LANDS.

### Nametag
```
/nametag <str>
```

Description: Label to jump to using TP.

str: Unique label name. Must start with at `$`.

### Place
```
/place
```

Description: Pop the first item of the player stack and set block at player position.

### Say
```
/say [in | out]
```

Description: Handle the user input and output.

in: Prompt user for input, clear IO Valley, and set the value of IO Valley.

out: Prints the IO Valley buffer.

### Spawn Point
```
/spawnpoint [abs | rel] <pos>
```

Description: Set the biome spawn point.

rel: Set the biome spawn point relative to player.

abs: Set the biome spawn point at pos.

pos: A position/shift in [00, FF].

Can throw FAR_LANDS.

### Teleport
```
/tp [c | nc | nz | z] [tag | pos]

or

/tp [tag | pos]
```

Description: Move code pointer to new location.

c: On carry flag.
rel: Relative to current code pointer.
nc: Not carry flag.
nz: Not zero flag.
z: On zero flag.
None: 
tag: Nametag to jump to.
pos: Position to jump to.

### Warp
```
/warp <biome>
```

Description: Move player to a biome at the biome spawn.

biome: One of [ascii | io | storage].

## Player

A representation of a player. Holds a position as [00, FF] and an inventory stack of 36 bytes.

### Position

A hex value of 1 byte [00, FF].

### Inventory
The inventory is a 36 byte stack.

## Biomes

Map of a single chunck of 16x16 bytes. The player spawns by default at 00.

### Ascii Valley

Stores all the ascii characters.

#### Conditions

- Can mine -> Block remains Ascii value.
- Cannot place

#### Grid

```
  0 1 2 3 4 5 6 7 8 9 A B C D E F
0   ☺ ☻ ♥ ♦ ♣ ♠ • ◘ ○ ◙ ♂ ♀ ♪ ♫ ☼
1 ► ◄ ↕ ‼ ¶ § ▬ ↨ ↑ ↓ → ← ∟ ↔ ▲ ▼
2   ! " # $ % & ' ( ) * + , - . /
3 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
4 @ A B C D E F G H I J K L M N O
5 P Q R S T U V W X Y Z [ \ ] ^ _
6 ` a b c d e f g h i j k l m n o
7 p q r s t u v w x y z { | } ~
8 Ç ü ☺ é â ä à å ç ê ë è ï î ì Ä
9 Å É æ Æ ô ö ò û ù ÿ Ö Ü ¢ £ ¥ ₧ 
A ƒ á í ó ú ñ Ñ ª º ¿ ⌐ ¬ ½ ¼ ¡ «
B » ░ ▒ ▓ │ ┤ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ┐
C └ ┴ ┬ ├ ─ ┼ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧ 
D ╨ ╤ ╥ ╙ ╘ ╒ ╓ ╫ ╪ ┘ ┌ █ ▄ ▌ ▐ ▀
E α ß Γ π Σ σ µ τ Φ Θ Ω δ ∞ φ ε ∩
F ≡ ± ≥ ≤ ⌠ ⌡ ÷ ≈ ° ∙ · √ ⁿ ² ■  
```

### IO Plains

Buffer of the 256 character used to input and output data to and from user.

#### Commands

- Can mine
- Can place

#### Grid
Example of "Hello World!".

```
  0 1 2 3 4 5 6 7 8 9 A B C D E F
0 H e l l o   W o r l d !
1
2
3
4
5
6
7
8
9
A
B
C
D
E
F
```

### Storage Fortress

[0, 9F] is a storage for blocks. [A0, FF] is reserved for registers and flags.

#### Commands

- Can mine
- Can place (except on flags) 

#### Grid
Example of "Hello World!" and a crafting of char 2.

```
  0 1 2 3 4 5 6 7 8 9 A B C D E F
0 H e l l o   W o r l d !
1
2
3
4
5
6
7
8
9
A
B
C                         
D
E
F                         2
```

#### Storage [00, 9F]

Standard storage for blocks.

#### Zero flag (C0)

Set to 01 when craft register is zero.

Throws NO_PLACE.

#### Carry Flag (CC)

Set to 01 when arithmatics overflows 255. Otherwise, set to 00.

Throws NO_PLACE.

#### Craft Register (CF)

If negative flag set, add first placed block and subtract remaining to a minimum of 0 else add placed blocks % FF.

Set Carry Register when sum overflows FF.

#### Dupe Register (D0)

Keep the value of the register to the last placed byte on the register. Persists even when mined.

#### Negative Flag (FF)

Set arthimatics to negative if set to 01.

Throws NO_PLACE.