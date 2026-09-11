from pathlib import Path
import shutil

import nbformat
from nbclient import NotebookClient
from courseware.manifest import load_lesson
from courseware.compose import compose
from courseware.cli import main

# Reading-level note: the Algebra 1 grade-8 Flesch-Kincaid gate lives in courseware/cli.py
# (`_grade`) and is measured on a COMPOSED notebook's full markdown, not on any one module file
# in isolation. A per-module spot check is not comparable (a short excerpt swings wildly on a
# single long word) — always re-measure against a built notebook, not a module's own text.

ROOT = Path(__file__).resolve().parents[2]
ROOTS = [ROOT / "courseware" / "modules"]


def test_same_concept_module_runs_on_two_datasets():
    a = load_lesson(ROOT / "lessons/pilot-grains-algebra1.yaml", ROOTS)
    b = load_lesson(ROOT / "lessons/pilot-roughness-explorer.yaml", ROOTS)
    ma = next(rm for rm in a.modules if rm.module.name == "concept_mean_median")
    mb = next(rm for rm in b.modules if rm.module.name == "concept_mean_median")
    assert ma.module.path == mb.module.path
    assert ma.settings != mb.settings


def test_concept_modules_use_only_standard_shape_names():
    for p in (ROOT / "courseware/modules/concepts").glob("*.py"):
        text = p.read_text()
        for dataset_name in ("area_nm2", "rms_roughness_nm", "load_grain_scans", "load_table"):
            assert dataset_name not in text, f"{p.name} names dataset detail {dataset_name}"


def test_mixed_lesson_has_different_guidance_per_module():
    lesson = load_lesson(ROOT / "lessons/pilot-grains-mixed.yaml", ROOTS)
    g = {rm.module.name: rm.settings.get("guidance") for rm in lesson.modules}
    assert g["concept_mean_median"] == "fill" and g["concept_outlier_effect"] == "open"
    assert compose(lesson).metadata["camel"]["lesson"] == "pilot-grains-mixed"


def test_curated_demo_manifests_build_with_objective_metadata(tmp_path):
    manifests = sorted((ROOT / "lessons").glob("demo-*.yaml"))
    assert len(manifests) == 6
    assert main(["build", *(str(p) for p in manifests), "--out", str(tmp_path)]) == 0
    for path in manifests:
        lesson = load_lesson(path, ROOTS)
        nb = compose(lesson)
        assert lesson.objective and lesson.standards
        assert nb.metadata["camel"]["objective"] == lesson.objective


def test_curated_demo_manifests_execute_against_real_slice(tmp_path):
    manifests = sorted((ROOT / "lessons").glob("demo-*.yaml"))
    out = tmp_path / "built"
    assert main(["build", *(str(p) for p in manifests), "--out", str(out)]) == 0
    source_zip = ROOT / "data" / "slice" / "camel-2dcc-v1.zip"
    for notebook_path in sorted(out.glob("*.ipynb")):
        work = tmp_path / notebook_path.stem
        work.mkdir()
        shutil.copy(source_zip, work / source_zip.name)
        notebook = nbformat.read(notebook_path, as_version=4)
        NotebookClient(notebook, timeout=300, kernel_name="python3",
                       resources={"metadata": {"path": str(work)}}).execute()
