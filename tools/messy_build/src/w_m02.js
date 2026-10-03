/* M-02: two "must be recorded" requirements decide which rows survive. */
(function(){
  var rows = CAMEL.expand(DATA), id = root.id, state = {time: "req", rough: "req"};
  var groups = {}, order = [];
  rows.forEach(function(d){
    var g = (d.g === null || d.g === undefined) ? "(blank)" : String(d.g);
    if (!(g in groups)){ groups[g] = {total: 0}; order.push(g); }
    groups[g].total++;
  });
  order.sort(function(a, b){ return groups[b].total - groups[a].total; });
  var MAXT = groups[order[0]].total;
  function ok(d){
    if (state.time === "req" && (d.time === null || d.time === undefined)) return false;
    if (state.rough === "req" && (d.rough === null || d.rough === undefined)) return false;
    return true;
  }
  var OPTS = [{v: "req", t: "required"}, {v: "any", t: "not required"}];
  root.innerHTML =
    '<div class="cw-q">Keep only the samples where…</div>' +
    '<div class="cw-ctls two"><div class="cw-ctl"><label>growth time was recorded</label><div id="' + id + '-st"></div></div>' +
    '<div class="cw-ctl"><label>roughness was measured</label><div id="' + id + '-sr"></div></div></div>' +
    '<div class="cw-big" id="' + id + '-read"></div>' +
    '<div id="' + id + '-chart"></div>' +
    '<div class="cw-verdict" id="' + id + '-verdict"></div>' +
    '<details><summary>Show the counts as a table</summary><div class="cw-scroll"><table id="' + id + '-table"></table></div></details>';
  function draw(){
    document.getElementById(id + "-st").innerHTML = CAMEL.ui.seg("time", OPTS, state.time);
    document.getElementById(id + "-sr").innerHTML = CAMEL.ui.seg("rough", OPTS, state.rough);
    order.forEach(function(g){ groups[g].keep = 0; });
    rows.forEach(function(d){
      var g = (d.g === null || d.g === undefined) ? "(blank)" : String(d.g);
      if (ok(d)) groups[g].keep++;
    });
    var keepAll = 0; order.forEach(function(g){ keepAll += groups[g].keep; });
    var el = document.getElementById(id + "-chart"), w = CAMEL.widthOf(el);
    el.innerHTML = CAMEL.hbars({width: w, reserve: w < 460 ? 120 : 160, max: MAXT, xlab: "samples (gray = all, blue = kept)",
      label: "Samples kept per growth method",
      items: order.map(function(g){ var p = Math.round(groups[g].keep / groups[g].total * 100);
        return {name: g, value: groups[g].keep, back: groups[g].total, tag: "of " + groups[g].total + " (" + p + "%)", bold: true}; })});
    var worst = order.slice().sort(function(a, b){ return groups[a].keep / groups[a].total - groups[b].keep / groups[b].total; })[0];
    var wp = Math.round(groups[worst].keep / groups[worst].total * 100);
    document.getElementById(id + "-verdict").innerHTML = wp < 50
      ? '<b>' + CAMEL.esc(worst) + ' almost disappears:</b> only ' + groups[worst].keep + ' of ' + groups[worst].total + ' samples (' + wp + '%) survive this rule.'
      : 'Both methods mostly survive. Now try requiring both.';
    document.getElementById(id + "-read").innerHTML = '<span class="num">' + keepAll + '</span> of ' + rows.length.toLocaleString("en-US") + ' samples kept (' + Math.round(keepAll / rows.length * 100) + '%)';
    var tr = ['<tr><th>growth method</th><th>kept</th><th>total</th><th>%</th></tr>'];
    order.forEach(function(g){ var p = Math.round(groups[g].keep / groups[g].total * 100);
      tr.push('<tr><td>' + CAMEL.esc(g) + '</td><td' + (p < 50 ? ' class="miss"' : '') + '>' + groups[g].keep + '</td><td>' + groups[g].total + '</td><td' + (p < 50 ? ' class="miss"' : '') + '>' + p + '%</td></tr>'); });
    document.getElementById(id + "-table").innerHTML = tr.join("");
    Array.prototype.forEach.call(root.querySelectorAll(".cw-segbtn"), function(b){
      b.addEventListener("click", function(){ state[b.getAttribute("data-g")] = b.getAttribute("data-v"); draw(); });
    });
  }
  draw(); CAMEL.onResize(root, draw);
})();
