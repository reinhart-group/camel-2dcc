/* Compare roughness across scan sizes, then control for scan size, showing why the first look was unfair. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var hasCompare = !!OPT.compare_key;
  var locked = false;

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    (hasCompare ? '<div class="cw-ctls">' +
      CAMEL.ui.button(id + "-lock", "control for scan size: only compare samples scanned the same size") +
      '</div>' : "") +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function validRows(){
    return DATA.filter(function(d){ return d.scan !== null && d.scan !== undefined &&
      d.rough !== null && d.rough !== undefined; });
  }
  function modeScan(rows){
    var c = {}, best = null, bn = 0;
    rows.forEach(function(d){ c[d.scan] = (c[d.scan] || 0) + 1; });
    Object.keys(c).forEach(function(k){ if (c[k] > bn){ bn = c[k]; best = +k; } });
    return best;
  }

  function draw(){
    var rows = validRows();
    var groups = {}, msg;
    if (hasCompare){
      var use = rows, m = null;
      if (locked){
        m = modeScan(rows);
        use = rows.filter(function(d){ return d.scan === m; });
      }
      use.forEach(function(d){
        var g = (d.g === null || d.g === undefined) ? "(blank)" : String(d.g);
        (groups[g] = groups[g] || []).push(d.rough);
      });
      msg = locked ?
        (use.length + " of " + rows.length + " samples were scanned at " + CAMEL.fmt(m, 1) +
          " &micro;m across (the most common size here). Only those are compared now, by " +
          CAMEL.esc(OPT.compare_label || OPT.compare_key) + ".") :
        (rows.length + " samples, scanned at many different sizes, compared without controlling for that.");
    } else {
      rows.forEach(function(d){
        var k = CAMEL.fmt(d.scan, 1) + " &micro;m scan";
        (groups[k] = groups[k] || []).push(d.rough);
      });
      msg = rows.length + " samples of one material, grouped by the size of the scan.";
    }
    document.getElementById(id + "-read").innerHTML = msg;
    document.getElementById(id + "-plot").innerHTML = CAMEL.box({groups: groups, ylab: "roughness (nm)",
      height: 320});
  }

  if (hasCompare){
    document.getElementById(id + "-lock").addEventListener("click", function(){
      locked = !locked;
      this.textContent = locked ? "show all scan sizes again (uncontrolled)" :
        "control for scan size: only compare samples scanned the same size";
      draw();
    });
  }
  draw();
}
