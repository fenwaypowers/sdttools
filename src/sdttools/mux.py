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
    """Write a record to the given binary file.

    Args:
        f (BinaryIO): The file to write to.
        rid (int): The record ID.
        payload (bytes, optional): The payload data. Defaults to b"".
        unk (int, optional): Unknown parameter. Defaults to 0.
        param (int, optional): Additional parameter. Defaults to 0.
    """

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
    Mux the given input files into an SDT file at the specified output path.

    Args:
        outpath (str): The path to the output SDT file.
        pacb_path (Optional[PathType], optional): Path to the subtitle file (.pacb). Defaults to None.
        m2v_path (Optional[PathType], optional): Path to the video file (.m2v). Defaults to None.
        mtaf_path (Optional[PathType], optional): Path to the audio file (.mtaf). Defaults to None.
    """

    with open(outpath, "wb") as out:

        if pacb_path:

            write_record(out, 0x10, b"", 0, 0x00000004)

            with open(pacb_path, "rb") as f:
                pacb: bytes = f.read()

            write_record(out, 0x00000004, pacb)

        if m2v_path:
            write_record(out, 0x10, b"", 0, 0x00000020)

        if mtaf_path:
            write_record(out, 0x10, b"", 0, 0x00110001)

        if mtaf_path:

            with open(mtaf_path, "rb") as f:
                mtaf: bytes = f.read()

            header: bytes = mtaf[:0x800]
            write_record(out, 0x00110001, header)

            audio: bytes = mtaf[0x800:]

            for c in chunks(audio, 0x3FC0):
                write_record(out, 0x00110001, c, 0, 0x3C)

        if m2v_path:

            with open(m2v_path, "rb") as f:

                for chunk in iter(lambda: f.read(0x10000), b""):
                    write_record(out, 0x00000020, chunk)

        write_record(out, 0xF0, b"", 0, 0)
