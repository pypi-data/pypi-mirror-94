"""Local types"""
from typing import Union, Callable, Any
import io

# pylint: disable=E1136
StreamType = Union[io.RawIOBase, io.BufferedIOBase]
PkgIdxType = Union[int, bytes]
SubCBType = Callable[[Any], None]
