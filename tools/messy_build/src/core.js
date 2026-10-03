/* Shared chart + control helpers for every activity on this page.
   Charts size themselves to their container so text stays readable on a phone. */
var CAMEL = (function(){
  var BLUE = "#2b6cb0", HI = "#d9730d", RED = "#c0392b", GREY = "#9ca3af", INK = "#374151";
  var PAL = [BLUE, "#c0392b", "#2f855a", "#b7791f", "#6b46c1", "#0f766e", "#9d174d", "#525252"];

  function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
  function fmt(v, nd){
    if (v === null || v === undefined || isNaN(v)) return "—";
    nd = (nd === undefined) ? 2 : nd;
    return (Math.round(v * Math.pow(10, nd)) / Math.pow(10, nd)).toFixed(nd);
  }
  function tidy(v){
    if (v === null || v === undefined || isNaN(v)) return "—";
    var r = Math.round(v * 1e4) / 1e4;
    return Math.abs(r) >= 10000 ? r.toLocaleString("en-US") : String(r);
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
  function stdev(a){
    if (a.length < 2) return 0;
    var m = mean(a), s = 0, i;
    for (i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / (a.length - 1));
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
  function niceUp(x){
    if (!(x > 0)) return 1;
    var e = Math.pow(10, Math.floor(Math.log(x) / Math.LN10)), f = x / e;
    var steps = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10], i;
    for (i = 0; i < steps.length; i++) if (f <= steps[i] + 1e-9) return steps[i] * e;
    return 10 * e;
  }
  /* A few extreme samples would squash everything else, so the axis stops near the
     98th percentile and the rest are pinned to the edge and counted in a caption. */
  function autoDomain(vals, o){
    o = o || {};
    var v = vals.filter(function(x){ return x !== null && x !== undefined && !isNaN(x); });
    var dom = extent(v);
    if (o.clip === false || v.length < 20) return {dom: dom, over: 0, total: v.length, clipped: false};
    if (typeof o.clip === "number")
      return {dom: [dom[0], o.clip], over: v.filter(function(x){ return x > o.clip; }).length, total: v.length, clipped: true};
    var q = quantile(v, o.q || 0.98), ratio = o.ratio || 1.5;
    if (!(q > 0) || dom[1] <= ratio * q) return {dom: dom, over: 0, total: v.length, clipped: false};
    var hi = niceUp(q);
    if (hi >= dom[1]) return {dom: dom, over: 0, total: v.length, clipped: false};
    return {dom: [dom[0], hi], over: v.filter(function(x){ return x > hi; }).length, total: v.length, clipped: true};
  }
  function fit(xs, ys){
    var n = xs.length;
    if (n < 2) return null;
    var mx = mean(xs), my = mean(ys), sxy = 0, sxx = 0, syy = 0, i, dx, dy;
    for (i = 0; i < n; i++){ dx = xs[i] - mx; dy = ys[i] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy; }
    if (!sxx || !syy) return null;
    var m = sxy / sxx;
    return {m: m, b: my - m * mx, r2: (sxy * sxy) / (sxx * syy), r: sxy / Math.sqrt(sxx * syy)};
  }
  function expand(p){
    if (!p || !p.cols) return p;
    return p.rows.map(function(r){ var o = {}, i; for (i = 0; i < p.cols.length; i++) o[p.cols[i]] = r[i]; return o; });
  }
  function T(x, y, txt, o){
    o = o || {};
    return '<text x="' + fmt(x, 1) + '" y="' + fmt(y, 1) + '" font-size="' + (o.size || 12) + '" text-anchor="' + (o.anchor || "start") +
      '"' + (o.fill ? ' fill="' + o.fill + '"' : ' fill="' + INK + '"') + (o.bold ? ' font-weight="600"' : "") + ">" + esc(txt) + "</text>";
  }
  function cap(note){ return note ? '<div class="cw-cap">' + esc(note) + "</div>" : ""; }
  /* Width to draw at: the container's real pixel width, so 12px text really is 12px. */
  function widthOf(el, max){
    var w = el && el.clientWidth ? el.clientWidth : 600;
    return Math.max(280, Math.min(max || 720, w));
  }

  /* ---- plot frame -------------------------------------------------- */
  function frame(o){
    var w = o.width || 600, h = o.height || 300;
    var pad = {l: o.padL || 54, r: o.padR || 16, t: o.padT || 12, b: o.padB || 46};
    var xs = o.xdom, ys = o.ydom;
    function px(v){ return pad.l + (v - xs[0]) / (xs[1] - xs[0]) * (w - pad.l - pad.r); }
    function py(v){ return h - pad.b - (v - ys[0]) / (ys[1] - ys[0]) * (h - pad.t - pad.b); }
    var s = ['<svg viewBox="0 0 ' + w + " " + h + '" width="' + w + '" height="' + h + '" role="img" aria-label="' +
             esc(o.label || (o.ylab || "") + " chart") + '" style="display:block;max-width:100%;height:auto;font-family:-apple-system,system-ui,sans-serif">'];
    (o.xticks || ticks(xs[0], xs[1], w < 420 ? 4 : 6)).forEach(function(t){
      s.push('<line x1="' + px(t) + '" y1="' + (h - pad.b) + '" x2="' + px(t) + '" y2="' + (h - pad.b + 5) + '" stroke="#555"/>');
      s.push(T(px(t), h - pad.b + 19, tidy(t), {anchor: "middle"}));
    });
    (o.yticks || ticks(ys[0], ys[1], 4)).forEach(function(t){
      s.push('<line x1="' + (pad.l - 5) + '" y1="' + py(t) + '" x2="' + (w - pad.r) + '" y2="' + py(t) + '" stroke="#e5e7eb"/>');
      s.push(T(pad.l - 8, py(t) + 4, tidy(t), {anchor: "end"}));
    });
    s.push('<line x1="' + pad.l + '" y1="' + (h - pad.b) + '" x2="' + (w - pad.r) + '" y2="' + (h - pad.b) + '" stroke="#333"/>');
    s.push('<line x1="' + pad.l + '" y1="' + pad.t + '" x2="' + pad.l + '" y2="' + (h - pad.b) + '" stroke="#333"/>');
    if (o.xlab) s.push(T((pad.l + w - pad.r) / 2, h - 6, o.xlab, {anchor: "middle", size: 13}));
    if (o.ylab) s.push('<text x="13" y="' + (pad.t + (h - pad.t - pad.b) / 2) + '" font-size="13" fill="' + INK +
      '" text-anchor="middle" transform="rotate(-90 13 ' + (pad.t + (h - pad.t - pad.b) / 2) + ')">' + esc(o.ylab) + "</text>");
    return {svg: s, px: px, py: py, w: w, h: h, pad: pad, done: function(){ s.push("</svg>"); return s.join(""); }};
  }

  function scatter(o){
    var pts = o.points.filter(function(p){ return p.x !== null && p.y !== null; });
    var dx = autoDomain(pts.map(function(p){ return p.x; }), {clip: o.xclip !== undefined ? o.xclip : o.clip});
    var dy = autoDomain(pts.map(function(p){ return p.y; }), {clip: o.yclip !== undefined ? o.yclip : o.clip});
    var xd = o.xdom || dx.dom, yd = o.ydom || dy.dom, notes = [];
    if (!o.xdom && dx.over) notes.push(dx.over + " samples are past " + tidy(xd[1]) + " " + (o.xunit || "") + " (drawn as hollow dots at the right edge)");
    if (!o.ydom && dy.over) notes.push(dy.over + " samples are above " + tidy(yd[1]) + " " + (o.yunit || "") + " (hollow dots at the top edge)");
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab, xdom: xd, ydom: yd, label: o.label});
    function dot(p, hi){
      var off = p.x > xd[1] || p.y > yd[1];
      var cx = f.px(Math.min(p.x, xd[1])), cy = f.py(Math.min(p.y, yd[1])), col = p.color || BLUE;
      var t = p.label ? "<title>" + esc(p.label) + "</title>" : "";
      var r = hi ? 5 : (o.r || 3.2);
      if (off) return '<circle cx="' + fmt(cx, 1) + '" cy="' + fmt(cy, 1) + '" r="' + r + '" fill="none" stroke="' + col +
        '" stroke-width="1.4">' + t + "</circle>";
      return '<circle cx="' + fmt(cx, 1) + '" cy="' + fmt(cy, 1) + '" r="' + r + '" fill="' + col + '" fill-opacity="' +
        (hi ? 0.95 : (o.alpha || 0.55)) + '"' + (hi ? ' stroke="#fff" stroke-width="1"' : "") + ">" + t + "</circle>";
    }
    pts.filter(function(p){ return !p.hi; }).forEach(function(p){ f.svg.push(dot(p, false)); });
    pts.filter(function(p){ return p.hi; }).forEach(function(p){ f.svg.push(dot(p, true)); });
    if (o.line){
      var y0 = o.line.m * xd[0] + o.line.b, y1 = o.line.m * xd[1] + o.line.b;
      f.svg.push('<line x1="' + f.px(xd[0]) + '" y1="' + f.py(Math.max(yd[0], Math.min(yd[1], y0))) + '" x2="' + f.px(xd[1]) +
        '" y2="' + f.py(Math.max(yd[0], Math.min(yd[1], y1))) + '" stroke="' + RED + '" stroke-width="2.2"/>');
      f.svg.push(T(f.px(xd[1]) - 6, f.py(Math.max(yd[0], Math.min(yd[1], y1))) - 8, "best-fit line", {anchor: "end", fill: RED, bold: true}));
    }
    return f.done() + cap(o.note || notes.join("; "));
  }

  /* Histogram. Samples above the axis limit get their own gray bar labelled "N+". */
  function hist(o){
    var v = o.values.filter(function(x){ return x !== null && !isNaN(x); });
    var d = o.xdom ? {dom: o.xdom, over: 0, total: v.length, clipped: false} : autoDomain(v, {clip: o.clip, q: o.q, ratio: o.ratio});
    var dom = d.dom, nb = o.bins || 20, wbin = (dom[1] - dom[0]) / nb;
    var counts = new Array(nb), over = 0, under = 0, i, k;
    for (i = 0; i < nb; i++) counts[i] = 0;
    for (i = 0; i < v.length; i++){
      if (v[i] > dom[1]) { over++; continue; }
      if (v[i] < dom[0]) { under++; continue; }
      k = Math.floor((v[i] - dom[0]) / wbin);
      if (k >= nb) k = nb - 1;
      counts[k]++;
    }
    var slots = over ? nb + 1 : nb, peak = o.ymax || Math.max.apply(null, counts.concat([over]));
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab || "number of samples",
                   xdom: [dom[0], dom[0] + slots * wbin], ydom: [0, peak * 1.1 || 1], label: o.label,
                   xticks: over ? ticks(dom[0], dom[1], 5).filter(function(t){ return t <= dom[1]; }) : null});
    for (i = 0; i < nb; i++){
      if (!counts[i]) continue;
      var x0 = f.px(dom[0] + i * wbin), x1 = f.px(dom[0] + (i + 1) * wbin);
      f.svg.push('<rect x="' + fmt(x0, 1) + '" y="' + fmt(f.py(counts[i]), 1) + '" width="' + fmt(Math.max(x1 - x0 - 1, 1), 1) +
        '" height="' + fmt(f.py(0) - f.py(counts[i]), 1) + '" fill="' + (o.color || BLUE) + '" fill-opacity="0.8"><title>' +
        counts[i] + " samples</title></rect>");
    }
    var notes = [];
    if (over){
      var ox0 = f.px(dom[1] + wbin * 0.15), ox1 = f.px(dom[1] + wbin);
      f.svg.push('<line x1="' + fmt(f.px(dom[1]), 1) + '" y1="' + f.pad.t + '" x2="' + fmt(f.px(dom[1]), 1) + '" y2="' + f.py(0) +
        '" stroke="#9ca3af" stroke-dasharray="3 3"/>');
      f.svg.push('<rect x="' + fmt(ox0, 1) + '" y="' + fmt(f.py(over), 1) + '" width="' + fmt(Math.max(ox1 - ox0 - 1, 1), 1) +
        '" height="' + fmt(f.py(0) - f.py(over), 1) + '" fill="#6b7280" fill-opacity="0.65"><title>' + over + " samples above " + tidy(dom[1]) + "</title></rect>");
      f.svg.push(T((ox0 + ox1) / 2, f.h - f.pad.b + 19, tidy(dom[1]) + "+", {anchor: "middle", fill: "#6b7280"}));
      notes.push(over + " of " + v.length + " samples are above " + tidy(dom[1]) + " " + (o.xunit || "") + " and are stacked in the gray bar at the right");
    }
    if (under) notes.push(under + " fall below the left edge");
    /* callouts in data coordinates: {x, yf (fraction of tallest bar), text, anchor, fill} */
    (o.callouts || []).forEach(function(c){
      f.svg.push(T(f.px(c.x), f.py(c.yf * peak), c.text, {anchor: c.anchor || "start", fill: c.fill || INK, bold: true}));
    });
    /* vertical marker lines, each label on its own row so two labels never collide */
    (o.marks || []).forEach(function(m, mi){
      var xx = f.px(m.x), right = (m.label.length * 6.6 > f.w - 4 - (xx + 5)) && ((xx - 5 - f.pad.l) > (f.w - 4 - (xx + 5))), yy = f.pad.t + 12 + mi * 15;
      f.svg.push('<line x1="' + xx + '" y1="' + f.pad.t + '" x2="' + xx + '" y2="' + f.py(0) + '" stroke="' + (m.color || RED) +
        '" stroke-width="2" stroke-dasharray="4 3"/>');
      f.svg.push(T(right ? xx - 5 : xx + 5, yy, m.label, {anchor: right ? "end" : "start", fill: m.color || RED, bold: true}));
    });
    return f.done() + cap(o.note !== undefined ? o.note : notes.join("; "));
  }

  /* Horizontal bars with the label at the left of each bar: no rotated text, any label length.
     Each item may carry `back` (pale bar behind) and `tag` (text after the value). */
  function hbars(o){
    var items = o.items, w = o.width || 600, rowH = o.rowH || 24;
    var maxLab = 0;
    items.forEach(function(d){ maxLab = Math.max(maxLab, String(d.name).length); });
    var padL = Math.min(Math.round(w * 0.42), Math.max(70, Math.round(maxLab * 6.6) + 14));
    var h = items.length * rowH + 50;
    var top = o.max || 0;
    items.forEach(function(d){ top = Math.max(top, d.value, d.back || 0); });
    var reserve = o.reserve || 74;                 /* room for the value text past the longest bar */
    var f = frame({width: w, height: h, xlab: o.xlab, ylab: "", xdom: [0, top], ydom: [0, 1], padL: padL, padR: reserve,
                   padT: 6, padB: 44, yticks: [], label: o.label});
    items.forEach(function(d, i){
      var y = 6 + i * rowH, bh = rowH * 0.66, cy = y + rowH / 2;
      var col = d.color || o.color || BLUE;
      if (d.back !== undefined && d.back !== null)
        f.svg.push('<rect x="' + padL + '" y="' + fmt(cy - bh / 2, 1) + '" width="' + fmt(f.px(d.back) - padL, 1) + '" height="' + fmt(bh, 1) +
          '" fill="#9ca3af" fill-opacity="0.28"><title>' + esc(d.name) + ": " + tidy(d.back) + " in total</title></rect>");
      f.svg.push('<rect x="' + padL + '" y="' + fmt(cy - bh / 2, 1) + '" width="' + fmt(Math.max(f.px(d.value) - padL, 1), 1) + '" height="' + fmt(bh, 1) +
        '" fill="' + col + '" fill-opacity="0.9"><title>' + esc(d.name) + ": " + tidy(d.value) + "</title></rect>");
      var maxc = Math.floor((padL - 12) / 6.6), nm = String(d.name);
      if (nm.length > maxc) nm = nm.slice(0, Math.max(1, maxc - 1)) + "\u2026";
      f.svg.push(T(padL - 8, cy + 4, nm, {anchor: "end", bold: !!d.bold, fill: d.bold ? "#111" : INK}));
      f.svg.push(T(f.px(Math.max(d.value, d.back || 0)) + 6, cy + 4, tidy(d.value) + (d.tag ? " " + d.tag : ""), {fill: "#111"}));
    });
    return f.done() + cap(o.note);
  }

  /* Dot-and-arrow comparison on a fixed axis: rows of {label, a, b}. */
  function dumbbell(o){
    var w = o.width || 600, rowH = 46, h = o.rows.length * rowH + 52;
    var f = frame({width: w, height: h, xlab: o.xlab, ylab: "", xdom: o.xdom, ydom: [0, 1], padL: 74, padR: 20, padT: 8, padB: 44,
                   yticks: [], label: o.label});
    o.rows.forEach(function(r, i){
      var cy = 8 + i * rowH + rowH / 2;
      f.svg.push(T(66, cy + 4, r.label, {anchor: "end", bold: true, fill: "#111"}));
      f.svg.push('<line x1="' + f.px(0) + '" y1="' + cy + '" x2="' + (w - 20) + '" y2="' + cy + '" stroke="#e5e7eb"/>');
      if (Math.abs(f.px(r.a) - f.px(r.b)) > 1)
        f.svg.push('<line x1="' + f.px(r.a) + '" y1="' + cy + '" x2="' + f.px(r.b) + '" y2="' + cy + '" stroke="' + BLUE + '" stroke-width="3"/>');
      f.svg.push('<circle cx="' + f.px(r.a) + '" cy="' + cy + '" r="8" fill="#fff" stroke="' + BLUE + '" stroke-width="2.5"/>');
      f.svg.push('<circle cx="' + f.px(r.b) + '" cy="' + cy + '" r="5.5" fill="' + BLUE + '"/>');
    });
    return f.done();
  }

  /* Box plot, one blue color, labels horizontal, median written on the chart. */
  function box(o){
    var names = Object.keys(o.groups), all = [], dom = o.ydom, d = null;
    names.forEach(function(n){ all = all.concat(o.groups[n]); });
    if (!dom){ d = autoDomain(all, {clip: o.clip, q: o.q, ratio: o.ratio}); dom = d.dom; }
    var w = o.width || 600, h = o.height || 300;
    var f = frame({width: w, height: h, xlab: "", ylab: o.ylab, xdom: [0, names.length], ydom: dom, xticks: [], padB: 52, label: o.label});
    var offTotal = 0;
    names.forEach(function(n, i){
      var v = o.groups[n].filter(function(x){ return x !== null && !isNaN(x); });
      if (!v.length) return;
      var cx = f.px(i + 0.5), bw = Math.min(70, (f.w - f.pad.l - f.pad.r) / names.length * 0.4);
      var q1 = quantile(v, 0.25), q2 = median(v), q3 = quantile(v, 0.75);
      var lo = Math.max(quantile(v, 0.05), dom[0]), hi = Math.min(quantile(v, 0.95), dom[1]);
      f.svg.push('<line x1="' + cx + '" y1="' + f.py(lo) + '" x2="' + cx + '" y2="' + f.py(hi) + '" stroke="#444"/>');
      v.forEach(function(x, k){
        var jx = cx + (((k * 37) % 101) / 101 - 0.5) * bw * 1.6, off = x > dom[1];
        if (off) offTotal++;
        f.svg.push('<circle cx="' + fmt(jx, 1) + '" cy="' + fmt(f.py(Math.max(dom[0], Math.min(dom[1], x))), 1) + '" r="2.2" fill="' +
          (off ? "none" : BLUE) + '" fill-opacity="0.3"' + (off ? ' stroke="' + BLUE + '"' : "") + "/>");
      });
      f.svg.push('<rect x="' + (cx - bw / 2) + '" y="' + f.py(q3) + '" width="' + bw + '" height="' + Math.max(f.py(q1) - f.py(q3), 1) +
        '" fill="' + BLUE + '" fill-opacity="0.35" stroke="' + BLUE + '"/>');
      f.svg.push('<line x1="' + (cx - bw / 2) + '" y1="' + f.py(q2) + '" x2="' + (cx + bw / 2) + '" y2="' + f.py(q2) + '" stroke="' + BLUE + '" stroke-width="3.5"/>');
      var mt = "median " + fmt(q2, 2), mright = cx + bw / 2 + 6 + mt.length * 7 > f.w - 4;
      f.svg.push(T(mright ? cx - bw / 2 - 6 : cx + bw / 2 + 6, f.py(q2) + 4, mt, {fill: "#111", bold: true, anchor: mright ? "end" : "start"}));
      f.svg.push(T(cx, f.h - f.pad.b + 18, n, {anchor: "middle", bold: true, fill: "#111"}));
      f.svg.push(T(cx, f.h - f.pad.b + 34, v.length + " measured", {anchor: "middle", fill: "#6b7280", size: 11}));
    });
    var note = o.note !== undefined ? o.note : (d && d.over ? offTotal + " samples are above " + tidy(dom[1]) + " and are drawn as hollow dots at the top edge" : "");
    return f.done() + cap(note);
  }

  function lineChart(o){
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab, xdom: o.xdom, ydom: o.ydom, label: o.label});
    var d = o.points.map(function(p, k){ return (k ? "L" : "M") + fmt(f.px(p[0]), 1) + " " + fmt(f.py(p[1]), 1); }).join(" ");
    f.svg.push('<path d="' + d + '" fill="none" stroke="' + BLUE + '" stroke-width="2.4"/>');
    (o.marks || []).forEach(function(m){
      f.svg.push('<circle cx="' + f.px(m.x) + '" cy="' + f.py(m.y) + '" r="6" fill="' + HI + '" stroke="#fff" stroke-width="1.5"/>');
      var right = f.px(m.x) + 10 + m.label.length * 6.6 > f.w - 4;
      f.svg.push(T(f.px(m.x) + (right ? -10 : 10), f.py(m.y) - 10, m.label, {anchor: right ? "end" : "start", fill: HI, bold: true}));
    });
    return f.done();
  }

  /* ---- controls ---------------------------------------------------- */
  function seg(group, opts, sel){
    return '<div class="cw-seg" role="radiogroup">' + opts.map(function(o){
      var on = o.v === sel;
      return '<button type="button" role="radio" aria-checked="' + on + '" class="cw-segbtn' + (on ? " on" : "") + '" data-g="' + group +
        '" data-v="' + esc(o.v) + '">' + (on ? "&#10003; " : "") + esc(o.t) + "</button>";
    }).join("") + "</div>";
  }
  function slider(id, label, min, max, val, step){
    return '<div class="cw-ctl"><label for="' + id + '">' + esc(label) + ': <b id="' + id + '-v">' + val +
      '</b></label><input id="' + id + '" type="range" min="' + min + '" max="' + max + '" value="' + val + '" step="' + (step || 1) + '"></div>';
  }
  function button(id, label, cls){ return '<button type="button" id="' + id + '" class="cw-btn ' + (cls || "") + '">' + esc(label) + "</button>"; }
  /* The mechanical cleanup rules from Find the Mess (junk piece, repeated name, list order). It never decides
     that two different labels are the same material; 2H-MoS2 -> MoS2 happens only when o.h2 is set. */
  function tidyLabel(m, o){
    if (m === null || m === undefined) return null;
    var p = String(m).split(";").map(function(x){ return x.replace(/^\s+|\s+$/g, ""); });
    var kept = p.filter(function(x){ return /[A-Za-z]/.test(x); }); if (kept.length) p = kept;
    if (p.every(function(x){ return x === p[0]; })) p = [p[0]];
    var out = p.slice().sort().join("; ");
    if (o && o.h2 && out === "2H-MoS2") out = "MoS2";
    return out;
  }
  var resizers = [];
  function onResize(root, fn){ resizers.push({root: root, fn: fn}); }
  var tick = null;
  window.addEventListener("resize", function(){
    if (tick) cancelAnimationFrame(tick);
    tick = requestAnimationFrame(function(){ resizers.forEach(function(r){ if (r.root.clientWidth > 0) r.fn(); }); });
  });

  return {BLUE: BLUE, HI: HI, RED: RED, palette: PAL, expand: expand, esc: esc, fmt: fmt, tidy: tidy, mean: mean, median: median,
          quantile: quantile, stdev: stdev, tidyLabel: tidyLabel, extent: extent, autoDomain: autoDomain, niceUp: niceUp, fit: fit, widthOf: widthOf,
          scatter: scatter, hist: hist, hbars: hbars, dumbbell: dumbbell, box: box, lineChart: lineChart, cap: cap,
          ui: {seg: seg, slider: slider, button: button}, onResize: onResize};
})();
