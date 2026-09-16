/* Scan size (the size of the microscope's scan patch, in micrometers/µm) can change a
   roughness reading on its own. Two modes, chosen by OPT.mode:
   "compare" (default) -- compare a measurement across groups, then lock to one scan size and
   watch the group sizes (n) as much as the medians.
   "step" -- one material only: step through scan sizes and watch the distribution, its median,
   and n move together, with an overview bar chart so the trend and the sparse tail both stay
   visible at once. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var mode = OPT.mode || "compare";
  var lowN = (OPT.low_n === undefined) ? 10 : OPT.low_n;
  var STD = [1, 2, 5, 10, 20, 30, 50, 70, 100];

  /* Scan sizes are recorded with a little noise (0.99, 1.99, 2.01 µm ...). Snap anything
     close to a round, standard size to that size; genuinely different sizes (2.5, 3.32, 6.64
     µm) keep their own value instead of being folded into a neighbour. */
  function nominal(x){
    for (var i = 0; i < STD.length; i++){
      if (Math.abs(x - STD[i]) <= STD[i] * 0.08) return STD[i];
    }
    return Math.round(x * 100) / 100;
  }
  function scanLabel(sz){
    return CAMEL.fmt(sz, sz < 10 ? 1 : 0) + " µm";
  }
  function validRows(){
    return DATA.filter(function(d){ return d.scan !== null && d.scan !== undefined &&
      d.rough !== null && d.rough !== undefined; });
  }
  function scanBuckets(rows){
    var c = {};
    rows.forEach(function(d){
      var n = nominal(d.scan);
      (c[n] = c[n] || []).push(d);
    });
    var sizes = Object.keys(c).map(Number).sort(function(a, b){ return a - b; });
    return {sizes: sizes, byScan: c};
  }

  if (mode === "step") buildStep(); else buildCompare();

  /* ---- compare mode: M-08 (by material) and M-09 (by growth method) ---- */
  function buildCompare(){
    var rows = validRows();
    var buckets = scanBuckets(rows);
    var sizeOpts = buckets.sizes.map(function(sz){
      return {v: String(sz), t: scanLabel(sz) + " (n=" + buckets.byScan[sz].length + ")"};
    });

    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
      '<div class="cw-ctls">' +
        CAMEL.ui.select(id + "-lock", "scan size to compare",
          [{v: "all", t: "all sizes together (uncontrolled)"}].concat(sizeOpts), "all") +
      '</div>' +
      '<div class="cw-read" id="' + id + '-read"></div>' +
      '<div id="' + id + '-plot"></div>' +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

    function draw(){
      var lock = document.getElementById(id + "-lock").value;
      var use = lock === "all" ? rows : (buckets.byScan[Number(lock)] || []);
      var groups = {};
      use.forEach(function(d){
        var g = (d.g === null || d.g === undefined) ? "(blank)" : String(d.g);
        (groups[g] = groups[g] || []).push(d.rough);
      });
      var names = Object.keys(groups).sort(function(a, b){
        return CAMEL.median(groups[b]) - CAMEL.median(groups[a]);
      });
      document.getElementById(id + "-plot").innerHTML =
        CAMEL.box({groups: groups, ylab: "roughness (nm)", height: 320});

      var head = lock === "all" ?
        ("All scan sizes together, uncontrolled: <b>" + use.length + "</b> of " + rows.length +
          " valid readings.") :
        ("Locked to <b>" + scanLabel(Number(lock)) + "</b> scans only: <b>" + use.length +
          "</b> of " + rows.length + " valid readings, compared by " +
          CAMEL.esc(OPT.compare_label || OPT.compare_key) + ".");
      var lines = [head];
      names.forEach(function(n){
        var v = groups[n];
        var warn = v.length < lowN ?
          (" &mdash; <b>fewer than " + lowN + " samples: not enough to trust</b>") : "";
        lines.push(CAMEL.esc(n) + ": median <b>" + CAMEL.fmt(CAMEL.median(v), 2) +
          "</b> nm (n = " + v.length + ")" + warn);
      });
      document.getElementById(id + "-read").innerHTML = lines.join("<br>");
    }
    document.getElementById(id + "-lock").addEventListener("change", draw);
    draw();
  }

  /* ---- step mode: M-10 (one material, step through scan sizes) ---- */
  function buildStep(){
    var rows = validRows();
    var buckets = scanBuckets(rows);
    var sizes = buckets.sizes;
    var overview = sizes.map(function(sz){
      return {sz: sz, vals: buckets.byScan[sz].map(function(d){ return d.rough; })};
    });

    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
      '<div class="cw-ctls">' +
        CAMEL.ui.slider(id + "-s", "scan size", 0, sizes.length - 1, 0, 1) +
      '</div>' +
      '<div class="cw-read" id="' + id + '-read"></div>' +
      '<p style="font-size:13px;margin:6px 0 2px;">median roughness at every scan size measured ' +
        'here (n given for each):</p>' +
      '<div id="' + id + '-overview"></div>' +
      '<p style="font-size:13px;margin:10px 0 2px;">the roughness readings at the scan size ' +
        'selected above:</p>' +
      '<div id="' + id + '-plot"></div>' +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

    function drawOverview(idx){
      document.getElementById(id + "-overview").innerHTML = CAMEL.bars({
        items: overview.map(function(o, i){
          return {
            name: scanLabel(o.sz) + " (n=" + o.vals.length + ")",
            value: CAMEL.median(o.vals),
            color: i === idx ? "#c0392b" : "#2b6cb0"
          };
        }),
        ylab: "median roughness (nm)", height: 220
      });
    }

    function draw(){
      var idx = +document.getElementById(id + "-s").value;
      document.getElementById(id + "-s-v").innerHTML = scanLabel(sizes[idx]);
      var vals = overview[idx].vals, med = CAMEL.median(vals);
      drawOverview(idx);
      document.getElementById(id + "-plot").innerHTML = CAMEL.hist({
        values: vals, bins: Math.max(4, Math.min(16, vals.length)), xlab: "roughness (nm)",
        marks: [{x: med, label: "median " + CAMEL.fmt(med, 2), color: "#c0392b"}],
        height: 240, clip: false
      });
      var warn = vals.length < lowN ?
        (" &mdash; <b>only " + vals.length + " sample" + (vals.length === 1 ? "" : "s") +
          " here</b>: this is a single scan or two, not a trend you can trust on its own.") : "";
      document.getElementById(id + "-read").innerHTML =
        "Scan size <b>" + scanLabel(sizes[idx]) + "</b>: median roughness <b>" +
        CAMEL.fmt(med, 2) + "</b> nm, from <b>n = " + vals.length + "</b> of " + rows.length +
        " valid readings in this set." + warn;
    }
    document.getElementById(id + "-s").addEventListener("input", draw);
    draw();
  }
}
