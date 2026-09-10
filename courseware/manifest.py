"""Lesson manifests: resolve each module's dial settings and validate the lesson.

Resolution order for a module's dial: preset < lesson ``dials`` < the module's
own override in ``modules:``. Only dials the module declares are kept.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from courseware.module import Module, ModuleError, find_module

PRESETS = yaml.safe_load((Path(__file__).parent / "presets.yaml").read_text())


class ManifestError(Exception):
    """A lesson manifest asks for something its modules cannot do."""


@dataclass
class ResolvedModule:
    module: Module
    settings: dict[str, str]


@dataclass
class Lesson:
    id: str
    title: str
    minutes: int
    params: dict[str, int]
    modules: list[ResolvedModule] = field(default_factory=list)
    preset: str | None = None


def _entries(items):
    for item in items:
        if isinstance(item, str):
            yield item, {}
        elif isinstance(item, dict) and len(item) == 1:
            (name, over), = item.items()
            yield name, dict(over or {})
        else:
            raise ManifestError(f"bad module entry: {item!r}")


def lesson_from_dict(data: dict, module_roots: list[Path]) -> Lesson:
    preset = data.get("preset")
    if preset and preset not in PRESETS:
        raise ManifestError(f"unknown preset {preset!r}; choose from {sorted(PRESETS)}")
    lesson_dials = {**(PRESETS.get(preset) or {}), **(data.get("dials") or {})}
    resolved: list[ResolvedModule] = []
    for name, override in _entries(data.get("modules") or []):
        try:
            mod = find_module(name, module_roots)
        except ModuleError as exc:
            raise ManifestError(str(exc)) from exc
        wanted = {**lesson_dials, **override}
        settings = {}
        for dial, allowed in mod.dials.items():
            value = wanted.get(dial, allowed[0])
            if value not in allowed:
                raise ManifestError(f"{name}: dial {dial}={value!r} not supported (allowed: {allowed})")
            settings[dial] = value
        for dial, allowed in mod.requires.items():
            if wanted.get(dial) not in allowed:
                raise ManifestError(f"{name}: requires {dial} in {allowed}, lesson has {wanted.get(dial)!r}")
        resolved.append(ResolvedModule(mod, settings))

    produced: set[str] = set()
    for rm in resolved:
        missing = [s for s in rm.module.accepts if s not in produced]
        if missing:
            raise ManifestError(f"{rm.module.name}: needs data shape(s) {missing}; add a dataset module "
                                f"that produces them earlier in the lesson")
        produced |= set(rm.module.produces)

    # Collect all params declared by modules and their specs
    param_specs: dict[str, list[tuple[str, dict]]] = {}  # param_name -> [(module_name, spec), ...]
    for rm in resolved:
        for pname, spec in rm.module.params.items():
            if pname not in param_specs:
                param_specs[pname] = []
            param_specs[pname].append((rm.module.name, spec))

    # Resolve param values, ensuring each param value satisfies ALL modules that declare it
    params: dict[str, int] = {}
    wanted_params = data.get("params") or {}
    for pname, declaring_modules in param_specs.items():
        if pname in wanted_params:
            value = wanted_params[pname]
        else:
            # Param not in manifest; check if all defaults agree
            defaults = [spec.get("default") for _, spec in declaring_modules]
            if len(set(defaults)) > 1:  # defaults differ
                module_names = ", ".join(name for name, _ in declaring_modules)
                raise ManifestError(f"param {pname} has different defaults in {module_names}; "
                                  f"set it explicitly in the manifest")
            value = defaults[0]

        # Check that value is an integer
        if not isinstance(value, int):
            raise ManifestError(f"param {pname}={value!r} is not an integer")

        # Validate against ALL modules' ranges
        for module_name, spec in declaring_modules:
            lo, hi = spec.get("min"), spec.get("max")
            if (lo is not None and value < lo) or (hi is not None and value > hi):
                raise ManifestError(f"param {pname}={value} outside [{lo}, {hi}] for {module_name}")

        params[pname] = value

    unknown = set(wanted_params) - set(params)
    if unknown:
        raise ManifestError(f"params not used by any module: {sorted(unknown)}")

    minutes_value = data.get("minutes")
    if minutes_value is not None:
        try:
            minutes = int(minutes_value)
        except (ValueError, TypeError):
            raise ManifestError(f"lesson minutes={minutes_value!r} is not an integer")
    else:
        minutes = 0
    need = sum(rm.module.minutes for rm in resolved)
    if minutes and need > minutes:
        raise ManifestError(f"modules need {need} minutes but the lesson allows {minutes}")

    return Lesson(id=data["id"], title=data["title"], minutes=minutes, params=params,
                  modules=resolved, preset=preset)


def load_lesson(path: Path, module_roots: list[Path]) -> Lesson:
    return lesson_from_dict(yaml.safe_load(Path(path).read_text()), module_roots)
