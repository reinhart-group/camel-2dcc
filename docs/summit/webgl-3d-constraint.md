# One live 3D view per page

Measured on the operator's device (Safari 26.6.2, macOS, Apple GPU) against Google Colab on
2026-09-16. This is the constraint every 3D figure in this project must respect.

## The rule

**A Colab page may hold at most one live Plotly 3D scene.** With three on a page, every one of
them fires `webglcontextlost` and drops to a 0x0 drawing buffer, including the newest, so the
page shows colour bars and nothing else. With one, it draws perfectly.

Both working arrangements were confirmed on the device:

- One Plotly 3D figure, alone in a notebook.
- Several scans sharing a single viewer inside **one output**, where selecting a scan calls
  `Plotly.purge` on the previous before drawing the next.

## Why the obvious fix does not work

Colab renders each cell's output in its own iframe. `window` is not shared between outputs, so
JavaScript in one output cannot see or tear down a plot in another, while the WebGL context
budget belongs to the whole tab. Coordination across outputs is therefore impossible, and any
"only keep the newest alive" scheme must live inside a single output. This is why a per-figure
tap-to-spin button, one figure per cell, still failed: each button only ever saw its own frame.

## What was ruled out, and how

Five hypotheses were proposed and refuted before the cause was measured. They are recorded so
nobody re-proposes them.

| Hypothesis | How it was refuted |
|---|---|
| plotly.js version mismatch | Real and worth fixing, but not the cause. plotly.py 7.0.0 reports `get_plotlyjs_version()` as 4.0.0 while writing arrays in the 6.x base64 `bdata` format, so `include_plotlyjs="cdn"` loaded a 2019 build. Pinned to 2.35.2 and traces built from plain Python lists. Symptom unchanged. |
| requirejs swallowing the UMD bundle | A loader that hides `define.amd` during load changed nothing. Also refuted logically: the colour bar drawing proves `newPlot` ran. |
| WebGL unavailable or context-starved | The device reports WebGL 2.0, Apple GPU, 16384 texture size, 40+ simultaneous bare contexts. |
| Canvas created at zero size | Tested four ways: explicit pixel size with `autosize:false`, a delayed `Plotly.Plots.resize`, a `ResizeObserver`, and `scatter3d` instead of `surface`. All unchanged. Instrumentation later showed the canvas is correctly sized at 1884x620 with a live context. |
| An incomplete float-texture framebuffer | Codex's leading hypothesis, traced through plotly's bundled `gl-fbo`, which prefers a float colour attachment. Refuted by a corrected probe: under WebGL 1 the device reports `OES_texture_float: yes` and `float FBO: COMPLETE`, with every extension plotly's gl3d stack requires present. |

Two of the early probe results were artifacts of bugs in the probe itself: it requested a WebGL 2
context and then reported WebGL 1 extensions as missing, which is correct and expected behaviour
under WebGL 2, and it built float textures with an unsized `RGBA` internal format, which is never
colour-renderable there. Codex independently identified the same context mismatch.

The cause was found only by instrumenting the failure — capturing errors, framebuffer state,
canvas dimensions and `webglcontextlost` events — rather than by reasoning about it.

## Consequences for the summit

3D is a bonus layer, never load-bearing. Every scan ships with a real rendered still image, so the
page carries its content when the reader never taps, when the venue blocks the Plotly CDN, and if
the browser reclaims the view anyway. The catalog activities themselves use SVG and 2D canvas and
are unaffected by any of this.
