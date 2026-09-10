"""Stage 3: fetch compacted growth recipes for every public sample that has one.

Writes data/raw/recipes.json ({sample_id: [recipe, ...]}) and
data/raw/recipes_errors.json. Resumable. Run from repo root with .env loaded.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from psu_list.client import ListClient
from psu_list.config import ListConfig

RAW = Path("data/raw")
OUT = RAW / "recipes.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("recipes")


def main() -> None:
    samples = json.loads((RAW / "list_samples.json").read_text())
    ids = [str(s["id"]) for s in samples if s["synthesisTechniques"]]
    done = json.loads(OUT.read_text()) if OUT.exists() else {}
    todo = [i for i in ids if i not in done]
    log.info("%d samples with synthesis, %d done, %d to go", len(ids), len(done), len(todo))
    client = ListClient(ListConfig.from_env())
    errors = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(client.recipes, sid): sid for sid in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            sid = futures[fut]
            try:
                done[sid] = fut.result()
            except Exception as exc:  # noqa: BLE001 — recorded with type and message
                errors[sid] = f"{type(exc).__name__}: {exc}"
            if n % 100 == 0:
                OUT.write_text(json.dumps(done))
                log.info("%d/%d, %d errors", n, len(todo), len(errors))
    OUT.write_text(json.dumps(done))
    (RAW / "recipes_errors.json").write_text(json.dumps(errors, indent=1))
    log.info("done: %d fetched, %d errors, %d with a recipe", len(done), len(errors),
             sum(bool(v) for v in done.values()))


if __name__ == "__main__":
    main()
