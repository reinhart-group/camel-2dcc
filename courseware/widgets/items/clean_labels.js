/* Tap a messy spelling, then tap where it belongs; the bar chart moves live. If OPT.mapping is
   set, the reveal draws a raw-spelling-to-script-bucket table instead of prose alone, marking
   every row where the reader's own pick disagreed with the cleanup script. */
function(root, RAW, OPT){
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var targets = OPT.targets;
  var assign = {};
  RAW.forEach(function(d){ assign[d.raw] = null; });
  var selected = null;
  var revealed = false;
  var total = RAW.reduce(function(s, d){ return s + d.n; }, 0);

  function totals(){
    var t = {}, unmerged = 0;
    targets.forEach(function(x){ t[x] = 0; });
    RAW.forEach(function(d){
      var a = assign[d.raw];
      if (a) t[a] += d.n; else unmerged += d.n;
    });
    return {t: t, unmerged: unmerged};
  }

  function mappingTable(){
    var rows = RAW.map(function(d){
      var mine = assign[d.raw];
      var mismatch = mine && mine !== d.script;
      return "<tr>" +
        "<td>" + CAMEL.esc(d.raw) + " (" + d.n + ")</td>" +
        '<td class="' + (mismatch ? "miss" : "") + '">' +
        (mine ? CAMEL.esc(mine) : "<i>not sorted yet</i>") + "</td>" +
        "<td>" + CAMEL.esc(d.script) + "</td>" +
        "<td>" + (mismatch ? "❗ disagree" : (mine ? "✓ match" : "")) + "</td>" +
        "</tr>";
    }).join("");
    return '<div class="cw-scroll"><table><thead><tr>' +
      "<th>Spelling</th><th>Your bucket</th><th>Script's bucket</th><th>&nbsp;</th>" +
      "</tr></thead><tbody>" + rows + "</tbody></table></div>";
  }

  function render(){
    var tot = totals();
    var sortedN = total - tot.unmerged;
    var chartItems = targets.map(function(x){ return {name: x, value: tot.t[x]}; });
    chartItems.push({name: "not sorted yet", value: tot.unmerged, color: "#9ca3af"});
    var bars = '<div id="' + id + '-chart">' +
      CAMEL.bars({items: chartItems, ylab: "rows", width: 520, height: 300}) + "</div>";

    var readout = '<p class="cw-read">' + sortedN + " of " + total +
      " rows sorted so far; <b>" + tot.unmerged + "</b> left.</p>";

    var chips = RAW.map(function(d){
      var a = assign[d.raw];
      var sel = (!a && d.raw === selected);
      var style = "display:block;width:100%;text-align:left;margin:4px 0;padding:8px 10px;" +
        "border-radius:8px;border:1px solid " + (sel ? "#2b6cb0" : "#bbb") + ";" +
        "background:" + (sel ? "#eaf1fb" : "#fff") + ";" + (a ? "opacity:0.55;" : "");
      var gloss = d.gloss ?
        '<div style="font-size:11px;color:#555;margin-top:2px;">' + CAMEL.esc(d.gloss) + "</div>" : "";
      return '<button class="cw-chip" data-raw="' + CAMEL.esc(d.raw) + '" style="' + style + '">' +
        '<span style="font-size:14px;">' + CAMEL.esc(d.raw) + " <b>(" + d.n + ")</b>" +
        (a ? " → " + CAMEL.esc(a) : "") + "</span>" + gloss + "</button>";
    }).join("");

    var targetBtns = selected ?
      ('<p class="cw-note">Sorting: <b>' + CAMEL.esc(selected) + '</b></p>' + targets.map(function(x){
        return '<button class="cw-target" data-t="' + CAMEL.esc(x) + '" style="display:block;' +
          "width:100%;text-align:left;margin:4px 0;padding:10px 12px;border-radius:6px;" +
          'border:1px solid #2b6cb0;background:#eaf1fb;font-size:14px;">' + CAMEL.esc(x) + "</button>";
      }).join("")) :
      '<p class="cw-note">Tap a spelling above, then tap where it belongs.</p>';

    var revealHtml = "";
    if (revealed){
      if (OPT.mapping) revealHtml += mappingTable();
      if (OPT.reveal_lines){
        revealHtml += '<div style="margin-top:8px;">' +
          OPT.reveal_lines.map(function(l){ return CAMEL.esc(l); }).join("<br><br>") + "</div>";
      }
    }

    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + "</p>" +
      readout + bars +
      '<div style="margin:8px 0;">' + chips + "</div>" +
      '<div id="' + id + '-targets">' + targetBtns + "</div>" +
      (OPT.reveal_lines || OPT.mapping ?
        CAMEL.ui.button(id + "-reveal", OPT.reveal_button || "How did the cleanup script sort these?") : "") +
      '<div class="cw-read" id="' + id + '-reveal-text"' + (revealed ? "" : " hidden") + ">" +
      revealHtml + "</div>" +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + "</p>";

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
        revealed = true;
        render();
      });
    }
  }
  render();
}
