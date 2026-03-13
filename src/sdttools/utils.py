import struct
from typing import Iterator


def get_u32_le(buf: bytes, offset: int) -> int:
    """
    Read a little-endian unsigned 32-bit integer from a byte buffer.

    Args:
        buf (bytes): The buffer to read from.
        offset (int): The byte offset within the buffer.

    Returns:
        int: The decoded little-endian unsigned 32-bit integer.
    """

    # struct.unpack returns a tuple, so extract the first value
    return struct.unpack("<I", buf[offset:offset + 4])[0]


def chunks(data: bytes, size: int) -> Iterator[bytes]:
    """
    Yield successive fixed-size chunks from a byte sequence.

    Args:
        data (bytes): The input data to split into chunks.
        size (int): Size of each chunk in bytes.

    Returns:
        Iterator[bytes]: Iterator yielding slices of the input data.
    """

    # Iterate through the data in steps of the requested chunk size
    for i in range(0, len(data), size):
        yield data[i:i + size]
