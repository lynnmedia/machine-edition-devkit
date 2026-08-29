"""Validation module interface for Machine Edition packages against Spec v0.1 schemas and invariants."""

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import List, Dict, Any, Optional
import jsonschema


@dataclass
class ValidationReport:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class MachineEditionValidator:
    """Reference validator implementation verifying structural conformance and referential integrity."""

    def __init__(self, schemas_dir: Optional[Path] = None):
        if schemas_dir is None:
            schemas_dir = Path(__file__).resolve().parent.parent.parent.parent / "schemas"
        self.schemas_dir = schemas_dir
        self._schemas = self._load_schemas()

    def _load_schemas(self) -> Dict[str, Any]:
        schemas = {}
        if self.schemas_dir.exists():
            for p in self.schemas_dir.glob("*.schema.json"):
                with open(p, "r", encoding="utf-8") as f:
                    schemas[p.name] = json.load(f)
        return schemas

    def validate_package(self, package_path: Path) -> ValidationReport:
        errors = []
        warnings = []

        manifest_path = package_path / "manifest.json"
        if not manifest_path.exists():
            return ValidationReport(is_valid=False, errors=["Missing required file: manifest.json"])

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            return ValidationReport(is_valid=False, errors=[f"Invalid JSON in manifest.json: {str(e)}"])

        if "manifest.schema.json" in self._schemas:
            try:
                jsonschema.validate(manifest, self._schemas["manifest.schema.json"])
            except jsonschema.ValidationError as e:
                errors.append(f"Manifest schema validation error: {e.message}")

        # Required files check
        required_files = ["meaning-units.jsonl", "provenance.jsonl", "LICENSE.txt"]
        for rf in required_files:
            if not (package_path / rf).exists():
                errors.append(f"Missing required package file: {rf}")

        # Referential integrity check
        prov_file = package_path / manifest.get("provenance_file", "provenance.jsonl")
        known_prov_ids = set()
        if prov_file.exists():
            with open(prov_file, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        known_prov_ids.add(record.get("id"))
                    except Exception as e:
                        errors.append(f"Invalid JSON in provenance.jsonl line {idx}: {str(e)}")

        mu_file = package_path / "meaning-units.jsonl"
        if mu_file.exists():
            with open(mu_file, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        if "meaning-unit.schema.json" in self._schemas:
                            try:
                                jsonschema.validate(record, self._schemas["meaning-unit.schema.json"])
                            except jsonschema.ValidationError as ve:
                                errors.append(f"meaning-units.jsonl line {idx} schema error: {ve.message}")

                        prov_id = record.get("provenance_id")
                        if prov_id and prov_id not in known_prov_ids:
                            errors.append(f"meaning-units.jsonl line {idx} references undefined provenance_id: {prov_id}")
                    except Exception as e:
                        errors.append(f"Invalid JSON in meaning-units.jsonl line {idx}: {str(e)}")

        return ValidationReport(is_valid=(len(errors) == 0), errors=errors, warnings=warnings)
