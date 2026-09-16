/* Scatter plot of roughness against one recipe variable, with an optional least-squares
   line, an R-squared readout, and a toggle to colour points by material. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var xKey = OPT.x_key, xLabel = OPT.x_label;
  var total = DATA.length;

  function canonical(m){
    if (m === null || m === undefined) return null;
    var base = String(m).split(";")[0].trim();
    return base === "2H-MoS2" ? "MoS2" : base;
  }

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    (OPT.allow_color ? '<div class="cw-ctls">' + CAMEL.ui.select(id + "-c", "colour",
      [{v: "off", t: "one colour"}, {v: "on", t: "colour by material"}], OPT.color_default || "off") +
      '</div>' : '') +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<div class="cw-key" id="' + id + '-key"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function draw(){
    var colorEl = document.getElementById(id + "-c");
    var colorOn = OPT.allow_color && colorEl && colorEl.value === "on";
    var pts = [], mats = {}, order = [];
    DATA.forEach(function(d){
      var x = d[xKey], y = d.rough;
      if (x === null || x === undefined || y === null || y === undefined) return;
      var m = canonical(d.mat) || "unlabeled";
      var col = CAMEL.palette[0];
      if (colorOn){
        if (!(m in mats)) { mats[m] = order.length; order.push(m); }
        col = CAMEL.palette[mats[m] % CAMEL.palette.length];
      }
      pts.push({x: x, y: y, color: col, label: m + ": " + x + " " + (OPT.x_unit || "") + ", " + y + " nm"});
    });
    var fit = CAMEL.fit(pts.map(function(p){ return p.x; }), pts.map(function(p){ return p.y; }));
    document.getElementById(id + "-plot").innerHTML = CAMEL.scatter({
      points: pts, xlab: xLabel, ylab: "roughness (nm)", line: fit, height: 300
    });
    var lines = [];
    lines.push("<b>" + pts.length + "</b> of the 1,005 samples have both " + CAMEL.esc(xLabel) +
      " and a roughness measurement recorded, so only those are drawn (<b>" + (total - pts.length) +
      "</b> left out).");
    if (fit){
      lines.push("least-squares line: slope <b>" + CAMEL.fmt(fit.m, 4) + "</b> nm per " +
        CAMEL.esc(OPT.x_unit || "unit") + ", R&sup2; <b>" + CAMEL.fmt(fit.r2, 3) + "</b>.");
      lines.push("these are observational records, not a controlled experiment: this line shows an " +
        "association, not that " + CAMEL.esc(xLabel) + " causes the roughness.");
    } else {
      lines.push("not enough paired points to fit a line.");
    }
    document.getElementById(id + "-read").innerHTML = lines.join("<br>");
    document.getElementById(id + "-key").innerHTML = (colorOn && order.length) ?
      CAMEL.ui.legend(order.slice(0, 8)) : "";
  }
  if (OPT.allow_color) document.getElementById(id + "-c").addEventListener("change", draw);
  draw();
}
