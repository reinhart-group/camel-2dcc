/* G-01: roughness against growth time, with a switchable best-fit line and color mode. */
(function(){
  var rows = CAMEL.expand(DATA), id = root.id, total = rows.length;
  var st = {line: "on", color: "one"};
  function canonical(m){ return CAMEL.tidyLabel(m); }   /* mechanical rules only; no domain merges */
  root.innerHTML =
    '<div class="cw-ctls two"><div class="cw-ctl"><label>Best-fit line</label><div id="' + id + '-sl"></div></div>' +
    '<div class="cw-ctl"><label>Color the dots</label><div id="' + id + '-sc"></div></div></div>' +
    '<div id="' + id + '-plot"></div><div class="cw-key" id="' + id + '-key"></div>' +
    '<div class="cw-stats" id="' + id + '-stats"></div>' +
    '<div class="cw-meter" id="' + id + '-meter"></div>' +
    '<div class="cw-read" id="' + id + '-read"></div>';
  function draw(){
    document.getElementById(id + "-sl").innerHTML = CAMEL.ui.seg("line", [{v: "on", t: "show"}, {v: "off", t: "hide"}], st.line);
    document.getElementById(id + "-sc").innerHTML = CAMEL.ui.seg("color", [{v: "one", t: "one color"}, {v: "wse2", t: "WSe2 highlighted"}, {v: "mat", t: "by material"}], st.color);
    var pts = [], mats = {}, order = [];
    rows.forEach(function(d){
      if (d.time === null || d.rough === null) return;
      var m = canonical(d.mat) || "unlabelled", col = CAMEL.BLUE, hi = false;
      if (st.color === "wse2"){ if (m === "WSe2") { col = CAMEL.HI; } else col = "#a9bfd8"; }
      else if (st.color === "mat"){
        if (!(m in mats)) { mats[m] = order.length; order.push(m); }
        col = CAMEL.palette[mats[m] % CAMEL.palette.length];
      }
      pts.push({x: d.time, y: d.rough, color: col, label: m + ": " + d.time + " min, " + d.rough + " nm"});
    });
    var f = CAMEL.fit(pts.map(function(p){ return p.x; }), pts.map(function(p){ return p.y; }));
    var el = document.getElementById(id + "-plot"), w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.scatter({points: pts, width: w, height: w < 420 ? 300 : 340, xlab: "growth time (minutes)", ylab: "roughness (nm)",
      xunit: "minutes", yunit: "nm", line: st.line === "on" ? f : null, label: "Roughness against growth time"});
    var key = "";
    if (st.color === "wse2") key = '<span class="k dot" style="background:' + CAMEL.HI + '"></span> WSe2 &nbsp; <span class="k dot" style="background:#a9bfd8"></span> other materials';
    if (st.color === "mat" && order.length) key = order.slice(0, 8).map(function(n, i){ return '<span class="k dot" style="background:' + CAMEL.palette[i % CAMEL.palette.length] + '"></span> ' + CAMEL.esc(n); }).join(" &nbsp; ");
    document.getElementById(id + "-key").innerHTML = key;
    var left = total - pts.length;
    if (f){
      document.getElementById(id + "-stats").innerHTML =
        '<div><span class="lab">Slope</span><span class="num">' + (f.m >= 0 ? "+" : "") + CAMEL.fmt(f.m, 3) + '</span><span class="sub">nm rougher per extra minute</span></div>' +
        '<div><span class="lab">R²</span><span class="num">' + CAMEL.fmt(f.r2, 3) + '</span><span class="sub">share of the differences it explains</span></div>';
      var pct = f.r2 * 100;
      document.getElementById(id + "-meter").innerHTML = '<div class="meter-lab">Growth time explains about <b>' + CAMEL.fmt(pct, 0) + '%</b> of the differences in roughness:</div>' +
        '<div class="meter"><i style="width:' + Math.max(pct, 0.6) + '%"></i></div><div class="meter-ends"><span>0%</span><span>100%</span></div>';
    }
    document.getElementById(id + "-read").innerHTML = '<b>' + pts.length + '</b> of ' + total.toLocaleString("en-US") + ' samples are drawn. <b>' + left +
      '</b> have no growth time or no roughness, so they are left out. Our film, sample 17458, is one of them: no growth time was recorded.';
    Array.prototype.forEach.call(root.querySelectorAll(".cw-segbtn"), function(b){
      b.addEventListener("click", function(){ st[b.getAttribute("data-g")] = b.getAttribute("data-v"); draw(); });
    });
  }
  draw(); CAMEL.onResize(root, draw);
})();
