from typing import BinaryIO, Optional
import struct

from .utils import chunks
from .types import PathType


def write_record(
    f: BinaryIO,
    rid: int,
    payload: bytes = b"",
    unk: int = 0,
    param: int = 0
) -> None:
    """
    Write an SDT record to a binary file.

    Args:
        f (BinaryIO): The file object to write to.
        rid (int): Record ID.
        payload (bytes): Record payload data.
        unk (int): Unknown header field.
        param (int): Additional parameter field used by some record types.
    """

    # Each SDT record begins with a 16-byte header
    size = 16 + len(payload)

    f.write(struct.pack("<IIII", rid, size, unk, param))
    f.write(payload)


def mux(
    outpath: str,
    pacb_path: Optional[PathType] = None,
    m2v_path: Optional[PathType] = None,
    mtaf_path: Optional[PathType] = None
) -> None:
    """
    Create an SDT container by muxing the given input streams.

    Args:
        outpath (str): Path where the output SDT file will be written.
        pacb_path (Optional[PathType]): Path to subtitle stream (.pacb).
        m2v_path (Optional[PathType]): Path to video stream (.m2v or .mp4).
        mtaf_path (Optional[PathType]): Path to audio stream (.mtaf).
    """

    with open(outpath, "wb") as out:

        # Register subtitle stream
        if pacb_path:

            write_record(out, 0x10, b"", 0, 0x00000004)

            with open(pacb_path, "rb") as f:
                pacb: bytes = f.read()

            write_record(out, 0x00000004, pacb)

        # Register video stream
        if m2v_path:
            write_record(out, 0x10, b"", 0, 0x00000020)

        # Register audio stream
        if mtaf_path:
            write_record(out, 0x10, b"", 0, 0x00110001)

        # Write MTAF audio stream
        if mtaf_path:

            with open(mtaf_path, "rb") as f:
                mtaf: bytes = f.read()

            # First 0x800 bytes contain the MTAF header
            header: bytes = mtaf[:0x800]
            write_record(out, 0x00110001, header)

            # Remaining data contains ADPCM frames
            audio: bytes = mtaf[0x800:]

            # SDT stores audio in 0x3FC0 byte chunks
            for c in chunks(audio, 0x3FC0):
                write_record(out, 0x00110001, c, 0, 0x3C)

        # Write video stream in 64 KB chunks
        if m2v_path:

            with open(m2v_path, "rb") as f:

                for chunk in iter(lambda: f.read(0x10000), b""):
                    write_record(out, 0x00000020, chunk)

        # Write SDT end-of-stream marker
        write_record(out, 0xF0, b"", 0, 0)
