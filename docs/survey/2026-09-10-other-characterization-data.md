# Non-AFM characterization data for HS math lessons

Survey of the public LiST catalog (1,413 samples) for characterization
techniques other than AFM that could anchor a grades 9-12 (non-AP) math
lesson. Method: for each technique with ≥8 tagged samples (plus Transport
and SQUID per brief), pulled `files()` on up to 15 samples, tabulated
formats by instrument code, downloaded 2-4 representative files per
promising technique, and tried to parse them into numbers. Raw survey
data: `data/raw/survey/files_by_technique.json`. Downloaded files and
plots: `data/raw/survey/*.csv|.txt|.xlsx|.tif|.png`.

**Important caveat on method**: `files()` returns every activity attached
to a sample, not just the one matching the technique tag used to find it
— a sample tagged "Raman" usually also has XRD, AFM, and growth-log
files. Extension/instrument counts below are re-grouped by the instrument
code prefix embedded in each filename (RMN=Raman, XRD=XRD, TRP=Transport,
UVV=UV-Vis, XPS=XPS, TEM=TEM, ARP=ARPES, SQD=SQUID, SEM=SEM,
RHEED=RHEED), which is more accurate than the sample-level tag.

## Ranked table

| Technique | N | Formats | Parse status | Math hook | Visual | Effort | Verdict |
|---|---|---|---|---|---|---|---|
| **Transport** | 48 | `.csv`/`.txt` R-T/R-H sweeps, clean ASCII | Parses cleanly | R vs T step function; Ohm's law; superconducting Tc | High — vertical drop | Low | **Strong** |
| **Raman** | 321 | `.txt` clean x/y (~1600 pts); `.l6s/.wip` proprietary | `.txt` clean | E2g/A1g subtraction → layer count via lookup curve | Medium-high | Low | **Strong** |
| **XRD** | 258 | `.csv` clean 2θ/intensity; `.xrdml` XML | Both clean | Bragg's law nλ=2d·sinθ, Cu Kα=1.5406 Å | Medium | Low-medium | **Strong** |
| **SEM** | 110 | `.tif` micrographs (scale bar burned in); `.docx` EDX reports | Images clean; reports manual | Counting/density/area, scale calibration | High | Medium | **Good, image-based** |
| **UV-VIS** | 32 | `.csv`/`.xlsx`, 12+ paired wavelength/%R columns | Parses but messy layout | E=1240/λ — but data is reflectance w/ thin-film fringes, not clean absorbance | Medium | Med-high | **Needs pre-processing** |
| **RHEED** | 211 | `.png` still frames only, no intensity file | Image only | Streak spacing ∝1/lattice spacing — no geometry metadata to get real units | High | Med-high | **Visual, not quantitative** |
| **Ellipsometry** | 26 (8 w/ data) | `.xlsx` Psi/Delta (~700 pts, only 8 samples); `.SE` proprietary | `.xlsx` clean, but needs Fresnel fit | Coverage-vs-time S-curve **not present as a file** | Low | High | **Too hard directly** |
| **TEM** | 8 | Pre-rendered `.png` fringe images; occasional `.cif` | Images clean, rarely scaled | Fringe counting → layers, if scale known | Med-high | Medium | **Narrow, spot-use** |
| **XPS** | 11 | `.vms`/`.spe`/`.pho` proprietary | Unparseable w/o vendor SW | Binding energy → stoichiometry | Low | High | **Too hard** |
| **ARPES** | 9 | `.pxt`/`.pxp` Igor binaries | Unparseable w/o Igor | Band dispersion — grad-level anyway | Low | High | **Wrong level** |
| **SQUID** | 2 | `.dat` text but ~4 MB dense header | Parses, but N=2 | M-H hysteresis, susceptibility slope | Low | High | **Too narrow** |

## Three lesson ideas

**1. "Find the superconducting transition" (Transport, Algebra I/II or Physical Science).**
Sample **20198** (`210916A_MS_FeSe_RT_300K_2K_data.csv`, and siblings
20199-20201, all "Superconducting FeSe thin films") gives clean
Temp_K/Rxx/Rxy columns, 300 rows. Rxx falls from ~1000 Ω at 300 K to
~0 Ω below 5 K — a textbook step transition (see
`data/raw/survey/plot_transport_FeSe_RvT.png`). Students plot R vs T,
estimate Tc from the midpoint of the drop, and apply Ohm's law in the
normal-state region. Four replicate samples let different groups compare
Tc.

**2. "How many layers of MoS2?" (Raman, Algebra I).**
Sample **32093** (`MCV1-210917A-NT_211001 Center R 4mW 30s 3a.txt`) has
two clean peaks at 383.1 and 403.5 cm⁻¹ (E2g and A1g,
`data/raw/survey/plot_raman_MoS2_peaks.png`). Students find each peak's
position (by eye or spreadsheet max), subtract to get Δω ≈ 20.4 cm⁻¹,
and use a provided reference table (monolayer ≈19, bulk ≈25 cm⁻¹) to
estimate layer count. ~200 other MoS2/WS2 Raman samples give enough
variety for a class set.

**3. "Measuring a crystal with a trig identity" (XRD, Geometry/Trig).**
Sample **20958** (`1hr_2theta-omega_program_1_export.csv`) is a clean
2θ/intensity scan with a sharp peak at 2θ≈41.7° that solves to d≈2.165 Å
via nλ=2d·sinθ (λ=1.5406 Å) — matching sapphire's known (0006) spacing
(c/6=2.165 Å), so the answer is independently checkable
(`data/raw/survey/plot_xrd_2theta_omega.png`). Broader film peaks in the
same scan are a good "why is this peak fat and that one skinny" extension
for stronger students.

## Honest caveats

Proprietary binaries (`.l6s/.l6v`, `.spm`, `.vms/.spe/.pho`, `.pxt/.pxp`,
`.SE`, `.BSW/.DSW`, `.gph/.opj`) are dead ends without vendor software —
only the plain-text/CSV/XLSX/image exports are classroom-ready, and not
every sample has those. RHEED and Ellipsometry are visually or narratively
appealing but the public files lack the calibration metadata (imaging
geometry; optical model) needed for a *quantitatively correct* result —
using them straight risks teaching something that looks right but isn't.
XPS, ARPES, SQUID are both too proprietary and arguably above non-AP
level. LiST itself is reachable only from the Penn State network/VPN, so
any of this needs to be pre-fetched into a slice for classroom use.
