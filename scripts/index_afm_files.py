"""Stage 1 of the slice build: list every file on every public AFM sample.

Writes data/raw/afm_files.json ({sample_id: [file, ...]}). Resumable: samples
already in the output are skipped. Run from the repo root:

    set -a; . ./.env; set +a; .venv/bin/python scripts/index_afm_files.py
"""

from __future__ import annotations

import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from camel_data.list_public import PublicLiST  # noqa: E402

RAW = Path("data/raw")
OUT = RAW / "afm_files.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("index")


def main() -> None:
    samples = json.loads((RAW / "list_samples.json").read_text())
    afm_ids = [s["id"] for s in samples if "AFM" in s["characterizationTechniques"]]
    index = json.loads(OUT.read_text()) if OUT.exists() else {}
    todo = [i for i in afm_ids if str(i) not in index]
    log.info("%d AFM samples, %d already indexed, %d to go", len(afm_ids), len(index), len(todo))
    client = PublicLiST()
    errors = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(client.files, sid): sid for sid in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            sid = futures[fut]
            try:
                index[str(sid)] = fut.result()
            except Exception as exc:  # noqa: BLE001 — recorded, not swallowed
                errors[str(sid)] = repr(exc)
                log.warning("sample %s: %r", sid, exc)
            if n % 100 == 0:
                OUT.write_text(json.dumps(index))
                log.info("%d/%d", n, len(todo))
    OUT.write_text(json.dumps(index))
    (RAW / "afm_files_errors.json").write_text(json.dumps(errors, indent=1))
    log.info("done: %d indexed, %d errors", len(index), len(errors))


if __name__ == "__main__":
    main()
