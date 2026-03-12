import struct
from typing import Iterator


def get_u32_le(buf: bytes, offset: int) -> int:
    """
    Read a little-endian unsigned 32-bit integer from the given buffer at the specified offset.
    Args:
        buf (bytes): The buffer to read from.
        offset (int): The offset to read from.
    Returns:
        int: The little-endian unsigned 32-bit integer.
    """
    return struct.unpack("<I", buf[offset:offset + 4])[0]


def chunks(data: bytes, size: int) -> Iterator[bytes]:
    """
    Yield successive chunks of the given data with the specified size.
    Args:
        data (bytes): The data to chunk.
        size (int): The size of each chunk.
    Returns:
        Iterator[bytes]: An iterator over the chunks.
    """
    for i in range(0, len(data), size):
        yield data[i:i + size]
