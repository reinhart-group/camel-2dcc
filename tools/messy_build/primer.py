import json
def link(card, text): return '<a href="#" class="prim" data-card="%s">%s</a>' % (card, text)

def svg_sheets():
    def rows(cx, n, y0, count=8):
        out = []
        for r in range(n):
            for k in range(count):
                x = cx - (count - 1) * 8 + k * 16 + (8 if r % 2 else 0) - 4
                out.append('<circle cx="%d" cy="%d" r="6.5" fill="#2b6cb0" fill-opacity="%.2f"/>' % (x, y0 + r * 13, 0.95 - 0.07 * r))
        return "".join(out)
    t = lambda x, y, s, b=False: '<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#1c1730"%s>%s</text>' % (x, y, ' font-weight="600"' if b else "", s)
    return ('<svg viewBox="0 0 520 190" role="img" aria-label="Three stacks of atoms: a thick crystal with many layers, a 2D material with one to three layers, and graphene with one layer" class="dg">'
        + rows(90, 7, 28) + rows(260, 2, 62) + '<g>' + "".join('<circle cx="%d" cy="75" r="6.5" fill="#4b5563"/>' % (370 + k * 16 + 4) for k in range(8)) + '</g>'
        + t(90, 140, "Bulk crystal", True) + t(90, 158, "hundreds of layers")
        + t(260, 140, "2D material", True) + t(260, 158, "1 to 3 layers")
        + t(435, 140, "Graphene", True) + t(435, 158, "1 layer of carbon")
        + '</svg>')

def svg_growth():
    import random
    rnd = random.Random(7)
    gas = "".join('<circle cx="%d" cy="%d" r="2.6" fill="#2b6cb0" fill-opacity="0.7"/>' % (24 + rnd.random() * 212, 60 + rnd.random() * 90) for _ in range(46))
    t = lambda x, y, s, b=False, a="middle", sz=13: '<text x="%d" y="%d" font-size="%d" text-anchor="%s" fill="#1c1730"%s>%s</text>' % (x, y, sz, a, ' font-weight="600"' if b else "", s)
    return ('<svg viewBox="0 0 520 230" role="img" aria-label="Two ways to grow a film: MOCVD with atoms carried in a gas, and MBE with beams of atoms aimed at the base" class="dg">'
        '<rect x="6" y="6" width="248" height="190" rx="6" fill="#f7f5fb" stroke="#d7cde5"/><rect x="266" y="6" width="248" height="190" rx="6" fill="#f7f5fb" stroke="#d7cde5"/>'
        + t(130, 26, "MOCVD", True, sz=15) + t(130, 44, "atoms ride in on a gas") + gas
        + '<rect x="30" y="150" width="200" height="6" fill="#2b6cb0"/><rect x="30" y="156" width="200" height="14" fill="#9ca3af"/>'
        + t(130, 188, "substrate (the base)", sz=12)
        + t(390, 26, "MBE", True, sz=15) + t(390, 44, "beams of atoms aimed at the base")
        + '<rect x="300" y="56" width="44" height="18" rx="3" fill="#6b7280"/><rect x="436" y="56" width="44" height="18" rx="3" fill="#6b7280"/>'
        + ''.join('<circle cx="%d" cy="%d" r="2.8" fill="#2b6cb0"/>' % (322 + (352 - 322) * f / 5 + 0, 80 + (146 - 80) * f / 5) for f in range(0, 6))
        + ''.join('<circle cx="%d" cy="%d" r="2.8" fill="#2b6cb0"/>' % (458 + (428 - 458) * f / 5, 80 + (146 - 80) * f / 5) for f in range(0, 6))
        + '<rect x="290" y="150" width="200" height="6" fill="#2b6cb0"/><rect x="290" y="156" width="200" height="14" fill="#9ca3af"/>'
        + t(390, 188, "substrate (the base)", sz=12)
        + t(260, 220, "Both happen inside a vacuum chamber. The blue layer is the new film.", sz=12)
        + '</svg>')

def svg_afm():
    # Animated by the AFM script in build.py: every .afm-anim svg that is visible gets the
    # moving tip, bending arm, moving laser spot and growing height trace. Class-based (no ids)
    # because the primer is cloned twice (inline and in the drawer).
    return ('<svg viewBox="0 0 640 360" role="img" aria-label="Atomic force microscope: a laser reflects off a flexible arm with a sharp tip; as the tip rides over bumps the arm bends, the reflected spot moves on a detector, and the height is recorded as a line" class="dg afm-anim">'
        '<rect x="20" y="236" width="600" height="34" rx="3" fill="#dfe6ef"/>'
        '<text x="610" y="258" text-anchor="end" font-size="12" fill="#4b5563">flat base (substrate)</text>'
        '<path class="a-surface" fill="#2b6cb0"/>'
        '<rect x="34" y="22" width="78" height="30" rx="5" fill="#1c1730"/><circle cx="73" cy="37" r="5" fill="#ff4d6d"/>'
        '<line class="a-in" stroke="#ff4d6d" stroke-width="2.5"/><line class="a-out" stroke="#ff4d6d" stroke-width="2.5" stroke-dasharray="6 4"/>'
        '<rect x="500" y="16" width="44" height="74" rx="4" fill="#1c1730"/><line x1="506" x2="538" y1="53" y2="53" stroke="#6b7280"/>'
        '<circle class="a-spot" cx="522" cy="53" r="6" fill="#ff4d6d"/>'
        '<rect class="a-arm" height="7" rx="2" fill="#c9a227"/><polygon class="a-tip" fill="#c9a227" stroke="#8a6d10"/>'
        '<polyline class="a-trace" fill="none" stroke="#1e8449" stroke-width="2.5" stroke-linejoin="round"/>'
        '<line x1="20" x2="620" y1="345" y2="345" stroke="#d1d5db"/>'
        '<g font-size="17" font-weight="700" fill="#fff">'
        '<circle cx="22" cy="37" r="12" fill="#8e2f8e"/><text x="22" y="43" text-anchor="middle">1</text>'
        '<circle class="a-b2c" r="12" fill="#8e2f8e"/><text class="a-b2t" text-anchor="middle">2</text>'
        '<circle cx="566" cy="53" r="12" fill="#8e2f8e"/><text x="566" y="59" text-anchor="middle">3</text>'
        '<circle cx="22" cy="322" r="12" fill="#1e8449"/><text x="22" y="328" text-anchor="middle">4</text></g>'
        '</svg>'
        '<ol class="afm-key"><li><b>Laser</b> shines on the back of the arm.</li>'
        '<li><b>Flexible arm with a sharp tip</b> rides up and down over every bump.</li>'
        '<li><b>Detector</b> sees the reflected spot move when the arm bends.</li>'
        '<li><b>Recorded line</b> of heights. Repeat, one line under the next, to build an image.</li></ol>')

def svg_rough():
    import math
    pts = [(20 + i * 8, 95 - 34 * math.sin(i / 3.1) * (0.6 + 0.4 * math.cos(i / 7.0)) - 10 * math.sin(i * 1.3)) for i in range(61)]
    d = "M" + " L".join("%.1f %.1f" % p for p in pts)
    bars = "".join('<line x1="%.1f" y1="95" x2="%.1f" y2="%.1f" stroke="#c0392b" stroke-width="2"/><circle cx="%.1f" cy="%.1f" r="3" fill="#2b6cb0"/>' % (pts[i][0], pts[i][0], pts[i][1], pts[i][0], pts[i][1]) for i in range(2, 61, 6))
    t = lambda x, y, s: '<text x="%d" y="%d" font-size="13" fill="#1c1730">%s</text>' % (x, y, s)
    return ('<svg viewBox="0 0 520 200" role="img" aria-label="A bumpy height line with a dashed average and red gaps measuring each point&apos;s distance from the average" class="dg">'
        '<path d="%s" fill="none" stroke="#2b6cb0" stroke-width="2"/>'
        '<line x1="20" y1="95" x2="500" y2="95" stroke="#1c1730" stroke-dasharray="6 5"/>%s'
        '<line x1="20" y1="10" x2="20" y2="150" stroke="#555"/><line x1="20" y1="150" x2="500" y2="150" stroke="#555"/>'
        % (d, bars) + t(28, 174, "dashed line: the average height") + t(28, 192, "red gaps: how far each point sits from that average")
        + t(30, 22, "height") + '</svg>')

def table_materials():
    rows = [("MoS<sub>2</sub>", "molybdenum disulfide", "The mineral molybdenite, also used as a lubricant. As one layer it is a semiconductor."),
            ("WSe<sub>2</sub>", "tungsten diselenide", "A semiconductor sheet studied for ultra-thin transistors and light sensors. <b>Our film is this.</b>"),
            ("WS<sub>2</sub>", "tungsten disulfide", "A close cousin of MoS<sub>2</sub>, also a dry lubricant."),
            ("MoSe<sub>2</sub>", "molybdenum diselenide", "Another cousin of MoS<sub>2</sub>."),
            ("GaSe", "gallium selenide", "A layered semiconductor that responds to light."),
            ("InSe", "indium selenide", "Electrons move through thin layers of it unusually easily."),
            ("In<sub>2</sub>Se<sub>3</sub>", "indium selenide (two indium per three selenium)", "Can switch its internal electric charge pattern, so it is studied for memory."),
            ("SnSe", "tin selenide", "Turns heat into electricity efficiently."),
            ("SnTe", "tin telluride", "Studied for unusual electrical behavior on its surface."),
            ("Bi<sub>2</sub>Se<sub>3</sub>", "bismuth selenide", "Conducts on its surface but not inside."),
            ("FeSe", "iron selenide", "A superconductor: cooled below about 8 kelvin, it carries electricity with no resistance.")]
    return ('<div class="cw-scroll mat"><table><thead><tr><th>Formula</th><th>Plain name</th><th>Why anyone cares</th></tr></thead><tbody>' +
            "".join("<tr><td><b>%s</b></td><td>%s</td><td class=\"wrap\">%s</td></tr>" % r for r in rows) + '</tbody></table></div>')

def row_table(d01):
    cols = d01["cols"]; rows = {r[0]: dict(zip(cols, r)) for r in d01["rows"]}
    picks = [rows[17207], rows[17458], rows[23056]]
    def v(x): return '<i class="blank">blank</i>' if x is None else (("%g" % x) if isinstance(x, float) else str(x))
    defs = [("id", "sample id", "A catalog number for one grown film."), ("mat", "material", "What the film is made of, typed by hand."),
            ("meth", "growth method", "How atoms were delivered: " + link("growth", "MOCVD or hybrid MBE") + "."),
            ("time", "growth time (min)", "Minutes the atoms kept landing."), ("temp", "temperature (&deg;C)", "The recipe’s temperature setting."),
            ("sub", "substrate", "The flat base the film grew on (Al<sub>2</sub>O<sub>3</sub> is sapphire)."),
            ("scan", "scan size (&micro;m)", "Width of the square patch the microscope scanned."),
            ("rough", "roughness (nm)", "Typical bump height in that scan, from the " + link("rough", "RMS") + " idea.")]
    h = '<thead><tr><th>Column</th><th>What it means</th>' + "".join("<th>Sample %s</th>" % p["id"] for p in picks) + "</tr></thead>"
    b = "".join("<tr><td><b>%s</b></td><td class=\"wrap\">%s</td>%s</tr>" % (n, e, "".join("<td>%s</td>" % v(p[k]) for p in picks)) for k, n, e in defs)
    return '<div class="cw-scroll rowt"><table>' + h + "<tbody>" + b + "</tbody></table></div>"

def primer(d01):
    return ('''
<div class="pcard" data-card="materials"><div class="pnum">1</div><div class="pbody"><h3>What are these materials?</h3>
<div class="ptext"><p>They are <b>2D materials</b>: crystals that form sheets only a few atoms thick.</p>
<p>Graphene, a single layer of the carbon in pencil graphite, is the famous one.</p>
<p>The names are chemical formulas. MoS<sub>2</sub> means one molybdenum atom for every two sulfur atoms.</p>
<p class="reassure"><b>You don&rsquo;t need the chemistry.</b> Treat each formula as a label.</p></div>
<div class="pfig">''' + svg_sheets() + '''</div>
<details class="ptable"><summary>The materials in this data: formula, name, why anyone cares</summary>''' + table_materials() + '''</details></div></div>

<div class="pcard" data-card="growth"><div class="pnum">2</div><div class="pbody"><h3>Why grow them, and why does smooth matter?</h3>
<div class="ptext"><p>Future chips need ultra-thin layers. A smooth layer is easier to build devices on, so labs track roughness.</p>
<p>A film grows when atoms land on a flat base, the <b>substrate</b> (here often a sapphire wafer), inside a vacuum chamber.</p>
<p><b>MOCVD</b>: a gas carries the atoms in, a bit like frost forming on a window.</p>
<p><b>MBE</b> (molecular beam epitaxy): beams of atoms are aimed at the base. <b>Hybrid MBE</b> supplies some ingredients as a gas.</p>
<p><b>Growth time</b> is how many minutes the atoms keep arriving.</p></div>
<div class="pfig">''' + svg_growth() + '''</div>
<p class="pnote">Smoother is not automatically better: roughness is one quality measure among many.</p></div></div>

<div class="pcard" data-card="afm"><div class="pnum">3</div><div class="pbody"><h3>How does the microscope work?</h3>
<div class="ptext"><p>An <b>atomic force microscope (AFM)</b> does not use light.</p>
<p>A very sharp tip on a tiny flexible arm is dragged across the surface, line by line, like a record-player needle.</p>
<p>It records the height at every point. The result is a grid of heights drawn as an image.</p>
<p><b>Color shows height</b>, not real color. <b>Scan size</b> is the width of the square patch.</p></div>
<div class="pfig">''' + svg_afm() + '''</div>
<div class="scale" role="img" aria-label="Scale from a hair, 70 micrometers, to a scan patch, 2 to 5 micrometers, to bumps measured in nanometers">
<div class="sstep"><span class="sq" style="width:64px;height:64px"></span><b>a human hair</b><span>about 70 &micro;m wide</span></div><span class="sarr">&rarr;</span>
<div class="sstep"><span class="sq" style="width:26px;height:26px"></span><b>one scan patch</b><span>2 to 5 &micro;m across</span></div><span class="sarr">&rarr;</span>
<div class="sstep"><span class="sq" style="width:7px;height:7px"></span><b>the bumps</b><span>about 1 to 10 nm tall</span></div></div>
<p class="pnote">A &micro;m (micrometer) is a millionth of a meter. A nm (nanometer) is 1,000 times smaller; 1 nm is about a few atoms. Sizes are not to scale.</p></div></div>

<div class="pcard" data-card="rough"><div class="pnum">4</div><div class="pbody"><h3>What is &ldquo;roughness&rdquo;?</h3>
<div class="ptext"><p><b>RMS roughness</b> is the typical up-and-down from the average height.</p>
<p>For a math teacher: it is the <b>standard deviation</b> of all the heights in the scan.</p>
<p class="formula">roughness = &radic;( mean of ( height &minus; average height )&sup2; )</p>
<p>Squaring means one extreme point counts for a lot. Round 1 shows exactly that.</p></div>
<div class="pfig">''' + svg_rough() + '''</div></div></div>

<div class="pcard" data-card="row"><div class="pnum">5</div><div class="pbody"><h3>What is one row of the data?</h3>
<div class="ptext"><p>Each row is one grown sample. Here are three real ones. &ldquo;Blank&rdquo; means nobody recorded it.</p></div>''' + row_table(d01) + '''</div></div>''')
