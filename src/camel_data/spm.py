"""Reader for Bruker/Veeco Nanoscope ``.spm`` AFM files.

A Nanoscope file is a text header (``\\key: value`` lines, sections starting
with ``\\*``) followed by binary image channels. Each ``\\*Ciao image list``
section describes one channel: where its bytes start (``Data offset``), its
size, and how raw integers convert to physical units.

Height conversion (Nanoscope v5+):
    height_nm = raw * hard_scale[V/LSB] * sensitivity[nm/V]
where the channel's ``\\@2:Z scale`` line carries ``(<hard_scale> V/LSB)`` and
names the sensitivity key in brackets, e.g. ``[Sens. ZsensSens]``, whose value
is in the global header as ``\\@Sens. ZsensSens: V 446.79 nm/V``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

_HEADER_END = b"\\*File list end"
_SCALE_RE = re.compile(r"\[(?P<sens>[^\]]+)\]\s*\((?P<hard>[-+0-9.eE]+)\s*V/LSB\)")
_FIELD_RE = re.compile(r"^\\(.+?):(?:\s(.*))?$")
_NUMBER_RE =re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


@dataclass
class AFMChannel:
    name: str                 # e.g. "Height Sensor", "Height", "Amplitude"
    data: np.ndarray          # 2D array in physical units (nm for height)
    unit: str
    scan_size_nm: float       # physical width of the square scan
    meta: dict = field(default_factory=dict)

    @property
    def pixel_nm(self) -> float:
        return self.scan_size_nm / self.data.shape[1]


def _parse_header(text: str) -> tuple[dict, list[dict]]:
    """Return (global_fields, [image_section_fields, ...])."""
    global_fields: dict = {}
    images: list[dict] = []
    current = global_fields
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("\\*"):
            section = line[2:].strip().lower()
            if section == "ciao image list":
                current = {}
                images.append(current)
            elif images and section != "file list end":
                current = {}  # some other trailing section; ignore
            continue
        # Keys may themselves contain ':' (``\@2:Image Data: S [Height] "..."``),
        # so split at the first ': ' (colon + space), not the first colon.
        m = _FIELD_RE.match(line)
        if m:
            current.setdefault(m.group(1).strip(), (m.group(2) or "").strip())
    return global_fields, images


def _first_number(value: str) -> float:
    m = _NUMBER_RE.search(value)
    if not m:
        raise ValueError(f"no number in {value!r}")
    return float(m.group())


def _sens_value(global_fields: dict, sens_key: str) -> float:
    """Look up ``@Sens. X`` (value like ``V 446.79 nm/V``)."""
    for key in (f"@{sens_key}", sens_key):
        if key in global_fields:
            return _first_number(global_fields[key].split(" ", 1)[-1] if global_fields[key].startswith("V") else global_fields[key])
    raise KeyError(f"sensitivity {sens_key!r} not in header")


def read_spm(path: str | Path) -> list[AFMChannel]:
    """Read every image channel in a Nanoscope ``.spm`` file."""
    blob = Path(path).read_bytes()
    end = blob.find(_HEADER_END)
    if end < 0:
        raise ValueError(f"{path}: not a Nanoscope file (no '\\*File list end')")
    header = blob[:end].decode("latin-1")
    global_fields, images = _parse_header(header)
    if not images:
        raise ValueError(f"{path}: no image channels in header")

    channels = []
    for img in images:
        offset = int(_first_number(img["Data offset"]))
        rows = int(_first_number(img["Number of lines"]))
        cols = int(_first_number(img["Samps/line"]))
        bpp = int(_first_number(img.get("Bytes/pixel", "2")))
        dtype = {2: "<i2", 4: "<i4"}[bpp]
        raw = np.frombuffer(blob, dtype=dtype, count=rows * cols, offset=offset)
        raw = raw.reshape(rows, cols).astype(np.float64)

        name_line = img.get("@2:Image Data", "")
        name_m = re.search(r'"([^"]+)"', name_line)
        name = name_m.group(1) if name_m else name_line or "unknown"

        scale_line = img.get("@2:Z scale", "")
        sm = _SCALE_RE.search(scale_line)
        if sm:
            hard = float(sm.group("hard"))
            sens = _sens_value(global_fields, sm.group("sens").strip())
            unit_m = re.search(r"([a-zA-Z°]+)/V", global_fields.get(f"@{sm.group('sens').strip()}", ""))
            unit = unit_m.group(1) if unit_m else "a.u."
            data = raw * hard * sens
        else:
            data, unit = raw, "raw"

        # Nanoscope stores the bottom scan line first; flip so row 0 is the top.
        data = data[::-1].copy()

        scan = img.get("Scan Size") or global_fields.get("Scan Size", "0 nm")
        size = _first_number(scan)
        if "~m" in scan or "um" in scan or "µm" in scan:
            size *= 1000.0
        channels.append(AFMChannel(name=name, data=data, unit=unit, scan_size_nm=size,
                                   meta={"bytes_per_pixel": bpp, "line_direction": img.get("Line Direction")}))
    return channels


def height_channel(channels: list[AFMChannel]) -> AFMChannel:
    """Pick the calibrated topography channel (prefer 'Height Sensor', then 'Height').

    Fails closed: a height-like channel whose units are not nanometres (e.g. an
    unrecognised scale line left it as raw counts) is never returned, so raw
    integers cannot end up labelled as nm downstream.
    """
    for want in ("height sensor", "height"):
        for ch in channels:
            if ch.name.lower() == want and ch.unit == "nm":
                return ch
    for ch in channels:
        if "height" in ch.name.lower() and ch.unit == "nm":
            return ch
    raise LookupError(f"no calibrated (nm) height channel among {[(c.name, c.unit) for c in channels]}")


def flatten(z: np.ndarray, order: int = 1) -> np.ndarray:
    """Line-by-line polynomial leveling (Nanoscope 'Flatten'), then zero the median.

    AFM scans each row separately, so each row gets its own offset/tilt;
    subtracting a per-row polynomial removes those scan-line artifacts.
    """
    x = np.arange(z.shape[1])
    out = np.empty_like(z)
    for i, row in enumerate(z):
        coeffs = np.polyfit(x, row, order)
        out[i] = row - np.polyval(coeffs, x)
    return out - np.median(out)


def rms_roughness(z: np.ndarray) -> float:
    """Root-mean-square roughness Rq: sqrt(mean((z - mean z)^2))."""
    return float(np.sqrt(np.mean((z - z.mean()) ** 2)))
