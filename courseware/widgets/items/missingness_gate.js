/* Two on/off requirements gate which rows survive, shown overall and per group. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var state = {time: true, rough: true};

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      CAMEL.ui.button(id + "-t", "require growth time recorded: ON") +
      CAMEL.ui.button(id + "-r", "require roughness recorded: ON") +
    '</div>' +
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
    draw();
  });
  document.getElementById(id + "-r").addEventListener("click", function(){
    state.rough = !state.rough;
    this.textContent = "require roughness recorded: " + (state.rough ? "ON" : "OFF");
    draw();
  });
  draw();
}
