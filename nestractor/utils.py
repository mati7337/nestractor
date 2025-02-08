from PIL import Image
import argparse
import os

# Palettes are 4 colors to use for tile rendering
# You can even use alpha!

KIRBY_PALETTE = [
    (0, 0, 0, 255),
    (0, 0, 0, 255),
    (255, 199, 219, 255),
    (255, 117, 182, 255),
]

GRAYSCALE_PALETTE = [
    (0, 0, 0, 255),
    (85, 85, 85, 255),
    (170, 170, 170, 255),
    (255, 255, 255, 255),
]

PALETTES = {
    "GRAYSCALE": GRAYSCALE_PALETTE,
    "KIRBY": KIRBY_PALETTE,
}

# First key from PALETTES
DEFAULT_PALETTE = PALETTES.keys().__iter__().__next__()

def get_tile(data, offset):
    # Returns NES tile as a 2d list from bytes
    # data: bytes of the ROM
    # offset: position of the tile
    # returns a 2d list with tile colors
    tile = []

    for row_i in range(8):
        row = []

        # Single row of pixels in a tile is composed of 2 planes, each 8 bits long
        # To get a color value we need to combine a bit from plane1 and a bit from plane2
        # Position of the bit is the x coordinate of the pixel
        # Eg.    if plane1 is 01101000
        #       and plane2 is 11001100
        # then the colors are 23103200
        # Repeat for all 8 rows
        plane1 = data[offset+row_i]
        plane2 = data[offset+row_i+8]

        for x in range(8):
            plane1_bit = (plane1 & (1 << (7-x))) != 0
            plane2_bit = (plane2 & (1 << (7-x))) != 0
            color = (plane2_bit << 1) + plane1_bit
            row.append(color)

        tile.append(row)

    return tile

def render_tile(img, pos, tile, palette):
    # Render tile returned from get_tile to img at pos using palette
    for y in range(8):
        for x in range(8):
            color_index = tile[y][x]
            img.putpixel((pos[0]+x, pos[1]+y), palette[color_index])

def extract_tiles(rom, table0=1, table1=1,
                  palette=PALETTES[DEFAULT_PALETTE], image_mode="RGBA",
                  debug=False):
    # Get pillow Image from game's CHR ROM
    # rom: bytes like object in an ines format
    assert table0 or table1, "Uhhh, you're not extracting anything??"

    assert len(rom) >= 16, "The rom you provided doesn't even have a header!"

    prg_size = 16*1024*rom[4]
    chr_size = 8 *1024*rom[5]
    flags6   = rom[6]
    flags_trainer = (flags6 & 0b00000100) != 0

    if chr_size == 0:
        raise Exception("ROM uses CHR RAM instead of CHR ROM!\n"
                        "Unable to extract tiles!")

    chr_offset = 16 + (512 if flags_trainer else 0) + prg_size
    assert len(rom) > chr_offset, "CHR offset outside of ROM boundaries!"

    if debug:
        print("CHR Offset:", hex(chr_offset))
        print("CHR Size:", hex(chr_size))

    img = Image.new(mode=image_mode, size=(8*0x10*(table0+table1),8*0x10))

    cur_x_offset = 0

    # Pattern Table 0
    assert len(rom) >= (chr_offset + 0x8 * 0x10), "Pattern table 0 outside of ROM boundaries!"

    if table0:
        for i in range(0x100):
            tile = get_tile(rom, chr_offset + 0x10*i)
            x = (i% 0x10) * 8
            y = (i//0x10) * 8
            render_tile(img, (x, y), tile, palette)

        cur_x_offset += 0x8 * 0x10

    # Pattern Table 1
    assert len(rom) >= (chr_offset + 0x8 * 0x10 * 2), "Pattern table 1 outside of ROM boundaries!"

    if table1:
        for i in range(0x100):
            tile = get_tile(rom, chr_offset + 0x1000 + 0x10*i)
            x = (i% 0x10) * 8
            y = (i//0x10) * 8
            render_tile(img, (cur_x_offset + x, y), tile, palette)

    return img
