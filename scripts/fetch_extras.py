"""Download the non-AFM data used by notebook 07 (PSU network + public key).

- Transport: every resistance-vs-temperature CSV (``*RT*data.csv``) on FeSe samples.
- Raman: one plain-text spectrum per MoS2 / WS2 sample (prefers a "Center" file),
  up to --raman-max samples.
- XRD and SEM examples are already in data/raw/survey/ (samples 20958, 32096).

Writes files to data/raw/extras/raw/ and an index data/raw/extras/fetched.json
(with per-file errors). Resumable. Run from repo root with .env loaded.
"""

from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from camel_data.list_public import PublicLiST  # noqa: E402

RAW = Path("data/raw")
OUT = RAW / "extras/raw"
INDEX = RAW / "extras/fetched.json"


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def pick(files: list[dict], kind: str) -> list[dict]:
    if kind == "transport":
        return [f for f in files if re.search(r"RT.*data\.csv$", f["filename"] or "", re.I)]
    # Raman: plain-text spectra only; instrument code RMN*
    txt = [f for f in files if (f["filename"] or "").lower().endswith(".txt")
           and (f.get("instrument") or "").upper().startswith("RMN")]
    center = [f for f in txt if "center" in f["filename"].lower() or "centre" in f["filename"].lower()]
    return (center or txt)[:1]


def main() -> None:
    raman_max = int(sys.argv[sys.argv.index("--raman-max") + 1]) if "--raman-max" in sys.argv else 120
    OUT.mkdir(parents=True, exist_ok=True)
    samples = json.loads((RAW / "list_samples.json").read_text())
    jobs = [(s["id"], "transport", s["materials"]) for s in samples
            if "Transport" in s["characterizationTechniques"] and any("FeSe" in m for m in s["materials"])]
    raman = [s for s in samples if "Raman" in s["characterizationTechniques"]
             and set(s["materials"]) & {"MoS2", "WS2"}]
    jobs += [(s["id"], "raman", s["materials"]) for s in raman[:raman_max]]
    index = json.loads(INDEX.read_text()) if INDEX.exists() else {}
    client = PublicLiST()

    def run(sid, kind, materials):
        got = []
        for f in pick(client.files(sid), kind):
            path = OUT / f"{sid}_{kind}_{_safe(f['filename'])}"
            if not path.exists():
                path.write_bytes(client.download(f["activity_id"], f["file_id"]))
            got.append({"file": f["filename"], "local": str(path), "instrument": f.get("instrument")})
        return {"sample_id": sid, "kind": kind, "materials": materials, "files": got}

    todo = [j for j in jobs if f"{j[0]}:{j[1]}" not in index]
    print(f"{len(jobs)} jobs ({sum(j[1] == 'transport' for j in jobs)} transport), {len(todo)} to go")
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run, *j): j for j in todo}
        for fut in as_completed(futures):
            sid, kind, _ = futures[fut]
            try:
                index[f"{sid}:{kind}"] = fut.result()
            except Exception as exc:  # noqa: BLE001 — recorded, not swallowed
                index[f"{sid}:{kind}"] = {"sample_id": sid, "kind": kind, "error": f"{type(exc).__name__}: {exc}"}
    INDEX.write_text(json.dumps(index, indent=1))
    n_files = sum(len(v.get("files", [])) for v in index.values())
    n_err = sum("error" in v for v in index.values())
    print(f"done: {n_files} files, {n_err} errors")


if __name__ == "__main__":
    main()
