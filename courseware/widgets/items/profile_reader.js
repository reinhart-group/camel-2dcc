/* A real AFM height map with a draggable horizontal line, whose height profile is
   plotted below so a learner reads heights straight off a real surface. The line is drawn
   as a black-and-white striped bar with an arrowhead at each end (not a single colour), so
   it stays visible over every colour the underlying scan can show, including on a washed-out
   projector or phone screen. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var H = RAW.heights, N = H.length, M = H[0].length;
  var lo = Infinity, hi = -Infinity, r, c;
  for (r = 0; r < N; r++) for (c = 0; c < M; c++){
    var v = H[r][c];
    if (v < lo) lo = v;
    if (v > hi) hi = v;
  }
  var stepNm = (RAW.width_um * 1000) / M;
  /* Dark purple to pale yellow: luminance rises monotonically with height (checked:
     ~33, 79, 176, 246 on a 0-255 scale), so the scan itself still reads correctly if a
     screen or projector desaturates it. */
  var stops = [[35, 23, 80], [178, 34, 52], [240, 170, 40], [255, 247, 214]];
  var LINE_COLOR = "#2b6cb0"; /* profile-line blue: not present anywhere in the heatmap ramp */

  function color(v){
    var t = (v - lo) / ((hi - lo) || 1);
    var seg = t * (stops.length - 1);
    var i = Math.min(stops.length - 2, Math.max(0, Math.floor(seg)));
    var f = seg - i;
    var a = stops[i], b = stops[i + 1];
    return [Math.round(a[0] + (b[0] - a[0]) * f), Math.round(a[1] + (b[1] - a[1]) * f),
      Math.round(a[2] + (b[2] - a[2]) * f)];
  }

  var info = RAW.info || {};
  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div style="position:relative;width:300px;max-width:100%;margin:0 auto 4px;touch-action:none">' +
      '<canvas id="' + id + '-cv" width="' + M + '" height="' + N +
      '" style="width:100%;height:auto;display:block;image-rendering:pixelated;border:1px solid #999"></canvas>' +
      '<div id="' + id + '-line" style="position:absolute;left:0;right:0;height:4px;' +
      'margin-top:-2px;background:repeating-linear-gradient(90deg,#111 0,#111 6px,#fff 6px,#fff 12px);' +
      'box-shadow:0 0 0 1px rgba(255,255,255,0.85);pointer-events:none"></div>' +
      '<div id="' + id + '-arrowL" style="position:absolute;left:-9px;width:0;height:0;' +
      'margin-top:-6px;border-top:6px solid transparent;border-bottom:6px solid transparent;' +
      'border-left:9px solid #111;filter:drop-shadow(1px 0 0 #fff) drop-shadow(-1px 0 0 #fff);' +
      'pointer-events:none"></div>' +
      '<div id="' + id + '-arrowR" style="position:absolute;right:-9px;width:0;height:0;' +
      'margin-top:-6px;border-top:6px solid transparent;border-bottom:6px solid transparent;' +
      'border-right:9px solid #111;filter:drop-shadow(1px 0 0 #fff) drop-shadow(-1px 0 0 #fff);' +
      'pointer-events:none"></div>' +
    '</div>' +
    CAMEL.ui.slider(id + "-row", "drag to move the line", 0, N - 1, Math.floor(N / 2), 1) +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(info.story || "") + " " + CAMEL.esc(OPT.note || "") + '</p>';

  var cv = document.getElementById(id + "-cv");
  var ctx = cv.getContext("2d");
  var img = ctx.createImageData(M, N);
  for (r = 0; r < N; r++){
    for (c = 0; c < M; c++){
      var rgb = color(H[r][c]);
      var idx = (r * M + c) * 4;
      img.data[idx] = rgb[0]; img.data[idx + 1] = rgb[1]; img.data[idx + 2] = rgb[2]; img.data[idx + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);

  function draw(){
    var rowEl = document.getElementById(id + "-row");
    document.getElementById(id + "-row-v").innerHTML = rowEl.value;
    var row = +rowEl.value;
    var pct = (N <= 1 ? 0 : (row / (N - 1)) * 100) + "%";
    document.getElementById(id + "-line").style.top = pct;
    document.getElementById(id + "-arrowL").style.top = pct;
    document.getElementById(id + "-arrowR").style.top = pct;
    var profile = H[row];
    var pts = profile.map(function(v, k){ return [k * stepNm, v]; });
    document.getElementById(id + "-plot").innerHTML = CAMEL.line({
      series: [{points: pts, color: LINE_COLOR, width: 2.5, dots: true}],
      xlab: "distance along the line (nm)", ylab: "height (nm)", height: 220
    });
    var minH = Math.min.apply(null, profile), maxH = Math.max.apply(null, profile);
    var biggestStep = 0, k;
    for (k = 1; k < profile.length; k++) biggestStep = Math.max(biggestStep, Math.abs(profile[k] - profile[k - 1]));
    document.getElementById(id + "-read").innerHTML =
      "this line (" + profile.length + " points sampled): height ranges from <b>" + CAMEL.fmt(minH, 2) +
      "</b> to <b>" + CAMEL.fmt(maxH, 2) + "</b> nm. biggest jump between neighboring points on this " +
      "line: <b>" + CAMEL.fmt(biggestStep, 2) + "</b> nm. real scan: " + CAMEL.esc(info.material || "") +
      ", " + CAMEL.fmt(RAW.width_um, 1) + " µm across, " + M + "×" + N + " points sampled.";
  }
  document.getElementById(id + "-row").addEventListener("input", draw);
  draw();
}
