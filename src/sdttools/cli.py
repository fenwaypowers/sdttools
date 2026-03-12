import argparse
import os
import sys
from typing import List, Optional

from .sdt import SDT, create_sdt


def main() -> None:
    """
    Command-line interface for sdttools. Parses arguments and performs extraction or repacking based on the provided inputs.
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
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input files (.sdt, .m2v, .mp4, .mtaf, .pacb)"
    )

    parser.add_argument(
        "-o",
        "--output",
        action="append",
        help=(
            "Output file(s).\n"
            "Extraction: specify filenames or use 'all'.\n"
            "Repacking: specify output .sdt file."
        )
    )

    args: argparse.Namespace = parser.parse_args()

    inputs: List[str] = args.inputs
    outputs: List[str] = args.output or []

    # Determine demux/mux mode based on input files
    sdt_inputs: List[str] = [i for i in inputs if i.lower().endswith(".sdt")]

    if sdt_inputs:
        mode: str = "extract"
    else:
        mode = "pack"

    if mode == "extract": # Demuxing/extracting

        if len(sdt_inputs) > 1:
            sys.exit("Error: Only one SDT file can be extracted at a time.")

        sdt_path: str = sdt_inputs[0]
        sdt = SDT(sdt_path)

        if not outputs:
            outputs = ["all"]

        if outputs == ["all"]:
            sdt.extract_all()
        else:
            sdt.extract(outputs)

    else: # Muxing/packing

        video: Optional[str] = None
        audio: Optional[str] = None
        subs: Optional[str] = None

        for i in inputs:

            ext = os.path.splitext(i)[1].lower()

            if ext in [".m2v", ".mp4"]:

                if video:
                    print(f"Warning: Multiple video files detected. Using '{video}', ignoring '{i}'.")
                else:
                    video = i

                if ext == ".mp4":
                    print(
                        "WARNING: MP4 files are likely only supported in the Master Collection version of Metal Gear Solid 2 and 3.\n"
                        "Use MPEG-2 .m2v for PS3 HD versions."
                    )

            elif ext == ".mtaf":

                if audio:
                    print(f"Warning: Multiple audio files detected. Using '{audio}', ignoring '{i}'.")
                else:
                    audio = i

            elif ext == ".pacb":

                if subs:
                    print(f"Warning: Multiple subtitle files detected. Using '{subs}', ignoring '{i}'.")
                else:
                    subs = i

            else:
                sys.exit(f"Unsupported input file: {i}")

        if not outputs:
            out_sdt: str = "output.sdt"
        else:

            if len(outputs) > 1:
                sys.exit("Error: Only one output .sdt can be specified.")

            out_sdt = outputs[0]

        create_sdt(out_sdt, video, audio, subs)

        print("Created:", out_sdt)
