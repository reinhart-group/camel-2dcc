/* G-15: pick a claim, weigh the evidence for and against, rewrite it. */
(function(){
  var rows = CAMEL.expand(DATA), id = root.id, claims = cfg.claims, cur = claims[0].key, drafts = {};
  function evalCorr(cl){
    var pts = [], total = rows.length;
    rows.forEach(function(d){ var x = d[cl.x_key], y = d.rough; if (x === null || y === null || x === undefined || y === undefined) return; pts.push({x: x, y: y, color: CAMEL.BLUE}); });
    var f = CAMEL.fit(pts.map(function(p){ return p.x; }), pts.map(function(p){ return p.y; }));
    var el = document.getElementById(id + "-plot"), w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.scatter({points: pts, width: w, height: w < 420 ? 270 : 300, xlab: cl.x_label, ylab: "roughness (nm)", xunit: "min", yunit: "nm", line: f, label: "Roughness against growth time"});
    var pro = [], con = [];
    if (!f) return {pro: ["Not enough paired data to say."], con: []};
    pro.push("Longer growth goes with " + (f.m > 0 ? "higher" : "lower") + " roughness along the line (slope " + CAMEL.fmt(f.m, 3) + " nm per minute).");
    con.push("R² is " + CAMEL.fmt(f.r2, 3) + ": growth time explains about " + CAMEL.fmt(f.r2 * 100, 0) + "% of the spread.");
    con.push("Only " + pts.length + " of " + total.toLocaleString("en-US") + " samples could be checked.");
    con.push("These are records, not a controlled experiment, so “makes” is the wrong verb.");
    return {pro: pro, con: con};
  }
  function evalGroup(cl){
    var groups = {}, counts = {};
    rows.forEach(function(d){
      var g = d[cl.group_key], y = d.rough;
      if (cl.groups.indexOf(g) < 0) return;
      if (!(g in groups)) groups[g] = [];
      if (y !== null && y !== undefined) groups[g].push(y);
      counts[g] = (counts[g] || 0) + 1;
    });
    var shown = {};
    cl.groups.forEach(function(g){ if (groups[g] && groups[g].length) shown[g] = groups[g]; });
    var el = document.getElementById(id + "-plot"), w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.box({groups: shown, ylab: "roughness (nm)", width: w, height: 300, label: "Roughness by growth method"});
    var a = cl.groups[0], b = cl.groups[1], ma = CAMEL.median(groups[a]), mb = CAMEL.median(groups[b]);
    var lo = ma < mb ? a : b;
    return {pro: [CAMEL.esc(lo) + " has the lower median roughness: " + CAMEL.fmt(ma, 2) + " nm for " + a + " against " + CAMEL.fmt(mb, 2) + " nm for " + b + " (a gap of " + CAMEL.fmt(Math.abs(ma - mb), 2) + " nm)."],
      con: ["The groups are lopsided: " + groups[a].length + " measured samples against " + groups[b].length + ".",
            "They were grown for different projects, on different substrates, and measured at different scan sizes.",
            "That makes this an association, not a trial."]};
  }
  function draw(){
    var cl = claims.filter(function(c){ return c.key === cur; })[0];
    root.innerHTML =
      '<div class="cw-claims">' + claims.map(function(c){ return '<button type="button" class="cw-claim' + (c.key === cur ? " on" : "") + '" data-k="' + c.key + '" aria-pressed="' + (c.key === cur) + '">&ldquo;' + CAMEL.esc(c.claim) + '&rdquo;</button>'; }).join("") + '</div>' +
      '<div id="' + id + '-plot"></div>' +
      '<div class="cw-evid"><div class="pro"><h5>Evidence for</h5><ul id="' + id + '-pro"></ul></div><div class="con"><h5>Evidence against</h5><ul id="' + id + '-con"></ul></div></div>' +
      '<div class="cw-ctl"><label for="' + id + '-rewrite">Rewrite the claim so it names its limits</label><textarea id="' + id + '-rewrite" rows="3" placeholder="Among the samples…"></textarea></div>' +
      '<details><summary>See a good rewrite</summary><p>“Among the samples 2DCC happened to measure, MOCVD films were typically smoother, but the two groups were not grown or measured under comparable conditions.” A good rewrite names the population and the limit.</p></details>';
    var ev = cl.type === "correlation" ? evalCorr(cl) : evalGroup(cl);
    document.getElementById(id + "-pro").innerHTML = ev.pro.map(function(x){ return "<li>" + x + "</li>"; }).join("");
    document.getElementById(id + "-con").innerHTML = ev.con.map(function(x){ return "<li>" + x + "</li>"; }).join("");
    var ta = document.getElementById(id + "-rewrite");
    ta.value = drafts[cur] || "";
    ta.addEventListener("input", function(){ drafts[cur] = ta.value; });
    Array.prototype.forEach.call(root.querySelectorAll(".cw-claim"), function(b){
      b.addEventListener("click", function(){ cur = b.getAttribute("data-k"); draw(); });
    });
  }
  draw(); CAMEL.onResize(root, function(){ var cl = claims.filter(function(c){ return c.key === cur; })[0]; if (cl.type === "correlation") evalCorr(cl); else evalGroup(cl); });
})();
