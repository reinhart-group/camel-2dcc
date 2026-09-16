/* A sortable, filterable table of odd-looking rows; the reader marks each keep, fix, or remove. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var cols = OPT.columns;
  var decisions = {};
  var sortKey = null, sortDir = 1;
  var filterReason = "all";
  var reasons = [];
  DATA.forEach(function(d){ if (reasons.indexOf(d.reason) < 0) reasons.push(d.reason); });

  function tally(){
    var t = {keep: 0, fix: 0, remove: 0, undecided: 0};
    DATA.forEach(function(d){ t[decisions[d.id] || "undecided"]++; });
    return t;
  }

  function sortedFiltered(){
    var rows = DATA.filter(function(d){ return filterReason === "all" || d.reason === filterReason; });
    if (sortKey){
      rows = rows.slice().sort(function(a, b){
        var av = a[sortKey], bv = b[sortKey];
        if (av === null || av === undefined) av = -Infinity;
        if (bv === null || bv === undefined) bv = -Infinity;
        if (av < bv) return -1 * sortDir;
        if (av > bv) return 1 * sortDir;
        return 0;
      });
    }
    return rows;
  }

  function render(){
    var rows = sortedFiltered();
    var t = tally();
    var filterCtl = reasons.length > 1 ? CAMEL.ui.select(id + "-f", "reason",
      [{v: "all", t: "all reasons"}].concat(reasons.map(function(r){ return {v: r, t: r}; })),
      filterReason) : "";
    var head = "<tr><th>why flagged</th>" + cols.map(function(c){
      return '<th data-k="' + c.key + '" style="cursor:pointer;">' + CAMEL.esc(c.label) +
        (sortKey === c.key ? (sortDir > 0 ? " &#9650;" : " &#9660;") : "") + "</th>";
    }).join("") + "<th>your call</th></tr>";
    var trs = rows.map(function(d){
      var tds = cols.map(function(c){
        var v = d[c.key];
        return "<td>" + (v === null || v === undefined ? "&mdash;" : CAMEL.esc(v)) + "</td>";
      }).join("");
      var dec = decisions[d.id];
      function b(v, label){
        var on = dec === v;
        return '<button class="cw-odd-btn" data-id="' + d.id + '" data-v="' + v + '" style="' +
          "padding:8px 9px;font-size:13px;margin:2px;border-radius:6px;border:1px solid #999;" +
          "background:" + (on ? "#2b6cb0" : "#fff") + ";color:" + (on ? "#fff" : "#111") + ';">' +
          label + "</button>";
      }
      return "<tr><td>" + CAMEL.esc(d.reason) + "</td>" + tds + "<td>" +
        b("keep", "keep") + b("fix", "fix") + b("remove", "remove") + "</td></tr>";
    }).join("");
    body.innerHTML =
      '<p class="cw-q">' + CAMEL.esc(OPT.question) + "</p>" +
      (filterCtl ? '<div class="cw-ctls">' + filterCtl + "</div>" : "") +
      '<div class="cw-read" id="' + id + '-read">' + rows.length + " of " + DATA.length +
        " flagged rows shown &middot; you marked keep " + t.keep + ", fix " + t.fix + ", remove " +
        t.remove + ", undecided " + t.undecided + ".</div>" +
      '<div class="cw-scroll"><table><thead>' + head + "</thead><tbody>" + trs + "</tbody></table></div>" +
      '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + "</p>";
    wire();
  }

  function wire(){
    var f = document.getElementById(id + "-f");
    if (f) f.addEventListener("change", function(){ filterReason = f.value; render(); });
    Array.prototype.forEach.call(body.querySelectorAll("th[data-k]"), function(th){
      th.addEventListener("click", function(){
        var k = th.getAttribute("data-k");
        if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; }
        render();
      });
    });
    Array.prototype.forEach.call(body.querySelectorAll(".cw-odd-btn"), function(btn){
      btn.addEventListener("click", function(){
        var rid = btn.getAttribute("data-id"), v = btn.getAttribute("data-v");
        decisions[rid] = (decisions[rid] === v) ? undefined : v;
        render();
      });
    });
  }
  render();
}
