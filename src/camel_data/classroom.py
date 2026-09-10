"""Classroom helpers used by the CAMEL Colab notebooks.

Kept small and readable on purpose: teachers may open this file. Everything
here works on the downloaded data slice (no LiST access needed).
"""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA_DIR = Path("camel-2dcc")  # the setup cell unzips the slice here


# -- loading ----------------------------------------------------------------


@dataclass
class AFMScan:
    """One AFM height map. ``z`` is height in nanometres; rows run top to bottom."""

    key: str
    z: np.ndarray
    scan_um: float          # the scan is scan_um x scan_um micrometres
    material: str
    title: str
    story: str              # one or two sentences for students
    sample_id: int
    doi: str | None = None

    @property
    def pixels(self) -> int:
        return self.z.shape[0]

    @property
    def pixel_nm(self) -> float:
        return self.scan_um * 1000 / self.z.shape[1]


def _data_dir(data_dir: str | Path | None) -> Path:
    return Path(data_dir) if data_dir else DATA_DIR


def load_gallery(data_dir: str | Path | None = None) -> dict[str, AFMScan]:
    """All curated scans, keyed by a short name like ``"sapphire_steps"``."""
    root = _data_dir(data_dir) / "afm_gallery"
    meta = json.loads((root / "gallery.json").read_text())
    fields = {"key", "scan_um", "material", "title", "story", "sample_id", "doi"}
    scans = {}
    for item in meta:
        with np.load(root / f"{item['key']}.npz") as blob:
            z = blob["height_nm"].astype(np.float64)
        scans[item["key"]] = AFMScan(z=z, **{k: v for k, v in item.items() if k in fields})
    return scans


def load_table(name: str, data_dir: str | Path | None = None):
    """Load one of the CSV tables (``samples``, ``afm_summary``, ``mbe_recipes``, ``chips``)."""
    import pandas as pd

    return pd.read_csv(_data_dir(data_dir) / f"{name}.csv")


def load_small_maps(data_dir: str | Path | None = None) -> dict[int, np.ndarray]:
    """Every AFM scan shrunk to 64 x 64 (heights in nm), keyed by sample id."""
    blob = np.load(_data_dir(data_dir) / "afm_small.npz")
    return {int(k): blob[k].astype(np.float64) for k in blob.files}


# -- pictures ---------------------------------------------------------------


def surface_3d(scan: AFMScan, exaggeration: float = 1.0, colorscale: str = "Viridis",
               max_pixels: int = 256):
    """Interactive Plotly 3D surface. ``exaggeration`` stretches heights so tiny bumps show."""
    import plotly.graph_objects as go

    z = scan.z
    step = max(1, z.shape[0] // max_pixels)
    z = z[::step, ::step]
    axis_nm = np.linspace(0, scan.scan_um * 1000, z.shape[0])
    fig = go.Figure(go.Surface(x=axis_nm, y=axis_nm, z=z, colorscale=colorscale,
                               colorbar=dict(title="height (nm)")))
    # Keep x and y true to scale; stretch z by the exaggeration factor.
    z_span = max(float(np.ptp(z)), 1e-9)
    xy_span = scan.scan_um * 1000
    fig.update_layout(
        title=f"{scan.title} — {scan.scan_um:g} µm × {scan.scan_um:g} µm, heights ×{exaggeration:g}",
        scene=dict(xaxis_title="x (nm)", yaxis_title="y (nm)", zaxis_title="height (nm)",
                   aspectmode="manual",
                   aspectratio=dict(x=1, y=1, z=min(exaggeration * z_span / xy_span, 3.0))),
        height=600, margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


def explore_3d(scans: dict[str, AFMScan]):
    """Dropdown + sliders for flying over any gallery scan (works in Colab and Jupyter)."""
    import ipywidgets as widgets
    from IPython.display import display

    names = {f"{s.title} ({s.material})": key for key, s in scans.items()}

    def show(sample, exaggeration, colors):
        surface_3d(scans[names[sample]], exaggeration, colors).show()

    ui = widgets.interactive(
        show,
        sample=widgets.Dropdown(options=list(names), description="Sample"),
        exaggeration=widgets.FloatLogSlider(value=50, base=10, min=0, max=3, step=0.1,
                                            description="Stretch ×", continuous_update=False),
        colors=widgets.Dropdown(options=["Viridis", "Cividis", "Inferno", "Earth", "Ice"],
                                description="Colors"),
    )
    display(ui)


def cross_section(scan: AFMScan, row: int):
    """Height along one horizontal line of the scan, as (distance_nm, height_nm)."""
    distance = np.arange(scan.z.shape[1]) * scan.pixel_nm
    return distance, scan.z[row]


def explore_cross_section(scan: AFMScan):
    """Slider that moves a cut line across the map and plots the height profile under it."""
    import ipywidgets as widgets
    import matplotlib.pyplot as plt

    def show(row):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
        extent = [0, scan.scan_um * 1000, scan.scan_um * 1000, 0]
        ax1.imshow(scan.z, cmap="viridis", extent=extent)
        y = row * scan.pixel_nm
        ax1.axhline(y, color="red", lw=2)
        ax1.set(title=scan.title, xlabel="x (nm)", ylabel="y (nm)")
        d, h = cross_section(scan, row)
        ax2.plot(d, h, color="red")
        ax2.set(title="Height along the red line", xlabel="distance (nm)", ylabel="height (nm)")
        ax2.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    widgets.interact(show, row=widgets.IntSlider(value=scan.pixels // 2, min=0,
                                                 max=scan.pixels - 1, description="Line"))


# -- 3D printing ------------------------------------------------------------


def to_stl(scan: AFMScan, path: str | Path, width_mm: float = 100.0, relief_mm: float = 15.0,
           base_mm: float = 3.0, max_pixels: int = 150) -> Path:
    """Write a closed, printable binary STL of the surface.

    The print is ``width_mm`` wide; the tallest feature rises ``relief_mm``
    above a solid ``base_mm`` slab. Returns the path.
    """
    z = scan.z
    step = max(1, z.shape[0] // max_pixels)
    z = z[::step, ::step]
    n = z.shape[0]
    lo, hi = np.percentile(z, 0.5), np.percentile(z, 99.5)  # ignore single-pixel spikes
    top = base_mm + relief_mm * np.clip((z - lo) / max(hi - lo, 1e-12), 0, 1)
    xy = np.linspace(0, width_mm, n)
    X, Y = np.meshgrid(xy, xy[::-1])

    tris = []

    def quad(a, b, c, d):  # two triangles, counter-clockwise seen from outside
        tris.append((a, b, c))
        tris.append((a, c, d))

    P = lambda i, j, h: (X[i, j], Y[i, j], h)  # noqa: E731
    for i in range(n - 1):
        for j in range(n - 1):
            quad(P(i, j, top[i, j]), P(i + 1, j, top[i + 1, j]),
                 P(i + 1, j + 1, top[i + 1, j + 1]), P(i, j + 1, top[i, j + 1]))
            quad(P(i, j, 0), P(i, j + 1, 0), P(i + 1, j + 1, 0), P(i + 1, j, 0))
    for k in range(n - 1):  # four side walls
        for (i0, j0), (i1, j1) in (((0, k), (0, k + 1)), ((n - 1, k + 1), (n - 1, k)),
                                   ((k + 1, 0), (k, 0)), ((k, n - 1), (k + 1, n - 1))):
            quad(P(i0, j0, 0), P(i0, j0, top[i0, j0]), P(i1, j1, top[i1, j1]), P(i1, j1, 0))

    path = Path(path)
    with path.open("wb") as fh:
        fh.write(b"CAMEL 2DCC AFM surface".ljust(80, b" "))
        fh.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            a, b, c = map(np.asarray, (a, b, c))
            nrm = np.cross(b - a, c - a)
            nrm = nrm / (np.linalg.norm(nrm) or 1.0)
            fh.write(struct.pack("<12fH", *nrm, *a, *b, *c, 0))
    return path


# -- statistics helpers -----------------------------------------------------


def rms(z: np.ndarray) -> float:
    """Root-mean-square roughness: the standard deviation of the heights."""
    z = np.asarray(z, dtype=float)
    return float(np.sqrt(np.mean((z - z.mean()) ** 2)))
