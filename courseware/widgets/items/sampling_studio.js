/* Draw random samples of n grains and watch the sample mean bounce around the population
   mean; optionally restrict sampling to one spot on the wafer. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;

  var SPOTS = {
    all: {label: "the whole scanned population", test: function(){ return true; }},
    center: {label: "the center spot only (median grain area 1,526 nm&sup2;)",
      test: function(d){ return d.spot === "center"; }},
    edge: {label: "the edge spot only (median grain area 2,792 nm&sup2;)",
      test: function(d){ return d.spot === "toward the edge"; }},
    flat: {label: "the spot toward the wafer flat only",
      test: function(d){ return d.spot === "toward the flat"; }}
  };

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      CAMEL.ui.select(id + "-r", "sample from",
        [{v: "all", t: "whole population"}, {v: "center", t: "center spot"},
         {v: "edge", t: "edge spot"}, {v: "flat", t: "toward the flat"}], OPT.default_spot || "all") +
      CAMEL.ui.slider(id + "-n", "sample size n", OPT.n_min || 3, OPT.n_max || 60, OPT.n_default || 10, 1) +
    '</div>' +
    '<div class="cw-ctls">' + CAMEL.ui.button(id + "-draw", "draw a new sample") + '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">These 501 grains come from three real scans across one WSe2 wafer ' +
    '(sample 17458) &mdash; a measured population, not a full wafer census. ' +
    CAMEL.esc(OPT.note || "") + '</p>';

  var means = [], lastKey = null, lastN = null;

  function population(key){ return DATA.filter(SPOTS[key].test); }

  function sampleOnce(pop, n){
    var idx = pop.map(function(_, i){ return i; });
    for (var i = idx.length - 1; i > 0; i--){
      var j = Math.floor(Math.random() * (i + 1));
      var t = idx[i]; idx[i] = idx[j]; idx[j] = t;
    }
    return idx.slice(0, Math.min(n, pop.length)).map(function(i){ return pop[i]; });
  }

  function draw(resetHistory){
    var key = document.getElementById(id + "-r").value;
    var nEl = document.getElementById(id + "-n");
    document.getElementById(id + "-n-v").innerHTML = nEl.value;
    var n = +nEl.value;
    var pop = population(key);
    if (resetHistory || key !== lastKey || n !== lastN){ means = []; lastKey = key; lastN = n; }
    var chosen = sampleOnce(pop, n);
    var sMean = CAMEL.mean(chosen.map(function(d){ return d.area; }));
    means.push(sMean);
    var popMean = CAMEL.mean(pop.map(function(d){ return d.area; }));
    document.getElementById(id + "-plot").innerHTML = CAMEL.hist({
      values: means, bins: Math.min(20, Math.max(5, means.length)),
      xlab: "sample mean grain area (nm²)",
      marks: [{x: popMean, label: "population mean " + CAMEL.fmt(popMean, 0), color: "#c0392b"}]
    });
    document.getElementById(id + "-read").innerHTML =
      "sampling from <b>" + SPOTS[key].label + "</b> (" + pop.length + " real measured grains).<br>" +
      "this draw: n=" + chosen.length + ", sample mean <b>" + CAMEL.fmt(sMean, 0) + "</b> nm&sup2;. " +
      "population mean: <b>" + CAMEL.fmt(popMean, 0) + "</b> nm&sup2; over all " + pop.length +
      " grains.<br>" + means.length + " sample" + (means.length === 1 ? "" : "s") + " drawn so far.";
  }
  document.getElementById(id + "-draw").addEventListener("click", function(){ draw(false); });
  document.getElementById(id + "-r").addEventListener("change", function(){ draw(true); });
  document.getElementById(id + "-n").addEventListener("input", function(){ draw(false); });
  draw(true);
}
