#!/usr/bin/env bash
# Run notebooks in a real Colab VM the way students do: each notebook gets a fresh
# kernel, and the data comes from the SharePoint link (no local zip on the VM).
#
#   scripts/colab_check.sh SESSION notebooks/05_chips_for_ai.ipynb notebooks/algebra1/A1_zoom_in.ipynb ...
#
# Prints one line per notebook: code-cell count and any error outputs.
set -u
SESSION="$1"; shift
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
# `colab status` does not fail for a pruned session, so look the name up in the live list.
if ! timeout 60 colab sessions 2>/dev/null | grep -q "\[$SESSION\]"; then
  timeout 200 colab new -s "$SESSION" | tail -1
fi
echo "import os, shutil; shutil.rmtree('/content/camel-2dcc', ignore_errors=True); [os.remove(p) for p in ['/content/camel-2dcc-v1.zip'] if os.path.exists(p)]" \
  | timeout 60 colab exec -s "$SESSION" >/dev/null 2>&1
for nb in "$@"; do
  name="$(basename "$nb" .ipynb)"
  cp "$nb" "$WORK/"
  timeout 120 colab restart-kernel -s "$SESSION" >/dev/null 2>&1
  (cd "$WORK" && timeout 900 colab exec -s "$SESSION" -f "$name.ipynb" --timeout 600 > "$name.log" 2>&1)
  if [ -f "$WORK/${name}_output.ipynb" ]; then
    "$ROOT/.venv/bin/python" - "$WORK/${name}_output.ipynb" "$name" <<'PY'
import sys, nbformat
nb = nbformat.read(sys.argv[1], 4)
errs = [(i, o.get("ename"), str(o.get("evalue"))[:120]) for i, c in enumerate(nb.cells)
        if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
print(f"{sys.argv[2]:40s} code cells {sum(c.cell_type == 'code' for c in nb.cells):3d}  errors {errs}")
PY
  else
    echo "$name NO OUTPUT: $(tail -2 "$WORK/$name.log")"
  fi
done
echo "outputs kept in $WORK"
