## NEStractor

A simple to use small CLI utility and a Python library to extract CHR ROM tiles from NES games in the iNES format.

### Installation

You can install nestractor directly from the git repo using pip:

```sh
pip install git+https://github.com/mati7337/nestractor
```

### CLI usage

```
usage: nestractor [-h] [--palette {GRAYSCALE,KIRBY}] [-0] [-1] input output

Extract CHR ROM tiles from NES games in the iNES format

positional arguments:
  input                 NES game in the iNES format
  output                Output path where the tiles will be saved

options:
  -h, --help            show this help message and exit
  --palette {GRAYSCALE,KIRBY}
                        Palette to use for tile rendering
  -0                    Extract only the patterntable0
  -1                    Extract only the patterntable1
```

The simplest way to use it is to extract every tile using the default nestractor's palette:

```sh
nestractor input.nes output.png
```

You can additionally specify `-0` or `-1` to extract only a single pattern table.

```sh
nestractor -0 input.nes output.png
```

You can also choose a different palette from the ones available

```sh
nestractor --palette KIRBY input.nes output.png
```

### Library usage

To extract tiles import nestractor and use the `extract_tiles` function

```python
import nestractor

MY_PALETTE = [
    (0, 0, 0, 255),
    (85, 85, 85, 255),
    (170, 170, 170, 255),
    (255, 255, 255, 255),
]

with open("input.nes", "rb") as fl:
    rom = fl.read()

img = nestractor.extract_tiles(rom, # ROM as bytes like object
                               table0=1, # Extract pattern table 0
                               table1=1, # Extract pattern table 1
                               palette=MY_PALETTE, # Our custom palette
                               image_mode="RGBA", # Pillow image mode
                               debug=True) # Print some additional info

# Now we have our tiles extracted as a Pillow Image object

img.save("output.png")
```