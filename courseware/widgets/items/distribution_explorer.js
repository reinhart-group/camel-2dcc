/* A histogram with a bin-count slider and toggles for the mean and median lines. */
function(root, RAW, OPT){
  var DATA = CAMEL.expand(RAW);
  var body = root.querySelector(".cw-body");
  var id = root.id;
  var hasGroup = !!(OPT.group_options && OPT.group_options.length);

  body.innerHTML =
    '<p class="cw-q">' + CAMEL.esc(OPT.question) + '</p>' +
    '<div class="cw-ctls">' +
      (hasGroup ? CAMEL.ui.select(id + "-g", OPT.group_label || "show", OPT.group_options,
        OPT.group_options[0].v) : "") +
      CAMEL.ui.slider(id + "-b", "number of bins", OPT.bins_min || 6, OPT.bins_max || 40,
        OPT.bins_default || 18, 1) +
    '</div>' +
    '<div class="cw-ctls">' +
      '<label style="font-size:14px;"><input type="checkbox" id="' + id + '-mean"> show mean</label>' +
      '<label style="font-size:14px;"><input type="checkbox" id="' + id + '-median" checked> show median</label>' +
    '</div>' +
    '<div class="cw-read" id="' + id + '-read"></div>' +
    '<div id="' + id + '-plot"></div>' +
    '<p class="cw-note">' + CAMEL.esc(OPT.note || "") + '</p>';

  function values(){
    var rows = DATA;
    if (hasGroup){
      var g = document.getElementById(id + "-g").value;
      rows = rows.filter(function(d){ return String(d.g) === String(g); });
    }
    return rows.map(function(d){ return d.v; }).filter(function(x){
      return x !== null && x !== undefined && !isNaN(x);
    });
  }

  function draw(){
    var xs = values();
    var bins = +document.getElementById(id + "-b").value;
    var marks = [];
    if (document.getElementById(id + "-mean").checked && xs.length){
      marks.push({x: CAMEL.mean(xs), label: "mean", color: "#2f855a"});
    }
    if (document.getElementById(id + "-median").checked && xs.length){
      marks.push({x: CAMEL.median(xs), label: "median", color: "#c0392b"});
    }
    document.getElementById(id + "-plot").innerHTML = CAMEL.hist({values: xs, bins: bins,
      xlab: OPT.value_label + (OPT.unit ? " (" + OPT.unit + ")" : ""), marks: marks});
    var lines = [xs.length + " samples shown" + (hasGroup ?
      " for " + CAMEL.esc(document.getElementById(id + "-g").value) : "") + "."];
    if (xs.length){
      lines.push("mean <b>" + CAMEL.fmt(CAMEL.mean(xs), 2) + "</b> " + CAMEL.esc(OPT.unit || "") +
        ", median <b>" + CAMEL.fmt(CAMEL.median(xs), 2) + "</b> " + CAMEL.esc(OPT.unit || "") + ".");
    }
    document.getElementById(id + "-read").innerHTML = lines.join(" ");
  }

  document.getElementById(id + "-b").addEventListener("input", function(){
    document.getElementById(id + "-b-v").textContent = this.value;
    draw();
  });
  document.getElementById(id + "-mean").addEventListener("change", draw);
  document.getElementById(id + "-median").addEventListener("change", draw);
  if (hasGroup) document.getElementById(id + "-g").addEventListener("change", draw);
  draw();
}
