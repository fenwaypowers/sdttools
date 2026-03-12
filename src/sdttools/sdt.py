from typing import Optional, Iterable, Dict, Union
from os import PathLike
import os
import tempfile
import shutil

from .demux import demux_sdt
from .mux import mux

PathType = Union[str, PathLike[str]]


class SDT:
    """
    Represents an SDT file and provides methods for extracting its contents.
    """

    def __init__(self, path: PathType) -> None:
        """
        Initialize the SDT object with the given file path.
        Args:
            path (PathType): The path to the SDT file.
        Raises:
            FileNotFoundError: If the specified SDT file does not exist.
        """

        self.path: str = os.fspath(path)

        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)


    def extract_all(self, out_dir: Optional[PathType] = None) -> None:
        """
        Extract all contents of the SDT file to the specified output directory.
        Args:
            out_dir (Optional[PathType], optional): The directory to extract to. Defaults to None, which extracts to the same directory as the SDT file.
        """

        if out_dir is None:
            out_dir = os.path.dirname(os.path.abspath(self.path))

        demux_sdt(self.path, os.fspath(out_dir))


    def extract(self, outputs: Iterable[PathType]) -> Dict[str, bool]:
        """
        Extract specified contents of the SDT file to the given output paths.
        Args:
            outputs (Iterable[PathType]): The paths to extract to.
        Returns:
            Dict[str, bool]: A dictionary mapping each output path to a boolean indicating whether the extraction was successful.
        """
        with tempfile.TemporaryDirectory() as tmp:

            demux_sdt(self.path, tmp)

            extracted: Dict[str, bool] = {}

            for f in os.listdir(tmp):

                ext = os.path.splitext(f)[1].lower()
                src = os.path.join(tmp, f)

                for out in outputs:

                    out_str = os.fspath(out)
                    oext = os.path.splitext(out_str)[1].lower()

                    if ext == oext or (ext == ".m2v" and oext == ".mp4"):

                        shutil.copy(src, out_str)
                        extracted[out_str] = True

            return extracted


def create_sdt(
    output: PathType,
    m2v: Optional[PathType] = None,
    mtaf: Optional[PathType] = None,
    pacb: Optional[PathType] = None
) -> None:
    """
    Create an SDT file by muxing the given input files.
    
    Args:
        output (PathType): The path to the output SDT file.
        m2v (Optional[PathType], optional): Path to the video file (.m2v). Defaults to None.
        mtaf (Optional[PathType], optional): Path to the audio file (.mtaf). Defaults to None.
        pacb (Optional[PathType], optional): Path to the subtitle file (.pacb). Defaults to None.
    """

    mux(
        os.fspath(output),
        os.fspath(pacb) if pacb else None,
        os.fspath(m2v) if m2v else None,
        os.fspath(mtaf) if mtaf else None
    )
