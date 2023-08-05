"""Stuff related to sending packets"""
from typing import Any

from .packer import pack
from .localtypes import StreamType, PkgIdxType

# pylint: disable=E1136
def send(stream: StreamType, pkgidx: PkgIdxType, data: Any) -> None:
    """Send a packet to the given stream"""
    packed = pack(pkgidx, data)
    stream.write(b"\0" + packed + b"\0")
