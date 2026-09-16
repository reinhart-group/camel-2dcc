/* Two on/off requirements gate which rows survive, shown as a live bar chart and a table,
   overall and per group. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var state = {time: true, rough: true};

  function btnStyle(on){
    return "padding:9px 12px;margin:3px 6px 3px 0;font-size:14px;border-radius:6px;" +
      "border:1px solid #2b6cb0;" +
      (on ? "background:#2b6cb0;color:#fff;" : "background:#fff;color:#2b6cb0;");
  }

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      '<button id="' + id + '-t" class="cw-btn" style="' + btnStyle(true) +
        '">require growth time recorded: ON</button>' +
      '<button id="' + id + '-r" class="cw-btn" style="' + btnStyle(true) +
        '">require roughness recorded: ON</button>' +
    '</div>' +
    '<div id="' + id + '-chart"></div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div class="cw-scroll"><table id="' + id + '-table"></table></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function survives(d){
    if (state.time && (d.time === null || d.time === undefined)) return false;
    if (state.rough && (d.rough === null || d.rough === undefined)) return false;
    return true;
  }

  function draw(){
    var groups = {}, order = [];
    DATA.forEach(function(d){
      var g = (d.g === null || d.g === undefined) ? "(blank)" : String(d.g);
      if (!(g in groups)){ groups[g] = {total: 0, keep: 0}; order.push(g); }
      groups[g].total++;
      if (survives(d)) groups[g].keep++;
    });
    order.sort(function(a, b){ return groups[b].total - groups[a].total; });

    var keepAll = 0;
    order.forEach(function(g){ keepAll += groups[g].keep; });

    document.getElementById(id + "-chart").innerHTML = CAMEL.bars({
      items: order.map(function(g){ return {name: g, value: groups[g].keep, back: groups[g].total}; }),
      ylab: "rows kept (pale = total)", width: 520, height: 280
    });

    var rows = ['<tr><th>' + CAMEL.esc(OPT.group_label || "group") + '</th><th>rows kept</th>' +
      '<th>rows total</th><th>%</th></tr>'];
    order.forEach(function(g){
      var gr = groups[g];
      var pct = gr.total ? Math.round(gr.keep / gr.total * 100) : 0;
      rows.push('<tr><td>' + CAMEL.esc(g) + '</td><td' + (pct < 50 ? ' class="miss"' : '') + '>' +
        gr.keep + '</td><td>' + gr.total + '</td><td' + (pct < 50 ? ' class="miss"' : '') + '>' +
        pct + '%</td></tr>');
    });
    document.getElementById(id + "-table").innerHTML = rows.join("");
    document.getElementById(id + "-read").innerHTML =
      "<b>" + keepAll + "</b> of <b>" + DATA.length + "</b> rows overall (" +
      Math.round(keepAll / DATA.length * 100) + "%) meet the requirements you picked.";
  }

  document.getElementById(id + "-t").addEventListener("click", function(){
    state.time = !state.time;
    this.textContent = "require growth time recorded: " + (state.time ? "ON" : "OFF");
    this.setAttribute("style", btnStyle(state.time));
    draw();
  });
  document.getElementById(id + "-r").addEventListener("click", function(){
    state.rough = !state.rough;
    this.textContent = "require roughness recorded: " + (state.rough ? "ON" : "OFF");
    this.setAttribute("style", btnStyle(state.rough));
    draw();
  });
  draw();
}
