# Writing a catalog item

Each item is one small, self-contained interactive widget. It is rendered once at build time and
its output is saved into a notebook, so **it must work with no Python running and no network**.

## The file

`courseware/widgets/items/<name>.js` holds a single anonymous function expression, nothing else:

```js
/* One line saying what the item does. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);        // only if the payload is columnar
  var body = root.querySelector(".cw-body");
  var id = root.id;                    // prefix every element id with this
  body.innerHTML = "...";              // build markup, then wire listeners, then draw once
}
```

Register it in `courseware/catalog_items_<yours>.py` as an entry in `ITEMS`:

```python
{
  "id": "M-07",                  # unique; W- warmup, M- mess, G- model, D- dials
  "round": "mess",               # warmup | mess | model | dials
  "title": "A question a teacher would ask",
  "blurb": "One sentence on what the learner does and sees.",
  "grades": "6-12",
  "source": "what the data actually is, honestly",
  "item": "<name>",              # the .js file
  "data": lambda: cd.compact(cd.samples(clean=True), ["mat", "rough"]),
  "opts": {...},                 # everything configurable, so variants reuse one .js
}
```

Build and check with:

```
node --check <(printf 'var f = '; cat courseware/widgets/items/<name>.js)
PYTHONPATH=courseware .venv/bin/python scripts/build_catalog.py
```

## The CAMEL API (courseware/widgets/core.js)

- `CAMEL.expand(payload)` columnar payload to array of objects.
- `CAMEL.scatter({points:[{x,y,color,label}], xlab, ylab, line:{m,b}, width, height, xdom, ydom})`
- `CAMEL.hist({values, bins, xlab, marks:[{x,label,color}], width, height, xdom})`
- `CAMEL.box({groups:{name:[values]}, ylab, height, dots})`
- `CAMEL.line({series:[{name,points:[[x,y]],color,dash,dots}], xlab, ylab, xdom, ydom})`
- `CAMEL.fit(xs, ys)` least squares, returns `{m, b, r2, r}` or null.
- `CAMEL.mean/median/quantile(values)`, `CAMEL.extent(values)`, `CAMEL.fmt(v, nd)`, `CAMEL.esc(s)`.
- `CAMEL.ui.select(id, label, options, selected)`, `CAMEL.ui.slider(id, label, min, max, val, step)`,
  `CAMEL.ui.button(id, label)`, `CAMEL.ui.legend(names)`, `CAMEL.palette`.

All plot helpers return an SVG string you drop into `innerHTML`. Points can carry a `<title>` via
`label`, which is what a tap shows.

## Rules

- No external libraries, no network calls, no `fetch`, no `require`.
- Must work at 360 px width and respond to touch. Controls are already styled by the shell.
- Slider handlers listen to `input`, not `change`, so dragging updates live.
- Payloads stay under about 60 KB per item; select only the columns you need.
- Every readout names its denominator: say how many samples are shown and how many were left out.
- Never invent data or relabel it to look tidier than it is. Blanks are blanks.
- Claims stay honest: these are observational records, so say "is associated with", never "causes",
  and never claim these samples became chips or that smoother means better.
