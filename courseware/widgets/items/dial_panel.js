/* The three CAMEL complexity dials (structural, provenance, statistical) over the
   sample table: same data throughout, only what a learner meets first changes. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var SUBS = {"Al2O3": 1, "MgO": 1, "GaAs": 1, "InP": 1, "SiO2": 1, "Si": 1, "C-Al2O3": 1};

  var COLS = {
    few: ["time", "rough"],
    some: ["mat", "meth", "time", "temp", "rough", "scan"],
    all: ["id", "mat", "sub", "meth", "time", "temp", "rough", "scan"]
  };
  var LABELS = {id: "sample id", mat: "material", sub: "substrate", meth: "growth method",
    time: "growth time (min)", temp: "temperature (°C)", rough: "roughness (nm)",
    scan: "scan size (µm)"};

  var DIALS = [
    {key: "structural", label: "Structural",
      options: [{v: "few", t: "few variables"}, {v: "some", t: "some variables"}, {v: "all", t: "all variables"}]},
    {key: "provenance", label: "Provenance",
      options: [{v: "resolved", t: "resolved"}, {v: "surfaced", t: "surfaced"}]},
    {key: "statistical", label: "Statistical",
      options: [{v: "implicit", t: "noise implicit"}, {v: "explicit", t: "noise explicit"}]}
  ];
  var show = OPT.show || ["structural", "provenance", "statistical"];
  var start = OPT.start || {structural: "some", provenance: "resolved", statistical: "implicit"};
  var fixed = OPT.fixed || {};

  function canonical(m){
    if (m === null || m === undefined) return null;
    var base = String(m).split(";")[0].trim();
    return base === "2H-MoS2" ? "MoS2" : base;
  }

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    (OPT.grade ? '<p class="cw-note"><b>' + CAMEL.esc(OPT.grade) +
      ' starting point shown below &mdash; try turning the dials.</b></p>' : '') +
    '<div class="cw-ctls">' + DIALS.filter(function(d){ return show.indexOf(d.key) >= 0; })
      .map(function(d){ return CAMEL.ui.select(id + "-" + d.key, d.label, d.options,
        (start[d.key] || d.options[0].v)); }).join("") + '</div>' +
    '<div class="cw-read" id="' + id + '-count"></div>' +
    '<ul class="cw-note" id="' + id + '-notes" style="margin:4px 0 10px 18px;padding:0"></ul>' +
    '<div id="' + id + '-plot"></div>' +
    '<div class="cw-key" id="' + id + '-key"></div>' +
    '<div class="cw-scroll" id="' + id + '-tbl"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note ||
      "The data never change. The dials only change what you meet first.") + '</p>';

  function settings(){
    var s = {};
    DIALS.forEach(function(d){
      var el = document.getElementById(id + "-" + d.key);
      s[d.key] = el ? el.value : (fixed[d.key] || start[d.key]);
    });
    return s;
  }

  function prepare(s){
    var rows = DATA.map(function(d){
      var c = {}, k;
      for (k in d) c[k] = d[k];
      return c;
    });
    var notes = [];
    if (s.provenance === "resolved"){
      var before = rows.length;
      rows = rows.filter(function(d){ return d.mat !== d.sub && !(d.mat in SUBS); });
      rows.forEach(function(d){ d.mat = canonical(d.mat); });
      rows = rows.filter(function(d){ return d.time !== null && d.rough !== null; });
      notes.push("resolved: material spellings merged, rows whose material field just named the " +
        "substrate removed, rows missing growth time or roughness removed (" + (before - rows.length) +
        " rows gone)");
    } else {
      notes.push("surfaced: every row as recorded, including " +
        DATA.filter(function(d){ return d.time === null; }).length + " with no growth time and " +
        DATA.filter(function(d){ return d.rough === null; }).length + " never measured for roughness");
    }
    if (s.statistical === "implicit"){
      var b2 = rows.length;
      rows = rows.filter(function(d){ return d.scan === 5 && d.rough !== null && d.rough < 10; });
      notes.push("noise implicit: only the common 5 µm scan size, and roughness under 10 nm, " +
        "kept (" + (b2 - rows.length) + " rows gone)");
    } else {
      notes.push("noise explicit: all scan sizes and all roughness values kept, so the spread is visible");
    }
    return {rows: rows, notes: notes};
  }

  function drawTable(rows, cols){
    var head = "<tr>" + cols.map(function(c){ return "<th>" + CAMEL.esc(LABELS[c] || c) + "</th>"; }).join("");
    head += "</tr>";
    var bodyRows = rows.slice(0, 12).map(function(d){
      return "<tr>" + cols.map(function(c){
        var v = d[c];
        var missing = (v === null || v === undefined);
        return "<td" + (missing ? ' class="miss"' : "") + ">" + (missing ? "&mdash;" : CAMEL.esc(v)) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    document.getElementById(id + "-tbl").innerHTML = "<table>" + head + bodyRows + "</table>";
  }

  function update(){
    var s = settings();
    var prep = prepare(s);
    var cols = COLS[s.structural];
    drawTable(prep.rows, cols);
    var pts = [], mats = {}, order = [];
    prep.rows.forEach(function(d){
      if (d.time === null || d.rough === null) return;
      var m = canonical(d.mat) || "unknown";
      if (!(m in mats)) { mats[m] = order.length; order.push(m); }
      pts.push({x: d.time, y: d.rough, color: CAMEL.palette[mats[m] % CAMEL.palette.length],
        label: m + ": " + d.time + " min, " + d.rough + " nm"});
    });
    document.getElementById(id + "-plot").innerHTML = CAMEL.scatter({
      points: pts, xlab: "growth time (min)", ylab: "roughness (nm)", height: 280
    });
    document.getElementById(id + "-key").innerHTML = order.length ? CAMEL.ui.legend(order.slice(0, 6)) : "";
    document.getElementById(id + "-count").innerHTML =
      "<b>" + prep.rows.length + "</b> of 1,005 samples in the table (<b>" + cols.length +
      "</b> columns shown). The graph can only draw the <b>" + pts.length +
      "</b> rows with both a growth time and a roughness value.";
    document.getElementById(id + "-notes").innerHTML =
      prep.notes.map(function(n){ return "<li>" + n + "</li>"; }).join("");
  }

  DIALS.filter(function(d){ return show.indexOf(d.key) >= 0; }).forEach(function(d){
    document.getElementById(id + "-" + d.key).addEventListener("change", update);
  });
  update();
}
