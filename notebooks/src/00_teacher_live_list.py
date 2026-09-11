# %% [markdown]
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reinhart-group/camel-2dcc/blob/main/notebooks/00_teacher_live_list.ipynb)

# %% [markdown]
# # Teacher & Researcher Guide: Live LiST Access
#
# The classroom notebooks (01–05) all run on an offline **data slice** — a downloaded snapshot of
# 2DCC-MIP's public sample database, so a class doesn't need special network access or credentials.
# This notebook is for **teachers and researchers**, not students. It shows how to reach the real,
# live database those slices are built from, using a public, read-only key.
#
# **⚠️ This will not work on a normal (hosted) Colab runtime.** LiST only answers requests that
# reach it from inside the Penn State network. A hosted Colab runtime is a computer on Google's
# infrastructure, not yours — putting *your laptop* on the campus Wi-Fi or GlobalProtect VPN does
# nothing for a hosted Colab kernel, because your laptop isn't where the request comes from. You
# need one of the two setups in **Step 1** below before Tasks 1–4 can reach live data. (Every cell
# still runs without live access — you'll just see friendly "not connected" messages.)
#
# **What you'll do**
# - Get the notebook's *kernel* running somewhere on the Penn State network (Step 1).
# - Set up a LiST API key as an environment variable or Colab Secret (never typed into the notebook itself).
# - Use `PublicLiST`, a small read-only client, to list samples, count AFM scans by material, and
#   fetch one sample's files live.
# - Download one real `.spm` AFM file and check it against the same scan already in the slice.
#
# **Time:** about 20-30 minutes, plus however long it takes to get a key from the project team and
# get a PSU-connected Jupyter kernel running.
#
# **Terms you'll see**
# - **LiST:** the 2DCC-MIP's Lifetime Sample Tracking database — the internal system where every
#   sample, measurement, and file is logged as it's made.
# - **Published record:** a sample LiST's owners have marked public. The public key this notebook
#   uses is intended to see only Published records; Task 1 double-checks that client-side and skips
#   anything else it's ever handed.
# - **API key:** a password-like string that identifies who (or what) is asking LiST for data.
# - **Colab Secret:** Colab's built-in, per-notebook secret storage (🔑 icon in the left sidebar) —
#   the right place for a key, because it's never saved into the notebook file itself. Only relevant
#   if you're using Colab as the *editor* — see Step 2.
# - **Kernel / runtime:** the actual Python process that runs your code. In hosted Colab this is a
#   Google-operated machine, not your computer — which is exactly why it can't reach LiST.
# - **Penn State network / VPN:** LiST only answers requests that reach it from a process actually
#   running on the Penn State campus network, or through Penn State's GlobalProtect VPN. It's the
#   *kernel's* network location that matters, not your browser's.
# - **`.spm` file:** the raw file format written by the Bruker/Veeco AFM instruments at the 2DCC.
# - **Activity / file ID:** LiST's way of organizing a sample's measurements (activities) and the
#   files attached to each one.

# %% [markdown]
# ## 🌐 Step 1 — Get the kernel onto the Penn State network
# Do this **before** worrying about the key — it's the part most setups get wrong. Pick one:
#
# **Option A — Local Jupyter (simplest).** Run this notebook's `.ipynb` file directly in Jupyter
# installed *on a Penn State-connected computer* (on campus Wi-Fi, or off-campus through
# GlobalProtect VPN). Nothing else to configure — the kernel and the network are the same machine.
#
# **Option B — Colab's editor, a local runtime.** If you want Colab's interface specifically, keep
# using it as the *editor*, but point it at a Jupyter server running on your PSU-connected computer
# instead of Google's hosted kernel:
#
# 1. On the PSU-connected computer: `pip install jupyter`
# 2. Start a server that allows Colab's origin:
#    `jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888`
# 3. Copy the `http://localhost:8888/?token=...` URL it prints.
# 4. In Colab: click the **Connect ▾** menu (top right) → **Connect to a local runtime** → paste
#    the URL → **Connect**.
#
# Either way, if the *kernel* isn't on the Penn State network, every live call below prints a short
# friendly message instead of data — that's expected, not a bug, and it's why classroom notebooks
# 01–05 ship an offline slice instead of depending on this. Every cell here is written so the
# notebook finishes top-to-bottom whether or not you're connected.

# %% [markdown]
# ## 🔑 Step 2 — Get a LiST API key
# The public read-only key is **not something you generate yourself** — it comes from the 2DCC-MIP
# project team. Once you have the key text, set it as an environment variable on the machine
# running the kernel (works for Option A, and for Option B since the local Jupyter server is that
# machine too):
#
# ```
# export LIST_API_KEY=paste-the-key-text-here
# ```
#
# *(Using hosted Colab as an editor anyway, just to edit this notebook without running the live
# cells?* You can instead add a Colab Secret: click the **🔑 key icon** in the left sidebar →
# **+ Add new secret** → Name `LIST_API_KEY`, paste the value, toggle **Notebook access** ON. This
# only lets *that* notebook read the key — it still won't let a hosted kernel reach LiST; use it
# only if you're not attempting Tasks 1–4 live.)
#
# *(Optional)* If the team gave you a non-default server address, set `LIST_BASE_URL` the same way.
#
# **Never** paste the key text into a code cell, a markdown cell, or any file you might save or
# share — that defeats the point of using an environment variable or Secret. This notebook never
# displays the key itself, only whether it worked.

# %% [markdown]
# ## 🔧 Setup (run this first)
# This downloads the same offline data slice the classroom notebooks use — we'll use it below to
# check a live download against it.

# %%
DATA_URL = "https://pennstateoffice365-my.sharepoint.com/:u:/g/personal/wfr5091_psu_edu/IQCkNUoFnJNJSK8lUEepTJeSAT3NukSFJzB9-9fS5GB5mp0?e=KafIFG"  # teacher: the only line you may need to change

import io, json, os, shutil, sys, zipfile, requests
def _ready():  # a complete copy has its manifest and every file it lists
    try:
        m = json.load(open("camel-2dcc/manifest.json"))
        return m["release_id"] == "camel-2dcc-v1" and all(os.path.exists("camel-2dcc/" + f["path"]) for f in m["files"])
    except (OSError, ValueError, KeyError):
        return False
if not _ready():
    shutil.rmtree("camel-2dcc", ignore_errors=True)  # clear any half-finished copy
    if os.path.exists("camel-2dcc-v1.zip"):
        zip_bytes = open("camel-2dcc-v1.zip", "rb").read()
    else:
        r = requests.get(DATA_URL + ("&" if "?" in DATA_URL else "?") + "download=1", timeout=120)
        r.raise_for_status()
        zip_bytes = r.content
    if zip_bytes[:2] != b"PK":
        raise RuntimeError("The download was not the data file. Check DATA_URL, or upload camel-2dcc-v1.zip "
                           "with the Files panel and run this cell again.")
    zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(".")
    if not _ready():
        raise RuntimeError("The data file is incomplete or the wrong version. Download camel-2dcc-v1.zip again.")
sys.path.insert(0, "camel-2dcc")
import importlib, camel_data.classroom  # reload so an updated data file never runs old helper code
importlib.reload(camel_data.classroom)
try:
    from google.colab import output
    output.enable_custom_widget_manager()
except ImportError:
    pass  # running outside Colab
from camel_data.classroom import *
print("✅ Data ready:", sorted(os.listdir("camel-2dcc"))[:6], "...")

# %% [markdown]
# ## Step 3 — Connect
# The data slice's `camel_data` package doesn't ship `PublicLiST` (it needs a live key, which the
# slice deliberately has no route to) — so here it is, copied straight from
# `src/camel_data/list_public.py` in the CAMEL repo (keep this copy in sync with that file by hand;
# there's no shared-import mechanism between the repo and a notebook running from an unzipped
# slice). `get_client()` wraps connecting in a try/except so a failure — missing key, wrong key, or
# off-network — prints one friendly line instead of a traceback.

# %%
# @title Helper code (just run this)

DEFAULT_BASE_URL = "https://m4-2dcc.vmhost.psu.edu/list/api/v2"
KEY_HEADER = "X-API-KEY"


def _api_key() -> str:
    missing = RuntimeError(
        "No LiST key found. Set the LIST_API_KEY environment variable, or in Colab "
        "add a Secret named LIST_API_KEY (key icon in the left sidebar) and allow "
        "this notebook to use it."
    )
    key = (os.environ.get("LIST_API_KEY") or "").strip()
    if key:
        return key
    try:  # Colab Secrets
        from google.colab import userdata  # type: ignore
        key = (userdata.get("LIST_API_KEY") or "").strip()
    except Exception as exc:  # noqa: BLE001 — re-raised with a clear message
        raise missing from exc
    if not key:
        raise missing
    return key


class PublicLiST:
    """Tiny read-only client for public LiST records."""

    def __init__(self, base_url=None, api_key=None, timeout: float = 60.0):
        env_base = os.environ.get("LIST_BASE_URL")
        self.base_url = base_url or (env_base.rstrip("/") + "/api/v2" if env_base else DEFAULT_BASE_URL)
        self.session = requests.Session()
        self.session.headers.update({KEY_HEADER: api_key or _api_key(), "Accept": "application/json"})
        self.timeout = timeout

    def _call(self, method: str, path: str, **kwargs):
        try:
            r = self.session.request(method, self.base_url + path, timeout=self.timeout, **kwargs)
        except requests.ConnectionError as exc:
            raise ConnectionError(
                "Could not reach LiST. It only answers from the Penn State network "
                "(campus Wi-Fi or GlobalProtect VPN). Off campus, use the SharePoint data slice."
            ) from exc
        if r.status_code in (401, 403):
            raise PermissionError(f"LiST rejected the API key (HTTP {r.status_code}).")
        r.raise_for_status()
        return r

    def samples(self, page_size: int = 500):
        """Every published sample (pages through the whole public catalog)."""
        rows, start = [], 0
        while True:
            payload = self._call("POST", "/samples/search", json={},
                                 params={"start": start, "length": page_size,
                                         "draw": start // page_size + 1}).json()
            batch = payload.get("data") or []
            rows.extend(batch)
            start += len(batch)
            if not batch or start >= payload.get("recordsFiltered", start):
                return rows

    def sample(self, sample_id: int):
        return self._call("GET", f"/samples/{sample_id}").json()

    def activities(self, sample_id: int):
        return self._call("GET", f"/samples/{sample_id}/activities").json()

    def files(self, sample_id: int):
        """Flat list of downloadable files across a sample's activities."""
        out = []
        for act in self.activities(sample_id):
            for group in act.get("files") or []:
                for f in group.get("files") or []:
                    out.append({"activity_id": act.get("id"), "file_id": f.get("id"),
                                "filename": f.get("filename"), "instrument": act.get("instrument"),
                                "activity_type": act.get("type")})
        return out

    def download(self, activity_id: int, file_id: int) -> bytes:
        return self._call("GET", f"/sample-activities/{activity_id}/files/{file_id}").content

    def afm_samples(self):
        return [s for s in self.samples() if "AFM" in (s.get("characterizationTechniques") or [])]


LIVE_ERRORS = (ConnectionError, PermissionError, RuntimeError, requests.exceptions.RequestException)


def safe_call(label, fn):
    """Run fn(); on any documented live-data failure, print one friendly line and return None."""
    try:
        return fn()
    except LIVE_ERRORS as exc:
        print(f"⚠️  {label}: {exc}")
        return None


def get_client():
    return safe_call("Connecting to LiST", lambda: PublicLiST())

# %%
client = get_client()
print("Connected." if client is not None else "Not connected — the live cells below will skip gracefully.")

# %% [markdown]
# ## Task 1 — List samples
# `PublicLiST.samples()` pages through every sample the key can see and returns it as a list of
# dicts. The public key is *intended* to see only `status == "Published"` records — but that's a
# server-side promise, not something the client can verify on its own, so we double-check every
# record before showing it and skip (with a warning) anything that isn't actually Published.

# %%
def published_only(records, label="samples"):
    """Keep only status == 'Published' records; warn and drop anything else."""
    ok = [r for r in records if r.get("status") == "Published"]
    skipped = len(records) - len(ok)
    if skipped:
        print(f"⚠️  Skipped {skipped} {label} whose status was not 'Published' "
              f"(unexpected for this key — worth reporting to the project team).")
    return ok


live_samples = client and safe_call("Listing samples", client.samples)
if live_samples is not None:
    live_samples = published_only(live_samples, "samples")
    print(f"{len(live_samples)} published samples right now.")
    print("Example record keys:", sorted(live_samples[0].keys())[:8], "...")

# %% [markdown]
# ## Task 2 — Count AFM samples by material
# `afm_samples()` filters to samples whose `characterizationTechniques` list includes `"AFM"`, then
# we count materials the same messy way notebook 05 does — a sample can list more than one.

# %%
if client is not None:
    afm_live = safe_call("Listing AFM samples", client.afm_samples)
    if afm_live is not None:
        afm_live = published_only(afm_live, "AFM samples")
        from collections import Counter
        live_counts = Counter(m for s in afm_live for m in (s.get("materials") or []))
        print(f"{len(afm_live)} live AFM samples.")
        print("Top materials (live):", live_counts.most_common(5))

        slice_samples = load_table("samples")
        n_afm_slice = slice_samples["measurements"].str.contains("AFM", na=False).sum()
        print(f"AFM samples in the offline slice: {n_afm_slice}")
        print("These two counts can differ slightly — the live database keeps changing (new "
              "samples are added and existing ones are re-classified) after each slice is built.")

# %% [markdown]
# ## Task 3 — One sample's file list
# Every scan in the gallery notebooks 01–05 use came from a real sample. Here's the "Atomic
# staircase" scan's sample (id 20390) — fetched live, straight from LiST.

# %%
sample_files = None
if client is not None:
    sample_id = 20390  # <-- change me: try another sample_id, e.g. from samples.csv
    sample_files = safe_call(f"Listing files for sample {sample_id}", lambda: client.files(sample_id))
    if sample_files is not None:
        for f in sample_files:
            print(f["filename"], "-", f["instrument"])

# %% [markdown]
# ## Task 4 — Download a real `.spm` file, and check it against the slice
# `camel_data.spm` (shipped in the data slice) reads the raw Nanoscope `.spm` format. We'll
# download the same file the "Atomic staircase" gallery scan was built from, and compare its RMS
# roughness with the pre-processed version already in the slice.

# %%
if client is not None and sample_files is not None:
    from camel_data.spm import read_spm, height_channel, flatten, rms_roughness

    spm_file = next((f for f in sample_files if f["filename"].lower().endswith(".spm")), None)
    raw_bytes = spm_file and safe_call("Downloading the .spm file",
                                       lambda: client.download(spm_file["activity_id"], spm_file["file_id"]))
    if raw_bytes is not None:
        with open("live_download.spm", "wb") as fh:
            fh.write(raw_bytes)
        channels = read_spm("live_download.spm")
        live_height = flatten(height_channel(channels).data)
        live_rms = rms_roughness(live_height)

        slice_scan = load_gallery()["atomic_staircase"]
        print(f"Live download:  {len(raw_bytes):,} bytes, shape {live_height.shape}, "
              f"RMS roughness = {live_rms:.4f} nm")
        print(f"Slice version:  shape {slice_scan.z.shape}, "
              f"RMS roughness = {rms(slice_scan.z):.4f} nm")
        print("Match!" if abs(live_rms - rms(slice_scan.z)) < 0.001 else
              "Close, but not identical — that can happen if the slice was rebuilt from a "
              "different version of the file, or with different rounding.")

# %% [markdown]
# ## What's in the offline slice
# For reference, here's what `camel-2dcc-v1.zip` (used by notebooks 01–05) actually contains:
#
# | File | What it holds |
# |------|----------------|
# | `samples.csv` | Every public sample: material, substrate, growth method, measurements, dates, data package, DOI. |
# | `afm_summary.csv` | One selected AFM height scan per sample (a fixed pick-one-scan rule, not every scan taken): scan size, pixels, RMS/average roughness, height range. |
# | `afm_small.npz` | Every AFM scan shrunk to 64x64 heights (nm), keyed by sample id. |
# | `afm_gallery/*.npz` + `gallery.json` | Hand-picked full-resolution height maps used in the notebooks. |
# | `growth_recipes.csv` | Step-by-step growth recipes (MOCVD and Hybrid MBE): step name, duration, start time, temperature, pressure. |
# | `growth_summary.csv` | One row per grown sample: total growth time, growth temperature/pressure, joined to AFM roughness when measured. |
# | `chips_timeline.csv`, `materials_reference.csv`, `superconductors.csv` | Curated context tables — see `SOURCES.md`. |
# | `stl/*.stl` | 3D-printable AFM surfaces. |
# | `camel_data/` | The `classroom.py` and `spm.py` helpers the notebooks import (no `list_public.py` — that needs a live key). |
# | `manifest.json` | Every file's size and SHA-256 checksum. |

# %% [markdown]
# ## Rebuilding or updating a slice
# Building a slice is a two-stage process, and only the first stage needs `PublicLiST` or the
# Penn State network:
#
# 1. **Network stage — run on a Penn State-connected machine**, in order: `scripts/index_afm_files.py`
#    (lists every public sample's files), `scripts/build_afm_summary.py` (downloads and measures one
#    primary AFM scan per sample), `scripts/fetch_recipes.py` (pulls growth recipes), and
#    `scripts/fetch_gallery_candidates.py` (pulls the hand-picked gallery scans). These are the
#    scripts that actually use `PublicLiST`, one call at a time, with a key that has the right
#    access — never run from inside a shared classroom notebook.
# 2. **Offline assembly — `scripts/build_slice.py`.** This stage touches no network at all; it just
#    reads the JSON/CSV files the network stage staged under `data/raw/` and `data/curated/`, and
#    assembles `data/slice/camel-2dcc/` and the `camel-2dcc-v1.zip` that ships to classrooms.
#
# If your school or district needs a refreshed slice (new samples added, a fixed data-entry typo,
# etc.), re-run stage 1 from the Penn State network, then stage 2 locally — `build_slice.py` itself
# does not go fetch anything new from LiST.
