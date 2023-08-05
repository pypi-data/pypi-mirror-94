"""Handle subscriptions"""
from __future__ import annotations
from typing import Dict, List
from dataclasses import dataclass, field
import logging

from cobs import cobs  # type: ignore

from .localtypes import PkgIdxType, StreamType, SubCBType
from .packer import normalize_pkgidx, unpack


LOGGER = logging.getLogger(__name__)


@dataclass()
class Subscription:
    """Subscription metadata for the tracker"""

    stream: StreamType
    pkgidx: PkgIdxType
    callback: SubCBType


@dataclass()
class SubscriptionTracker:
    """Track subscriptions"""

    chunk_size: int = field(default=1024)
    subs_by_stream: Dict[StreamType, Dict[int, List[Subscription]]] = field(init=False, default_factory=dict)
    buffers_by_stream: Dict[StreamType, bytes] = field(init=False, default_factory=dict)

    def subscribe(self, stream: StreamType, pkgidx: PkgIdxType, callback: SubCBType) -> None:
        """Subscribe to given index/stream combo"""
        sub = Subscription(stream, pkgidx, callback)
        pkgidx = normalize_pkgidx(pkgidx)[0]  # we want the byte as integer
        if stream not in self.subs_by_stream:
            self.subs_by_stream[stream] = {}
            self.buffers_by_stream[stream] = b""
        if pkgidx not in self.subs_by_stream[stream]:
            self.subs_by_stream[stream][pkgidx] = []
        self.subs_by_stream[stream][pkgidx].append(sub)

    def parse(self) -> None:
        """Parse all streams and fire callbacks"""
        for stream in self.subs_by_stream:
            subs_by_idx = self.subs_by_stream[stream]
            read = stream.read(self.chunk_size)
            if not read:
                # No new data
                continue
            self.buffers_by_stream[stream] += read

            # Get complete packets, put incomplete stuff back to buffer
            packets = self.buffers_by_stream[stream].split(b"\0")
            self.buffers_by_stream[stream] = packets[-1]
            packets = packets[:-1]
            for packet in packets:
                if not packet:
                    # ignore empty packets
                    continue
                try:
                    pkgidx, data = unpack(packet)
                except (ValueError, cobs.DecodeError) as exc:
                    LOGGER.warning("Could not parse packet: {}".format(exc))
                    LOGGER.debug("packet was {}".format(repr(packet)))
                    continue
                if pkgidx not in subs_by_idx:
                    LOGGER.info("No subscriptions for idx {}".format(pkgidx))
                    LOGGER.debug("data was {}".format(repr(data)))
                    continue
                for sub in subs_by_idx[pkgidx]:
                    sub.callback(data)  # type: ignore # false positive for "too many arguments"


DEFAULT_TRACKER = SubscriptionTracker()


def subscribe(stream: StreamType, pkgidx: PkgIdxType, callback: SubCBType) -> None:
    """Subscribe to given index/stream combo on the default tracker"""
    DEFAULT_TRACKER.subscribe(stream, pkgidx, callback)


def parse() -> None:
    """Parse all streams and fire callbacks on the default tracker"""
    DEFAULT_TRACKER.parse()
