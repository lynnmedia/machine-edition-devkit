"""Inspection module interface for Machine Edition packages."""

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Dict, Any, List, Optional


@dataclass(frozen=True)
class PackageSummary:
    package_id: str
    title: str
    version: str
    status: str
    scope: str
    formats: List[str]
    resolution_levels: List[str]
    has_definitions: bool
    has_boundaries: bool
    has_relationships: bool
    meaning_units_count: int
    provenance_count: int


def inspect_package(package_path: Path) -> PackageSummary:
    """Inspects a Machine Edition directory and returns its summary metadata without loading heavy contents."""
    manifest_file = package_path / "manifest.json"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest not found in {package_path}")

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    meaning_units_file = package_path / "meaning-units.jsonl"
    mu_count = 0
    if meaning_units_file.exists():
        with open(meaning_units_file, "r", encoding="utf-8") as f:
            mu_count = sum(1 for line in f if line.strip())

    prov_file = package_path / manifest.get("provenance_file", "provenance.jsonl")
    prov_count = 0
    if prov_file.exists():
        with open(prov_file, "r", encoding="utf-8") as f:
            prov_count = sum(1 for line in f if line.strip())

    return PackageSummary(
        package_id=manifest.get("package_id", ""),
        title=manifest.get("title", ""),
        version=manifest.get("version", ""),
        status=manifest.get("status", ""),
        scope=manifest.get("scope", ""),
        formats=manifest.get("formats", []),
        resolution_levels=manifest.get("resolution_levels", []),
        has_definitions=(package_path / "definitions.jsonl").exists(),
        has_boundaries=(package_path / "boundaries.jsonl").exists(),
        has_relationships=(package_path / "relationships.jsonl").exists(),
        meaning_units_count=mu_count,
        provenance_count=prov_count,
    )
