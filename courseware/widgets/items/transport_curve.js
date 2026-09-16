/* Resistance versus temperature for a real superconducting sample, with a draggable
   threshold to estimate where the resistance falls to (near) zero. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var DATA = RAW; // already an array of {T, R}, sorted by temperature
  var n = DATA.length;
  var maxR = DATA.reduce(function(m, d){ return Math.max(m, d.R); }, 0);
  var thStep = Math.max(1, Math.round(maxR / 200));

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' + CAMEL.ui.slider(id + "-t", "resistance threshold (Ω)", 0,
      Math.ceil(maxR), OPT.threshold_default || Math.round(maxR * 0.05), thStep) + '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function draw(){
    var tEl = document.getElementById(id + "-t");
    document.getElementById(id + "-t-v").innerHTML = tEl.value;
    var th = +tEl.value;
    var cross = null;
    for (var i = 1; i < n; i++){
      if (DATA[i - 1].R < th && DATA[i].R >= th){ cross = {lo: DATA[i - 1], hi: DATA[i]}; break; }
    }
    var pts = DATA.map(function(d){
      var isCross = cross && (d === cross.lo || d === cross.hi);
      return {x: d.T, y: d.R, color: isCross ? "#c0392b" : CAMEL.palette[0],
        label: d.T + " K: " + d.R + " Ω"};
    });
    document.getElementById(id + "-plot").innerHTML = CAMEL.scatter({
      points: pts, xlab: "temperature (K)", ylab: "resistance (Ω)", height: 300, r: 3
    });
    if (cross){
      var frac = (th - cross.lo.R) / (cross.hi.R - cross.lo.R);
      var tEst = cross.lo.T + frac * (cross.hi.T - cross.lo.T);
      document.getElementById(id + "-read").innerHTML =
        "resistance crosses <b>" + th + " Ω</b> between <b>" + CAMEL.fmt(cross.lo.T, 1) +
        "</b> and <b>" + CAMEL.fmt(cross.hi.T, 1) + "</b> K &mdash; about <b>" + CAMEL.fmt(tEst, 1) +
        "</b> K, estimated by interpolating between the two nearest of the " + n +
        " real measurements (sample 20201, 2 K to " + CAMEL.fmt(DATA[n - 1].T, 0) + " K).";
    } else {
      document.getElementById(id + "-read").innerHTML =
        "this threshold is never crossed across the " + n + " measured temperatures (2 K to " +
        CAMEL.fmt(DATA[n - 1].T, 0) + " K).";
    }
  }
  document.getElementById(id + "-t").addEventListener("input", draw);
  draw();
}
