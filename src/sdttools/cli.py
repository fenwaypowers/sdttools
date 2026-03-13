import argparse
import os
import sys
from typing import List, Optional

from .sdt import SDT, create_sdt


def main() -> None:
    """
    Entry point for the sdttools command-line interface.

    Parses command-line arguments and determines whether to extract
    streams from an SDT file or create a new SDT container from
    provided input streams.
    """

    parser = argparse.ArgumentParser(
        prog="sdttools",
        description=(
            "Extract or repack SDT container files used in Metal Gear Solid games.\n\n"
            "Basic usage:\n"
            "  sdttools movie.sdt                Extract all streams\n"
            "  sdttools movie.sdt -o video.m2v   Extract specific streams\n"
            "  sdttools video.m2v audio.mtaf     Create output.sdt\n"
            "  sdttools video.m2v -o movie.sdt   Create custom SDT\n\n"
            "Drag-and-drop is supported when using the executable version."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input files (.sdt, .m2v, .mp4, .mtaf, .pacb)",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="append",
        help=(
            "Output file(s).\n"
            "Extraction: specify filenames or use 'all'.\n"
            "Repacking: specify the output .sdt file."
        ),
    )

    args: argparse.Namespace = parser.parse_args()

    inputs: List[str] = args.inputs
    outputs: List[str] = args.output or []

    # Determine operation mode based on whether an SDT file was provided
    sdt_inputs: List[str] = [i for i in inputs if i.lower().endswith(".sdt")]

    if sdt_inputs:
        mode: str = "extract"
    else:
        mode = "pack"

    if mode == "extract":  # Demuxing / extracting

        if len(sdt_inputs) > 1:
            sys.exit("Error: Only one SDT file can be extracted at a time.")

        sdt_path: str = sdt_inputs[0]
        sdt = SDT(sdt_path)

        # Default behavior is to extract everything
        if not outputs:
            outputs = ["all"]

        if outputs == ["all"]:
            sdt.extract_all()
        else:
            sdt.extract(outputs)

    else:  # Muxing / packing

        video: Optional[str] = None
        audio: Optional[str] = None
        subs: Optional[str] = None

        # Identify input streams based on file extensions
        for i in inputs:

            ext = os.path.splitext(i)[1].lower()

            if ext in [".m2v", ".mp4"]:

                if video:
                    print(
                        f"Warning: Multiple video files detected. "
                        f"Using '{video}', ignoring '{i}'."
                    )
                else:
                    video = i

                # MP4 compatibility warning
                if ext == ".mp4":
                    print(
                        "WARNING: MP4 files are likely only supported in the "
                        "Master Collection version of Metal Gear Solid 2 and 3.\n"
                        "Use MPEG-2 .m2v for PS3 HD versions."
                    )

            elif ext == ".mtaf":

                if audio:
                    print(
                        f"Warning: Multiple audio files detected. "
                        f"Using '{audio}', ignoring '{i}'."
                    )
                else:
                    audio = i

            elif ext == ".pacb":

                if subs:
                    print(
                        f"Warning: Multiple subtitle files detected. "
                        f"Using '{subs}', ignoring '{i}'."
                    )
                else:
                    subs = i

            else:
                sys.exit(f"Unsupported input file: {i}")

        # Default output filename if none was provided
        if not outputs:
            out_sdt: str = "output.sdt"
        else:

            if len(outputs) > 1:
                sys.exit("Error: Only one output .sdt can be specified.")

            out_sdt = outputs[0]

        create_sdt(out_sdt, video, audio, subs)

        print("Created:", out_sdt)
