/* D-01: three complexity dials over the same table. */
(function(){
  var rows = CAMEL.expand(DATA), id = root.id, TOTAL = rows.length;
  var TMAX = Math.ceil(Math.max.apply(null, rows.filter(function(d){ return d.time !== null; }).map(function(d){ return d.time; })) / 10) * 10;
  var SUBS = {"Al2O3": 1, "MgO": 1, "GaAs": 1, "InP": 1, "SiO2": 1, "Si": 1, "C-Al2O3": 1};
  var COLS = {few: ["time", "rough"], some: ["mat", "meth", "time", "temp", "rough", "scan"], all: ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]};
  var LABELS = {id: "sample id", mat: "material", sub: "substrate", meth: "growth method", time: "growth time (min)", temp: "temperature (°C)", rough: "roughness (nm)", scan: "scan size (µm)"};
  var DIALS = [
    {key: "structural", t: "Structural", q: "How many variables?", opts: [{v: "few", t: "2"}, {v: "some", t: "6"}, {v: "all", t: "all 8"}]},
    {key: "provenance", t: "Provenance", q: "Mess shown or hidden?", opts: [{v: "surfaced", t: "show the mess"}, {v: "resolved", t: "tidy it quietly"}]},
    {key: "statistical", t: "Statistical", q: "Noise shown or hidden?", opts: [{v: "explicit", t: "show the noise"}, {v: "implicit", t: "typical samples only"}]},
    {key: "merge", t: "A judgment call", q: "Is 2H-MoS2 the same as MoS2?", opts: [{v: "no", t: "keep separate"}, {v: "yes", t: "treat as MoS2"}]}
  ];
  var st = {structural: "some", provenance: "resolved", statistical: "implicit", merge: "no"};   /* a designed starting view, not a neutral baseline */
  root.innerHTML =
    '<div class="cw-dials">' + DIALS.map(function(d){ return '<div class="cw-dial"><div class="dh"><b>' + d.t + '</b><span>' + d.q + '</span></div><div id="' + id + '-' + d.key + '"></div></div>'; }).join("") + '</div>' +
    '<div class="cw-funnel" id="' + id + '-funnel"></div>' +
    '<div class="cw-verdict" id="' + id + '-thread"></div>' +
    '<div id="' + id + '-plot"></div><div class="cw-key" id="' + id + '-key"></div>' +
    '<details open><summary>The table a student would see (first 12 rows)</summary><div class="cw-scroll" id="' + id + '-tbl"></div></details>' +
    '<div class="cw-cap">Tidying uses only the mechanical rules from Find the Mess. Treating 2H-MoS2 as MoS2 is a domain assumption no text rule can make, so it is your choice and starts off.</div>' +
    '<div class="cw-cap">The source table stays fixed. The dials change which rows, columns and labels you meet first. This starting view is one designed presentation, not a neutral baseline.</div>';
  function prepare(){
    var r = rows.map(function(d){ var c = {}, k; for (k in d) c[k] = d[k]; return c; });
    var steps = [{name: "all samples", n: r.length}];
    if (st.provenance === "resolved"){
      r = r.filter(function(d){ return d.mat !== d.sub && !(d.mat in SUBS); });
      r.forEach(function(d){ d.mat = CAMEL.tidyLabel(d.mat, {h2: st.merge === "yes"}); });
      r = r.filter(function(d){ return d.time !== null && d.rough !== null; });
      steps.push({name: "after tidying", n: r.length});
    }
    if (st.statistical === "implicit"){
      r = r.filter(function(d){ return d.scan === 5 && d.rough !== null && d.rough < 10; });
      steps.push({name: "typical only", n: r.length});
    }
    return {rows: r, steps: steps};
  }
  function draw(){
    DIALS.forEach(function(d){ document.getElementById(id + "-" + d.key).innerHTML = CAMEL.ui.seg(d.key, d.opts, st[d.key]); });
    var p = prepare(), cols = COLS[st.structural];
    var pts = [], mats = {}, order = [];
    p.rows.forEach(function(d){
      if (d.time === null || d.rough === null) return;
      var col = CAMEL.BLUE, m = (st.provenance === "resolved" ? d.mat : (d.mat === null ? null : String(d.mat))) || "unknown";
      if (st.structural !== "few"){          /* a material color only when material is one of the variables shown */
        if (!(m in mats)) { mats[m] = order.length; order.push(m); }
        col = CAMEL.palette[mats[m] % CAMEL.palette.length];
      }
      pts.push({x: d.time, y: d.rough, color: col, label: m + ": " + d.time + " min, " + d.rough + " nm"});
    });
    var steps = p.steps.slice(); steps.push({name: "drawn on graph", n: pts.length});
    var fw = CAMEL.widthOf(document.getElementById(id + "-funnel"));
    document.getElementById(id + "-funnel").innerHTML = '<div class="subhead">How many samples are left at each step</div>' +
      CAMEL.hbars({width: fw, max: TOTAL, reserve: 60, items: steps.map(function(s, i){ return {name: s.name, value: s.n, bold: i === steps.length - 1}; }),
      xlab: "number of samples (of " + TOTAL.toLocaleString("en-US") + ")", label: "Samples remaining after each step"});
    var el = document.getElementById(id + "-plot"), w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.scatter({points: pts, width: w, height: w < 420 ? 270 : 300, xlab: "growth time (minutes)", ylab: "roughness (nm)", xunit: "min", yunit: "nm",
      label: "Roughness against growth time", xdom: [0, TMAX], ydom: [0, st.statistical === "implicit" ? 10 : 100],
      note: st.statistical === "implicit" ? "Axes are frozen at 0 to " + TMAX + " min and 0 to 10 nm so the dials can be compared. Typical-only hides everything above 10 nm."
                                          : "Axes are frozen at 0 to " + TMAX + " min and 0 to 100 nm so the dials can be compared. Squashed near the bottom is the real shape of the data."});
    document.getElementById(id + "-key").innerHTML = (st.structural !== "few" && order.length) ?
      order.slice(0, 6).map(function(n, i){ return '<span class="k dot" style="background:' + CAMEL.palette[i % CAMEL.palette.length] + '"></span> ' + CAMEL.esc(n); }).join(" &nbsp; ") : '<span class="k dot" style="background:' + CAMEL.BLUE + '"></span> one color: with only time and roughness, there is nothing else to tell dots apart';
    var in17 = p.rows.some(function(d){ return d.id === 17458; });
    document.getElementById(id + "-thread").innerHTML = '<b>Where is sample 17458, our WSe2 film?</b> ' + (in17
      ? 'Still in the table (a row, but with no growth time, so it is never a dot).'
      : (st.provenance === "resolved" ? 'Gone. The tidy-up removed it because no growth time was recorded.'
                                      : 'Gone. \u201ctypical samples only\u201d removed it: it was scanned at 2 \u00b5m, not the common 5 \u00b5m.'));
    var head = "<tr>" + cols.map(function(c){ return "<th>" + CAMEL.esc(LABELS[c]) + "</th>"; }).join("") + "</tr>";
    var body = p.rows.slice(0, 12).map(function(d){
      return "<tr>" + cols.map(function(c){ var v = d[c], miss = v === null || v === undefined; return "<td" + (miss ? ' class="miss"' : "") + ">" + (miss ? "&mdash;" : CAMEL.esc(v)) + "</td>"; }).join("") + "</tr>";
    }).join("");
    document.getElementById(id + "-tbl").innerHTML = "<table>" + head + body + "</table>";
    Array.prototype.forEach.call(root.querySelectorAll(".cw-segbtn"), function(b){
      b.addEventListener("click", function(){ st[b.getAttribute("data-g")] = b.getAttribute("data-v"); draw(); });
    });
  }
  draw(); CAMEL.onResize(root, draw);
})();
