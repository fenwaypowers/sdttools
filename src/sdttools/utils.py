import struct
from typing import Iterator


def get_u32_le(buf: bytes, offset: int) -> int:
    return struct.unpack("<I", buf[offset:offset + 4])[0]


def chunks(data: bytes, size: int) -> Iterator[bytes]:
    for i in range(0, len(data), size):
        yield data[i:i + size]
