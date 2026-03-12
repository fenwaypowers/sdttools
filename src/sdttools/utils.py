import struct

def get_u32_le(buf, offset):
    return struct.unpack("<I", buf[offset:offset+4])[0]

def chunks(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]
