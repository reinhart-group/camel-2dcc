(function(){
  var DATA = __DATA__;
  var SUBS = {"Al2O3":1,"MgO":1,"GaAs":1,"InP":1,"SiO2":1,"Si":1,"C-Al2O3":1};
  var root = document.getElementById("__ID__");
  var $ = function(s){ return root.querySelector(s); };

  function canonical(m){
    if (m === null || m === undefined) return null;
    var base = String(m).split(";")[0].trim();
    if (base === "2H-MoS2") base = "MoS2";
    return base;
  }

  var COLS = {
    few:  ["time","rough"],
    some: ["mat","meth","time","temp","rough","scan"],
    all:  ["id","label","mat","sub","meth","steps","time","temp","press","rough","hrange","scan","pix","lines","date","doi"]
  };
  var LABEL = {id:"sample id", label:"sample label", mat:"material", sub:"substrate",
    meth:"growth method", steps:"steps", time:"growth time (min)", temp:"temperature (C)",
    press:"pressure (Torr)", rough:"roughness (nm)", hrange:"height range (nm)",
    scan:"scan size (um)", pix:"pixels", lines:"lines", date:"growth date", doi:"DOI"};

  function settings(){
    return {
      structural: $("#st").value,
      provenance: $("#pr").value,
      statistical: $("#sa").value
    };
  }

  function prepare(s){
    var rows = DATA.map(function(d){
      var c = {};
      for (var k in d) c[k] = d[k];
      return c;
    });
    var notes = [];
    if (s.provenance === "resolved") {
      var before = rows.length;
      rows = rows.filter(function(d){ return d.mat !== d.sub && !SUBS[d.mat]; });
      rows.forEach(function(d){ d.mat = canonical(d.mat); });
      rows = rows.filter(function(d){ return d.time !== null && d.rough !== null; });
      notes.push("resolved: material spellings merged, rows whose material was really a substrate removed, rows missing growth time or roughness removed (" + (before - rows.length) + " rows gone)");
    } else {
      notes.push("surfaced: every row as recorded, including " +
        DATA.filter(function(d){ return d.time === null; }).length + " with no growth time and " +
        DATA.filter(function(d){ return d.rough === null; }).length + " never measured");
    }
    if (s.statistical === "implicit") {
      var b2 = rows.length;
      rows = rows.filter(function(d){ return d.scan === 5 && d.rough !== null && d.rough < 10; });
      notes.push("implicit: only the common 5 um scan size, and roughness under 10 nm (" + (b2 - rows.length) + " rows gone)");
    } else {
      notes.push("explicit: all scan sizes and all roughness values kept, so the noise is visible");
    }
    return {rows: rows, notes: notes};
  }

  function fmt(v){ return (v === null || v === undefined) ? "" : v; }

  function drawTable(rows, cols){
    var head = "<tr>" + cols.map(function(c){ return "<th>" + LABEL[c] + "</th>"; }).join("") + "</tr>";
    var body = rows.slice(0, 12).map(function(d){
      return "<tr>" + cols.map(function(c){
        var v = fmt(d[c]);
        var cls = (v === "") ? ' class="miss"' : "";
        return "<td" + cls + ">" + (v === "" ? "&mdash;" : v) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    $("#tbl").innerHTML = "<table>" + head + body + "</table>";
  }

  var PALETTE = ["#2b6cb0","#c0392b","#2f855a","#b7791f","#6b46c1","#718096"];

  function drawPlot(rows){
    var pts = rows.filter(function(d){ return d.time !== null && d.rough !== null; });
    var w = Math.min(root.clientWidth - 10, 520), h = 300, pad = 46;
    var xs = pts.map(function(d){ return d.time; }), ys = pts.map(function(d){ return d.rough; });
    var xmax = Math.max.apply(null, xs.concat([1])), ymax = Math.max.apply(null, ys.concat([1]));
    var mats = {}, order = [];
    pts.forEach(function(d){
      var m = canonical(d.mat) || "unknown";
      if (!(m in mats)) { mats[m] = order.length; order.push(m); }
    });
    function px(v){ return pad + (v / xmax) * (w - pad - 12); }
    function py(v){ return h - pad - (v / ymax) * (h - pad - 14); }
    var svg = ['<svg width="' + w + '" height="' + h + '" style="max-width:100%">'];
    svg.push('<line x1="' + pad + '" y1="' + (h - pad) + '" x2="' + (w - 10) + '" y2="' + (h - pad) + '" stroke="#444"/>');
    svg.push('<line x1="' + pad + '" y1="14" x2="' + pad + '" y2="' + (h - pad) + '" stroke="#444"/>');
    pts.forEach(function(d){
      var m = canonical(d.mat) || "unknown";
      var col = PALETTE[mats[m] % PALETTE.length];
      svg.push('<circle cx="' + px(d.time).toFixed(1) + '" cy="' + py(d.rough).toFixed(1) +
               '" r="3.2" fill="' + col + '" fill-opacity="0.65"><title>sample ' + d.id +
               ' ' + (d.mat || "") + ': ' + d.time + ' min, ' + d.rough + ' nm</title></circle>');
    });
    svg.push('<text x="' + (w / 2) + '" y="' + (h - 12) + '" text-anchor="middle" font-size="13">growth time (minutes)</text>');
    svg.push('<text x="14" y="' + (h / 2) + '" text-anchor="middle" font-size="13" transform="rotate(-90 14 ' + (h / 2) + ')">roughness (nm)</text>');
    svg.push('<text x="' + (w - 12) + '" y="' + (h - pad + 16) + '" text-anchor="end" font-size="12">' + xmax + '</text>');
    svg.push('<text x="' + (pad - 6) + '" y="20" text-anchor="end" font-size="12">' + ymax.toFixed(1) + '</text>');
    svg.push("</svg>");
    var key = order.slice(0, 6).map(function(m, i){
      return '<span style="color:' + PALETTE[i % PALETTE.length] + '">&#9679;</span> ' + m;
    }).join(" &nbsp; ");
    $("#plot").innerHTML = svg.join("") + '<div class="key">' + key + "</div>";
    return pts.length;
  }

  function update(){
    var s = settings();
    var prep = prepare(s);
    var cols = COLS[s.structural];
    drawTable(prep.rows, cols);
    var plotted = drawPlot(prep.rows);
    $("#count").innerHTML = "<b>" + prep.rows.length + "</b> of 1005 samples in the table, " +
      "<b>" + cols.length + "</b> columns. The graph can only draw the <b>" + plotted +
      "</b> that have both a growth time and a roughness value.";
    $("#notes").innerHTML = prep.notes.map(function(n){ return "<li>" + n + "</li>"; }).join("");
  }

  ["#st","#pr","#sa"].forEach(function(sel){
    root.querySelector(sel).addEventListener("change", update);
  });
  window.addEventListener("resize", function(){ update(); });
  update();
})();
