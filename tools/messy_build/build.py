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
def fac(body, label="teachers &middot; notes for this activity"):
    return '<details class="teacher"><summary>%s</summary><div class="teacher-body">%s</div></details>' % (label, body)
def fnote(usually, ask, watch):
    return fac('<p><b>Teams usually:</b> %s</p><p><b>Ask the room:</b> %s</p><p><b>Watch for:</b> %s</p>' % (usually, ask, watch))
def more(summary, body): return '<details><summary>%s</summary>%s</details>' % (summary, body)

P = lambda card, text: PR.link(card, text)
LOOK = {
 "cw-warm": "Three real " + P("afm", "AFM") + " scans drawn in 3D. Height is stretched 25&times; and color shows height. Materials: Bi<sub>2</sub>Se<sub>3</sub>, FeSe, SnTe (" + P("materials", "table") + ").",
 "cw-w01": "An " + P("afm", "AFM") + " height map of a WSe<sub>2</sub> (tungsten diselenide) film: each bright triangle is a tiny crystal island. Color shows height.",
 "cw-w02": "Each bar counts films by " + P("rough", "roughness") + ", the typical bump height. The unit stays hidden until you reveal it.",
 "cw-m05": "The material name, typed by hand. Each tile counts samples with that exact spelling. Formulas are just labels (" + P("materials", "table") + ").",
 "cw-m02": "Each row is one grown sample. <b>Growth method</b>: how atoms arrive (" + P("growth", "MOCVD or hybrid MBE") + "). <b>Growth time</b>: minutes of growing.",
 "cw-m11": "The 66 samples at 5 nm or rougher. <b>Roughness</b> is typical bump height; <b>scan size</b> is the width of the patch " + P("afm", "scanned") + ".",
 "cw-g01": "Each dot is one sample: minutes grown (across) against how bumpy it came out (up). " + P("growth", "What is growth time?"),
 "cw-g15": "Two claims, same records. In a box chart the box holds the middle half of the values; the thick line is the median.",
 "cw-g06": "<b>Grains</b> are crystal islands in an " + P("afm", "AFM scan") + " of sample 17458&rsquo;s wafer. Each bar counts samples of n grains by average area.",
 "cw-d01": "Each row is one sample: <b>substrate</b> (the flat base), <b>growth method</b>, <b>scan size</b>, <b>roughness</b>. " + P("row", "See a real row") + ".",
}

def why_block(t): return '<div class="why"><div class="why-h">Why this matters</div><p>%s</p></div>' % t if t else ""
def figure(svg, cap, cls=""): return '<figure class="fig %s">%s<figcaption>%s</figcaption></figure>' % (cls, svg, cap) if svg else ""
def panel(icon, title, tag, point, task, wid, take, extra="", flag="", look="", note="", why="", fig="", after=""):
    look = look or LOOK.get(wid, "")
    return ('<section class="panel"><div class="panel-header"><h2>%s%s%s</h2><span class="panel-tag">%s</span></div><div class="panel-body">'
            '<p class="point">%s</p>%s%s%s<p class="task">%s</p>%s%s%s%s</div></section>') % (ic(icon), title, flag, tag, point, why_block(why), fig, ('<p class="look">%s<span><b>What you&rsquo;re looking at:</b> %s</span></p>' % (ic("eye"), look)) if look else "", task, widget(wid), after, takeaway(take, wid if wid in ("cw-w01", "cw-w02") else None), extra + note)
def script(body): return "<script>(function(){" + body + "})();</script>"
def wscript(wid, data, js, extra=""):
    return script('var root = document.getElementById("%s"); var DATA = %s; %s\n%s' % (wid, data, extra, js))

TABS = [("warmup", "crystal", "Warm Up"), ("notice", "eye", "1 &middot; Notice &amp; Wonder"), ("mess", "search", "2 &middot; Find the Mess"),
        ("model", "trend", "3 &middot; Model It"), ("dials", "dials", "4 &middot; Turn the Dials"), ("reflect", "chat", "Reflect")]
tabs_html = "".join('<button class="tab%s" id="tab-%s" onclick="switchTab(\'%s\')">%s%s</button>' % (" active" if i == 0 else "", k, k, ic(i_), l) for i, (k, i_, l) in enumerate(TABS))

def cfg(d): return "var cfg = " + json.dumps(d, ensure_ascii=False) + ";"


# ---- M-05 example cards: every number is computed from the embedded M-05 rows ----------------
_M5 = json.loads(DATA["m05"])["rows"]
def _n(f): return sum(r[2] for r in _M5 if f(r))
def _parts(s): return [p.strip() for p in s.split(";")]
def _only(name): return lambda r: all(p == name for p in _parts(r[0])) and bool(r[0])
M5 = dict(
    sn_exact=_n(lambda r: r[0] == "SnSe"), sn_all=_n(_only("SnSe")), sn_rep=_n(lambda r: r[0] == "SnSe; SnSe"),
    fe_a=_n(lambda r: r[0] == "FeSe; FeTe"), fe_b=_n(lambda r: r[0] == "FeTe; FeSe"),
    mo_exact=_n(lambda r: r[0] == "MoS2"), mo_rep=_n(lambda r: r[0] == "MoS2; MoS2"), mo_junk=_n(lambda r: r[0] == "MoS2; 0"),
    sub_all=_n(lambda r: r[0] and r[0] == r[1]), sub_al=_n(lambda r: r[0] == "Al2O3" and r[1] == "Al2O3"), sub_ga=_n(lambda r: r[0] == "GaAs" and r[1] == "GaAs"),
    h2=_n(lambda r: r[0] == "2H-MoS2"), mow=_n(lambda r: r[0] == "Mo-WSe2"), w_exact=_n(lambda r: r[0] == "WSe2"),
)
M5["mo_all"] = M5["mo_exact"] + M5["mo_rep"] + M5["mo_junk"]
M5["w_all"] = M5["w_exact"] + M5["mow"]
assert (M5["mo_exact"], M5["mo_all"]) == (334, 338) and M5["sub_all"] == 5 and M5["sn_all"] == 34
def _card(kind, lines, why):
    return ('<div class="m5c"><div class="m5k">%s</div>%s<p class="m5why">%s</p></div>' %
            (kind, "".join('<div class="m5raw"><b>%s</b><i>%d sample%s</i></div>' % (t, n, "" if n == 1 else "s") for t, n in lines), why))
M05_CARDS = ('<div class="m5cards"><div class="m5h">Six real entries from the material box, exactly as typed</div><div class="m5grid">' + "".join([
    _card("same name twice", [("SnSe; SnSe", M5["sn_rep"])],
          "Counting the exact text &ldquo;SnSe&rdquo; gives %d samples. Counting the repeats too gives %d." % (M5["sn_exact"], M5["sn_all"])),
    _card("same pair, two orders", [("FeSe; FeTe", M5["fe_a"]), ("FeTe; FeSe", M5["fe_b"])],
          "Counting one order gives %d samples. Both orders give %d." % (M5["fe_a"], M5["fe_a"] + M5["fe_b"])),
    _card("a piece that isn&rsquo;t a name", [("MoS2; 0", M5["mo_junk"])],
          "Counting the exact text &ldquo;MoS2&rdquo; gives %d samples. Adding %d repeated and this %d with a stray 0 gives %d." % (M5["mo_exact"], M5["mo_rep"], M5["mo_junk"], M5["mo_all"])),
    _card("substrate typed as the material", [("Al2O3", M5["sub_al"]), ("GaAs", M5["sub_ga"])],
          "A tally by material puts %d samples under the names of the flat base they grew on (Al<sub>2</sub>O<sub>3</sub>: %d, GaAs: %d)." % (M5["sub_all"], M5["sub_al"], M5["sub_ga"])),
    _card("2H-MoS2", [("2H-MoS2", M5["h2"])],
          "The %d &ldquo;MoS2&rdquo; samples leave out these %d. Deciding whether 2H-MoS2 belongs with MoS2 requires domain knowledge." % (M5["mo_all"], M5["h2"])),
    _card("Mo-WSe2", [("Mo-WSe2", M5["mow"])],
          "Cutting everything before the dash moves these %d samples into WSe2, from %d to %d. Deciding whether Mo-WSe2 should count as WSe2 requires domain knowledge." % (M5["mow"], M5["w_exact"], M5["w_all"])),
]) + '</div></div>')

# ---------------- panes -----------------------------------------------------------------
warm = lede("crystal", "Let&rsquo;s put a number on &ldquo;rough&rdquo;.",
            "<b>Your job:</b> skim the five cards, then pick a surface. Which looks roughest, and what would you measure to prove it?")
warm += '<div class="path">' + "".join(
    '<button onclick="switchTab(\'%s\')">%s<div><b>%s</b><span>%s</span></div></button>' % (k, ic(i_), n, m)
    for k, i_, n, m in [("warmup", "crystal", "Warm up", "5 min"), ("notice", "eye", "Notice and wonder", "5 min"), ("mess", "search", "Find the mess", "10 min"),
                         ("model", "trend", "Model it", "12 min"), ("dials", "dials", "Turn the dials", "8 min")]) + '</div>'
warm += '<section class="panel primer" id="primer-panel"><div class="panel-header"><h2>%s What Am I Looking At?</h2><span class="panel-tag">five quick cards &middot; reopen any time with the button at the bottom right</span></div><div class="panel-body" id="primer-inline"></div></section>' % ic("key")
warm += panel("cube", "Three Real Surfaces", "warm up",
    "Real crystal surfaces, magnified until you can see the bumps.",
    "Pick a surface, then drag to rotate it and scroll or pinch to zoom.", "cw-warm",
    "We compare surfaces with a number, <b>roughness</b>. Every activity here uses it.",
    more("How these scans were made", "<p>A very sharp tip moves across the surface of a real film and records its height 250,000 times.</p>"
         "<p>Each scan is one to two micrometers across, about a fiftieth of the width of a human hair.</p>"),
    why="&ldquo;Looks rough&rdquo; is a judgment call. SnTe&rsquo;s typical bump is 0.36 nm, a number two people can both check. Schools do the same when they turn &ldquo;a good week&rdquo; into an attendance rate.",
    note=fnote("say the first surface is rough and the last is smooth before anyone asks.",
               "what would you measure to turn that word into a number? That number is roughness, and every later activity uses it.",
               "teams meaning different things by &ldquo;rough&rdquo; (tall bumps, many bumps, sharp bumps). Let that disagreement stand. The 3D view needs internet; if it will not draw, the still picture does the same job."))
warm += ('<section class="panel"><div class="panel-header"><h2>%s The Data, and Our Film</h2><span class="panel-tag">2D Crystal Consortium</span></div><div class="panel-body">'
 '<p class="point">Every number here is a real record, left exactly as the scientists kept it.</p>'
 '<p>Penn State grows crystal films two or three atoms thick, as candidates for future electronics.</p>'
 '<div class="tiles"><div class="tile"><div class="n">1,005</div><div class="l">samples grown</div></div>'
 '<div class="tile"><div class="n">899</div><div class="l">with a roughness measurement</div></div>'
 '<div class="tile"><div class="n">1 nm</div><div class="l">a millionth of a millimeter. A sheet of paper is about 100,000 nm thick.</div></div></div>'
 '<div class="thread">%s<h3>%s Follow one film: sample 17458</h3>'
 '<p>It is tungsten diselenide (WSe<sub>2</sub>). We meet it again in every round.</p><ol>'
 '<li>%s<span><b>Notice &amp; Wonder:</b> its microscope scan, with a glitch in it.</span></li>'
 '<li>%s<span><b>Find the Mess:</b> one of the 66 extreme readings. WSe2 is the orange tile.</span></li>'
 '<li>%s<span><b>Model It:</b> it has no growth time, so it cannot be plotted. The sampling grains come from its wafer.</span></li>'
 '<li>%s<span><b>Turn the Dials:</b> turn on the tidy-up settings and it drops out of the data.</span></li></ol></div>'
 '%s</div></section>') % (
    ic("pin"), "", ic("pin"), ic("image"), ic("alert"), ic("trend"), ic("dials"),
    more("Why some counts read 1,000 and 894", "<p>A few activities first set aside five rows where someone typed the substrate&rsquo;s name (the flat base) into the material box. "
         "Their counts are 1,000 samples and 894 measurements, not 1,005 and 899. Each activity says which it uses.</p><p>The page embeds the source records unchanged. Each activity states the filters or grouping rules it applies.</p>"))
warm = warm.replace('<div class="thread">' + ic("pin") + '<h3>', '<div class="thread"><h3>')  # (icon already in h3)
warm += wscript("cw-warm", "null", rd("w_warm.js"), ITEMS)

notice = lede("eye", "Let&rsquo;s look at the picture before we trust the number.",
              "<b>Your job:</b> write two things you notice and one thing you wonder. Then reveal. Spotting something the reveal skips counts as a win.")
notice += panel("image", "Look at This Picture", "W-01 &middot; one microscope scan",
    "Start with the image. Write what you notice before opening the measurement.", "Look first, name it second. Zoom in if you can.", "cw-w01",
    "The 6.10 nm comes mostly from one faulty line out of 512. The other 511 lines are still usable.",
    why="One roughness number summarizes the whole scan. Looking at the picture first is how we check what that number rests on. A teacher does the same with a class average: look at the grades before trusting it.",
    fig=figure(PR.svg_afm(False), "A scan is built one line at a time, one pass of the tip per line.", "fig-afm") + PR.afm_key() ,
    note=fnote("name the triangles first. Some also spot the dark horizontal stripe partway down the scan.",
               "which parts of this picture are the crystal, and which are the instrument?",
               "teams who treat the stripe as part of the crystal, or who decide the whole scan is useless. The fault is one line; the rest of the scan is usable. The same sample, 17458, comes back in every round."))
notice += wscript("cw-w01", DATA["w01"], rd("w_notice.js"), cfg({
    "kind": "image", "question": "This is a real picture from a scientific instrument. What do you notice? What do you wonder?",
    "title": "Tiny triangles of tungsten diselenide (WSe2), with a glitch.",
    "lines": ["It is an atomic force microscope scan: a very sharp tip moves across the surface and records its height.",
              "The triangles are WSe2 crystal islands. WSe2 is studied for atomically thin transistor channels.",
              "The stripe records a bad pass of the tip rather than a −455 nm surface feature. The remaining scan lines are still usable.",
              "With the bad line included, the computed roughness is 6.10 nm; without it, the result is 0.80 nm."],
    "more": "The color scale shows the crystals themselves are only about 2 nm tall. Over a 2 µm × 2 µm patch the recorded roughness is 6.10 nm; leave out that single line and it is 0.80 nm.",
    "thread": "This scan is <b>sample 17458</b>, our WSe2 film. Remember its 6.10 nm."}))
notice += panel("hist", "Now Look at This Pile of Numbers", "W-02 &middot; 894 roughness measurements",
    "A histogram shows the shape of many numbers at once.", "Start with the shape. Write what you notice before revealing the variable and unit.", "cw-w02",
    "One typical value describes the big pile and leaves the far-out readings out. In round 2 you decide which of those readings to trust.",
    why="A histogram shows every value at once, so we can check the shape before we summarize it. Attendance rates and test scores deserve the same look.",
    note=fnote("say &ldquo;most are about the same and a few are way out.&rdquo; Both halves matter later: the big pile is round 3&rsquo;s problem and the long thin tail is round 2&rsquo;s.",
               "which of the far-out ones would you believe, and what would you need to know to decide?",
               "a team deciding the tail must be errors. Some of it may be, and some is a genuinely lumpy film. Nothing in a histogram separates the two. Round 2 starts there."))
notice += wscript("cw-w02", DATA["w02"], rd("w_notice.js"), cfg({
    "kind": "hist", "question": "Here are 894 real measurements with no label yet. What do you notice about their shape? What do you wonder?",
    "title": "Roughness, in nanometers, of 894 real crystal films grown at Penn State.",
    "lines": ["Roughness is how bumpy a film’s surface is. A flatter film has a smaller number.",
              "Most films are very flat: under 2 nm, which is just a few atoms tall.",
              "A handful are far rougher, over 50 nm. They are real samples."],
    "more": "Roughness also depends on how big an area was scanned, which is not plotted here."}))

mess = lede("search", "Let&rsquo;s apply cleaning rules to real records and see what each one does.",
            "<b>Your job:</b> for each activity, write the <em>rule</em> you would apply. A rule is something a computer could follow.")
mess += panel("text", "One Text Box, Thirty-Five Answers", "M-05 &middot; 1,005 samples, raw material field",
    "Some spellings merge by rule. Others need someone who knows the field.",
    "Every rule starts at <b>keep as typed</b>. Switch one to merge, read which tiles will move, then press <b>Merge</b> to watch it happen. No chemistry needed.", "cw-m05",
    "Four rules fix the mechanical mess. Four labels still require domain knowledge. Until then, leave them unresolved.",
    more("A rule that tidies the most but fixes nothing", "<p>Folding labels under 5 samples into &ldquo;rare&rdquo; combines the small labels into one category and fixes no spelling. It combines 18 labels with no other rule on and 10 with all of them on; the count under the button shows the number for your current choices.</p>"),
    why="Hand-entered labels often appear in several spellings. Course titles, school names and student names do too.", fig=M05_CARDS,
    note=fnote("find the easy merges fast (a name typed twice, a list in a different order). Nobody needs to know the chemistry.",
               "after every rule is on, four labels that all look like MoS<sub>2</sub> are still separate. Who gets to decide whether they are the same thing?",
               "a team choosing the &ldquo;rare&rdquo; rule because it gives the shortest chart, or one that strips everything before a dash (right for one label, wrong for others). A team that answers &ldquo;unresolved, ask someone in the field&rdquo; has it right, so say that out loud. Press the reveal button when teams have tried all five rules."))
mess += wscript("cw-m05", DATA["m05"], rd("w_m05.js"))
mess += panel("filter", "A Common Filter That Removes Most of One Method", "M-02 &middot; 1,005 samples, uncleaned",
    "One common filter removes most of one group.", "Turn each requirement on and off. Watch which method disappears.", "cw-m02",
    "The same missing-value rule affects the two methods differently, because their records are filled in unevenly.",
    more("A question for your own data", "<p>What does your student information system do when a field is blank? Is it blank at random?</p>"),
    flag='<span class="star-flag">most important</span>',
    why="Hybrid MBE loses 219 of its 233 samples to this filter and MOCVD loses 32 of 772. In school data, &ldquo;drop students with a missing score&rdquo; has the same shape when the missing scores belong to students who were absent on test day.",
    fig=figure(PR.svg_growth(), "Two growth methods. Their records are filled in unevenly.", "fig-growth"),
    note=fnote("agree that &ldquo;only keep complete rows&rdquo; sounds like basic hygiene, then are surprised when one growth method nearly vanishes.",
               "what does your own student information system do with a blank field, and is it blank at random?",
               "teams who see the shrinking count but not that it fell unevenly across the two methods. Protect time for this one; if the session runs short, skip the optional activities instead."))
mess += wscript("cw-m02", DATA["m02"], rd("w_m02.js"))
mess += panel("alert", "Which Extreme Readings Would You Trust?", "M-11 &middot; 66 of 1,000 cleaned samples, 5 nm or rougher",
    "Removing extreme values changes the mean far more than the median.", "Mark readings keep or remove, or try a shortcut. Fix the one reading whose fault is known. Watch the two dots.", "cw-m11",
    "Removing the 66 readings changes the mean a lot and the median little, so the keep-or-remove decision matters most if you report the mean.",
    more("There is no answer key", "<p>A scan can have RMS roughness near 92 nm because of real topography or contamination. The number alone does not distinguish them. Record your reasons, not just your tally.</p>"
         "<p>If you saw the glitch in W-01, you have already met one of these rows: sample 17458, at 6.1 nm.</p>"),
    flag='<span class="optional-flag">if time</span>',
    why="Only one of the 66 readings has a known fault: sample 17458&rsquo;s bad scan line. The <b>mean</b> is the usual average. It uses every value, so a few large readings pull it up. The <b>median</b> is the middle value and depends on rank, so extreme values change it much less. A district&rsquo;s average days absent can shift on a handful of students.",
    note=fnote("split over whether the biggest values are real. Some keep them all, some remove them all.",
               "what is the difference between fixing a reading and removing it? (Fixing needs a known cause. Sample 17458&rsquo;s fault is known, so it is the only one that can be fixed.)",
               "teams who watch only the mean and miss that the median barely moves. If a team saw the glitch line in W-01, point out that they have already met one of these rows."))
mess += wscript("cw-m11", DATA["m11"], rd("w_m11.js"))


G15_L, G15_R = PR.svg_g15()
G15_AFTER = ('<div class="g15x"><h3>Two ways to compare, and what each lumps together</h3>'
 '<div class="fig-pair"><figure class="fig">' + G15_L + '<figcaption><b>Trend line</b> (schematic). The line runs through every film at once, so anything else that changes with growth time is mixed into the slope.</figcaption></figure>'
 '<figure class="fig">' + G15_R + '<figcaption><b>Two groups</b> (schematic). Each box pools films that differ in other ways, growth time included.</figcaption></figure></div>'
 '<p>Of the 754 samples on the trend line, 740 are MOCVD, and the slope is about the same with MOCVD alone (about 0.06 nm per minute either way). Method barely varies along it. Material, substrate and project all vary.</p>'
 '<p>In the group comparison, growth time varies inside each box. Only 24 of the 233 hybrid MBE samples have a growth time recorded, and only 14 have both a time and a roughness. With 14, you can&rsquo;t check whether the method gap is really a growth-time gap. Among the 24 recorded hybrid MBE times, the median is 7 min, against 15 min for MOCVD. That points the opposite way from a growth-time explanation of the method gap, and 14 pairs are too few to say more.</p>'
 '<p><b>Whichever comparison you choose, say what it lumps together.</b> Comparing like with like (same material, same time range) is the fix, and these records mostly have too few matching samples.</p></div>')
model = lede("trend", "Let&rsquo;s fit lines to the records and check how much each one explains.",
             "<b>Your job:</b> write one sentence you would defend, limits included. &ldquo;The line explains about 2% of the variation&rdquo; is a real finding.")
model += panel("trend", "Does Growing a Film Longer Make It Rougher?", "G-01 &middot; 754 samples with growth time and roughness",
    "A line can be fitted to any cloud of dots, so check how much it explains.", "Hide and show the line. Change the dot colors. Read the slope and R&sup2;.", "cw-g01",
    "Growth time alone leaves most of the variation in roughness unexplained.",
    more("A rank-based measure, and who is missing", "<p>Spearman&rsquo;s rank correlation is +0.29. Ranking reduces the influence of the largest roughness values, so it measures something different from the fitted line.</p>"
         "<p>Missingness is not random: 251 samples lack growth time, roughness, or both. See M-02.</p>"),
    why="R&sup2; is the share of the ups and downs in roughness that the line accounts for. Claims like &ldquo;more study time means higher scores&rdquo; or &ldquo;more absences means lower grades&rdquo; get the same check.",
    note=fnote("expect a clear upward trend and are let down by how loose the cloud is.",
               "how many of the 1,005 samples are in this picture? (754. The other 251 lack a growth time or a roughness, and the gaps are not random; see M-02.)",
               "teams reading the fitted line as a result. A line can be fitted to anything, so ask how much it explains, not only which way it slopes. &ldquo;This fitted line explains about 2% of the variation in roughness&rdquo; is a good sentence to write. If you mention Spearman, add that the rank-based association is modestly positive."))
model += wscript("cw-g01", DATA["g01"], rd("w_g01.js"))
model += panel("claim", "Check a Claim, Then Rewrite It", "G-15 &middot; two claims, one dataset",
    "A claim needs evidence on both sides, plus its limits.", "Pick a claim. Read both columns. Then rewrite it so it is true.", "cw-g15",
    "These observational comparisons support associations, not causal conclusions. A good rewrite names who was measured and under what conditions.",
    why="&ldquo;Growing a film longer makes it rougher&rdquo; is one sentence. Behind it are 754 samples, a slope of 0.06 nm per minute and R&sup2; = 0.020.",
    after=G15_AFTER,
    note=fnote("believe both claims at the start, then find there is real evidence on each side.",
               "what is the smallest change that makes this sentence true? (The first claim fails on the verb &ldquo;makes&rdquo;. In the second, the two methods were grown for different projects and measured differently, so it is a lopsided observation, not a trial.)",
               "rewrites that only soften the wording (&ldquo;might make&rdquo;). A good rewrite names who was measured and warns that the groups were not comparable."))
model += wscript("cw-g15", DATA["g15"], rd("w_g15.js"), cfg({"claims": [
    {"key": "time_rough", "claim": "Growing a film longer makes it rougher.", "type": "correlation", "x_key": "time", "x_label": "growth time (minutes)"},
    {"key": "method_smooth", "claim": "MOCVD makes smoother films than hybrid MBE.", "type": "group", "group_key": "meth", "groups": ["MOCVD", "Hybrid MBE"]}]}))
model += panel("dice", "How Close Is One Sample to the Whole?", "G-06 &middot; 501 grains from sample 17458&rsquo;s wafer",
    "Sampling variation decreases as n increases. A sample of only the easy-to-reach grains stays off target at any size.", "Slide n up. Then sample from the center or the edge only.", "cw-g06",
    "As n increases, sample means narrow around the mean of the grains being sampled. For a center-only sample, that is not the all-grains mean.",
    more("About the grains", "<p>The 501 grains come from three real scans across one WSe2 wafer, sample 17458: a measured population, not a full wafer census.</p>"
         ""),
    flag='<span class="optional-flag">if time</span>',
    why="Mean grain area is 1,469 nm&sup2; at the center, 2,818 nm&sup2; toward the edge, and 1,889 nm&sup2; across all 501 observed grains, so a center-only sample is centered away from the all-grains mean at any size. A survey of only the students who answer email has the same problem.",
    note=fnote("watch the spread of sample averages narrow as n goes up.",
               "if you could only grab the crystals that were easy to reach, what would your sample miss?",
               "the idea that a bigger sample fixes a biased one. Center-only and edge-only samples stay off target at any size, and their spread keeps narrowing around the center mean or the edge mean, not the all-grains mean."))
model += wscript("cw-g06", DATA["g06"], rd("w_g06.js"))

dials = lede("dials", "The same table can be taught simply or in full. Turning a dial changes what students see first.",
             "<b>Your job:</b> pick the setting for day one and the one you want by the end. Say what you gave up.")
dials += panel("dials", "Turn All Three Complexity Dials", "D-01 &middot; 1,005 samples, every dial position",
    "The source table stays fixed. Only the rows, columns and labels a student meets first change.", "Turn each dial. Watch the sample count, the graph and the table.", "cw-d01",
    "The simplest setting shows 2 variables and a clean graph. The fullest shows all 8 variables, the mess, and every recorded scan, and is harder to start from.",
    more("What each dial means", "<p><b>Structural:</b> how many variables are in front of you.</p>"
         "<p><b>Provenance:</b> whether missing values and odd spellings are shown or resolved.</p>"
         "<p><b>Statistical:</b> which scans are included. One setting keeps every recorded scan. The other keeps only 5 &micro;m scans under 10 nm.</p>"),
    why="With the Provenance dial on &ldquo;tidy it up&rdquo;, sample 17458 leaves the table because it has no growth time. With the Statistical dial on &ldquo;5 &micro;m scans under 10 nm&rdquo;, it leaves because it was scanned at 2 &micro;m. On &ldquo;show the mess&rdquo; and &ldquo;all recorded scans&rdquo;, it stays.",
    note=fnote("start with the simplest setting because it is the easiest to teach, then notice what disappeared.",
               "what did you give up at the setting you chose?",
               "teams picking a side (&ldquo;simple is best&rdquo; or &ldquo;always show everything&rdquo;) instead of naming the trade. A team that can say what each setting costs has got the point of the session."))
dials += wscript("cw-d01", DATA["d01"], rd("w_d01.js"))

reflect = lede("chat", "Take these three questions back to the room.", "There are no right answers.")
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Reflection Questions</h2><span class="panel-tag">for the room</span></div><div class="panel-body">'
 '<div class="reflect-q">%s<div><b>1. Where did your team disagree?</b><p>Which spellings match, which extremes to trust, whether a line means anything.</p></div></div>'
 '<div class="reflect-q">%s<div><b>2. What did the dials cost?</b><p>Where would you set them for your students, and what would you tell them you turned down?</p></div></div>'
 '<div class="reflect-q">%s<div><b>3. What is the equivalent dataset in your building?</b><p>Attendance, benchmarks, course requests. Which of these messes is already in that file?</p></div></div>'
 '</div></section>') % (ic("chat"), ic("flag"), ic("dials"), ic("search"))
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Our Film&rsquo;s Journey</h2><span class="panel-tag">sample 17458, WSe2</span></div><div class="panel-body">'
 '<p class="point">One film, five lessons.</p><ol class="claim-list">'
 '<li>%s<span><b>Notice:</b> with one bad scan line included it reads 6.10 nm; without it, 0.80 nm.</span></li>'
 '<li>%s<span><b>Mess:</b> one of 66 extreme readings, and a tile among 35 spellings.</span></li>'
 '<li>%s<span><b>Model:</b> no growth time was recorded, so the plot excludes sample 17458.</span></li>'
 '<li>%s<span><b>Sampling:</b> the 501 measured grains came from three scans across its wafer.</span></li>'
 '<li>%s<span><b>Dials:</b> tidy settings removed it.</span></li></ol></div></section>') % (ic("pin"), ic("image"), ic("alert"), ic("trend"), ic("dice"), ic("dials"))
CLAIMS_NOTE = fac("<p>Teams reach for all three, and all three are wrong. Say so kindly, and give them the true version.</p>"
    "<p><b>&ldquo;So these are the chips in AI data centers.&rdquo;</b> Nothing in these records shows that any sample became a chip. 2D materials are <em>researched</em> as candidates for future electronics, which is still exciting.</p>"
    "<p><b>&ldquo;Smoother is better.&rdquo;</b> Roughness is one quality measurement among many, and nothing here connects it to whether a device works.</p>"
    "<p><b>&ldquo;Longer growth causes rougher films.&rdquo;</b> Every relationship on this page is an association in records of experiments that were never designed to be compared.</p>", "teachers &middot; claims to correct if you hear them")
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Three Claims We Are Careful Not to Make</h2><span class="panel-tag">keep these limits explicit</span></div><div class="panel-body">'
 '<ul class="claim-list">'
 '<li>%s<span>A smoother film is a better device. Roughness is one quality measure among many.</span></li>'
 '<li>%s<span>These samples became computer chips. 2D materials are <em>researched</em> as candidates for future electronics.</span></li>'
 '<li>%s<span>Any of these relationships is a cause. They are associations in records of experiments never designed to be compared.</span></li></ul>' + CLAIMS_NOTE + '</div></section>') % (ic("alert"), ic("alert"), ic("alert"), ic("alert"))
reflect += ('<section class="panel"><div class="panel-header"><h2>%s Go Further</h2><span class="panel-tag">beyond this page</span></div><div class="panel-body">'
 '<p>Everything here runs inside this page, with no account. The full 40-item catalog, and each analysis in a dozen lines of Python, is in '
 '<a href="../CAMEL/index.html">the CAMEL notebook catalog</a>.</p></div></section>') % ic("claim")

PANES = [("warmup", warm), ("notice", notice), ("mess", mess), ("model", model), ("dials", dials), ("reflect", reflect)]
panes_html = "".join('<div class="pane%s" id="pane-%s">%s</div>' % (" active" if i == 0 else "", k, h) for i, (k, h) in enumerate(PANES))
# scripts are placed after the panes, inside the pane they belong to: move them out for clarity
LOGO = '<svg class="logo" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"><path d="M24 4l16 9.2v18.6L24 41 8 31.800V13.200z"/><path d="M24 4v37M8 13.2L24 23l16-9.8" /><path d="M10 44q7-5 14 0t14 0" stroke="#8e2f8e"/></svg>'

SESSION = fac("<ul>"
  "<li><b>Setup:</b> one phone, tablet or laptop per team. Nothing to install and no account or sign-in. Teams work from this page alone; the five cards and each &ldquo;Your job&rdquo; line are the instructions.</li>"
  "<li><b>Order and time:</b> Warm up 5 min, 1 &middot; Notice &amp; Wonder 5, 2 &middot; Find the Mess 10, 3 &middot; Model It 12, 4 &middot; Turn the Dials 8, then Reflect with the room. Teams move on with the tabs.</li>"
  "<li><b>If you are short on time:</b> skip the activities marked <em>if time</em> (M-11 and G-06). Protect M-02, marked <em>most important</em>.</li>"
  "<li><b>Internet:</b> only the 3D warm-up needs it (it fetches a drawing library). If it is blocked, the still picture works the same, and everything else runs offline once the page has loaded.</li>"
  "<li><b>Notes:</b> under each activity, a closed <em>teachers</em> bar holds what teams usually notice, one question to ask, and the misreading to watch for. Teams can ignore them.</li>"
  "<li><b>Before you start:</b> the Reflect tab ends with three wrong claims teams often make, with the true version of each. Worth reading first.</li></ul>",
  "teachers &middot; running this session").replace('class="teacher"', 'class="teacher session"')
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
 '<p class="header-sub">Real, uncleaned crystal-growth records from Penn State. Find the mess in them, and see how one table can be taught different ways.</p>'
 '<div class="header-meta"><span><b>Source:</b> Penn State 2D Crystal Consortium, LiST sample records</span>'
 '<span><b>Adapted from:</b> the PA Dept. of Education Data Literacy Summit session (Reinhart group, Penn State)</span></div></header>\n' + SESSION +
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
