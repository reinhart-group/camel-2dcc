/* Tap a messy spelling, then tap where it belongs; group counts update as you sort them. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var targets = OPT.targets;
  var assign = {};
  RAW.forEach(function(d){ assign[d.raw] = null; });
  var selected = null;

  function totals(){
    var t = {}, unmerged = 0;
    targets.forEach(function(x){ t[x] = 0; });
    RAW.forEach(function(d){
      var a = assign[d.raw];
      if (a) t[a] += d.n; else unmerged += d.n;
    });
    return {t: t, unmerged: unmerged};
  }

  function render(){
    var tot = totals();
    var chartItems = targets.map(function(x){ return {name: x, value: tot.t[x]}; });
    chartItems.push({name: "not sorted yet", value: tot.unmerged, color: "#9ca3af"});
    var bars = '<div id="' + id + '-chart">' +
      CAMEL.bars({items: chartItems, ylab: "rows", width: 520, height: 300}) + '</div>';

    var chips = RAW.map(function(d){
      var a = assign[d.raw];
      var style = a ? "opacity:0.4;text-decoration:line-through;" :
        (d.raw === selected ? "outline:3px solid #2b6cb0;" : "");
      return '<button class="cw-chip" data-raw="' + CAMEL.esc(d.raw) + '" style="' + style +
        'margin:3px;padding:9px 11px;border:1px solid #999;border-radius:16px;background:#fff;' +
        'font-size:14px;">' + CAMEL.esc(d.raw) + " <b>(" + d.n + ")</b>" +
        (a ? " &rarr; " + CAMEL.esc(a) : "") + "</button>";
    }).join("");

    var targetBtns = selected ?
      ('<p class="cw-note">Sorting: <b>' + CAMEL.esc(selected) + '</b></p>' + targets.map(function(x){
        return '<button class="cw-target" data-t="' + CAMEL.esc(x) + '" style="margin:3px;' +
          'padding:11px 13px;border-radius:6px;border:1px solid #2b6cb0;background:#eaf1fb;' +
          'font-size:14px;">' + CAMEL.esc(x) + "</button>";
      }).join("")) :
      '<p class="cw-note">Tap a spelling above, then tap where it belongs.</p>';

    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
      bars +
      '<div style="margin:8px 0;">' + chips + '</div>' +
      '<div id="' + id + '-targets">' + targetBtns + '</div>' +
      (OPT.reveal_lines ? CAMEL.ui.button(id + "-reveal", OPT.reveal_button || "How did the cleanup script sort these?") : "") +
      '<div class="cw-read" id="' + id + '-reveal-text" hidden></div>' +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

    Array.prototype.forEach.call(body.querySelectorAll(".cw-chip"), function(btn){
      btn.addEventListener("click", function(){
        selected = btn.getAttribute("data-raw");
        render();
      });
    });
    Array.prototype.forEach.call(body.querySelectorAll(".cw-target"), function(btn){
      btn.addEventListener("click", function(){
        if (selected){ assign[selected] = btn.getAttribute("data-t"); selected = null; render(); }
      });
    });
    var revealBtn = document.getElementById(id + "-reveal");
    if (revealBtn){
      revealBtn.addEventListener("click", function(){
        var el = document.getElementById(id + "-reveal-text");
        el.hidden = false;
        el.innerHTML = (OPT.reveal_lines || []).map(function(l){ return CAMEL.esc(l); }).join("<br>");
        this.disabled = true;
      });
    }
  }
  render();
}
