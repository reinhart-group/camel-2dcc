/* Show one image or plot with no explanation, ask what you notice and wonder, then reveal what it is. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var plotHtml = "";
  if (OPT.kind === "image"){
    plotHtml = '<img src="data:image/jpeg;base64,' + RAW.img + '" alt="a microscope height map" ' +
      'style="width:100%;max-width:340px;display:block;margin:0 auto;border:1px solid #ccc;border-radius:8px;">' +
      '<p class="cw-note">This picture shows a square patch of surface ' + CAMEL.fmt(RAW.width_um, 1) +
      ' micrometers on a side (one micrometer is about 1/100th the width of a human hair). ' +
      'Color shows height, not real color &mdash; the microscope only measures how tall things are.</p>';
  } else if (OPT.kind === "hist"){
    plotHtml = '<div id="' + id + '-plot">' + CAMEL.hist({values: RAW.values, bins: OPT.bins || 24,
      xlab: OPT.xlab}) + '</div>' +
      '<p class="cw-note">' + RAW.values.length + ' measurements are plotted here.</p>';
  } else if (OPT.kind === "line"){
    plotHtml = '<div id="' + id + '-plot">' + CAMEL.line({series: [{name: "", points: RAW.points,
      dots: (RAW.points.length < 60)}], xlab: OPT.xlab, ylab: OPT.ylab}) + '</div>' +
      '<p class="cw-note">' + RAW.points.length + ' measurements are plotted here.</p>';
  }
  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    plotHtml +
    '<div class="cw-ctls">' +
      '<div class="cw-ctl"><label for="' + id + '-notice">What do you notice?</label>' +
        '<textarea id="' + id + '-notice" rows="2" style="width:100%;font-size:15px;padding:6px;' +
        'border:1px solid #999;border-radius:6px;"></textarea></div>' +
      '<div class="cw-ctl"><label for="' + id + '-wonder">What do you wonder?</label>' +
        '<textarea id="' + id + '-wonder" rows="2" style="width:100%;font-size:15px;padding:6px;' +
        'border:1px solid #999;border-radius:6px;"></textarea></div>' +
    '</div>' +
    CAMEL.ui.button(id + "-reveal", OPT.reveal_button || "Show what this is") +
    '<div class="cw-read" id="' + id + '-reveal-text" hidden></div>';

  document.getElementById(id + "-reveal").addEventListener("click", function(){
    var el = document.getElementById(id + "-reveal-text");
    el.hidden = false;
    el.innerHTML = "<b>" + CAMEL.esc(OPT.reveal_title || "") + "</b><br>" +
      (OPT.reveal_lines || []).map(function(l){ return CAMEL.esc(l); }).join("<br>");
    this.disabled = true;
    this.textContent = OPT.reveal_button_after || "Revealed";
  });
}
