# Brainstorm brief for Codex — CAMEL 2DCC data packages + HS math Colab demos

You are a brainstorming partner and later code reviewer. Claude does the implementation. Do NOT write code in this repo right now; write your answer to the output file you are given.

## Context
- CAMEL = NSF award 2621173 (Collaboratory to Advance Mathematics Education and Learning), PI Rebecca Napolitano (Penn State). Goal: grades 9–12 students do math modeling with authentic, noisy research data in Python notebooks (Google Colab). Audience is typical HS Algebra 1/2, Geometry, and intro Statistics students and their teachers — NOT AP. Notebooks must be exciting, low-code (fill-in-a-number, sliders), and teacher-friendly.
- Data source: LiST (Lifetime Sample Tracking), the 2DCC-MIP (2D Crystal Consortium, Penn State) sample database. REST API v2, header auth `X-API-KEY`, public read-only key sees 1,413 Published samples. The LiST host is PSU-network-gated, so Colab cannot hit it directly. Plan: we pull a curated slice locally, publish it to a OneDrive/SharePoint folder, and notebooks fetch it via a SharePoint anonymous sharing URL (`?download=1`) with `requests`.
- Census of public data: AFM on 1,068 samples (Bruker Nanoscope `.spm` files, 256–512 px, 0.5–5 µm scans), Raman 321, XRD 258, RHEED 211, SEM 110. Materials: MoS2 452, WSe2 257, WS2 203, GaSe, In2Se3, SnSe, MoSe2, (Bi,Sb)2Te3, FeSe (superconductor), TaS2, CrSb, SnTe. Growth: MOCVD 775, hybrid MBE 246, MBE 49. Samples link to citable data packages (DOIs 10.26207/...), e.g. "Analyzing the impact of Se concentration during MBE deposition of 2D SnSe", "Superconducting FeSe thin films", "Wafer-scale MOCVD TMD films used for 3D Monolithic Integration", "Enabling SRAM cell scaling with monolithic 3D integration of 2D FETs", "Large-scale memtransistor crossbar arrays based on 2D MoS2", "High-performance p-type WSe2 FET".
- MBE recipes carry step tables (duration, pressure, substrate temp, source temps, flux).
- Existing figure (afm-stats): boxplots of SnSe grain area by deposition order (co-dep / Se-first / Sn-first) and Se:Sn ratio.
- Required content: AFM statistics; Plotly 3D AFM height maps with ipywidgets controls; nanotech algebra and/or geometry; discussion of semiconductors, electronics, photonics, and computer chips for AI data centers. Also an STL export of an AFM surface for 3D printing (owed to Becca).

## Questions — answer each concisely (bullets), with your top recommendation
1. Notebook lineup: propose 4–6 notebooks (title, math standard/concept, the data slice it uses, the "wow" moment, 3–5 student tasks). Keep each doable in one 45–50 min class period.
2. Algebra/geometry hooks that are genuinely correct physics but HS-accessible (e.g., layers = thickness / 0.65 nm per MoS2 layer; scaling a 5 µm scan to a football field; hexagon lattice geometry; transistor count vs. area; surface-area-to-volume; exponential growth / Moore's law).
3. Dataset slice design: file formats (CSV + compact .npz/.npy height maps? PNG thumbnails?), sizes, a manifest schema, and how to keep SharePoint URLs out of code but easy for teachers to swap.
4. Pitfalls: AFM plane-leveling/scan-line artifacts, unit confusion (nm vs µm), Colab widget quirks (plotly FigureWidget needs `google.colab.output.enable_custom_widget_manager()`), SharePoint download URL quirks, rate limits.
5. Anything we'd regret not including for teachers (answer keys, standards alignment table, "complexity dials").
