import struct
from .utils import chunks


def write_record(f, rid, payload=b"", unk=0, param=0):

    size = 16 + len(payload)
    f.write(struct.pack("<IIII", rid, size, unk, param))
    f.write(payload)


def mux(outpath, pacb_path=None, m2v_path=None, mtaf_path=None):

    with open(outpath, "wb") as out:

        if pacb_path:

            write_record(out, 0x10, b"", 0, 0x00000004)

            with open(pacb_path, "rb") as f:
                pacb = f.read()

            write_record(out, 0x00000004, pacb)

        if m2v_path:
            write_record(out, 0x10, b"", 0, 0x00000020)

        if mtaf_path:
            write_record(out, 0x10, b"", 0, 0x00110001)

        if mtaf_path:

            with open(mtaf_path, "rb") as f:
                mtaf = f.read()

            header = mtaf[:0x800]
            write_record(out, 0x00110001, header)

            audio = mtaf[0x800:]

            for c in chunks(audio, 0x3FC0):
                write_record(out, 0x00110001, c, 0, 0x3C)

        if m2v_path:

            with open(m2v_path, "rb") as f:

                for chunk in iter(lambda: f.read(0x10000), b""):
                    write_record(out, 0x00000020, chunk)

        write_record(out, 0xF0, b"", 0, 0)
