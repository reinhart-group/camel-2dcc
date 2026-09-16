/* Clean a hand-typed text column by switching general RULES on and off, and watch the
   number of distinct labels fall and the bar chart tidy up.

   The point of this item is that the reader never has to know what any of the values mean.
   Two earlier versions asked them to sort chemical names into categories, and the operator
   rejected both: "high school math teachers won't know what FeTe is", and then "there are
   too many materials and the participants won't have a clue what they mean". Every rule
   here is decidable from the shape of the text, or from comparing two columns of the same
   row, so the whole activity works with no chemistry at all.

   RAW is {rows: [[material, substrate, count], ...]} -- one entry per distinct pair. */
function(root, RAW, OPT){
  var ROWS = RAW.rows;
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var TOP = OPT.top || 12;
  var RARE = OPT.rare_below || 5;
  var revealed = false;

  var RULES = [
    {key: "dedupe", label: "the same name, typed twice",
     hint: "“SnSe; SnSe” is one material written twice, not two materials."},
    {key: "order", label: "the same list in a different order",
     hint: "“FeSe; FeTe” and “FeTe; FeSe” name the same pair."},
    {key: "junk", label: "a piece that isn't a name at all",
     hint: "“MoS2; 0” has a number where the second name should be."},
    {key: "substrate", label: "the value matches this row's “grown on” column",
     hint: "Someone typed the name of the disc into the box meant for the crystal. " +
           "You can tell without knowing any chemistry: it is the same word as the other " +
           "column on that same row."},
    {key: "rare", label: "fold labels under " + RARE + " samples into “rare”",
     hint: "Not a mistake — a real choice, and one that hides small groups."}
  ];
  var on = {};
  RULES.forEach(function(r){ on[r.key] = false; });

  function parts(s){
    return s.split(";").map(function(p){ return p.replace(/^\s+|\s+$/g, ""); });
  }

  /* Apply the active text rules to one typed value. Returns null when the row leaves the
     chart entirely (the substrate rule moves it to its own pile). */
  function clean(mat, sub){
    if (!mat) return "(nothing typed)";
    if (on.substrate && sub && mat === sub) return null;
    var p = parts(mat);
    if (on.junk){
      var kept = p.filter(function(x){ return /[A-Za-z]/.test(x); });
      if (kept.length) p = kept;
    }
    if (on.dedupe){
      var same = p.every(function(x){ return x === p[0]; });
      if (same) p = [p[0]];
    }
    if (on.order) p = p.slice().sort();
    return p.join("; ");
  }

  function state(){
    var counts = {}, moved = 0, movedLabels = {}, merges = {};
    ROWS.forEach(function(r){
      var mat = r[0], sub = r[1], n = r[2];
      var out = clean(mat, sub);
      if (out === null){ moved += n; movedLabels[mat] = (movedLabels[mat] || 0) + n; return; }
      counts[out] = (counts[out] || 0) + n;
      if (mat && out !== mat) merges[mat] = {to: out, n: n};
    });
    var named = Object.keys(counts).filter(function(k){ return k !== "(nothing typed)"; });
    var rareLabels = [];
    if (on.rare){
      named.forEach(function(k){ if (counts[k] < RARE) rareLabels.push(k); });
      if (rareLabels.length){
        var tot = 0;
        rareLabels.forEach(function(k){ tot += counts[k]; delete counts[k]; });
        counts["rare (" + rareLabels.length + " labels)"] = tot;
      }
    }
    return {counts: counts, distinct: named.length - rareLabels.length + (rareLabels.length ? 1 : 0),
            spellings: named.length, moved: moved, movedLabels: movedLabels,
            merges: merges, rare: rareLabels.length};
  }

  function chart(s){
    var entries = Object.keys(s.counts).map(function(k){ return {name: k, value: s.counts[k]}; });
    entries.sort(function(a, b){ return b.value - a.value; });
    var shown = entries.slice(0, TOP), rest = entries.slice(TOP);
    if (rest.length){
      var tot = 0;
      rest.forEach(function(d){ tot += d.value; });
      shown.push({name: "everything else (" + rest.length + ")", value: tot, color: "#9ca3af"});
    }
    return CAMEL.bars({items: shown, ylab: "samples", width: 520, height: 300,
                       note: rest.length ? "The last bar holds " + rest.length +
                         " more labels, each too small to draw." : ""});
  }

  function mergeTable(s){
    var keys = Object.keys(s.merges);
    if (!keys.length && !s.moved) return "";
    keys.sort(function(a, b){ return s.merges[b].n - s.merges[a].n; });
    var trs = keys.map(function(k){
      return "<tr><td>" + CAMEL.esc(k) + "</td><td>" + CAMEL.esc(s.merges[k].to) +
        "</td><td>" + s.merges[k].n + "</td></tr>";
    });
    Object.keys(s.movedLabels).forEach(function(k){
      trs.push("<tr><td>" + CAMEL.esc(k) + "</td><td><i>set aside: this is the disc, not the " +
        "crystal</i></td><td>" + s.movedLabels[k] + "</td></tr>");
    });
    return '<div class="cw-scroll"><table><thead><tr><th>what was typed</th>' +
      "<th>what your rules count it as</th><th>samples</th></tr></thead><tbody>" +
      trs.join("") + "</tbody></table></div>";
  }

  function render(){
    var s = state();
    var btns = RULES.map(function(r){
      var active = on[r.key];
      return '<button class="cw-rule" data-k="' + r.key + '" style="text-align:left;' +
        "flex:1 1 230px;padding:10px 12px;margin:3px;font-size:13px;border-radius:7px;" +
        "border:1px solid " + (active ? "#2b6cb0" : "#999") + ";background:" +
        (active ? "#2b6cb0" : "#fff") + ";color:" + (active ? "#fff" : "#111") + ';">' +
        (active ? "&#10003; " : "") + CAMEL.esc(r.label) + '<br><span style="font-size:11px;' +
        "opacity:" + (active ? "0.85" : "0.7") + '">' + CAMEL.esc(r.hint) + "</span></button>";
    }).join("");

    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + "</p>" +
      '<div class="cw-read" style="font-size:16px">This one box was typed into by hand. It ' +
        "holds <b>" + s.spellings + "</b> different spelling" + (s.spellings === 1 ? "" : "s") +
        (s.moved ? ", and <b>" + s.moved + "</b> row" + (s.moved === 1 ? "" : "s") +
          " have been set aside" : "") + ".</div>" +
      '<div id="' + id + '-plot">' + chart(s) + "</div>" +
      '<p class="cw-note" style="margin-top:10px"><b>Turn on a rule and watch the chart.</b> ' +
        "Every rule below can be decided from the text itself, or by comparing two columns " +
        "of the same row. None of them needs you to know what any of these substances are." +
      "</p>" +
      '<div class="cw-ctls" style="align-items:stretch">' + btns + "</div>" +
      mergeTable(s) +
      '<div style="margin-top:10px">' + CAMEL.ui.button(id + "-rev",
        revealed ? "hide what the rules cannot fix" : "what do the rules leave behind?") + "</div>" +
      (revealed ? '<div class="cw-read" style="background:#f8fafc;padding:10px;border-radius:8px">' +
        CAMEL.esc(OPT.reveal_title || "") + "<ul>" +
        (OPT.reveal_lines || []).map(function(l){ return "<li>" + CAMEL.esc(l) + "</li>"; }).join("") +
        "</ul></div>" : "") +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + "</p>";
    wire();
  }

  function wire(){
    Array.prototype.forEach.call(body.querySelectorAll(".cw-rule"), function(b){
      b.addEventListener("click", function(){
        var k = b.getAttribute("data-k");
        on[k] = !on[k];
        render();
      });
    });
    document.getElementById(id + "-rev").addEventListener("click", function(){
      revealed = !revealed;
      render();
    });
  }
  render();
}
