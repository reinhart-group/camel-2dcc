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


def load_extra(name: str, data_dir: str | Path | None = None):
    """Load a non-AFM file from ``extras/``: ``.csv`` → DataFrame, ``.json`` → dict,
    ``.png`` → 2D NumPy array (grey levels 0-255)."""
    path = _data_dir(data_dir) / "extras" / name
    if path.suffix == ".csv":
        import pandas as pd

        return pd.read_csv(path)
    if path.suffix == ".json":
        return json.loads(path.read_text())
    if path.suffix == ".png":
        from PIL import Image

        return np.asarray(Image.open(path).convert("L"))
    raise ValueError(f"unsupported file type: {name}")


def load_small_maps(data_dir: str | Path | None = None) -> dict[int, np.ndarray]:
    """Every AFM scan shrunk to 64 x 64 (heights in nm), keyed by sample id."""
    blob = np.load(_data_dir(data_dir) / "afm_small.npz")
    return {int(k): blob[k].astype(np.float64) for k in blob.files}


# -- pictures ---------------------------------------------------------------


def _square(scan: AFMScan) -> np.ndarray:
    """The 3D and STL views assume a square scan (every gallery scan is square)."""
    if scan.z.ndim != 2 or scan.z.shape[0] != scan.z.shape[1]:
        raise ValueError(f"{scan.key}: expected a square height map, got shape {scan.z.shape}")
    return scan.z


def surface_3d(scan: AFMScan, exaggeration: float = 1.0, colorscale: str = "Viridis",
               max_pixels: int = 256):
    """Interactive Plotly 3D surface. ``exaggeration`` stretches heights so tiny bumps show."""
    import plotly.graph_objects as go

    z = _square(scan)
    step = max(1, -(-z.shape[0] // max_pixels))  # ceiling division: never exceed max_pixels
    z = z[::step, ::step]
    axis_nm = np.linspace(0, scan.scan_um * 1000, z.shape[0])
    # Colour by the 1st-99th percentile so one dust speck or glitch line
    # doesn't wash out every other feature (the surface itself is unchanged).
    lo, hi = np.percentile(z, [1, 99])
    # Hand Plotly plain Python lists, never numpy arrays. plotly.py 6+ encodes numpy
    # as base64 ("bdata"), which older plotly.js builds silently fail to decode: the
    # axes and colourbar draw and the surface is simply absent. Lists are understood
    # by every version. See PLOTLYJS_URL below for the other half of this.
    fig = go.Figure(go.Surface(
        x=[round(float(v), 3) for v in axis_nm],
        y=[round(float(v), 3) for v in axis_nm],
        z=[[round(float(v), 3) for v in row] for row in z],
        colorscale=colorscale, cmin=float(lo), cmax=float(hi),
        colorbar=dict(title="height (nm)")))
    # Keep x and y true to scale; stretch z by the exaggeration factor.
    z_span = max(float(np.ptp(z)), 1e-9)
    xy_span = scan.scan_um * 1000
    # Plotly boxes get unreadable if the height axis is more than 3x the width,
    # so the stretch is capped; the title reports the stretch actually drawn.
    z_box = min(exaggeration * z_span / xy_span, 3.0)
    shown = z_box * xy_span / z_span
    note = "" if shown >= exaggeration * 0.999 else f" (capped from ×{exaggeration:g})"
    fig.update_layout(
        title=f"{scan.title} — {scan.scan_um:g} µm × {scan.scan_um:g} µm, heights ×{shown:.0f}{note}",
        scene=dict(xaxis_title="x (nm)", yaxis_title="y (nm)", zaxis_title="height (nm)",
                   aspectmode="manual", aspectratio=dict(x=1, y=1, z=z_box)),
        height=600, margin=dict(l=0, r=0, t=50, b=0),
    )
    return _Viewable(fig)


# plotly.py 7.0.0 reports get_plotlyjs_version() == "4.0.0" while writing arrays in the
# 6.x+ base64 format, so include_plotlyjs="cdn" loads a 2019 build that cannot read its
# own output. Pin a version confirmed to render these figures on a phone instead of
# trusting the library to describe itself.
PLOTLYJS_URL = "https://cdn.plot.ly/plotly-2.35.2.min.js"


def surface_preview(scan, size: int = 320, exaggeration: float = 1.0) -> str:
    """A still 3D render of a scan as a base64 PNG, drawn with matplotlib.

    Used as the poster image for a lazily-drawn Plotly scene, so a page can show several
    scans while only ever holding one live WebGL context (see ``figure_html``).
    """
    import base64
    import io

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    z = _square(scan)
    step = max(1, -(-z.shape[0] // 120))
    z = z[::step, ::step]
    lo, hi = np.percentile(z, [1, 99])
    grid = np.linspace(0, scan.scan_um * 1000, z.shape[0])
    xx, yy = np.meshgrid(grid, grid)
    fig, ax = plt.subplots(figsize=(size / 100, size / 100 * 0.78), dpi=100,
                           subplot_kw={"projection": "3d"})
    ax.plot_surface(xx, yy, z * exaggeration, cmap="viridis", vmin=lo, vmax=hi,
                    linewidth=0, antialiased=False, rcount=90, ccount=90)
    ax.set_axis_off()
    ax.view_init(elev=42, azim=-56)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=False)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def figure_html(fig, height: int = 520, url: str = PLOTLYJS_URL, preview: str | None = None) -> str:
    """Self-contained HTML for a Plotly figure that actually draws inside Colab.

    Plotly's own ``to_html(include_plotlyjs="cdn")`` emits a plain ``<script src>`` tag. That
    is enough in JupyterLab and not enough in Colab: Colab defines requirejs, and plotly.js
    is a UMD bundle, so with ``define.amd`` present it registers as an anonymous AMD module
    and never assigns ``window.Plotly``. The following ``Plotly.newPlot`` call then throws and
    the reader is left with an empty box -- axes, colourbar and all, but no data.

    So load the library by hand with AMD hidden for the duration, put ``define`` back
    afterwards, and only then draw. The figure travels as JSON from ``to_json()``, which is
    free of the base64 array encoding as long as the trace was built from Python lists.
    """
    import json
    import uuid

    spec = json.loads(fig.to_json())
    if preview is not None:
        return _lazy_figure_html(spec, preview, height, url)
    if "bdata" in json.dumps(spec)[:200000]:  # pragma: no cover - guarded by tests
        raise ValueError("figure contains base64 arrays; build traces from Python lists")
    div = "camel-plot-" + uuid.uuid4().hex[:12]
    return (
        f'<div id="{div}" style="height:{height}px;width:100%;"></div>\n'
        "<script>(function(){\n"
        f'  var spec = {json.dumps(spec, separators=(",", ":"))};\n'
        f'  var el = document.getElementById("{div}");\n'
        "  function draw(){ Plotly.newPlot(el, spec.data, spec.layout, {responsive:true}); }\n"
        "  if (window.Plotly) { draw(); return; }\n"
        "  var amd = window.define; window.define = undefined;\n"
        "  var s = document.createElement('script');\n"
        f'  s.src = "{url}"; s.charset = "utf-8";\n'
        "  s.onload = function(){ window.define = amd; draw(); };\n"
        "  s.onerror = function(){ window.define = amd; el.innerHTML =\n"
        "    \"<p style='font:14px system-ui;color:#b45309'>This 3D picture needs to fetch a \"+\n"
        "    \"drawing library from the internet, and the connection blocked it. Every other \"+\n"
        "    \"picture in these notebooks works offline.</p>\"; };\n"
        "  document.head.appendChild(s);\n"
        "})();</script>"
    )


def surface_gallery_html(entries, height: int = 420, url: str = PLOTLYJS_URL) -> str:
    """Several scans in ONE output, sharing a single 3D view.

    Two facts, both measured on the operator's device on 2026-09-16, force this shape:

    1. A Colab page in Safari cannot hold more than one live Plotly 3D scene. With three on
       screen every one fires ``webglcontextlost`` and drops to a 0x0 drawing buffer,
       including the newest. Alone on a page, a scene draws perfectly.
    2. Colab renders each cell's output in its own iframe, so code in one output cannot
       reach or tear down a plot in another. Coordinating across outputs is impossible;
       coordinating inside one output is trivial.

    So all the scans live in a single output that owns exactly one plot container. Choosing a
    scan purges the previous one before drawing the next, and the WebGL context budget never
    exceeds one. Each scan also carries a still render, shown until the reader asks for 3D and
    restored if the view is ever reclaimed, so the page is never empty.

    ``entries`` is a sequence of ``(name, caption, plotly_spec_dict, preview_png_base64)``.
    """
    import json
    import uuid

    uid = "camel-gal-" + uuid.uuid4().hex[:10]
    items = [{"name": n, "caption": c, "spec": spec, "png": png} for n, c, spec, png in entries]
    buttons = "".join(
        f'<button data-i="{i}" class="{uid}-pick" style="padding:9px 13px;margin:3px;'
        'font-size:14px;border-radius:7px;border:1px solid #2b6cb0;background:#fff;color:#2b6cb0">'
        f'{e["name"]}</button>' for i, e in enumerate(items))
    return (
        f'<div style="font-family:-apple-system,system-ui,sans-serif">\n'
        f'  <div>{buttons}</div>\n'
        f'  <p id="{uid}-cap" style="font-size:14px;color:#374151;margin:8px 2px"></p>\n'
        f'  <div style="position:relative;height:{height}px;width:100%">\n'
        f'    <img id="{uid}-img" style="width:100%;height:100%;object-fit:contain" alt="3D view">\n'
        f'    <div id="{uid}-plot" style="display:none;height:{height}px;width:100%"></div>\n'
        f'    <button id="{uid}-go" style="position:absolute;left:50%;bottom:6px;'
        'transform:translateX(-50%);padding:11px 18px;font-size:15px;border-radius:8px;'
        'border:1px solid #2b6cb0;background:#2b6cb0;color:#fff">spin it</button>\n'
        "  </div>\n</div>\n"
        "<script>(function(){\n"
        f'  var items = {json.dumps(items, separators=(",", ":"))};\n'
        f'  var img = document.getElementById("{uid}-img"), el = document.getElementById("{uid}-plot");\n'
        f'  var go = document.getElementById("{uid}-go"), cap = document.getElementById("{uid}-cap");\n'
        "  var cur = 0, live = false;\n"
        "  function still(){\n"
        "    if (live) { try { Plotly.purge(el); } catch(e){} live = false; }\n"
        "    el.style.display = 'none'; img.style.display = ''; go.style.display = '';\n"
        "    go.textContent = 'spin it';\n"
        "  }\n"
        "  function show(i){\n"
        "    cur = i; still();\n"
        "    img.src = 'data:image/png;base64,' + items[i].png;\n"
        "    cap.textContent = items[i].caption;\n"
        f'    Array.prototype.forEach.call(document.querySelectorAll(".{uid}-pick"), function(b){{\n'
        "      var on = +b.getAttribute('data-i') === i;\n"
        "      b.style.background = on ? '#2b6cb0' : '#fff';\n"
        "      b.style.color = on ? '#fff' : '#2b6cb0';\n"
        "    });\n"
        "  }\n"
        "  function draw(){\n"
        "    if (live) { try { Plotly.purge(el); } catch(e){} }\n"
        "    img.style.display = 'none'; el.style.display = ''; go.style.display = 'none';\n"
        "    live = true;\n"
        "    Plotly.newPlot(el, items[cur].spec.data, items[cur].spec.layout, {responsive:true})\n"
        "      .then(function(){\n"
        "        var cv = el.querySelector('canvas');\n"
        "        if (cv) cv.addEventListener('webglcontextlost', function(){\n"
        "          still(); go.textContent = 'the browser reclaimed the 3D view \u2014 tap to redraw';\n"
        "        });\n"
        "      });\n"
        "  }\n"
        f'  Array.prototype.forEach.call(document.querySelectorAll(".{uid}-pick"), function(b){{\n'
        "    b.addEventListener('click', function(){ show(+b.getAttribute('data-i')); });\n"
        "  });\n"
        "  go.addEventListener('click', function(){\n"
        "    if (window.Plotly) { draw(); return; }\n"
        "    go.textContent = 'loading\u2026';\n"
        "    var amd = window.define; window.define = undefined;\n"
        "    var s = document.createElement('script');\n"
        f'    s.src = "{url}"; s.charset = "utf-8";\n'
        "    s.onload = function(){ window.define = amd; draw(); };\n"
        "    s.onerror = function(){ window.define = amd;\n"
        "      go.textContent = 'could not reach the 3D library \u2014 the picture is still real'; };\n"
        "    document.head.appendChild(s);\n"
        "  });\n"
        "  show(0);\n"
        "})();</script>"
    )


def _lazy_figure_html(spec: dict, preview_png: str, height: int, url: str) -> str:
    """A still picture that becomes a live 3D plot when tapped, one at a time.

    Safari in a Colab notebook cannot keep several Plotly 3D scenes alive on one page: with
    three on screen every one of them loses its WebGL context and goes blank, while a single
    scene on its own page draws perfectly. Measured on the operator's device, 2026-09-16.

    So each scan ships as a poster image and is drawn only on request, and starting one tears
    the previous one down with ``Plotly.purge``. At most one live context exists at any moment,
    which is the condition under which 3D is known to work here.
    """
    import json
    import uuid

    div = "camel-plot-" + uuid.uuid4().hex[:12]
    return (
        f'<div id="{div}-wrap" style="position:relative;height:{height}px;width:100%">\n'
        f'  <img id="{div}-img" src="data:image/png;base64,{preview_png}" alt="3D view of the scan"'
        '   style="width:100%;height:100%;object-fit:contain">\n'
        f'  <div id="{div}" style="display:none;height:{height}px;width:100%"></div>\n'
        f'  <button id="{div}-go" style="position:absolute;left:50%;bottom:8px;'
        'transform:translateX(-50%);padding:11px 18px;font-size:15px;border-radius:8px;'
        'border:1px solid #2b6cb0;background:#2b6cb0;color:#fff">spin this one</button>\n'
        "</div>\n"
        "<script>(function(){\n"
        f'  var spec = {json.dumps(spec, separators=(",", ":"))};\n'
        f'  var el = document.getElementById("{div}"), img = document.getElementById("{div}-img");\n'
        f'  var btn = document.getElementById("{div}-go");\n'
        "  window.__camelLive = window.__camelLive || null;\n"
        "  function release(){\n"
        "    var live = window.__camelLive;\n"
        "    if (live && live.el !== el){ try { Plotly.purge(live.el); } catch(e){}\n"
        "      live.el.style.display = 'none'; live.img.style.display = ''; live.btn.style.display = '';\n"
        "    }\n"
        "  }\n"
        "  function draw(){\n"
        "    release();\n"
        "    img.style.display = 'none'; el.style.display = ''; btn.style.display = 'none';\n"
        f'    window.__camelLive = {{el: el, img: img, btn: btn}};\n'
        "    Plotly.newPlot(el, spec.data, spec.layout, {responsive:true}).then(function(){\n"
        "      var cv = el.querySelector('canvas');\n"
        "      if (cv) cv.addEventListener('webglcontextlost', function(){\n"
        "        el.style.display = 'none'; img.style.display = ''; btn.style.display = '';\n"
        "        btn.textContent = 'the browser reclaimed the 3D view \u2014 tap to redraw';\n"
        "      });\n"
        "    });\n"
        "  }\n"
        "  btn.addEventListener('click', function(){\n"
        "    if (window.Plotly) { draw(); return; }\n"
        "    btn.textContent = 'loading\u2026';\n"
        "    var amd = window.define; window.define = undefined;\n"
        "    var s = document.createElement('script');\n"
        f'    s.src = "{url}"; s.charset = "utf-8";\n'
        "    s.onload = function(){ window.define = amd; draw(); };\n"
        "    s.onerror = function(){ window.define = amd;\n"
        "      btn.textContent = 'could not reach the 3D library \u2014 the picture above is still real'; };\n"
        "    document.head.appendChild(s);\n"
        "  });\n"
        "})();</script>"
    )


class _Viewable:
    """Wraps a Plotly figure so ``.show()`` leaves a picture behind in the saved notebook.

    Plotly's own ``show()`` stores a mime bundle that a reader only sees while a kernel is
    attached: opening the notebook on a phone, or in Colab without signing in, shows an empty
    space. Writing the figure out as self-contained HTML keeps it interactive for every reader.
    """

    def __init__(self, fig):
        self.fig = fig

    def __getattr__(self, name):  # update_layout(), add_trace(), ... still work
        return getattr(self.fig, name)

    def to_html(self, height: int = 520, **kw):
        if kw:
            kw.setdefault("include_plotlyjs", PLOTLYJS_URL)
            kw.setdefault("full_html", False)
            return self.fig.to_html(**kw)
        return figure_html(self.fig, height=height)

    def _repr_html_(self):
        return self.to_html()

    def show(self, **kw):
        from IPython.display import HTML, display

        display(HTML(self.to_html()))


def show(fig, **kw):
    """Display any Plotly figure so the saved output survives without a running kernel."""
    _Viewable(fig).show(**kw)


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


def stl_height_range_nm(scan: AFMScan) -> tuple[float, float]:
    """The (low, high) heights in nm that ``to_stl`` stretches to ``relief_mm``.

    It uses the 0.5th and 99.5th percentiles, so a few spike pixels don't set
    the scale. Vertical scale factor of a print = relief_mm / (high - low).
    """
    lo, hi = np.percentile(scan.z, [0.5, 99.5])
    return float(lo), float(hi)


def to_stl(scan: AFMScan, path: str | Path, width_mm: float = 100.0, relief_mm: float = 15.0,
           base_mm: float = 3.0, max_pixels: int = 150) -> Path:
    """Write a closed, printable binary STL of the surface.

    The print is ``width_mm`` wide; the tallest feature rises ``relief_mm``
    above a solid ``base_mm`` slab. Returns the path.
    """
    z = _square(scan)
    step = max(1, -(-z.shape[0] // max_pixels))  # ceiling division: never exceed max_pixels
    z = z[::step, ::step]
    n = z.shape[0]
    lo, hi = stl_height_range_nm(scan)
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
