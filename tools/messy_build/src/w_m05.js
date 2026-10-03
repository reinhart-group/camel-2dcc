/* M-05: switch general cleaning rules from "keep as typed" to "merge" and watch the chart. */
(function(){
  var ROWS = DATA.rows, id = root.id, TOP = 12, RARE = 5, revealed = false;
  var RULES = [
    {key: "dedupe", label: "Same name typed twice", ex: "“SnSe; SnSe” is one material written twice."},
    {key: "order", label: "Same list, different order", ex: "“FeSe; FeTe” and “FeTe; FeSe” name the same pair."},
    {key: "junk", label: "A piece that isn’t a name", ex: "“MoS2; 0” has a number where a name should be."},
    {key: "substrate", label: "Matches the “grown on” column", ex: "The material box holds the substrate’s name (the flat base), the same word as the other column on that row."},
    {key: "rare", label: "Fold labels under " + RARE + " samples into “rare”", ex: "A real choice, and it hides small groups."}
  ];
  var on = {};
  RULES.forEach(function(r){ on[r.key] = false; });      /* default for every rule: keep as typed */

  function parts(s){ return s.split(";").map(function(p){ return p.replace(/^\s+|\s+$/g, ""); }); }
  function clean(mat, sub, on){
    if (!mat) return "(nothing typed)";
    if (on.substrate && sub && mat === sub) return null;
    var p = parts(mat);
    if (on.junk){ var kept = p.filter(function(x){ return /[A-Za-z]/.test(x); }); if (kept.length) p = kept; }
    if (on.dedupe){ if (p.every(function(x){ return x === p[0]; })) p = [p[0]]; }
    if (on.order) p = p.slice().sort();
    return p.join("; ");
  }
  function state(on){
    var counts = {}, moved = 0, movedLabels = {}, merges = {};
    ROWS.forEach(function(r){
      var out = clean(r[0], r[1], on);
      if (out === null){ moved += r[2]; movedLabels[r[0]] = (movedLabels[r[0]] || 0) + r[2]; return; }
      counts[out] = (counts[out] || 0) + r[2];
      if (r[0] && out !== r[0]) merges[r[0]] = {to: out, n: r[2]};
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
    return {counts: counts, spellings: named.length, hidden: rareLabels.length, moved: moved,
            movedLabels: movedLabels, merges: merges};
  }
  var BASE = state(on).spellings;
  function gain(key){            /* how many spellings this rule removes given the other rules' current state */
    var a = {}, b = {}; RULES.forEach(function(r){ a[r.key] = on[r.key]; b[r.key] = on[r.key]; });
    a[key] = false; b[key] = true;
    return state(a).spellings - state(b).spellings;
  }

  function hid(key){ var b = {}; RULES.forEach(function(r){ b[r.key] = on[r.key]; }); b[key] = true; return state(b).hidden; }
  /* Spelling wall: one tile per distinct spelling, sized by sample count. When a rule changes,
     the move plays in three slow steps so it can be followed:
     1) tiles about to go turn red and say where they go ("-> SnSe"); tiles that will grow are marked;
     2) the red tiles shrink away in place;  3) the new wall appears and the grown tiles pulse. */
  var prevOn = null, token = 0, SHRINK = 2000;
  function copyOn(o){ var c = {}; RULES.forEach(function(r){ c[r.key] = o[r.key]; }); return c; }
  function labeller(o){
    var st = state(o), rareName = Object.keys(st.counts).filter(function(k){ return /^rare \(/.test(k); })[0];
    return {s: st, of: function(r){ var out = clean(r[0], r[1], o); if (out === null) return "set aside";
      if (!(out in st.counts) && rareName) return rareName; return out; }};
  }
  function ordered(st){
    var e = Object.keys(st.counts).map(function(k){ return {name: k, value: st.counts[k]}; });
    e.sort(function(a, b){ return b.value - a.value || (a.name < b.name ? -1 : 1); }); return e;
  }
  function wallHtml(entries, maxV, mark){
    return '<div class="sp-wall" role="img" aria-label="' + entries.length + ' distinct spellings">' + entries.map(function(e){
      var fs = (12 + 10 * Math.sqrt(e.value / maxV)).toFixed(1), cls = "sp-tile", extra = "", m = mark[e.name] || {};
      if (e.name === "WSe2") cls += " sp-hi";
      if (/^rare \(/.test(e.name)) cls += " sp-rare";
      if (e.name === "(nothing typed)") cls += " sp-empty";
      if (m.leave){ cls += " sp-leaving"; extra = '<span class="sp-to">&rarr; ' + CAMEL.esc(m.leave) + '</span>'; }
      if (m.coming){ cls += " sp-target"; extra = '<span class="sp-plus">+' + m.coming + ' coming</span>'; }
      if (m.fresh){ cls += " sp-grew"; extra = '<span class="sp-plus">back as typed</span>'; }
      if (m.gained){ cls += " sp-grew"; extra = '<span class="sp-plus">+' + m.gained + ' from ' + m.from + (m.from === 1 ? " spelling" : " spellings") + '</span>'; }
      return '<span class="' + cls + '" data-name="' + CAMEL.esc(e.name) + '" style="font-size:' + fs + 'px"><b>' + CAMEL.esc(e.name) + '</b><i>' + e.value + '</i>' + extra + '</span>';
    }).join("") + '</div>';
  }
  function trayHtml(st){
    var aside = Object.keys(st.movedLabels);
    return aside.length ? '<div class="sp-aside"><span>Set aside (substrate typed as the material):</span>' + aside.map(function(k){
      return '<span class="sp-tile sp-out"><b>' + CAMEL.esc(k) + '</b><i>' + st.movedLabels[k] + '</i></span>'; }).join("") + '</div>' : "";
  }
  var NOTE = '<p class="sp-note">Each tile is one spelling, sized by how many samples use it. Orange: WSe2, the material of our film. Change a rule, read the plan, then press the button to watch the merge.</p>';
  function finalHtml(st, gainedMark){
    var e = ordered(st); return wallHtml(e, e.length ? e[0].value : 1, gainedMark || {}) + trayHtml(st) + NOTE;
  }
  function chart(s){
    /* Viewer-paced: a rule change first shows the plan (red tiles say where they go) and waits for
       "Merge these" / "Apply"; the move then plays slowly. prevOn is the last state actually shown. */
    var el = document.getElementById(id + "-plot"), my = ++token;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!prevOn || reduce){ prevOn = copyOn(on); return finalHtml(s); }
    var A = labeller(prevOn), B = labeller(on), mark = {}, gainedMark = {}, leaving = 0, arriving = 0, moved = false;
    ROWS.forEach(function(r){
      var a = A.of(r), b = B.of(r); if (a === b) return; moved = true;
      if (!(a in B.s.counts) && !mark[a]){ mark[a] = {leave: b}; leaving++; }
      if (b !== "set aside" && (b in A.s.counts)){
        mark[b] = mark[b] || {}; mark[b].coming = (mark[b].coming || 0) + r[2];
        var g = gainedMark[b] = gainedMark[b] || {gained: 0, from: 0, seen: {}};
        g.gained += r[2]; if (!g.seen[a]){ g.seen[a] = 1; g.from++; }
      } else if (b !== "set aside" && !gainedMark[b]){ gainedMark[b] = {fresh: true}; arriving++; }
    });
    if (!moved){ prevOn = copyOn(on); return finalHtml(s); }
    var eA = ordered(A.s), target = copyOn(on);
    var label = leaving ? "Merge these " + leaving + (leaving === 1 ? " spelling" : " spellings") + " &rarr;" : "Split them back apart &rarr;";
    var plan = leaving ? leaving + " red " + (leaving === 1 ? "tile is" : "tiles are") + " about to merge. Each says where it goes."
                       : arriving + (arriving === 1 ? " spelling comes" : " spellings come") + " back as typed.";
    window.setTimeout(function(){
      var btn = document.getElementById(id + "-go"); if (!btn) return;
      btn.addEventListener("click", function(){
        if (my !== token) return; btn.disabled = true;
        Array.prototype.forEach.call(el.querySelectorAll(".sp-leaving"), function(t){ t.classList.add("sp-shrink"); });
        window.setTimeout(function(){ if (my !== token) return; prevOn = target; el.innerHTML = finalHtml(s, gainedMark); }, SHRINK);
      });
    }, 0);
    return '<div class="sp-plan"><span>' + plan + '</span><button type="button" class="cw-btn" id="' + id + '-go">' + label + '</button></div>' +
      wallHtml(eA, eA.length ? eA[0].value : 1, mark) + trayHtml(A.s) + NOTE;
  }
  function mergeTable(s){
    var keys = Object.keys(s.merges);
    if (!keys.length && !s.moved) return "";
    keys.sort(function(a, b){ return s.merges[b].n - s.merges[a].n; });
    var trs = keys.map(function(k){ return "<tr><td>" + CAMEL.esc(k) + "</td><td>" + CAMEL.esc(s.merges[k].to) + "</td><td>" + s.merges[k].n + "</td></tr>"; });
    Object.keys(s.movedLabels).forEach(function(k){
      trs.push("<tr><td>" + CAMEL.esc(k) + "</td><td><i>set aside: this is the substrate (the base), not the crystal</i></td><td>" + s.movedLabels[k] + "</td></tr>");
    });
    return '<details open><summary>What your rules changed (' + trs.length + ' labels)</summary><div class="cw-scroll"><table><thead><tr><th>typed</th><th>counted as</th><th>samples</th></tr></thead><tbody>' +
      trs.join("") + "</tbody></table></div></details>";
  }

  function render(){
    var s = state(on), anyOn = RULES.some(function(r){ return on[r.key]; });
    var rows = RULES.map(function(r){
      var g = gain(r.key);
      return '<div class="cw-rule"><div class="cw-rule-t"><b>' + CAMEL.esc(r.label) + '</b><span>' + CAMEL.esc(r.ex) + '</span></div>' +
        CAMEL.ui.seg(r.key, [{v: "keep", t: "keep as typed"}, {v: "merge", t: r.key === "substrate" ? "set aside" : (r.key === "rare" ? "fold" : "merge")}], on[r.key] ? "merge" : "keep") +
        '<div class="cw-rule-g">' + (r.key === "rare"
          ? (on[r.key] ? "now hides " : "would hide ") + hid(r.key) + " small labels in the chart, and fixes 0 spellings (given your current choices)"
          : (on[r.key] ? "now removes " : "would remove ") + g + (g === 1 ? " spelling" : " spellings") + ", given your current choices") + '</div></div>';
    }).join("");
    root.innerHTML =
      '<div class="cw-big"><span class="num">' + s.spellings + '</span> different spellings <span class="sub2">given your current choices</span>' +
        (s.spellings !== BASE ? ' <span class="delta">down from ' + BASE + '</span>' : '') +
        (s.moved ? '<div class="sub">' + s.moved + ' rows set aside</div>' : "") + '</div>' +
      '<div id="' + id + '-plot"></div>' +
      '<div class="cw-ctls"><button type="button" class="cw-btn ghost" id="' + id + '-reset">Keep everything as typed</button>' +
        '<button type="button" class="cw-btn ghost" id="' + id + '-all">Turn on all five rules</button></div>' +
      '<div class="cw-rules">' + rows + '</div>' + mergeTable(s) +
      '<div class="cw-ctls">' + CAMEL.ui.button(id + "-rev", revealed ? "Hide what rules cannot fix" : "What do the rules leave behind?") + '</div>' +
      (revealed ? revealBox() : "");
    document.getElementById(id + "-plot").innerHTML = chart(s);
    wire();
  }
  function chip(n, c){ return '<span class="chip"><b>' + CAMEL.esc(n) + '</b> ' + c + '</span>'; }
  function revealBox(){
    return '<div class="cw-reveal"><h4>All five rules take 35 spellings down to 25. Four labels still look related:</h4>' +
      '<div class="chips">' + chip("MoS2", 338) + chip("2H-MoS2", 2) + chip("MoS2-WS2", 1) + chip("Mo-WSe2", 18) + '</div>' +
      '<ul><li>No rule written from the text can say which of these name the same substance.</li>' +
      '<li>A rule that strips everything before a dash merges all four: right about one, wrong about the others, and just as tidy.</li>' +
      '<li>The mechanical mess is fixable by anyone. The rest needs someone who knows the field, or an honest “unresolved”.</li>' +
      '<li>Fifteen samples had nothing typed in the box at all, and no rule fixes those either.</li></ul></div>';
  }
  function wire(){
    Array.prototype.forEach.call(root.querySelectorAll(".cw-segbtn"), function(b){
      b.addEventListener("click", function(){ on[b.getAttribute("data-g")] = b.getAttribute("data-v") === "merge"; render(); });
    });
    document.getElementById(id + "-reset").addEventListener("click", function(){ RULES.forEach(function(r){ on[r.key] = false; }); render(); });
    document.getElementById(id + "-all").addEventListener("click", function(){ RULES.forEach(function(r){ on[r.key] = true; }); render(); });
    document.getElementById(id + "-rev").addEventListener("click", function(){ revealed = !revealed; render(); });
  }
  render(); 
})();
