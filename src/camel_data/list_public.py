"""Public-data route into LiST (the 2DCC-MIP Lifetime Sample Tracking database).

The public read-only key only sees records whose status is ``Published``.
It is not a secret, but it is still never written into code or notebooks:
it is read from, in order,

1. the ``LIST_API_KEY`` environment variable (``.env`` in this repo), or
2. a Colab Secret named ``LIST_API_KEY`` (key icon in the Colab sidebar).

LiST only answers from inside the Penn State network (campus or VPN), so
classroom notebooks use the SharePoint data slice instead; this module is the
route teachers and researchers use to explore or rebuild that slice.
"""

from __future__ import annotations

import os

import requests

DEFAULT_BASE_URL = "https://m4-2dcc.vmhost.psu.edu/list/api/v2"
KEY_HEADER = "X-API-KEY"


def _api_key() -> str:
    key = os.environ.get("LIST_API_KEY")
    if key:
        return key
    try:  # Colab Secrets
        from google.colab import userdata  # type: ignore

        return userdata.get("LIST_API_KEY")
    except Exception as exc:  # noqa: BLE001 — re-raised with a clear message
        raise RuntimeError(
            "No LiST key found. Set the LIST_API_KEY environment variable, or in Colab "
            "add a Secret named LIST_API_KEY (key icon in the left sidebar) and allow "
            "this notebook to use it."
        ) from exc


class PublicLiST:
    """Tiny read-only client for public LiST records."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout: float = 60.0):
        env_base = os.environ.get("LIST_BASE_URL")
        self.base_url = base_url or (env_base.rstrip("/") + "/api/v2" if env_base else DEFAULT_BASE_URL)
        self.session = requests.Session()
        self.session.headers.update({KEY_HEADER: api_key or _api_key(), "Accept": "application/json"})
        self.timeout = timeout

    def _call(self, method: str, path: str, **kwargs):
        try:
            r = self.session.request(method, self.base_url + path, timeout=self.timeout, **kwargs)
        except requests.ConnectionError as exc:
            raise ConnectionError(
                "Could not reach LiST. It only answers from the Penn State network "
                "(campus Wi-Fi or GlobalProtect VPN). Off campus, use the SharePoint data slice."
            ) from exc
        if r.status_code in (401, 403):
            raise PermissionError(f"LiST rejected the API key (HTTP {r.status_code}).")
        r.raise_for_status()
        return r

    def samples(self, page_size: int = 500) -> list[dict]:
        """Every published sample (pages through the whole public catalog)."""
        rows, start = [], 0
        while True:
            payload = self._call("POST", "/samples/search", json={},
                                 params={"start": start, "length": page_size,
                                         "draw": start // page_size + 1}).json()
            batch = payload.get("data") or []
            rows.extend(batch)
            start += len(batch)
            if not batch or start >= payload.get("recordsFiltered", start):
                return rows

    def sample(self, sample_id: int) -> dict:
        return self._call("GET", f"/samples/{sample_id}").json()

    def activities(self, sample_id: int) -> list[dict]:
        return self._call("GET", f"/samples/{sample_id}/activities").json()

    def files(self, sample_id: int) -> list[dict]:
        """Flat list of downloadable files across a sample's activities."""
        out = []
        for act in self.activities(sample_id):
            for group in act.get("files") or []:
                for f in group.get("files") or []:
                    out.append({"activity_id": act.get("id"), "file_id": f.get("id"),
                                "filename": f.get("filename"), "instrument": act.get("instrument"),
                                "activity_type": act.get("type")})
        return out

    def download(self, activity_id: int, file_id: int) -> bytes:
        return self._call("GET", f"/sample-activities/{activity_id}/files/{file_id}").content

    def afm_samples(self) -> list[dict]:
        return [s for s in self.samples() if "AFM" in (s.get("characterizationTechniques") or [])]
