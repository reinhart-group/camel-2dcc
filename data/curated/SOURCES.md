# Sources for the curated context tables

These tables are context, not LiST data. Values are rounded, widely reported figures chosen for
classroom use; students should treat them as approximate.

- `chips_timeline.csv` — transistor counts as published by the chip makers (Intel, Apple, NVIDIA
  product announcements and datasheets), as compiled in the Wikipedia "Transistor count" article.
  Blackwell B200 counts both dies in the package.
- `materials_reference.csv` — layer thickness (one repeating layer, which may hold several planes of
  atoms: a MoS2 layer is S–Mo–S), in-plane lattice constant (the repeat distance between neighbouring
  metal atoms, not a bond length), and energies from standard review literature on 2D materials
  (e.g., Manzeli et al., *Nat. Rev. Mater.* 2, 17033 (2017) for TMDs). `optical_energy_monolayer_eV`
  is the approximate energy of the main light a single layer absorbs and emits; it is close to, but
  not the same as, the electronic band gap, and shifts with substrate, strain, and temperature.
  `band_gap_bulk_eV` is the (indirect) electronic gap of the thick crystal. Blank = no meaningful
  single classroom value (graphene has no gap).
- `superconductors.csv` — critical temperatures from standard references, measured as the point where
  resistance drops to zero. For single-layer FeSe on SrTiO3, labs report superconducting signatures
  from about 40 K to 65 K depending on sample and method (Wang et al., *Chin. Phys. Lett.* 29, 037402
  (2012); He et al., *Nat. Mater.* 12, 605 (2013)), so it is given as a range, not one number.
- `chips_timeline.csv` is a hand-picked set of well-known chips, not a complete or consistent series:
  it switches from single-die CPUs to phone chips and AI accelerators, and `dies_in_package` = 2 for
  Blackwell B200. A doubling time fitted to it describes this selection.
- Data-centre electricity figures quoted in notebook 5: International Energy Agency, *Energy and AI*
  (April 2025): data centres used about 415 TWh in 2024 (about 1.5% of world electricity), projected
  to roughly double to about 945 TWh by 2030.
