"""Stub methods"""
from typing import Any


from .localtypes import StreamType, PkgIdxType


def post() -> None:
    """no-op, we do not support the timed publish and send acts immediately"""


# pylint: disable=E1136
def publish(stream: StreamType, pkgidx: PkgIdxType, data: Any) -> None:
    """Timed publish, but we don't (and won't) support it.

Many reasons, Pythons type system and copy vs reference being some, just use send and handle the timing yourself"""
    raise NotImplementedError("We will not support this")
