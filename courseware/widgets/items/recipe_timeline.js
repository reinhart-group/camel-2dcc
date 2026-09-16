/* A real growth recipe as temperature versus elapsed time, step by step, with each
   step's duration and the rate of change from the previous step. One recipe, or two
   recipes compared on the same axes. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var compare = OPT.mode === "compare";
  var recipes = compare ?
    [{rows: RAW.a, meta: OPT.a}, {rows: RAW.b, meta: OPT.b}] :
    [{rows: RAW, meta: OPT.a}];

  function stepPoints(rows){
    var pts = [];
    rows.forEach(function(r){
      if (r.temp === null || r.temp === undefined) return;
      pts.push([r.start, r.temp]);
      pts.push([r.start + r.dur, r.temp]);
    });
    return pts;
  }

  var series = recipes.map(function(r, i){
    return {name: r.meta.label, points: stepPoints(r.rows), color: CAMEL.palette[i % CAMEL.palette.length]};
  });

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div id="' + id + '-plot"></div>' +
    (compare ? '<div class="cw-key" id="' + id + '-key"></div>' : '') +
    '<div class="cw-scroll" id="' + id + '-tbl"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  document.getElementById(id + "-plot").innerHTML = CAMEL.line({
    series: series, xlab: "elapsed time (minutes)", ylab: "temperature (°C)", height: 300
  });
  if (compare){
    document.getElementById(id + "-key").innerHTML =
      CAMEL.ui.legend(recipes.map(function(r){ return r.meta.label; }));
  }

  function stepTable(rows, label){
    var rowsHtml = rows.map(function(r, i){
      var prevTemp = i > 0 ? rows[i - 1].temp : null;
      var rate = "&mdash;";
      if (r.temp !== null && r.temp !== undefined && prevTemp !== null && prevTemp !== undefined && r.dur){
        rate = CAMEL.fmt((r.temp - prevTemp) / r.dur, 2) + " °C/min";
      }
      return "<tr><td>" + CAMEL.esc(r.step) + "</td><td>" +
        (r.dur === null || r.dur === undefined ? "&mdash;" : CAMEL.fmt(r.dur, 1)) + "</td><td>" +
        (r.temp === null || r.temp === undefined ? "&mdash;" : CAMEL.fmt(r.temp, 0)) + "</td><td>" +
        rate + "</td></tr>";
    }).join("");
    return "<p><b>" + CAMEL.esc(label) + "</b></p><table><tr><th>step</th><th>duration (min)</th>" +
      "<th>temperature (°C)</th><th>change from previous step</th></tr>" + rowsHtml + "</table>";
  }
  document.getElementById(id + "-tbl").innerHTML =
    recipes.map(function(r){ return stepTable(r.rows, r.meta.label); }).join("");
}
