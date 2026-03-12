import os
import tempfile
import shutil

from .demux import demux_sdt
from .mux import mux


class SDT:

    def __init__(self, path):

        self.path = path

        if not os.path.exists(path):
            raise FileNotFoundError(path)

    def extract_all(self, out_dir=None):

        if out_dir is None:
            out_dir = os.path.dirname(os.path.abspath(self.path))

        demux_sdt(self.path, out_dir)

    def extract(self, outputs):

        with tempfile.TemporaryDirectory() as tmp:

            demux_sdt(self.path, tmp)

            extracted = {}

            for f in os.listdir(tmp):

                ext = os.path.splitext(f)[1].lower()
                src = os.path.join(tmp, f)

                for out in outputs:

                    oext = os.path.splitext(out)[1].lower()

                    if ext == oext or (ext == ".m2v" and oext == ".mp4"):

                        shutil.copy(src, out)
                        extracted[out] = True

            return extracted


def create_sdt(output, m2v=None, mtaf=None, pacb=None):

    mux(output, pacb, m2v, mtaf)
