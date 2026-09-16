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
    ticks(xs[0], xs[1], 5).forEach(function(t){
      s.push('<line x1="' + px(t) + '" y1="' + (h - pad.b) + '" x2="' + px(t) + '" y2="' +
             (h - pad.b + 5) + '" stroke="#555"/>');
      s.push('<text x="' + px(t) + '" y="' + (h - pad.b + 19) + '" font-size="12" text-anchor="middle">' + t + '</text>');
    });
    ticks(ys[0], ys[1], 4).forEach(function(t){
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
    return {svg: s, px: px, py: py, w: w, h: h, pad: pad,
            done: function(){ s.push("</svg>"); return s.join(""); }};
  }

  function scatter(o){
    var pts = o.points.filter(function(p){ return p.x !== null && p.y !== null; });
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab,
                   xdom: o.xdom || extent(pts.map(function(p){ return p.x; })),
                   ydom: o.ydom || extent(pts.map(function(p){ return p.y; }))});
    pts.forEach(function(p){
      f.svg.push('<circle cx="' + fmt(f.px(p.x), 1) + '" cy="' + fmt(f.py(p.y), 1) + '" r="' +
        (o.r || 3.4) + '" fill="' + (p.color || PAL[0]) + '" fill-opacity="' + (o.alpha || 0.62) +
        '">' + (p.label ? "<title>" + esc(p.label) + "</title>" : "") + "</circle>");
    });
    if (o.line){
      var xd = o.xdom || extent(pts.map(function(p){ return p.x; }));
      f.svg.push('<line x1="' + f.px(xd[0]) + '" y1="' + f.py(o.line.m * xd[0] + o.line.b) +
        '" x2="' + f.px(xd[1]) + '" y2="' + f.py(o.line.m * xd[1] + o.line.b) +
        '" stroke="#c0392b" stroke-width="2"/>');
    }
    return f.done();
  }

  function hist(o){
    var v = o.values.filter(function(x){ return x !== null && !isNaN(x); });
    var dom = o.xdom || extent(v), nb = o.bins || 20, wbin = (dom[1] - dom[0]) / nb;
    var counts = new Array(nb), i, k;
    for (i = 0; i < nb; i++) counts[i] = 0;
    for (i = 0; i < v.length; i++){
      k = Math.floor((v[i] - dom[0]) / wbin);
      if (k >= nb) k = nb - 1;
      if (k >= 0) counts[k]++;
    }
    var f = frame({width: o.width, height: o.height, xlab: o.xlab, ylab: o.ylab || "how many samples",
                   xdom: dom, ydom: [0, Math.max.apply(null, counts) * 1.1 || 1]});
    for (i = 0; i < nb; i++){
      if (!counts[i]) continue;
      var x0 = f.px(dom[0] + i * wbin), x1 = f.px(dom[0] + (i + 1) * wbin);
      f.svg.push('<rect x="' + fmt(x0, 1) + '" y="' + fmt(f.py(counts[i]), 1) + '" width="' +
        fmt(Math.max(x1 - x0 - 1, 1), 1) + '" height="' + fmt(f.py(0) - f.py(counts[i]), 1) +
        '" fill="' + (o.color || PAL[0]) + '" fill-opacity="0.75"><title>' + counts[i] + " samples</title></rect>");
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
    var names = Object.keys(o.groups), dom = o.ydom;
    if (!dom){
      var all = [];
      names.forEach(function(n){ all = all.concat(o.groups[n]); });
      dom = extent(all);
    }
    var w = o.width || 520, h = o.height || 300;
    var f = frame({width: w, height: h, xlab: o.xlab || "", ylab: o.ylab, xdom: [0, names.length], ydom: dom});
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
          f.svg.push('<circle cx="' + fmt(jx, 1) + '" cy="' + fmt(f.py(x), 1) +
            '" r="2.2" fill="' + col + '" fill-opacity="0.35"/>');
        });
      }
      f.svg.push('<text x="' + cx + '" y="' + (f.h - f.pad.b + 19) + '" font-size="12" text-anchor="middle">' +
        esc(n) + " (" + v.length + ")</text>");
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

  return {palette: PAL, expand: expand, esc: esc, fmt: fmt, mean: mean, median: median, quantile: quantile,
          extent: extent, fit: fit, scatter: scatter, hist: hist, box: box, line: line,
          ui: {select: select, slider: slider, button: button, legend: legend}};
})();
