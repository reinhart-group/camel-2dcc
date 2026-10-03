import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
ORIG = open(os.path.join(HERE, "original.html")).read().split("\n")
def rd(n): return open(os.path.join(SRC, n)).read()

# ---- real data, copied verbatim from the original page -------------------------------
def data_of(line_no):
    s = ORIG[line_no - 1]
    i = s.index("var DATA = ") + len("var DATA = ")
    j = s.index(", OPT = ")
    return s[i:j]
DATA = {k: data_of(v) for k, v in dict(w01=605, w02=1056, m05=1520, m02=2093, m11=2583, g01=3138, g15=3609, g06=4121, d01=4678).items()}
s146 = ORIG[145]
_arr = json.loads(s146[s146.index("["):s146.rindex("];") + 1])
for _it in _arr: _it.pop("png", None)          # the still PNG placeholders are gone; the live 3D surface data are untouched
ITEMS = "var items = " + json.dumps(_arr, ensure_ascii=False, separators=(",", ":")) + ";"
import primer as PR

ICONS = {
 "crystal": '<path d="M12 3l7.5 4.3v9.4L12 21l-7.5-4.3V7.3z"/><path d="M12 3v18M4.5 7.3L12 12l7.5-4.7"/>',
 "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l6 6"/><path d="M8 10.5h5M10.5 8v5"/>',
 "trend": '<path d="M4 4v16h16"/><circle cx="8" cy="15" r="1"/><circle cx="12" cy="11" r="1"/><circle cx="15" cy="13" r="1"/><circle cx="19" cy="7" r="1"/><path d="M7 16l12-9"/>',
 "dials": '<path d="M4 7h9M17 7h3M4 12h3M11 12h9M4 17h11M19 17h1"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="17" cy="17" r="2"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 16l5-5 4 4 3-3 6 6"/><circle cx="16" cy="9" r="1.3"/>',
 "hist": '<path d="M4 20h16"/><rect x="5" y="9" width="3" height="11"/><rect x="10" y="4" width="3" height="16"/><rect x="15" y="14" width="3" height="6"/>',
 "text": '<path d="M4 6h16M4 11h10M4 16h14M4 21h7"/>',
 "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
 "alert": '<path d="M12 4l9 16H3z"/><path d="M12 10v5M12 17.5v.5"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
 "dice": '<rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="9" cy="9" r="1"/><circle cx="15" cy="9" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="9" cy="15" r="1"/><circle cx="15" cy="15" r="1"/>',
 "cube": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12L4 7.5M12 12v9"/>',
 "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "claim": '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
 "key": '<path d="M12 3a6 6 0 00-3.5 10.9V18l3.5 3 3.5-3v-4.1A6 6 0 0012 3z"/><path d="M9.5 18h5"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
}
def ic(name, cls="ic"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, name)
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(
    '<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (k, v) for k, v in ICONS.items()) + '</defs></svg>'

def lede(icon, point, job):
    return '<div class="lede">%s<div><div class="pt">%s</div><div class="job">%s</div></div></div>' % (ic(icon, "ic big-ic"), point, job)
def widget(wid): return '<div class="cw" id="%s"></div>' % wid
def takeaway(t, hid=None): return '<div class="takeaway"%s>%s<div><b>Takeaway.</b> %s</div></div>' % ((' id="%s-take" hidden' % hid) if hid else '', ic("key"), t)
def more(summary, body): return '<details><summary>%s</summary>%s</details>' % (summary, body)

P = lambda card, text: PR.link(card, text)
LOOK = {
 "cw-warm": "Three real " + P("afm", "AFM") + " scans drawn in 3D. Height is stretched 25&times; and color shows height. Materials: Bi<sub>2</sub>Se<sub>3</sub>, FeSe, SnTe (" + P("materials", "table") + ").",
 "cw-w01": "An " + P("afm", "AFM") + " height map of a WSe<sub>2</sub> (tungsten diselenide) film: each bright triangle is a tiny crystal island. Color shows height.",
 "cw-w02": "Each bar counts films by " + P("rough", "roughness") + ", the typical bump height. The unit stays hidden until you reveal it.",
 "cw-m05": "The material name, typed by hand. Each bar counts samples with that exact spelling. Formulas are just labels (" + P("materials", "table") + ").",
 "cw-m02": "Each row is one grown sample. <b>Growth method</b>: how atoms arrive (" + P("growth", "MOCVD or hybrid MBE") + "). <b>Growth time</b>: minutes of growing.",
 "cw-m11": "The 66 samples at 5 nm or rougher. <b>Roughness</b> is typical bump height; <b>scan size</b> is the width of the patch " + P("afm", "scanned") + ".",
 "cw-g01": "Each dot is one sample: minutes grown (across) against how bumpy it came out (up). " + P("growth", "What is growth time?"),
 "cw-g15": "Two claims, same records. In a box chart the box holds the middle half of the values; the thick line is the median.",
 "cw-g06": "<b>Grains</b> are crystal islands in an " + P("afm", "AFM scan") + " of sample 17458&rsquo;s wafer. Each bar counts samples of n grains by average area.",
 "cw-d01": "Each row is one sample: <b>substrate</b> (the flat base), <b>growth method</b>, <b>scan size</b>, <b>roughness</b>. " + P("row", "See a real row") + ".",
}

def panel(icon, title, tag, point, task, wid, take, extra="", flag="", look=""):
    look = look or LOOK.get(wid, "")
    return ('<section class="panel"><div class="panel-header"><h2>%s%s%s</h2><span class="panel-tag">%s</span></div><div class="panel-body">'
            '<p class="point">%s</p>%s<p class="task">%s</p>%s%s%s</div></section>') % (ic(icon), title, flag, tag, point, ('<p class="look">%s<span><b>What you&rsquo;re looking at:</b> %s</span></p>' % (ic("eye"), look)) if look else "", task, widget(wid), takeaway(take, wid if wid in ("cw-w01", "cw-w02") else None), extra)
def script(body): return "<script>(function(){" + body + "})();</script>"
def wscript(wid, data, js, extra=""):
    return script('var root = document.getElementById("%s"); var DATA = %s; %s\n%s' % (wid, data, extra, js))

TABS = [("warmup", "crystal", "Warm Up"), ("notice", "eye", "1 &middot; Notice &amp; Wonder"), ("mess", "search", "2 &middot; Find the Mess"),
        ("model", "trend", "3 &middot; Model It"), ("dials", "dials", "4 &middot; Turn the Dials"), ("reflect", "chat", "Reflect")]
tabs_html = "".join('<button class="tab%s" id="tab-%s" onclick="switchTab(\'%s\')">%s%s</button>' % (" active" if i == 0 else "", k, k, ic(i_), l) for i, (k, i_, l) in enumerate(TABS))

def cfg(d): return "var cfg = " + json.dumps(d, ensure_ascii=False) + ";"

# ---------------- panes -----------------------------------------------------------------
warm = lede("crystal", "&ldquo;Rough&rdquo; is just a word until you measure it.",
            "<b>Your job:</b> skim the five cards, then pick a surface. Which looks roughest, and what would you measure to prove it?")
warm += '<div class="path">' + "".join(
    '<button onclick="switchTab(\'%s\')">%s<div><b>%s</b><span>%s</span></div></button>' % (k, ic(i_), n, m)
    for k, i_, n, m in [("warmup", "crystal", "Warm up", "5 min"), ("notice", "eye", "Notice and wonder", "5 min"), ("mess", "search", "Find the mess", "10 min"),
                         ("model", "trend", "Model it", "12 min"), ("dials", "dials", "Turn the dials", "8 min")]) + '</div>'
warm += '<section class="panel primer" id="primer-panel"><div class="panel-header"><h2>%s What Am I Looking At?</h2><span class="panel-tag">five quick cards &middot; reopen any time with the button at the bottom right</span></div><div class="panel-body" id="primer-inline"></div></section>' % ic("key")
warm += panel("cube", "Three Real Surfaces", "warm up",
    "Real crystal surfaces, magnified until you can see the bumps.",
    "Pick a surface, then drag to rotate it and scroll or pinch to zoom.", "cw-warm",
    "To compare surfaces we need a number. That number is <b>roughness</b>, and every activity here uses it.",
    more("How these scans were made", "<p>A needle sharpened to a single atom was dragged across a real film, recording its height 250,000 times.</p>"
         "<p>Each scan is one to two micrometers across, about a fiftieth of the width of a human hair.</p>"))
warm += ('<section class="panel"><div class="panel-header"><h2>%s The Data, and Our Film</h2><span class="panel-tag">2D Crystal Consortium</span></div><div class="panel-body">'
 '<p class="point">Every number here is a real record, left exactly as the scientists kept it.</p>'
 '<p>Penn State grows crystal films two or three atoms thick, as candidates for future electronics.</p>'
 '<div class="tiles"><div class="tile"><div class="n">1,005</div><div class="l">samples grown</div></div>'
 '<div class="tile"><div class="n">899</div><div class="l">with a roughness measurement</div></div>'
 '<div class="tile"><div class="n">1 nm</div><div class="l">a millionth of a millimeter. A sheet of paper is about 100,000 nm thick.</div></div></div>'
 '<div class="thread">%s<h3>%s Follow one film: sample 17458</h3>'
 '<p>It is tungsten diselenide (WSe<sub>2</sub>). We meet it again in every round.</p><ol>'
 '<li>%s<span><b>Notice &amp; Wonder:</b> its microscope scan, with a glitch in it.</span></li>'
 '<li>%s<span><b>Find the Mess:</b> one of the 66 extreme readings. WSe2 is the orange bar.</span></li>'
 '<li>%s<span><b>Model It:</b> it has no growth time, so it cannot be plotted. Its wafer supplies the sampling grains.</span></li>'
 '<li>%s<span><b>Turn the Dials:</b> watch tidy-up settings drop it from the data.</span></li></ol></div>'
 '%s</div></section>') % (
    ic("pin"), "", ic("pin"), ic("image"), ic("alert"), ic("trend"), ic("dials"),
    more("Why some counts read 1,000 and 894", "<p>A few activities first set aside five rows where someone typed the substrate&rsquo;s name (the flat base) into the material box. "
         "Their counts are 1,000 samples and 894 measurements, not 1,005 and 899. Each activity says which it uses.</p><p>Nothing was cleaned up, simplified or invented for this page.</p>"))
warm = warm.replace('<div class="thread">' + ic("pin") + '<h3>', '<div class="thread"><h3>')  # (icon already in h3)
warm += wscript("cw-warm", "null", rd("w_warm.js"), ITEMS)

notice = lede("eye", "Looking closely finds what a summary number hides.",
              "<b>Your job:</b> write two things you notice and one thing you wonder. Then reveal. Spotting something the reveal skips counts as a win.")
notice += panel("image", "Look at This Picture", "W-01 &middot; one microscope scan",
    "A single bad scan line can quietly change a number.", "Look first, name it second. Zoom in if you can.", "cw-w01",
    "One bad line in 512 multiplied the roughness by more than seven. Look at the data before you trust the summary.")
notice += wscript("cw-w01", DATA["w01"], rd("w_notice.js"), cfg({
    "kind": "image", "question": "This is a real picture from a scientific instrument. What do you notice? What do you wonder?",
    "title": "Tiny triangles of tungsten diselenide (WSe2), with a glitch.",
    "lines": ["It is an atomic force microscope scan: a needle drags across the surface and feels its height.",
              "The triangles are WSe2 crystals, thin enough to make transistors thinner than any silicon one.",
              "The dark stripe is the instrument misbehaving, not the crystal: one scan line out of 512, dipping to −455 nm.",
              "One bad line in 512 multiplied the headline number by more than seven."],
    "more": "The color scale shows the crystals themselves are only about 2 nm tall. Over a 2 µm × 2 µm patch the recorded roughness is 6.10 nm; leave out that single line and it is 0.80 nm.",
    "thread": "This scan is <b>sample 17458</b>, our WSe2 film. Remember its 6.10 nm."}))
notice += panel("hist", "Now Look at This Pile of Numbers", "W-02 &middot; 894 roughness measurements",
    "A histogram shows the shape of many numbers at once.", "Shape first, meaning second. Same routine: notice, wonder, reveal.", "cw-w02",
    "Most films are flat and a few are far rougher. Round 2 asks which of those few to trust.")
notice += wscript("cw-w02", DATA["w02"], rd("w_notice.js"), cfg({
    "kind": "hist", "question": "Here are 894 real measurements with no label yet. What do you notice about their shape? What do you wonder?",
    "title": "Roughness, in nanometers, of 894 real crystal films grown at Penn State.",
    "lines": ["Roughness is how bumpy a film’s surface is. A flatter film has a smaller number.",
              "Most films are very flat: under 2 nm, which is just a few atoms tall.",
              "A handful are far rougher, over 50 nm. They are real samples, not mistakes."],
    "more": "Roughness also depends on how big an area was scanned, which this chart does not show."}))

mess = lede("search", "Real data hides problems that tidy-looking rules cannot see.",
            "<b>Your job:</b> for each activity, write the <em>rule</em> you would apply. A rule is something a computer could follow.")
mess += panel("text", "One Text Box, Thirty-Five Answers", "M-05 &middot; 1,005 samples, raw material field",
    "Cleaning rules can merge typos, but only an expert can say which labels mean the same thing.",
    "Every rule starts at <b>keep as typed</b>. Switch one to merge, read which tiles will move, then press <b>Merge</b> to watch it happen. No chemistry needed.", "cw-m05",
    "Mechanical mess is fixable by anyone. The rest needs someone who knows the field, or an honest &ldquo;unresolved&rdquo;.",
    more("A rule that tidies the most but fixes nothing", "<p>Folding labels under 5 samples into &ldquo;rare&rdquo; hides 10 labels and changes nothing. It makes the chart look cleanest, which is why it is worth pointing at.</p>"))
mess += wscript("cw-m05", DATA["m05"], rd("w_m05.js"))
mess += panel("filter", "A Reasonable Rule That Deletes a Whole Method", "M-02 &middot; 1,005 samples, uncleaned",
    "A sensible-sounding filter can quietly delete most of one group.", "Turn each requirement on and off. Watch which method disappears.", "cw-m02",
    "&ldquo;Only complete rows&rdquo; keeps 740 of 772 MOCVD samples but only 14 of 233 hybrid MBE.",
    more("A question for your own data", "<p>What does your student information system do when a field is blank? Is it blank at random?</p>"),
    flag='<span class="star-flag">most important</span>')
mess += wscript("cw-m02", DATA["m02"], rd("w_m02.js"))
mess += panel("alert", "Which Extreme Readings Would You Trust?", "M-11 &middot; 66 of 1,000 cleaned samples, 5 nm or rougher",
    "Removing extreme values moves the mean far more than the median.", "Mark readings keep or remove, or try a shortcut. Fix the one reading whose fault is known. Watch the two dots.", "cw-m11",
    "Removing all 66 moves the mean from 1.83 to 1.01 nm but the median only from 0.74 to 0.66.",
    more("There is no answer key", "<p>A real bump can be 92 nm tall. So can a speck of dust the microscope tripped over. Record your reasons, not just your tally.</p>"
         "<p>If you saw the glitch in W-01, you have already met one of these rows: sample 17458, at 6.1 nm.</p>"),
    flag='<span class="optional-flag">if time</span>')
mess += wscript("cw-m11", DATA["m11"], rd("w_m11.js"))

model = lede("trend", "A model summarizes a pattern. Ask how much it explains and what it leaves out.",
             "<b>Your job:</b> write one sentence you would defend, limits included. &ldquo;We found no relationship&rdquo; is a real finding.")
model += panel("trend", "Does Growing a Film Longer Make It Rougher?", "G-01 &middot; 754 samples with growth time and roughness",
    "A line can be fitted to any cloud of dots, so check how much it explains.", "Hide and show the line. Change the dot colors. Read the slope and R&sup2;.", "cw-g01",
    "The line rises about 0.06 nm per minute, yet explains only 2% of the variation (R&sup2; = 0.020). How steep it is and how well it fits are separate questions.",
    more("A stronger measure, and who is missing", "<p>The rank correlation is stronger (Spearman +0.29) because roughness is so skewed. That is a good advanced conversation, not the headline.</p>"
         "<p>The 251 left-out samples did not leave at random. See M-02.</p>"))
model += wscript("cw-g01", DATA["g01"], rd("w_g01.js"))
model += panel("claim", "Check a Claim, Then Rewrite It", "G-15 &middot; two claims, one dataset",
    "A claim needs evidence on both sides, plus its limits.", "Pick a claim. Read both columns. Then rewrite it so it is true.", "cw-g15",
    "Both claims are associations in observational records, never causes. A good rewrite names who was measured and under what conditions.")
model += wscript("cw-g15", DATA["g15"], rd("w_g15.js"), cfg({"claims": [
    {"key": "time_rough", "claim": "Growing a film longer makes it rougher.", "type": "correlation", "x_key": "time", "x_label": "growth time (minutes)"},
    {"key": "method_smooth", "claim": "MOCVD makes smoother films than hybrid MBE.", "type": "group", "group_key": "meth", "groups": ["MOCVD", "Hybrid MBE"]}]}))
model += panel("dice", "How Much Does One Sample Tell You?", "G-06 &middot; 501 grains from sample 17458&rsquo;s wafer",
    "Bigger samples wander less, but an easy-to-take sample can be off target for good.", "Slide n up. Then sample from the center or the edge only.", "cw-g06",
    "More grains shrink the wander. A center-only sample stays away from the all-grains mean at any size.",
    more("About the grains", "<p>The 501 grains come from three real scans across one WSe2 wafer, sample 17458: a measured population, not a full wafer census.</p>"
         "<p>The center&rsquo;s median grain is 1,526 nm&sup2; and the edge&rsquo;s is 2,792 nm&sup2;.</p>"),
    flag='<span class="optional-flag">if time</span>')
model += wscript("cw-g06", DATA["g06"], rd("w_g06.js"))

dials = lede("dials", "The same data can be taught simply or honestly. Each dial trades one for the other.",
             "<b>Your job:</b> pick the setting for day one and the one you want by the end. Say what you gave up.")
dials += panel("dials", "Turn All Three Complexity Dials", "D-01 &middot; 1,005 samples, every dial position",
    "The source table stays fixed. Only the rows, columns and labels a student meets first change.", "Turn each dial. Watch the sample count, the graph and the table.", "cw-d01",
    "The simplest setting is easy to teach but promises what the data cannot keep. The full setting is honest but hard to start with.",
    more("What each dial means", "<p><b>Structural:</b> how many variables are in front of you.</p>"
         "<p><b>Provenance:</b> whether missing values and odd spellings are shown or quietly resolved.</p>"
         "<p><b>Statistical:</b> whether the noise and the outliers are left in.</p>"))
dials += wscript("cw-d01", DATA["d01"], rd("w_d01.js"))

reflect = lede("chat", "Take these three questions back to the room.", "There are no right answers. Disagreement is where the data literacy is.")
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Reflection Questions</h2><span class="panel-tag">for the room</span></div><div class="panel-body">'
 '<div class="reflect-q">%s<div><b>1. Where did your team disagree?</b><p>Which spellings match, which extremes to trust, whether a line means anything. Those calls are the data literacy.</p></div></div>'
 '<div class="reflect-q">%s<div><b>2. What did the dials cost?</b><p>Where would you set them for your students, and what would you tell them you turned down?</p></div></div>'
 '<div class="reflect-q">%s<div><b>3. What is the equivalent dataset in your building?</b><p>Attendance, benchmarks, course requests. Which of these messes is already in that file?</p></div></div>'
 '</div></section>') % (ic("chat"), ic("flag"), ic("dials"), ic("search"))
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Our Film&rsquo;s Journey</h2><span class="panel-tag">sample 17458, WSe2</span></div><div class="panel-body">'
 '<p class="point">One film, five lessons.</p><ol class="claim-list">'
 '<li>%s<span><b>Notice:</b> one bad scan line made it read 6.10 nm instead of 0.80 nm.</span></li>'
 '<li>%s<span><b>Mess:</b> one of 66 extreme readings, and a bar among 35 spellings.</span></li>'
 '<li>%s<span><b>Model:</b> no growth time, so it was never a dot.</span></li>'
 '<li>%s<span><b>Sampling:</b> its wafer gave the 501 grains.</span></li>'
 '<li>%s<span><b>Dials:</b> tidy settings quietly removed it.</span></li></ol></div></section>') % (ic("pin"), ic("image"), ic("alert"), ic("trend"), ic("dice"), ic("dials"))
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Three Claims We Are Careful Not to Make</h2><span class="panel-tag">keep these limits explicit</span></div><div class="panel-body">'
 '<ul class="claim-list">'
 '<li>%s<span>A smoother film is a better device. Roughness is one quality measure among many.</span></li>'
 '<li>%s<span>These samples became computer chips. 2D materials are <em>researched</em> as candidates for future electronics.</span></li>'
 '<li>%s<span>Any of these relationships is a cause. They are associations in records of experiments never designed to be compared.</span></li></ul></div></section>') % (ic("alert"), ic("alert"), ic("alert"), ic("alert"))
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Go Further</h2><span class="panel-tag">beyond this page</span></div><div class="panel-body">'
 '<p>Everything here runs inside this page, with no account. The full 40-item catalog, and each analysis in a dozen lines of Python, is in '
 '<a href="../CAMEL/index.html">the CAMEL notebook catalog</a>.</p></div></section>') % ic("claim")

PANES = [("warmup", warm), ("notice", notice), ("mess", mess), ("model", model), ("dials", dials), ("reflect", reflect)]
panes_html = "".join('<div class="pane%s" id="pane-%s">%s</div>' % (" active" if i == 0 else "", k, h) for i, (k, h) in enumerate(PANES))
# scripts are placed after the panes, inside the pane they belong to: move them out for clarity
LOGO = '<svg class="logo" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"><path d="M24 4l16 9.2v18.6L24 41 8 31.800V13.200z"/><path d="M24 4v37M8 13.2L24 23l16-9.8" /><path d="M10 44q7-5 14 0t14 0" stroke="#8e2f8e"/></svg>'

HEAD = ORIG[0:7]   # doctype..fonts preconnect (checked below)
page = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
 '<title>Modeling the Messy | epiSTEMic</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">\n'
 '<style>\n' + rd("style.css") + '</style>\n</head>\n<body>\n' + SPRITE + '\n<template id="primer-tpl">' + PR.primer(json.loads(DATA["d01"])) + '</template>\n'
 '<button type="button" class="primer-fab" id="primer-fab" aria-haspopup="dialog" aria-label="What am I looking at?" title="What am I looking at?">' + ic("key") + '<span>What am I looking at?</span></button>\n'
 '<div class="drawer" id="drawer" hidden role="dialog" aria-modal="true" aria-label="What am I looking at?"><div class="drawer-bg" id="drawer-bg"></div>'
 '<aside class="drawer-panel"><div class="drawer-head"><b>What am I looking at?</b><button type="button" class="drawer-x" id="drawer-x">Close</button></div>'
 '<div class="drawer-body primer" id="drawer-body"></div></aside></div>\n<div class="app">\n'
 '<div class="nav"><a href="../index.html">epiSTEMic</a><span>/</span><span class="nav-current">Modeling the Messy</span></div>\n'
 '<header><div class="header-eyebrow">Materials Science &amp; Data Literacy &middot; Guided Investigation</div>'
 '<div class="titlerow">' + LOGO + '<h1>Modeling the Messy</h1></div>'
 '<p class="header-sub">Real, uncleaned crystal-growth records from Penn State. Find what the mess hides, and see how the same numbers teach different lessons.</p>'
 '<div class="header-meta"><span><b>Source:</b> Penn State 2D Crystal Consortium, LiST sample records</span>'
 '<span><b>Adapted from:</b> the PA Dept. of Education Data Literacy Summit session (Reinhart group, Penn State)</span></div></header>\n'
 '<div class="tabs" role="tablist">' + tabs_html + '</div>\n' + panes_html + '\n'
 '<footer><p>epiSTEMic &middot; Materials Science &amp; Data Literacy</p><p>Data: Penn State 2D Crystal Consortium, via the LiST sample records. Investigation adapted from the Pennsylvania Department of Education Data Literacy Summit session built by the Reinhart group at Penn State.</p></footer>\n</div>\n'
 '<script>\n' + rd("core.js") + '\n</script>\n')
# widget scripts: they were appended inside panes' HTML (wscript) -- fine, but they run before core? core must come first -> move core to <head>-end
PAGE = page
tail = ('<script>\nfunction switchTab(tab){\n  ["warmup","notice","mess","model","dials","reflect"].forEach(function(t){\n'
        '    document.getElementById("tab-"+t).classList.toggle("active", t===tab);\n    document.getElementById("pane-"+t).classList.toggle("active", t===tab);\n  });\n'
        '  window.dispatchEvent(new Event("resize"));\n}\n'
        '(function(){\n'
        '  var tpl = document.getElementById("primer-tpl"), drawer = document.getElementById("drawer"), body = document.getElementById("drawer-body"), last = null;\n'
        '  document.getElementById("primer-inline").appendChild(tpl.content.cloneNode(true));\n'
        '  body.appendChild(tpl.content.cloneNode(true));\n'
        '  function openP(card){\n'
        '    last = document.activeElement; drawer.hidden = false; document.body.style.overflow = "hidden";\n'
        '    var t = card ? body.querySelector(\'[data-card="\' + card + \'"]\') : null;\n'
        '    body.scrollTop = t ? t.offsetTop - 8 : 0; document.getElementById("drawer-x").focus();\n'
        '  }\n'
        '  function closeP(){ drawer.hidden = true; document.body.style.overflow = ""; if (last && last.focus) last.focus(); }\n'
        '  document.getElementById("primer-fab").addEventListener("click", function(){ openP(null); });\n'
        '  document.getElementById("drawer-x").addEventListener("click", closeP);\n'
        '  document.getElementById("drawer-bg").addEventListener("click", closeP);\n'
        '  document.addEventListener("keydown", function(e){ if (e.key === "Escape" && !drawer.hidden) closeP(); });\n'
        '  document.addEventListener("click", function(e){\n'
        '    var a = e.target.closest ? e.target.closest("a.prim") : null;\n'
        '    if (!a) return; e.preventDefault(); openP(a.getAttribute("data-card"));\n'
        '  });\n'
        '})();\n' + '(function(){\n  // AFM schematic animation (see primer.svg_afm).\n  function sy(x){return 222-9*Math.sin(x/23)-6*Math.sin(x/9.3+1.2)-11*Math.exp(-Math.pow((x-300)/18,2))-7*Math.exp(-Math.pow((x-470)/14,2));}\n  var surf="M20 236",x0;for(x0=20;x0<=620;x0+=3)surf+=" L"+x0+" "+sy(x0).toFixed(1);surf+=" L620 236 Z";\n  function q(s,c){return s.querySelector("."+c);}\n  function set(e,a){for(var k in a)e.setAttribute(k,a[k]);}\n  function draw(s,tx,trace){\n    q(s,"a-surface").setAttribute("d",surf);\n    var ty=sy(tx),ay=ty-62,ax=tx-150,lift=222-ty,sp=53-lift*1.4;\n    set(q(s,"a-arm"),{x:ax,y:ay,width:156});\n    q(s,"a-tip").setAttribute("points",(tx-9)+","+(ay+7)+" "+(tx+9)+","+(ay+7)+" "+tx+","+(ty-1));\n    set(q(s,"a-in"),{x1:96,y1:44,x2:tx-12,y2:ay});set(q(s,"a-out"),{x1:tx-12,y1:ay,x2:506,y2:sp.toFixed(1)});\n    q(s,"a-spot").setAttribute("cy",sp.toFixed(1));\n    set(q(s,"a-b2c"),{cx:ax+20,cy:ay-16});set(q(s,"a-b2t"),{x:ax+20,y:ay-10});\n    q(s,"a-trace").setAttribute("points",trace.map(function(p){return p[0]+","+(330-(222-p[1])).toFixed(1);}).join(" "));\n  }\n  var still=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,x=170,trace=[];\n  if(still){var all=[];for(var i=170;i<=600;i+=4)all.push([i,sy(i)]);Array.prototype.forEach.call(document.querySelectorAll(".afm-anim"),function(s){draw(s,420,all);});return;}\n  (function frame(){\n    var live=Array.prototype.filter.call(document.querySelectorAll(".afm-anim"),function(s){return s.getClientRects().length>0;});\n    if(live.length){x+=1.6;if(x>600){x=170;trace=[];}trace.push([x,sy(x)]);live.forEach(function(s){draw(s,x,trace);});}\n    window.requestAnimationFrame(frame);\n  })();\n})();\n' + '</script>\n</body>\n</html>\n')
# core must load before the widget scripts that sit inside the panes
core_block = '<script>\n' + rd("core.js") + '\n</script>\n'
PAGE = PAGE.replace(core_block, "")
PAGE = PAGE.replace('<body>\n', '<body>\n' + core_block, 1)
PAGE += tail
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "investigation.new.html")
open(out, "w").write(PAGE)
print("wrote", out, len(PAGE))
