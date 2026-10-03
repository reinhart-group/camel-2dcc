/* G-06: draw random samples of grains and watch the sample means narrow as n grows.
   The horizontal axis is frozen: one fixed range for every spot and every n. */
(function(){
  var rows = CAMEL.expand(DATA), id = root.id, BATCH = 300, N_MIN = 3, N_MAX = 60;
  var SPOTS = {
    all: {t: "all 501 grains", test: function(){ return true; }},
    center: {t: "center only", test: function(d){ return d.spot === "center"; }},
    edge: {t: "edge only", test: function(d){ return d.spot === "toward the edge"; }},
    flat: {t: "toward the flat", test: function(d){ return d.spot === "toward the flat"; }}
  };
  function pop(k){ return rows.filter(SPOTS[k].test); }
  function areas(k){ return pop(k).map(function(d){ return d.area; }); }
  var ALLMEAN = CAMEL.mean(areas("all"));
  /* Samples are drawn WITHOUT replacement from a finite set of N grains, so the spread of sample means is
     sigma / sqrt(n) * sqrt((N - n) / (N - 1)), with sigma the standard deviation of those N grains. */
  function theory(a, n){
    var N = a.length, mu = CAMEL.mean(a), ss = 0, i;
    for (i = 0; i < N; i++) ss += (a[i] - mu) * (a[i] - mu);
    return Math.sqrt(ss / N) / Math.sqrt(n) * Math.sqrt((N - n) / (N - 1));
  }
  /* one range for everything: wide enough for the noisiest case (n = 3) at every spot */
  var lo = Infinity, hi = -Infinity;
  Object.keys(SPOTS).forEach(function(k){
    var a = areas(k), m = CAMEL.mean(a), half = 3.3 * theory(a, N_MIN);
    lo = Math.min(lo, m - half); hi = Math.max(hi, m + half);
  });
  var DOM = [Math.max(0, Math.floor(lo / 500) * 500), Math.ceil(hi / 500) * 500];
  var st = {spot: "all", n: 10}, means = [], last = null, key = null, lastN = null;

  root.innerHTML =
    '<div class="cw-ctls two"><div class="cw-ctl"><label>Sample from</label><div id="' + id + '-sp"></div></div>' +
    CAMEL.ui.slider(id + "-n", "Sample size n", N_MIN, N_MAX, st.n, 1) + '</div>' +
    '<div class="cw-ctls">' + CAMEL.ui.button(id + "-one", "Draw one more sample") + CAMEL.ui.button(id + "-again", "Redraw " + BATCH + " samples", "ghost") + '</div>' +
    '<div class="cw-stats" id="' + id + '-stats"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<div class="cw-cap">The horizontal axis never changes (' + DOM[0].toLocaleString("en-US") + ' to ' + DOM[1].toLocaleString("en-US") + ' nm²), so every redraw can be compared with the last.</div>' +
    '<div class="cw-verdict" id="' + id + '-verdict"></div>' +
    '<div class="cw-subhead">How the typical wander shrinks as n grows</div><div id="' + id + '-se"></div>' +
    '<div class="cw-cap">Theory line: each sample draws grains without repeats from a fixed set of N grains (501 for all, fewer for one spot), so it includes the finite-population correction.</div>';

  function sampleMean(a, n){
    var idx = a.map(function(_, i){ return i; });
    for (var i = idx.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
    return CAMEL.mean(idx.slice(0, Math.min(n, a.length)).map(function(i){ return a[i]; }));
  }
  function batch(a, n){ var o = []; for (var i = 0; i < BATCH; i++) o.push(sampleMean(a, n)); return o; }

  function render(){
    document.getElementById(id + "-sp").innerHTML = CAMEL.ui.seg("spot", Object.keys(SPOTS).map(function(k){ return {v: k, t: SPOTS[k].t}; }), st.spot);
    var a = areas(st.spot), pm = CAMEL.mean(a), obs = CAMEL.stdev(means), th = theory(a, st.n);
    var el = document.getElementById(id + "-plot"), w = CAMEL.widthOf(el);
    var marks = [{x: ALLMEAN, label: "all-grains mean " + CAMEL.fmt(ALLMEAN, 0), color: CAMEL.RED}];
    if (st.spot !== "all") marks.push({x: pm, label: st.spot + "-spot mean " + CAMEL.fmt(pm, 0), color: "#4b5563"});
    if (last !== null) marks.push({x: last, label: "last draw " + CAMEL.fmt(last, 0), color: "#2f855a"});
    el.innerHTML = CAMEL.hist({values: means, bins: 48, xdom: DOM, width: w, height: w < 420 ? 280 : 320, marks: marks,
      xlab: "average grain area of one sample (nm²)", ylab: "number of samples", label: "Histogram of sample means", note: ""});
    document.getElementById(id + "-stats").innerHTML =
      '<div><span class="lab">Samples drawn</span><span class="num">' + means.length + '</span><span class="sub">each of n = ' + st.n + ' grains</span></div>' +
      '<div><span class="lab">Typical wander</span><span class="num">±' + CAMEL.fmt(obs, 0) + '</span><span class="sub">nm²; theory says ' + CAMEL.fmt(th, 0) + '</span></div>';
    document.getElementById(id + "-verdict").innerHTML = st.spot === "all"
      ? 'Sampling variation decreases as n increases: the pile narrows around the mean of all 501 grains. Try center only or edge only: easy to take, but off target.'
      : '<b>A convenient sample is off target.</b> Its pile centers on ' + CAMEL.fmt(pm, 0) + ', not the mean of all 501 grains ' + CAMEL.fmt(ALLMEAN, 0) + '. Increasing n does not remove selection bias.';
    var pts = [], n;
    for (n = N_MIN; n <= N_MAX; n++) pts.push([n, theory(a, n)]);
    var el2 = document.getElementById(id + "-se"), w2 = CAMEL.widthOf(el2);
    el2.innerHTML = CAMEL.lineChart({width: w2, height: 230, xdom: [N_MIN, N_MAX], ydom: [0, theory(a, N_MIN) * 1.08], points: pts,
      xlab: "sample size n (grains per sample)", ylab: "typical wander (nm²)", label: "Typical wander of a sample mean against n",
      marks: [{x: st.n, y: th, label: "n = " + st.n + ": " + CAMEL.fmt(th, 0)}]});
  }
  function refresh(){
    var nEl = document.getElementById(id + "-n"); st.n = +nEl.value;
    document.getElementById(id + "-n-v").innerHTML = st.n;
    var a = areas(st.spot);
    if (key !== st.spot || lastN !== st.n){ means = batch(a, st.n); last = null; key = st.spot; lastN = st.n; }
    render();
  }
  document.getElementById(id + "-n").addEventListener("input", refresh);
  document.getElementById(id + "-one").addEventListener("click", function(){ last = sampleMean(areas(st.spot), st.n); means.push(last); render(); });
  document.getElementById(id + "-again").addEventListener("click", function(){ means = batch(areas(st.spot), st.n); last = null; render(); });
  root.addEventListener("click", function(e){
    var b = e.target.closest ? e.target.closest(".cw-segbtn") : null;
    if (!b) return;
    st.spot = b.getAttribute("data-v"); refresh();
  });
  refresh(); CAMEL.onResize(root, render);
})();
