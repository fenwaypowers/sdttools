import os
from .utils import get_u32_le

STREAM_ID_ADPCM = 1

extmap = {
    0x00000001: ".genh",   # ADPCM -> GENH / ".sdx_0"
    0x00000002: ".dmx",    # this container was found on Zone of the Enders HD Remaster
	0x00000003: ".nrm",
    0x00000004: ".pacb",   # has "PACB" magic not seen in any of the original versions the HD remaster was based on
    0x00000005: ".dmx",    # ditto
    0x00000006: ".bpx",    
    0x0000000c: ".pac",    # XBOX version of MGS2 - MPEG2 video format
    0x0000000d: ".pac",    # XBOX version of MGS2 - MPEG2 video format
	0x0000000e: ".pss",    # PS2 version of MGS2 - MPEG2 video format
	0x0000000f: ".ipu",    # PS2 version of MGS2 - MPEG2 video format
    0x00000020: ".m2v",    # this container is present even on all versions of the HD remaster(PS3, XBOX360, PSVITA), regardless of format
    0x00010001: ".sdx_1",
	0x00010004: ".sub_en", # it's a made-up container, becuase in the executable of those Metal Gear Solid PS2 games there's no indication of a container used for these formats
    0x00020001: ".sdx_2",
	0x00020004: ".sub_fr", # ditto
    0x00030001: ".msf",    # PS3 HD remaster audio format
	0x00030004: ".sub_de", # ditto
	0x00040001: ".xwma",   # XBOX360 HD remaster audio format
	0x00040004: ".sub_it", # ditto
	0x00050001: ".9tav",   # PSVITA HD remaster audio format
	0x00050004: ".sub_es", # ditto
	0x00060004: ".sub_jp", # ditto
	0x00070004: ".sub_jp", # ditto
    0x00100001: ".vag",    # VAG1/VAG2 format
    0x00110001: ".mtaf",   # MTAF format
}


def demux_sdt(sdt_path, out_dir):

    streams = {}

    with open(sdt_path, "rb") as sdt:

        sdt_size = os.path.getsize(sdt_path)

        while sdt.tell() < sdt_size:

            header = sdt.read(16)
            rid = get_u32_le(header, 0)

            if rid == 0xF0:
                break

            elif rid == 0x10:

                sid = get_u32_le(header, 0x0C)

                if sid in extmap:
                    path = os.path.join(
                        out_dir,
                        os.path.splitext(os.path.basename(sdt_path))[0] + extmap[sid]
                    )
                else:
                    path = os.path.join(
                        out_dir,
                        "%s_%08X.bin" % (
                            os.path.splitext(os.path.basename(sdt_path))[0],
                            sid
                        )
                    )

                streams[sid] = open(path, "w+b")

                if sid == STREAM_ID_ADPCM:
                    streams[sid].write(b"\0" * 4096)

            elif rid in streams:

                size = get_u32_le(header, 4) - 16
                streams[rid].write(sdt.read(size))

            else:
                raise RuntimeError("unknown header ID")

    for s in streams.values():
        s.close()
