# sdttools

Extract (demux) and repack (mux) SDT container files used in Metal Gear Solid games.

sdttools is a command-line utility and Python library for working with SDT container files used in Metal Gear Solid 2 and 3.

It can extract video, audio, and subtitle streams from SDT files and repack them into new SDT containers.

## Features

- Extract any and all streams from `.sdt` files
- Currently **only** supports repacking `.m2v`/`.mp4`, `.mtaf`, and `.pacb` into new SDT containers
- Simple drag-and-drop support for `.exe` use
- Works as both a CLI tool and Python library, allowing for automation through python scrpiting

## How To Use

### Windows:

- Simply download the most recent `.exe` file from the [Releases tab](https://github.com/fenwaypowers/sdttools/releases).
- To extract, drag your `.sdt` file onto the `.exe`.
- To repack, select the files you wish to pack into one `.sdt` file, and then drag them onto the `.exe`.

### Linux

- Simply download the most recent binary from the [Releases tab](https://github.com/fenwaypowers/sdttools/releases).
- See the Command-Line Use section to learn how to use the command line arguments.

You can also simply install the package with Python and use it on any computer that runs python.

## Command-Line Use

```
usage: sdttools [-h] [-o OUTPUT] inputs [inputs ...]

Extract or repack SDT container files used in Metal Gear Solid games.

Basic usage:
  sdttools movie.sdt                Extract all streams
  sdttools movie.sdt -o video.m2v   Extract specific streams
  sdttools video.m2v audio.mtaf     Create output.sdt
  sdttools video.m2v -o movie.sdt   Create custom SDT

Drag-and-drop is supported when using the executable version.

positional arguments:
  inputs               Input files (.sdt, .m2v, .mp4, .mtaf, .pacb)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output file(s).
                       Extraction: specify filenames or use 'all'.
                       Repacking: specify the output .sdt file.
```

## Install as a package

Clone the repository and install locally:

```bash
git clone https://github.com/fenwaypowers/sdttools
cd sdttools
pip install -e .
```

Example Python use:

```py
from sdttools import SDT, create_sdt

# extract
sdt = SDT("movie.sdt")
sdt.extract_all()

# repack
create_sdt("new.sdt", m2v="video.m2v", mtaf="audio.mtaf")
```

This can be used to automate extracting/repacking SDT files if you are dealing with a lot of them at once.

## Credit where credit is due

This project is based entirely from the `std_demux.py` script.

- Credit to [Nisto](https://hcs64.com/mboard/forum.php?userinfo=1220) for [creating the original script](https://hcs64.com/mboard/forum.php?showthread=46911).
- Credit to [AnonRunzes](https://hcs64.com/mboard/forum.php?userinfo=1710) for [updating the script](https://hcs64.com/mboard/forum.php?showthread=46911&showpage=1).

## License

[MIT](https://github.com/fenwaypowers/sdttools?tab=MIT-1-ov-file)

## Future Features

The plan for the future is to continue the functionality of this by allowing repacking more formats found in the `.sdt` container.

Hopefully, people will add these extra functionalities by contributing to the project. m2v, mtaf, and pacb support is really all I was after, so I'm not sure I'll be working super hard on those other formats. 

I encourage pull requests!

## Reporting Issues

When reporting bugs, please include:

- the command you ran
- the expected behavior
- the actual behavior
- the full error message
