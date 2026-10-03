# Modeling the Messy build

Generates `materials-science/investigation.html` in the epistemic-demo fork
(`~/Code/epistemic-demo`, branch `summit-fixes`).

```sh
cd tools/messy_build
git -C ~/Code/epistemic-demo show 72c8d1c:materials-science/investigation.html > original.html
python3 build.py ~/Code/epistemic-demo/materials-science/investigation.html
```

`original.html` is Kathy's pre-polish page. The build pulls the nine embedded datasets from it
byte-for-byte, so data never changes. It is gitignored because it is about 1 MB.

The widgets are in `src/w_*.js`, the shared chart code in `src/core.js`, and the primer cards in
`primer.py`.

Browser checks use Playwright WebKit:
`uv run --with playwright python messy_check.py` (all tabs) and `walk3.py` (outlier lesson).
Before running them, serve the fork and edit the URL at the top of each script.
