"""Stage 2: download one primary AFM height scan per sample and measure it.

For each AFM sample in data/raw/afm_files.json, pick the primary scan
(``.spm``, not an operator-"modified" copy, preferring the largest scan
size), download it to data/raw/spm/, and compute roughness statistics after
line-by-line flattening. Writes:

- data/raw/afm_measurements.json  {sample_id: {...stats, file...}}
- data/raw/afm_measure_errors.json {sample_id: "error"}
- data/raw/afm64/<sample_id>.npy   64x64 float16 flattened height map (nm)

Resumable. Run from repo root with the .env loaded.
"""

from __future__ import annotations

import json
import os
import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from camel_data.list_public import PublicLiST  # noqa: E402
from camel_data.spm import flatten, height_channel, read_spm, rms_roughness  # noqa: E402

RAW = Path("data/raw")
SPM_DIR = RAW / "spm"
SMALL_DIR = RAW / "afm64"
OUT = RAW / "afm_measurements.json"
ERR = RAW / "afm_measure_errors.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("measure")

# Scan-size hints in operator filenames: "5by5um", "1x1um", "center5um", "_2um".
# The rule is a fixed tie-breaker, not a scientific choice of "best" scan;
# afm_summary.csv records the chosen scan's size so comparisons can control for it.
_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:(?:by|x)\s*\d+(?:\.\d+)?\s*)?um", re.I)


def _scan_hint_um(name: str) -> float:
    m = _SIZE_RE.search(name)
    return float(m.group(1)) if m else 0.0


def pick_primary(files: list[dict]) -> dict | None:
    spm = [f for f in files if (f.get("filename") or "").lower().endswith(".spm")]
    if not spm:
        return None
    unmodified = [f for f in spm if "modif" not in f["filename"].lower()] or spm
    return max(unmodified, key=lambda f: (_scan_hint_um(f["filename"]), -len(f["filename"])))


def downsample(z: np.ndarray, n: int = 64) -> np.ndarray:
    """Average into an n x n grid covering the whole scan (no cropping).

    Rows and columns are split into n nearly equal bins, so every pixel lands
    in exactly one output cell. A non-square scan is squeezed into a square
    grid; afm_summary.csv records the original lines and pixels per line.
    """
    rows = np.array_split(np.arange(z.shape[0]), n)
    cols = np.array_split(np.arange(z.shape[1]), n)
    return np.array([[z[np.ix_(r, c)].mean() for c in cols] for r in rows])


def measure(client: PublicLiST, sid: str, files: list[dict]) -> dict:
    f = pick_primary(files)
    if f is None:
        raise LookupError("no .spm file on this sample")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", f["filename"])
    path = SPM_DIR / f"{sid}_{safe}"
    if not path.exists():
        # Write to a temp name and rename only after it parses, so an
        # interrupted or error-body download is never cached as the real file.
        tmp = path.with_name(path.name + ".part")
        tmp.write_bytes(client.download(f["activity_id"], f["file_id"]))
        read_spm(tmp)
        tmp.replace(path)
    h = height_channel(read_spm(path))
    z = flatten(h.data)
    SMALL_DIR.mkdir(parents=True, exist_ok=True)
    np.save(SMALL_DIR / f"{sid}.npy", downsample(z).astype(np.float16))
    return {
        "file": f["filename"], "local": str(path), "activity_id": f["activity_id"], "file_id": f["file_id"],
        "instrument": f.get("instrument"), "channel": h.name,
        "scan_size_um": round(h.scan_size_nm / 1000, 4), "pixels": int(h.data.shape[1]),
        "lines": int(h.data.shape[0]),  # fewer lines than pixels = the scan stopped early
        "rms_nm": round(rms_roughness(z), 4),
        "ra_nm": round(float(np.mean(np.abs(z - z.mean()))), 4),
        "range_nm": round(float(np.ptp(z)), 4),
        "p1_p99_nm": round(float(np.percentile(z, 99) - np.percentile(z, 1)), 4),
        "n_spm_files": sum((x.get("filename") or "").lower().endswith(".spm") for x in files),
    }


def main() -> None:
    SPM_DIR.mkdir(parents=True, exist_ok=True)
    index = json.loads((RAW / "afm_files.json").read_text())
    # --remeasure recomputes every sample (cached .spm files are reused, so
    # this is offline for samples already downloaded).
    done = json.loads(OUT.read_text()) if OUT.exists() and "--remeasure" not in sys.argv else {}
    errors = {}
    todo = [s for s in index if s not in done]
    log.info("%d indexed samples, %d measured, %d to go", len(index), len(done), len(todo))
    client = PublicLiST()
    with ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "4"))) as pool:
        futures = {pool.submit(measure, client, sid, index[sid]): sid for sid in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            sid = futures[fut]
            try:
                done[sid] = fut.result()
            except Exception as exc:  # noqa: BLE001 — recorded with type and message
                errors[sid] = f"{type(exc).__name__}: {exc}"
            if n % 50 == 0:
                OUT.write_text(json.dumps(done))
                log.info("%d/%d measured, %d errors", n, len(todo), len(errors))
    OUT.write_text(json.dumps(done))
    ERR.write_text(json.dumps(errors, indent=1))
    log.info("done: %d measured, %d errors", len(done), len(errors))


if __name__ == "__main__":
    main()
