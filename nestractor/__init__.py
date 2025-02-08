from . import utils
from .utils import PALETTES, extract_tiles

import argparse

def cli():
    parser = argparse.ArgumentParser(
            prog="nestractor",
            description="Extract CHR ROM tiles from NES games in the iNES format")
    parser.add_argument("input", help="NES game in the iNES format")
    parser.add_argument("output", help="Output path where the tiles will be saved")
    parser.add_argument("--palette",
                        default=utils.DEFAULT_PALETTE,
                        dest="palette",
                        choices=utils.PALETTES.keys(),
                        help="Palette to use for tile rendering")
    parser.add_argument("-0", dest="table0",
                        action="store_true",
                        help="Extract only the patterntable0")
    parser.add_argument("-1", dest="table1",
                        action="store_true",
                        help="Extract only the patterntable1")
    args = parser.parse_args()

    extract_table0 = 0
    extract_table1 = 0
    if (args.table0 == 0) and (args.table1 == 0):
        extract_table0 = 1
        extract_table1 = 1
    else:
        extract_table0 = args.table0
        extract_table1 = args.table1

    with open(args.input, "rb") as fl:
        rom = fl.read()

    img = extract_tiles(rom,
                        table0=extract_table0,
                        table1=extract_table1,
                        palette=PALETTES[args.palette])

    outpath = args.output

    print(f"Saving to {outpath}")
    img.save(outpath)
