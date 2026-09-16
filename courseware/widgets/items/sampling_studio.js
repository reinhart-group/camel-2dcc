/* Draw random samples of n grains and watch the DISTRIBUTION of sample means narrow as
   n grows; optionally restrict sampling to one spot on the wafer. Moving the sample-size
   slider redraws a large batch of samples at that n so the shape appears at once, and the
   horizontal axis is held fixed (sized for the smallest n) so the narrowing is visible
   instead of hidden by an axis that rescales with the data. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var BATCH = OPT.batch || 300;
  var N_MIN = OPT.n_min || 3;

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
    '<div class="cw-ctls">' + CAMEL.ui.button(id + "-draw", "draw one more sample") + '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">These 501 grains come from three real scans across one WSe2 wafer ' +
    '(sample 17458) &mdash; a measured population, not a full wafer census. Moving the sample ' +
    'size slider redraws ' + BATCH + ' fresh samples at that size so the whole distribution of ' +
    'sample means appears at once; the "draw one more sample" button adds a single extra draw ' +
    'to that distribution instead of starting over. ' + CAMEL.esc(OPT.note || "") + '</p>';

  var means = [], lastKey = null, lastN = null, lastSingle = null;
  var domInfo = null; /* {popMean, popSd, dom: [lo, hi]}, fixed while the spot stays the same */

  function population(key){ return DATA.filter(SPOTS[key].test); }

  function stdev(a){
    if (a.length < 2) return 0;
    var m = CAMEL.mean(a), s = 0, i;
    for (i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
    return Math.sqrt(s / (a.length - 1));
  }

  function sampleOnce(pop, n){
    var idx = pop.map(function(_, i){ return i; });
    for (var i = idx.length - 1; i > 0; i--){
      var j = Math.floor(Math.random() * (i + 1));
      var t = idx[i]; idx[i] = idx[j]; idx[j] = t;
    }
    return idx.slice(0, Math.min(n, pop.length)).map(function(i){ return pop[i]; });
  }

  function sampleMean(pop, n){
    return CAMEL.mean(sampleOnce(pop, n).map(function(d){ return d.area; }));
  }

  function drawBatch(pop, n, count){
    var out = [], i;
    for (i = 0; i < count; i++) out.push(sampleMean(pop, n));
    return out;
  }

  /* A domain wide enough to hold the spread expected at the smallest n on the slider
     (that is where sample means bounce around the most), fixed for as long as the
     population (the spot chosen) does not change, so raising n visibly narrows the plot
     instead of an auto-scaling axis hiding it. */
  function fixedDomain(pop){
    var areas = pop.map(function(d){ return d.area; });
    var popMean = CAMEL.mean(areas), popSd = stdev(areas);
    var seAtMin = popSd / Math.sqrt(Math.max(1, N_MIN));
    var half = 3.3 * seAtMin || 1;
    return {popMean: popMean, popSd: popSd, dom: [popMean - half, popMean + half]};
  }

  function render(pop, n, key){
    var obsSd = stdev(means);
    var theorySE = domInfo.popSd / Math.sqrt(n);
    var marks = [{x: domInfo.popMean, label: "population mean " + CAMEL.fmt(domInfo.popMean, 0), color: "#c0392b"}];
    if (lastSingle !== null){
      marks.push({x: lastSingle, label: "your last single draw " + CAMEL.fmt(lastSingle, 0), color: "#2f855a"});
    }
    document.getElementById(id + "-plot").innerHTML = CAMEL.hist({
      values: means, bins: 24, xdom: domInfo.dom,
      xlab: "sample mean grain area (nm²)", ylab: "how many sample means",
      marks: marks
    });
    document.getElementById(id + "-read").innerHTML =
      "sampling from <b>" + SPOTS[key].label + "</b> (" + pop.length + " real measured grains).<br>" +
      "sample size n=" + n + ": " + means.length + " sample means drawn. observed spread " +
      "(standard deviation) of those sample means: <b>" + CAMEL.fmt(obsSd, 0) + "</b> nm&sup2;, " +
      "close to the " + CAMEL.fmt(theorySE, 0) + " nm&sup2; predicted from this population's own " +
      "spread at n=" + n + ".<br>population mean: <b>" + CAMEL.fmt(domInfo.popMean, 0) +
      "</b> nm&sup2; over all " + pop.length + " grains." +
      (lastSingle !== null ? " your last single draw landed at <b>" + CAMEL.fmt(lastSingle, 0) +
        "</b> nm&sup2;." : "");
  }

  function refresh(){
    var key = document.getElementById(id + "-r").value;
    var nEl = document.getElementById(id + "-n");
    document.getElementById(id + "-n-v").innerHTML = nEl.value;
    var n = +nEl.value;
    var pop = population(key);
    if (key !== lastKey){
      domInfo = fixedDomain(pop);
      means = drawBatch(pop, n, BATCH);
      lastSingle = null;
      lastKey = key; lastN = n;
    } else if (n !== lastN){
      means = drawBatch(pop, n, BATCH);
      lastSingle = null;
      lastN = n;
    }
    render(pop, n, key);
  }

  function drawOneMore(){
    var pop = population(lastKey);
    var m = sampleMean(pop, lastN);
    means.push(m);
    lastSingle = m;
    render(pop, lastN, lastKey);
  }

  document.getElementById(id + "-draw").addEventListener("click", drawOneMore);
  document.getElementById(id + "-r").addEventListener("change", refresh);
  document.getElementById(id + "-n").addEventListener("input", refresh);
  refresh();
}
