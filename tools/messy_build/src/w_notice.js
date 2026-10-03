/* Notice-and-wonder: look, jot, then reveal. cfg.kind is "image" or "hist". */
(function(){
  var id = root.id, W = {};
  var html = "";
  if (cfg.kind === "image"){
    html += '<div class="cw-imgwrap"><img src="data:image/png;base64,' + DATA.img + '" alt="Microscope height map of a crystal film: orange triangles on a dark background, color showing height">' +
      '<div class="cw-flag" id="' + id + '-flag" hidden><span>bad scan line</span></div></div>' +
      '<div class="cw-cap">A square patch ' + CAMEL.fmt(DATA.width_um, 1) + ' micrometers on a side (a micrometer is about 1/100th of a hair’s width). Color shows height, not real color.</div>';
  } else {
    html += '<div id="' + id + '-plot"></div>';
  }
  root.innerHTML =
    '<div class="cw-q">' + CAMEL.esc(cfg.question) + '</div>' + html +
    '<div class="cw-ctls two">' +
      '<div class="cw-ctl"><label for="' + id + '-notice">I notice…</label><textarea id="' + id + '-notice" rows="2"></textarea></div>' +
      '<div class="cw-ctl"><label for="' + id + '-wonder">I wonder…</label><textarea id="' + id + '-wonder" rows="2"></textarea></div>' +
    '</div>' +
    '<div class="cw-ctls">' + CAMEL.ui.button(id + "-reveal", "Show what this is") + '</div>' +
    '<div class="cw-reveal" id="' + id + '-out" hidden></div>';
  var revealed = false;
  function drawHist(){
    var el = document.getElementById(id + "-plot");
    if (!el) return;
    var w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.hist({values: DATA.values, bins: 24, width: w, height: w < 420 ? 260 : 300,
      xlab: revealed ? "roughness (nm)" : "value (unit not shown yet)", xunit: revealed ? "nm" : "",
      label: "Histogram of 894 measurements",
      callouts: revealed ? [{x: 2.4, yf: 0.82, text: "most films: under 2 nm", anchor: "start", fill: CAMEL.BLUE},
                           {x: 14.2, yf: 0.34, text: "a long, thin tail", anchor: "end", fill: CAMEL.RED}] : []});
  }
  drawHist(); CAMEL.onResize(root, drawHist);
  document.getElementById(id + "-reveal").addEventListener("click", function(){
    revealed = true; this.disabled = true; this.textContent = "Revealed";
    var out = document.getElementById(id + "-out");
    out.hidden = false;
    var tk = document.getElementById(id + "-take"); if (tk) tk.hidden = false;
    var extra = "";
    if (cfg.kind === "image"){
      document.getElementById(id + "-flag").hidden = false;
      var bw = CAMEL.widthOf(out, 640);
      extra = '<div id="' + id + '-cmp">' + CAMEL.hbars({width: bw, items: [
        {name: "as recorded", value: 6.10, tag: "nm", color: CAMEL.RED},
        {name: "bad line out", value: 0.80, tag: "nm"}], max: 7, xlab: "roughness of this scan (nm)", label: "Roughness with and without the bad line"}) + '</div>';
    } else drawHist();
    out.innerHTML = '<h4>' + CAMEL.esc(cfg.title) + '</h4>' + extra + '<ul>' +
      cfg.lines.map(function(l){ return "<li>" + CAMEL.esc(l) + "</li>"; }).join("") + '</ul>' +
      (cfg.more ? '<details><summary>More detail</summary><p>' + CAMEL.esc(cfg.more) + '</p></details>' : "") +
      (cfg.thread ? '<p class="thread-note">' + cfg.thread + '</p>' : "");
  });
})();
