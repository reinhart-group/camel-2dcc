/* Compare a measurement across groups: box plots, medians, and the gap between two groups. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var groupings = OPT.groupings;
  var id = root.id;
  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      CAMEL.ui.select(id + "-g", OPT.group_label || "compare by",
        groupings.map(function(g){ return {v: g.key, t: g.label}; }), groupings[0].key) +
      (OPT.allow_log ? CAMEL.ui.select(id + "-s", "vertical scale",
        [{v: "linear", t: "as measured"}, {v: "trim", t: "hide values above 10 nm"}], "trim") : "") +
    '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function draw(){
    var key = document.getElementById(id + "-g").value;
    var sEl = document.getElementById(id + "-s");
    var trim = sEl ? sEl.value === "trim" : false;
    var groups = {}, counts = {};
    DATA.forEach(function(d){
      var g = d[key], v = d[OPT.value_key];
      if (g === null || g === undefined || v === null) return;
      if (trim && v > 10) return;
      if (!(g in groups)) { groups[g] = []; counts[g] = 0; }
      groups[g].push(v); counts[g]++;
    });
    var names = Object.keys(groups).filter(function(n){ return groups[n].length >= (OPT.min_n || 5); });
    names.sort(function(a, b){ return groups[b].length - groups[a].length; });
    names = names.slice(0, OPT.max_groups || 5);
    var shown = {};
    names.forEach(function(n){ shown[n] = groups[n]; });
    document.getElementById(id + "-plot").innerHTML =
      CAMEL.box({groups: shown, ylab: OPT.value_label, height: 320});
    var lines = names.map(function(n){
      return CAMEL.esc(n) + ": median <b>" + CAMEL.fmt(CAMEL.median(groups[n]), 2) +
        "</b> " + CAMEL.esc(OPT.unit || "") + " (" + groups[n].length + " samples)";
    });
    if (names.length >= 2){
      var gap = CAMEL.median(groups[names[0]]) - CAMEL.median(groups[names[1]]);
      lines.push("gap between the first two medians: <b>" + CAMEL.fmt(Math.abs(gap), 2) + "</b> " +
        CAMEL.esc(OPT.unit || ""));
    }
    document.getElementById(id + "-read").innerHTML = lines.join("<br>");
  }
  document.getElementById(id + "-g").addEventListener("change", draw);
  if (document.getElementById(id + "-s")) document.getElementById(id + "-s").addEventListener("change", draw);
  draw();
}
