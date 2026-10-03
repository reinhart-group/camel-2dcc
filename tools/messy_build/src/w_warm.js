/* Warm-up: ONE live 3D viewer. The three buttons swap the surface (the old one is purged first). */
(function(){
  root.innerHTML =
    '<div class="cw-seg" id="wu-picks" role="radiogroup" aria-label="Choose a surface"></div>' +
    '<div class="wu-cap" id="wu-cap"></div>' +
    '<div class="wu-stage"><div id="wu-plot"></div><div class="wu-msg" id="wu-msg">Loading the 3D surface…</div></div>' +
    '<div class="cw-cap">Drag to rotate, scroll or pinch to zoom. On a phone, swipe the text above or below to scroll the page. All three surfaces are stretched 25 times vertically, by the same amount, so they compare fairly.</div>';
  var el = document.getElementById("wu-plot"), msg = document.getElementById("wu-msg"), cap = document.getElementById("wu-cap");
  var picks = document.getElementById("wu-picks");
  var cur = 0, state = "loading", drawnFor = -1;
  function say(t){ msg.textContent = t; msg.style.display = t ? "" : "none"; el.style.visibility = t ? "hidden" : "visible"; }
  function purge(){ if (drawnFor >= 0) { try { Plotly.purge(el); } catch(e){} drawnFor = -1; } }
  function draw(){
    if (state !== "ready" || !(root.clientWidth > 0)) return;
    if (drawnFor === cur) { try { Plotly.Plots.resize(el); } catch(e){} return; }
    purge();
    var it = items[cur], w = root.clientWidth;
    var layout = JSON.parse(JSON.stringify(it.spec.layout));
    layout.height = w < 520 ? 420 : 560;
    layout.paper_bgcolor = "#ffffff";
    if (w < 520 && layout.title) { var tt = layout.title.text || ""; layout.title = {text: tt.replace(" \u2014 ", "<br>"), font: {size: 14}, x: 0.02, xanchor: "left"}; layout.margin = {l: 0, r: 0, t: 64, b: 0}; }
    if (layout.scene && layout.scene.zaxis) layout.scene.zaxis.nticks = 4;
    say("");
    Plotly.newPlot(el, it.spec.data, layout, {responsive: true, displaylogo: false}).then(function(){
      drawnFor = cur;
      var cv = el.querySelector("canvas");
      if (cv) cv.addEventListener("webglcontextlost", function(){ drawnFor = -1; say("The browser reclaimed the 3D view. Tap a surface button to redraw it."); });
    });
  }
  function show(i){
    cur = i;
    cap.textContent = items[i].caption;
    picks.innerHTML = items.map(function(it, k){
      return '<button type="button" role="radio" aria-checked="' + (k === i) + '" class="cw-segbtn' + (k === i ? " on" : "") + '" data-i="' + k + '">' + (k === i ? "&#10003; " : "") + CAMEL.esc(it.name) + '</button>';
    }).join("");
    Array.prototype.forEach.call(picks.querySelectorAll("button"), function(b){ b.addEventListener("click", function(){ show(+b.getAttribute("data-i")); }); });
    if (state === "failed") say("The 3D viewer could not load (it needs an internet connection). Everything else on this page still works.");
    else if (state === "ready") { say(""); draw(); }
  }
  function loaded(){ state = "ready"; show(cur); }
  function failed(){ state = "failed"; purge(); show(cur); }
  CAMEL.onResize(root, function(){ if (state === "ready") draw(); });
  show(0);
  if (window.Plotly) loaded();
  else {
    var amd = window.define; window.define = undefined;
    var s = document.createElement("script");
    s.src = "https://cdn.plot.ly/plotly-2.35.2.min.js"; s.charset = "utf-8";
    s.onload = function(){ window.define = amd; loaded(); };
    s.onerror = function(){ window.define = amd; failed(); };
    document.head.appendChild(s);
  }
})();
