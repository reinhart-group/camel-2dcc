/* CAMEL widget core: tiny SVG plotting and touch-friendly controls.
   Every catalog item gets its own copy of this inside its own output frame. */
var CAMEL = (function(){
  var PAL = ["#2b6cb0","#c0392b","#2f855a","#b7791f","#6b46c1","#0f766e","#9d174d","#525252"];

  function esc(s){
    return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function fmt(v, nd){
    if (v === null || v === undefined || isNaN(v)) return "—";
    nd = (nd === undefined) ? 2 : nd;
    return (Math.round(v * Math.pow(10, nd)) / Math.pow(10, nd)).toFixed(nd);
  }
  function tidy(v){
    if (v === null || v === undefined || isNaN(v)) return "\u2014";
    return String(Math.round(v * 1e4) / 1e4);
  }
  function mean(a){ var s = 0, i; for (i = 0; i < a.length; i++) s += a[i]; return a.length ? s / a.length : NaN; }
  function median(a){
    if (!a.length) return NaN;
    var b = a.slice().sort(function(x, y){ return x - y; }), n = b.length, h = n >> 1;
    return n % 2 ? b[h] : (b[h - 1] + b[h]) / 2;
  }
  function quantile(a, q){
    if (!a.length) return NaN;
    var b = a.slice().sort(function(x, y){ return x - y; });
    var p = (b.length - 1) * q, lo = Math.floor(p), hi = Math.ceil(p);
    return b[lo] + (b[hi] - b[lo]) * (p - lo);
  }
  function extent(a){
    var lo = Infinity, hi = -Infinity, i;
    for (i = 0; i < a.length; i++){ if (a[i] < lo) lo = a[i]; if (a[i] > hi) hi = a[i]; }
    if (!isFinite(lo)) { lo = 0; hi = 1; }
    if (lo === hi) { hi = lo + 1; }
    return [lo, hi];
  }
  function ticks(lo, hi, n){
    var span = hi - lo, step = Math.pow(10, Math.floor(Math.log(span / n) / Math.LN10));
    var err = (span / n) / step;
    if (err >= 7.5) step *= 10; else if (err >= 3) step *= 5; else if (err >= 1.5) step *= 2;
    var out = [], v = Math.ceil(lo / step) * step;
    for (; v <= hi + step * 0.001; v += step) out.push(Math.round(v * 1e6) / 1e6);
    return out;
  }
  /* A round number at or just above x, for axis limits. */
  function niceUp(x){
    if (!(x > 0)) return 1;
    var e = Math.pow(10, Math.floor(Math.log(x) / Math.LN10)), f = x / e;
    var steps = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10], i;
    for (i = 0; i < steps.length; i++) if (f <= steps[i] + 1e-9) return steps[i] * e;
    return 10 * e;
  }

  /* Pick a plotting domain for values with a long right tail.
     A few extreme samples otherwise stretch the axis and squash everything else:
     2DCC roughness runs to 92 nm while 98% of films sit under 11 nm. When the
     maximum is more than `ratio` times the q-quantile, stop the axis at a round
     number near that quantile and report how many samples fall beyond it. The
     caller must draw those off-scale samples distinctly and name the count, so
     nothing is hidden. Well-behaved variables are left at their full extent. */
  function autoDomain(vals, o){
    o = o || {};
    var v = vals.filter(function(x){ return x !== null && x !== undefined && !isNaN(x); });
    var dom = extent(v);
    if (o.clip === false || v.length < 20) return {dom: dom, over: 0, total: v.length, clipped: false};
    if (typeof o.clip === "number") {
      return {dom: [dom[0], o.clip], over: v.filter(function(x){ return x > o.clip; }).length,
              total: v.length, clipped: true};
    }
    var q = quantile(v, o.q || 0.98), ratio = o.ratio || 1.5;
    if (!(q > 0) || dom[1] <= ratio * q) return {dom: dom, over: 0, total: v.length, clipped: false};
    var hi = niceUp(q);
    if (hi >= dom[1]) return {dom: dom, over: 0, total: v.length, clipped: false};
    return {dom: [dom[0], hi], over: v.filter(function(x){ return x > hi; }).length,
            total: v.length, clipped: true};
  }

  /* One-line caption naming the samples an axis could not reach. */
  function offscaleNote(d, what){
    if (!d.clipped || !d.over) return "";
    return d.over + " of " + d.total + " " + (what || "samples") + " measure above " +
           tidy(d.dom[1]) + " and are drawn at the edge";
  }

  function fit(xs, ys){
    var n = xs.length;
    if (n < 2) return null;
    var mx = mean(xs), my = mean(ys), sxy = 0, sxx = 0, syy = 0, i, dx, dy;
    for (i = 0; i < n; i++){
      dx = xs[i] - mx; dy = ys[i] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy;
    }
    if (!sxx || !syy) return null;
    var m = sxy / sxx;
    return {m: m, b: my - m * mx, r2: (sxy * sxy) / (sxx * syy), r: sxy / Math.sqrt(sxx * syy)};
  }

  /* ---- plot frame -------------------------------------------------- */
  function frame(o){
    var w = o.width || 520, h = o.height || 300;
    var pad = {l: 56, r: 12, t: 14, b: 44};
    var xs = o.xdom, ys = o.ydom;
    function px(v){ return pad.l + (v - xs[0]) / (xs[1] - xs[0]) * (w - pad.l - pad.r); }
    function py(v){ return h - pad.b - (v - ys[0]) / (ys[1] - ys[0]) * (h - pad.t - pad.b); }
    var s = ['<svg viewBox="0 0 ' + w + ' ' + h + '" width="100%" style="max-width:' + w +
             'px;height:auto;font-family:-apple-system,system-ui,sans-serif">'];
    (o.xticks || ticks(xs[0], xs[1], 5)).forEach(function(t){
      s.push('<line x1="' + px(t) + '" y1="' + (h - pad.b) + '" x2="' + px(t) + '" y2="' +
             (h - pad.b + 5) + '" stroke="#555"/>');
      s.push('<text x="' + px(t) + '" y="' + (h - pad.b + 19) + '" font-size="12" text-anchor="middle">' + t + '</text>');
    });
    (o.yticks || ticks(ys[0], ys[1], 4)).forEach(function(t){
      s.push('<line x1="' + (pad.l - 5) + '" y1="' + py(t) + '" x2="' + (w - pad.r) + '" y2="' +
             py(t) + '" stroke="#e5e7eb"/>');
      s.push('<text x="' + (pad.l - 8) + '" y="' + (py(t) + 4) + '" font-size="12" text-anchor="end">' + t + '</text>');
    });
    s.push('<line x1="' + pad.l + '" y1="' + (h - pad.b) + '" x2="' + (w - pad.r) + '" y2="' +
           (h - pad.b) + '" stroke="#333"/>');
    s.push('<line x1="' + pad.l + '" y1="' + pad.t + '" x2="' + pad.l + '" y2="' + (h - pad.b) + '" stroke="#333"/>');
    if (o.xlab) s.push('<text x="' + ((pad.l + w - pad.r) / 2) + '" y="' + (h - 6) +
                       '" font-size="13" text-anchor="middle">' + esc(o.xlab) + '</text>');
    if (o.ylab) s.push('<text x="13" y="' + (h / 2) + '" font-size="13" text-anchor="middle" transform="rotate(-90 13 ' +
                       (h / 2) + ')">' + esc(o.ylab) + '</text>');
    if (o.note) s.push('<text x="' + (w - pad.r) + '" y="' + (pad.t + 2) +
                       '" font-size="11" fill="#6b7280" text-anchor="end">' + esc(o.note) + '</text>');
    return {svg: s, px: px, py: py, w: w, h: h, pad: pad,
            done: function(){ s.push("</svg>"); return s.join(""); }};
  }

  function scatter(o){
    var pts = o.points.filter(function(p){ return p.x !== null && p.y !== null; });
    var dx = autoDomain(pts.map(function(p){ return p.x; }), {clip: o.xclip !== undefined ? o.xclip : o.clip});
    var dy = autoDomain(pts.map(function(p){ return p.y; }), {clip: o.yclip !== undefined ? o.yclip : o.clip});
    var xd = o.xdom || dx.dom, yd = o.ydom || dy.dom;
    var notes = [];
    if (!o.xdom && dx.over) notes.push(dx.over + " past " + tidy(xd[1]) + " " + (o.xunit || "") + "→");
    if (!o.ydom && dy.over) notes.push(dy.over + " above " + tidy(yd[1]) + " " + (o.yunit || "") + "↑");
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab,
                   xdom: xd, ydom: yd, note: o.note || notes.join("  ")});
    pts.forEach(function(p){
      var off = p.x > xd[1] || p.y > yd[1];
      var cx = f.px(Math.min(p.x, xd[1])), cy = f.py(Math.min(p.y, yd[1]));
      var col = p.color || PAL[0];
      var t = p.label ? "<title>" + esc(p.label) + "</title>" : "";
      if (off){
        /* Pinned to the edge, hollow, so it never reads as a real position. */
        f.svg.push('<circle cx="' + fmt(cx, 1) + '" cy="' + fmt(cy, 1) + '" r="' + (o.r || 3.4) +
          '" fill="none" stroke="' + col + '" stroke-width="1.4" stroke-dasharray="2 2">' + t + "</circle>");
      } else {
        f.svg.push('<circle cx="' + fmt(cx, 1) + '" cy="' + fmt(cy, 1) + '" r="' + (o.r || 3.4) +
          '" fill="' + col + '" fill-opacity="' + (o.alpha || 0.62) + '">' + t + "</circle>");
      }
    });
    if (o.line){
      var y0 = o.line.m * xd[0] + o.line.b, y1 = o.line.m * xd[1] + o.line.b;
      f.svg.push('<line x1="' + f.px(xd[0]) + '" y1="' + f.py(Math.max(yd[0], Math.min(yd[1], y0))) +
        '" x2="' + f.px(xd[1]) + '" y2="' + f.py(Math.max(yd[0], Math.min(yd[1], y1))) +
        '" stroke="#c0392b" stroke-width="2"/>');
    }
    return f.done();
  }

  function hist(o){
    var v = o.values.filter(function(x){ return x !== null && !isNaN(x); });
    var d = o.xdom ? {dom: o.xdom, over: 0, total: v.length, clipped: false}
                   : autoDomain(v, {clip: o.clip, q: o.q, ratio: o.ratio});
    var dom = d.dom, nb = o.bins || 20, wbin = (dom[1] - dom[0]) / nb;
    var counts = new Array(nb), over = 0, i, k;
    for (i = 0; i < nb; i++) counts[i] = 0;
    for (i = 0; i < v.length; i++){
      if (v[i] > dom[1]) { over++; continue; }
      k = Math.floor((v[i] - dom[0]) / wbin);
      if (k >= nb) k = nb - 1;
      if (k >= 0) counts[k]++;
    }
    /* Off-scale samples get their own bar past the axis limit, labelled "N+",
       rather than being folded into the last real bin. */
    var slots = over ? nb + 1 : nb, peak = Math.max.apply(null, counts.concat([over]));
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab || "how many samples",
                   xdom: [dom[0], dom[0] + slots * wbin], ydom: [0, peak * 1.1 || 1],
                   xticks: over ? ticks(dom[0], dom[1], 5).filter(function(t){ return t <= dom[1]; }) : null,
                   note: o.note || (over ? offscaleNote({clipped: true, over: over, total: v.length, dom: dom},
                                                        o.what) : "")});
    for (i = 0; i < nb; i++){
      if (!counts[i]) continue;
      var x0 = f.px(dom[0] + i * wbin), x1 = f.px(dom[0] + (i + 1) * wbin);
      f.svg.push('<rect x="' + fmt(x0, 1) + '" y="' + fmt(f.py(counts[i]), 1) + '" width="' +
        fmt(Math.max(x1 - x0 - 1, 1), 1) + '" height="' + fmt(f.py(0) - f.py(counts[i]), 1) +
        '" fill="' + (o.color || PAL[0]) + '" fill-opacity="0.75"><title>' + counts[i] + " samples</title></rect>");
    }
    if (over){
      var ox0 = f.px(dom[1] + wbin * 0.15), ox1 = f.px(dom[1] + wbin);
      f.svg.push('<line x1="' + fmt(f.px(dom[1]), 1) + '" y1="' + f.pad.t + '" x2="' +
        fmt(f.px(dom[1]), 1) + '" y2="' + f.py(0) + '" stroke="#9ca3af" stroke-dasharray="3 3"/>');
      f.svg.push('<rect x="' + fmt(ox0, 1) + '" y="' + fmt(f.py(over), 1) + '" width="' +
        fmt(Math.max(ox1 - ox0 - 1, 1), 1) + '" height="' + fmt(f.py(0) - f.py(over), 1) +
        '" fill="#6b7280" fill-opacity="0.6"><title>' + over + " samples above " + tidy(dom[1]) +
        "</title></rect>");
      f.svg.push('<text x="' + fmt((ox0 + ox1) / 2, 1) + '" y="' + (f.h - f.pad.b + 19) +
        '" font-size="12" fill="#6b7280" text-anchor="middle">' + tidy(dom[1]) + '+</text>');
    }
    (o.marks || []).forEach(function(m){
      f.svg.push('<line x1="' + f.px(m.x) + '" y1="' + f.pad.t + '" x2="' + f.px(m.x) + '" y2="' +
        f.py(0) + '" stroke="' + (m.color || "#c0392b") + '" stroke-width="2" stroke-dasharray="4 3"/>');
      f.svg.push('<text x="' + (f.px(m.x) + 4) + '" y="' + (f.pad.t + 12) + '" font-size="12" fill="' +
        (m.color || "#c0392b") + '">' + esc(m.label) + "</text>");
    });
    return f.done();
  }

  function box(o){
    var names = Object.keys(o.groups), dom = o.ydom, d = null, all = [];
    names.forEach(function(n){ all = all.concat(o.groups[n]); });
    if (!dom){
      d = autoDomain(all, {clip: o.clip, q: o.q, ratio: o.ratio});
      dom = d.dom;
    }
    var w = o.width || 520, h = o.height || 300;
    var f = frame({width: w, height: h, xlab: o.xlab || "", ylab: o.ylab, xdom: [0, names.length],
                   ydom: dom, note: o.note || (d ? offscaleNote(d, o.what) : "")});
    names.forEach(function(n, i){
      var v = o.groups[n].filter(function(x){ return x !== null && !isNaN(x); });
      if (!v.length) return;
      var cx = f.px(i + 0.5), bw = Math.min(54, (f.w - f.pad.l - f.pad.r) / names.length * 0.5);
      var q1 = quantile(v, 0.25), q2 = median(v), q3 = quantile(v, 0.75);
      var lo = Math.max(quantile(v, 0.05), dom[0]), hi = Math.min(quantile(v, 0.95), dom[1]);
      var col = PAL[i % PAL.length];
      f.svg.push('<line x1="' + cx + '" y1="' + f.py(lo) + '" x2="' + cx + '" y2="' + f.py(hi) + '" stroke="#444"/>');
      f.svg.push('<rect x="' + (cx - bw / 2) + '" y="' + f.py(q3) + '" width="' + bw + '" height="' +
        Math.max(f.py(q1) - f.py(q3), 1) + '" fill="' + col + '" fill-opacity="0.35" stroke="' + col + '"/>');
      f.svg.push('<line x1="' + (cx - bw / 2) + '" y1="' + f.py(q2) + '" x2="' + (cx + bw / 2) +
        '" y2="' + f.py(q2) + '" stroke="' + col + '" stroke-width="3"/>');
      if (o.dots !== false){
        v.forEach(function(x){
          var jx = cx + (Math.random() - 0.5) * bw * 0.8;
          var off = x > dom[1] || x < dom[0];
          var cy = f.py(Math.max(dom[0], Math.min(dom[1], x)));
          f.svg.push('<circle cx="' + fmt(jx, 1) + '" cy="' + fmt(cy, 1) + '" r="2.2" fill="' +
            (off ? "none" : col) + '" fill-opacity="0.35"' +
            (off ? ' stroke="' + col + '" stroke-width="1.1" stroke-dasharray="2 2"' : "") + "/>");
        });
      }
      f.svg.push('<text x="' + cx + '" y="' + (f.h - f.pad.b + 19) + '" font-size="12" text-anchor="middle">' +
        esc(n) + " (" + v.length + ")</text>");
    });
    return f.done();
  }

  /* Categorical bars. Each item may carry a `back` value drawn as a pale bar
     behind it, so "kept out of total" reads as one shape per category. */
  function bars(o){
    var items = o.items.filter(function(d){ return d && isFinite(d.value); });
    var top = 0;
    items.forEach(function(d){ top = Math.max(top, d.value, d.back || 0); });
    var w = o.width || 520, h = o.height || 280;
    var f = frame({width: w, height: h, xlab: o.xlab || "", ylab: o.ylab,
                   xdom: [0, items.length || 1], ydom: [0, top * 1.12 || 1],
                   xticks: [], note: o.note || ""});
    var slot = (f.w - f.pad.l - f.pad.r) / (items.length || 1);
    var bw = Math.min(56, slot * 0.66);
    items.forEach(function(d, i){
      var cx = f.px(i + 0.5), col = d.color || PAL[i % PAL.length];
      if (d.back !== undefined && d.back !== null){
        f.svg.push('<rect x="' + fmt(cx - bw / 2, 1) + '" y="' + fmt(f.py(d.back), 1) + '" width="' +
          fmt(bw, 1) + '" height="' + fmt(Math.max(f.py(0) - f.py(d.back), 1), 1) +
          '" fill="#9ca3af" fill-opacity="0.25"><title>' + esc(d.name) + ": " + tidy(d.back) +
          " total</title></rect>");
      }
      f.svg.push('<rect x="' + fmt(cx - bw / 2, 1) + '" y="' + fmt(f.py(d.value), 1) + '" width="' +
        fmt(bw, 1) + '" height="' + fmt(Math.max(f.py(0) - f.py(d.value), 1), 1) + '" fill="' + col +
        '" fill-opacity="0.8"><title>' + esc(d.name) + ": " + tidy(d.value) + "</title></rect>");
      if (o.values !== false){
        f.svg.push('<text x="' + fmt(cx, 1) + '" y="' + fmt(f.py(Math.max(d.value, d.back || 0)) - 4, 1) +
          '" font-size="11" text-anchor="middle" fill="#374151">' + tidy(d.value) + "</text>");
      }
      var lab = String(d.name), rot = items.length > 5 || lab.length > 7;
      f.svg.push('<text x="' + fmt(cx, 1) + '" y="' + (f.h - f.pad.b + (rot ? 14 : 17)) +
        '" font-size="11" text-anchor="' + (rot ? "end" : "middle") + '"' +
        (rot ? ' transform="rotate(-38 ' + fmt(cx, 1) + " " + (f.h - f.pad.b + 14) + ')"' : "") +
        ">" + esc(lab) + "</text>");
    });
    return f.done();
  }

  function line(o){
    var all = [];
    o.series.forEach(function(s){ all = all.concat(s.points); });
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab,
                   xdom: o.xdom || extent(all.map(function(p){ return p[0]; })),
                   ydom: o.ydom || extent(all.map(function(p){ return p[1]; }))});
    o.series.forEach(function(s, i){
      var d = s.points.map(function(p, k){
        return (k ? "L" : "M") + fmt(f.px(p[0]), 1) + " " + fmt(f.py(p[1]), 1);
      }).join(" ");
      f.svg.push('<path d="' + d + '" fill="none" stroke="' + (s.color || PAL[i % PAL.length]) +
        '" stroke-width="' + (s.width || 2) + '"' + (s.dash ? ' stroke-dasharray="5 4"' : "") + "/>");
      if (s.dots){
        s.points.forEach(function(p){
          f.svg.push('<circle cx="' + fmt(f.px(p[0]), 1) + '" cy="' + fmt(f.py(p[1]), 1) +
            '" r="3" fill="' + (s.color || PAL[i % PAL.length]) + '"/>');
        });
      }
    });
    return f.done();
  }


  /* columnar payload -> array of objects */
  function expand(p){
    if (!p || !p.cols) return p;
    return p.rows.map(function(r){
      var o = {}, i;
      for (i = 0; i < p.cols.length; i++) o[p.cols[i]] = r[i];
      return o;
    });
  }

  /* ---- controls ---------------------------------------------------- */
  function select(id, label, opts, sel){
    var o = opts.map(function(x){
      var v = (typeof x === "string") ? x : x.v, t = (typeof x === "string") ? x : x.t;
      return '<option value="' + esc(v) + '"' + (v === sel ? " selected" : "") + ">" + esc(t) + "</option>";
    }).join("");
    return '<div class="cw-ctl"><label for="' + id + '">' + esc(label) + '</label><select id="' +
      id + '">' + o + "</select></div>";
  }
  function slider(id, label, min, max, val, step){
    return '<div class="cw-ctl"><label for="' + id + '">' + esc(label) +
      ': <b id="' + id + '-v">' + val + '</b></label><input id="' + id + '" type="range" min="' +
      min + '" max="' + max + '" value="' + val + '" step="' + (step || 1) + '"></div>';
  }
  function button(id, label){
    return '<button id="' + id + '" class="cw-btn">' + esc(label) + "</button>";
  }
  function legend(names){
    return '<div class="cw-key">' + names.map(function(n, i){
      return '<span style="color:' + PAL[i % PAL.length] + '">&#9679;</span> ' + esc(n);
    }).join(" &nbsp; ") + "</div>";
  }

  return {palette: PAL, expand: expand, esc: esc, fmt: fmt, tidy: tidy, mean: mean, median: median, quantile: quantile,
          extent: extent, autoDomain: autoDomain, niceUp: niceUp, offscaleNote: offscaleNote,
          fit: fit, scatter: scatter, hist: hist, box: box, line: line, bars: bars,
          ui: {select: select, slider: slider, button: button, legend: legend}};
})();
