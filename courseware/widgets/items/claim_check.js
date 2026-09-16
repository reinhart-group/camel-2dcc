/* A learner picks a claim about the data, sees the evidence for and against it
   (including the missing-data imbalance), then rewrites the claim with a limitation. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var claims = OPT.claims;

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question ||
      "Pick a claim about this data. What does the evidence actually show?") + '</p>' +
    '<div class="cw-ctls">' + CAMEL.ui.select(id + "-c", "claim",
      claims.map(function(cl){ return {v: cl.key, t: cl.claim}; }),
      OPT.default_claim || claims[0].key) + '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<div class="cw-read" id="' + id + '-verdict"></div>' +
    '<div class="cw-ctls"><label style="display:block;font-size:13px;font-weight:600;margin-bottom:3px" ' +
      'for="' + id + '-rewrite">rewrite the claim with a limitation</label>' +
    '<textarea id="' + id + '-rewrite" rows="2" style="width:100%;font-size:14px;padding:8px;' +
      'border:1px solid #999;border-radius:6px" placeholder="e.g. In this dataset, longer growth ' +
      'times are associated with slightly higher roughness, but growth time was only recorded for ' +
      'part of the samples."></textarea></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function evalCorrelation(cl){
    var pts = [], total = DATA.length;
    DATA.forEach(function(d){
      var x = d[cl.x_key], y = d.rough;
      if (x === null || x === undefined || y === null || y === undefined) return;
      pts.push({x: x, y: y, color: CAMEL.palette[0]});
    });
    var fit = CAMEL.fit(pts.map(function(p){ return p.x; }), pts.map(function(p){ return p.y; }));
    document.getElementById(id + "-plot").innerHTML = CAMEL.scatter({
      points: pts, xlab: cl.x_label, ylab: "roughness (nm)", line: fit, height: 280
    });
    var lines = ["<b>" + pts.length + "</b> of " + total + " samples have both " +
      CAMEL.esc(cl.x_label) + " and roughness recorded (" + (total - pts.length) + " left out)."];
    var verdict;
    if (!fit){
      verdict = "not enough paired data to say either way.";
    } else {
      var dir = fit.m > 0 ? "higher" : "lower";
      lines.push("least-squares slope <b>" + CAMEL.fmt(fit.m, 4) + "</b> nm per unit, R&sup2; <b>" +
        CAMEL.fmt(fit.r2, 3) + "</b>.");
      if (Math.abs(fit.r2) < 0.05){
        verdict = "evidence for: a weak trend in that direction. evidence against: R&sup2; is very " +
          "low, so " + CAMEL.esc(cl.x_label) + " alone explains very little of the spread in " +
          "roughness. this is an association in observational data, not a controlled experiment.";
      } else {
        verdict = "evidence for: " + CAMEL.esc(cl.x_label) + " is associated with " + dir +
          " roughness along this line. evidence against: R&sup2; of " + CAMEL.fmt(fit.r2, 3) +
          " means most of the spread is not explained by " + CAMEL.esc(cl.x_label) + " alone, and " +
          "only " + pts.length + " of " + total + " samples could even be checked. still an " +
          "association, not a cause.";
      }
    }
    document.getElementById(id + "-read").innerHTML = lines.join("<br>");
    document.getElementById(id + "-verdict").innerHTML = verdict;
  }

  function evalGroup(cl){
    var groups = {}, counts = {};
    DATA.forEach(function(d){
      var g = d[cl.group_key], y = d.rough;
      if (cl.groups.indexOf(g) < 0) return;
      if (!(g in groups)) groups[g] = [];
      if (y !== null && y !== undefined) groups[g].push(y);
      counts[g] = (counts[g] || 0) + 1;
    });
    var shown = {};
    cl.groups.forEach(function(g){ if (groups[g] && groups[g].length) shown[g] = groups[g]; });
    document.getElementById(id + "-plot").innerHTML = CAMEL.box({groups: shown, ylab: "roughness (nm)", height: 280});
    var lines = cl.groups.map(function(g){
      var total = counts[g] || 0, measured = (groups[g] || []).length;
      return CAMEL.esc(g) + ": <b>" + measured + "</b> of " + total +
        " samples have roughness recorded, median " +
        (measured ? CAMEL.fmt(CAMEL.median(groups[g]), 2) : "&mdash;") + " nm.";
    });
    document.getElementById(id + "-read").innerHTML = lines.join("<br>");
    var a = cl.groups[0], b = cl.groups[1], verdict;
    if (!groups[a] || !groups[b] || !groups[a].length || !groups[b].length){
      verdict = "not enough measured samples in one of the groups to compare.";
    } else {
      var ma = CAMEL.median(groups[a]), mb = CAMEL.median(groups[b]);
      var smoother = ma < mb ? a : b;
      verdict = "evidence for: " + CAMEL.esc(smoother) + " has the lower median roughness here (gap " +
        CAMEL.fmt(Math.abs(ma - mb), 2) + " nm). evidence against: the two groups have very " +
        "different sample counts (" + counts[a] + " vs " + counts[b] + " samples, and not every " +
        "sample was measured), so this could reflect which materials or recipes happen to use each " +
        "method rather than the method itself. an association, not a cause.";
    }
    document.getElementById(id + "-verdict").innerHTML = verdict;
  }

  function draw(){
    var key = document.getElementById(id + "-c").value;
    var cl = claims.filter(function(c){ return c.key === key; })[0];
    if (cl.type === "correlation") evalCorrelation(cl); else evalGroup(cl);
  }
  document.getElementById(id + "-c").addEventListener("change", draw);
  draw();
}
