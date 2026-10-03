/* M-11: mark each extreme reading keep or remove (or fix, where the fault is known) and watch the mean and median move. */
(function(){
  var rows = CAMEL.expand(DATA.flagged), BG = DATA.bg, id = root.id;
  var decisions = {}, sortKey = "rough", sortDir = -1;
  /* "Fix" is only honest where we know exactly what went wrong. Sample 17458's scan has one corrupted
     line (Notice & Wonder, W-01); with that line dropped the scan measures 0.80 nm. */
  var FIXES = {17458: {to: 0.80, why: "one corrupted scan line; without it the scan measures 0.80 nm"}};
  var COLS = [{key: "mat", label: "material"}, {key: "meth", label: "method"}, {key: "scan", label: "scan size (µm)"}, {key: "rough", label: "roughness (nm)"}];
  var allV = rows.map(function(d){ return d.rough; });
  var whole = BG.concat(allV);
  var XMAX = 2;      /* frozen axis: the whole-dataset mean (1.83) is the largest value that can appear */
  function tally(){ var t = {keep: 0, fix: 0, remove: 0, undecided: 0}; rows.forEach(function(d){ t[decisions[d.id] || "undecided"]++; }); return t; }
  function sorted(){
    return rows.slice().sort(function(a, b){
      var av = a[sortKey], bv = b[sortKey];
      if (av === null || av === undefined) av = -Infinity;
      if (bv === null || bv === undefined) bv = -Infinity;
      return av < bv ? -sortDir : av > bv ? sortDir : 0;
    });
  }
  function render(){
    var t = tally(), kept = [];
    rows.forEach(function(d){ var dec = decisions[d.id]; if (dec === "remove") return; kept.push(dec === "fix" && FIXES[d.id] ? FIXES[d.id].to : d.rough); });
    var after = BG.concat(kept);
    var m0 = CAMEL.mean(whole), m1 = CAMEL.mean(after), d0 = CAMEL.median(whole), d1 = CAMEL.median(after);
    var w = CAMEL.widthOf(root);
    var head = "<tr><th>your call</th>" + COLS.map(function(c){
      return '<th data-k="' + c.key + '" tabindex="0" class="sortable">' + CAMEL.esc(c.label) + (sortKey === c.key ? (sortDir > 0 ? " &#9650;" : " &#9660;") : " &#8645;") + "</th>";
    }).join("") + "</tr>";
    var trs = sorted().map(function(d){
      var dec = decisions[d.id];
      function b(v){ return '<button type="button" class="cw-odd-btn' + (dec === v ? " on" : "") + '" data-id="' + d.id + '" data-v="' + v + '">' + v + "</button>"; }
      var fx = FIXES[d.id];
      return "<tr" + (fx ? ' class="fixable"' : "") + "><td class=\"calls\">" + b("keep") + (fx ? b("fix") : "") + b("remove") + (fx ? '<div class="fix-note">' + (dec === "fix" ? "Fixed: sample " + d.id + " now counts as " + fx.to.toFixed(2) + " nm instead of " + d.rough.toFixed(2) + "." : "Sample " + d.id + ", our film: one corrupted scan line. Fix it to count the corrected " + fx.to.toFixed(2) + " nm.") + "</div>" : "") + "</td>" + COLS.map(function(c){ var v = d[c.key]; return "<td data-label=\"" + CAMEL.esc(c.label) + "\">" + (v === null || v === undefined ? "&mdash;" : CAMEL.esc(v)) + "</td>"; }).join("") + "</tr>";
    }).join("");
    root.innerHTML =
      '<div class="cw-q">These 66 readings are 5 nm or rougher, up to 92 nm. Mark each one <b>keep</b> or <b>remove</b>, or use a shortcut. One row can also be <b>fixed</b>, because its fault is known.</div>' +
      '<div class="cw-ctls"><button type="button" class="cw-btn ghost" id="' + id + '-all">Remove all 66</button>' +
        '<button type="button" class="cw-btn ghost" id="' + id + '-ten">Remove the 10 roughest</button>' +
        '<button type="button" class="cw-btn ghost" id="' + id + '-clr">Clear my marks</button></div>' +
      '<div class="cw-stats"><div><span class="lab">Mean (average)</span><span class="num">' + CAMEL.fmt(m0, 2) + ' &rarr; ' + CAMEL.fmt(m1, 2) + '</span><span class="sub">' + (m0 ? Math.round((m1 - m0) / m0 * 100) : 0) + '% change</span></div>' +
        '<div><span class="lab">Median (middle value)</span><span class="num">' + CAMEL.fmt(d0, 2) + ' &rarr; ' + CAMEL.fmt(d1, 2) + '</span><span class="sub">' + (d0 ? Math.round((d1 - d0) / d0 * 100) : 0) + '% change</span></div></div>' +
      '<div class="cw-key"><span class="k hollow"></span> all ' + whole.length + ' samples &nbsp; <span class="k solid"></span> after your removals (' + after.length + ')</div>' +
      CAMEL.dumbbell({width: w, xdom: [0, XMAX], xlab: "roughness (nm), axis fixed at 0 to 2", label: "Mean and median roughness before and after removals",
        rows: [{label: "mean", a: m0, b: m1}, {label: "median", a: d0, b: d1}]}) +
      '<div class="cw-read">You marked: keep ' + t.keep + ', fix ' + t.fix + ', remove ' + t.remove + ', undecided ' + t.undecided + '.</div>' +
      '<div class="cw-sortsel"><label for="' + id + '-sort">Sort by</label> <select id="' + id + '-sort">' + [["rough|-1", "roughness, high to low"], ["rough|1", "roughness, low to high"], ["mat|1", "material"], ["meth|1", "method"], ["scan|1", "scan size"]].map(function(o){ return '<option value="' + o[0] + '"' + (o[0] === sortKey + "|" + sortDir ? " selected" : "") + ">" + o[1] + "</option>"; }).join("") + '</select></div>' +
      '<div class="cw-scroll"><table class="cards"><thead>' + head + "</thead><tbody>" + trs + "</tbody></table></div>" +
      '<div class="cw-cap">Most films measure under 1 nm. Every row here is flagged for the same reason: 5 nm or more. <b>Keep</b> counts it as read. <b>Remove</b> drops it. <b>Fix</b> corrects the value, and only sample 17458 (orange) has a known fault, one corrupted scan line. Fixed, it counts as 0.80 nm instead of 6.10.</div>';
    wire();
  }
  function wire(){
    Array.prototype.forEach.call(root.querySelectorAll("th[data-k]"), function(th){
      function go(){ var k = th.getAttribute("data-k"); if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; } render(); }
      th.addEventListener("click", go);
      th.addEventListener("keydown", function(e){ if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
    });
    Array.prototype.forEach.call(root.querySelectorAll(".cw-odd-btn"), function(btn){
      btn.addEventListener("click", function(){
        var rid = btn.getAttribute("data-id"), v = btn.getAttribute("data-v");
        decisions[rid] = (decisions[rid] === v) ? undefined : v; render();
      });
    });
    document.getElementById(id + "-all").addEventListener("click", function(){ rows.forEach(function(d){ decisions[d.id] = "remove"; }); render(); });
    document.getElementById(id + "-ten").addEventListener("click", function(){
      decisions = {}; rows.slice().sort(function(a, b){ return b.rough - a.rough; }).slice(0, 10).forEach(function(d){ decisions[d.id] = "remove"; }); render(); });
    document.getElementById(id + "-sort").addEventListener("change", function(){ var v = this.value.split("|"); sortKey = v[0]; sortDir = +v[1]; render(); });
    document.getElementById(id + "-clr").addEventListener("click", function(){ decisions = {}; render(); });
  }
  render(); CAMEL.onResize(root, render);
})();
