"""Parser module interface for Machine Edition data records."""

from dataclasses import dataclass
from pathlib import Path
import json
from typing import List, Dict, Any, Optional, Iterator


@dataclass(frozen=True)
class MeaningUnit:
    id: str
    record_type: str
    version: str
    resolution_level: str
    title: str
    claim: str
    provenance_id: str
    scope: str


@dataclass(frozen=True)
class ProvenanceRecord:
    id: str
    record_type: str
    source_title: str
    source_url: Optional[str]
    source_scope: str
    retrieved_for_preview: Optional[str]


class MachineEditionParser:
    """Parses Machine Edition packages into typed domain objects."""

    def __init__(self, package_path: Path):
        self.package_path = package_path

    def iter_meaning_units(self) -> Iterator[MeaningUnit]:
        mu_path = self.package_path / "meaning-units.jsonl"
        if not mu_path.exists():
            return
        with open(mu_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                yield MeaningUnit(
                    id=d["id"],
                    record_type=d["record_type"],
                    version=d["version"],
                    resolution_level=d["resolution_level"],
                    title=d["title"],
                    claim=d["claim"],
                    provenance_id=d["provenance_id"],
                    scope=d["scope"],
                )

    def load_provenance(self) -> Dict[str, ProvenanceRecord]:
        prov_path = self.package_path / "provenance.jsonl"
        results = {}
        if not prov_path.exists():
            return results
        with open(prov_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                results[d["id"]] = ProvenanceRecord(
                    id=d["id"],
                    record_type=d["record_type"],
                    source_title=d.get("source_title", ""),
                    source_url=d.get("source_url"),
                    source_scope=d.get("source_scope", ""),
                    retrieved_for_preview=d.get("retrieved_for_preview"),
                )
        return results
