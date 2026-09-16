/* Compare a measurement across groups: box plots, medians, and the gap between two groups.
   Can show the full range (with outliers) or a zoomed-in typical range; either way the
   readout always says which view is on screen and how many samples are off-scale in it. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var groupings = OPT.groupings;
  var id = root.id;
  var showRange = OPT.range_toggle !== false;
  var defaultView = OPT.default_view || "clip";

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      CAMEL.ui.select(id + "-g", OPT.group_label || "compare by",
        groupings.map(function(g){ return {v: g.key, t: g.label}; }), groupings[0].key) +
      (showRange ? CAMEL.ui.select(id + "-v", "view",
        [{v: "full", t: OPT.full_label || "full range (with outliers)"},
         {v: "clip", t: OPT.clip_label || "typical range (zoomed in)"}], defaultView) : "") +
    '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function draw(){
    var key = document.getElementById(id + "-g").value;
    var vEl = document.getElementById(id + "-v");
    var view = vEl ? vEl.value : "full";
    var groups = {};
    DATA.forEach(function(d){
      var g = d[key], v = d[OPT.value_key];
      if (g === null || g === undefined || v === null || v === undefined) return;
      if (!(g in groups)) groups[g] = [];
      groups[g].push(v);
    });
    var names = Object.keys(groups).filter(function(n){ return groups[n].length >= (OPT.min_n || 5); });
    names.sort(function(a, b){ return groups[b].length - groups[a].length; });
    names = names.slice(0, OPT.max_groups || 5);
    var shown = {}, all = [];
    names.forEach(function(n){ shown[n] = groups[n]; all = all.concat(groups[n]); });

    document.getElementById(id + "-plot").innerHTML = CAMEL.box({
      groups: shown, ylab: OPT.value_label, height: 320,
      clip: view === "full" ? false : undefined
    });

    var d = CAMEL.autoDomain(all, {});
    var viewLine;
    if (view === "full"){
      viewLine = "Showing the <b>full range, including every outlier</b>: 0 of " + all.length +
        " samples are cut off this chart.";
    } else if (d.clipped){
      viewLine = "Showing a <b>zoomed-in, typical range</b>: <b>" + d.over + "</b> of " + all.length +
        " samples across these groups measure above " + CAMEL.fmt(d.dom[1], 1) + " " +
        CAMEL.esc(OPT.unit || "") + " and are drawn pinned to the top edge of the chart, not at " +
        "their real height.";
    } else {
      viewLine = "Showing a <b>zoomed-in, typical range</b>: every one of these " + all.length +
        " samples already fits on the chart, so 0 are off-scale here.";
    }

    var lines = [viewLine];
    names.forEach(function(n){
      lines.push(CAMEL.esc(n) + ": median <b>" + CAMEL.fmt(CAMEL.median(groups[n]), 2) +
        "</b> " + CAMEL.esc(OPT.unit || "") + " (n = " + groups[n].length + ")");
    });
    if (names.length >= 2){
      var gap = CAMEL.median(groups[names[0]]) - CAMEL.median(groups[names[1]]);
      lines.push("gap between the first two medians: <b>" + CAMEL.fmt(Math.abs(gap), 2) + "</b> " +
        CAMEL.esc(OPT.unit || ""));
    }
    document.getElementById(id + "-read").innerHTML = lines.join("<br>");
  }
  document.getElementById(id + "-g").addEventListener("change", draw);
  if (document.getElementById(id + "-v")) document.getElementById(id + "-v").addEventListener("change", draw);
  draw();
}
