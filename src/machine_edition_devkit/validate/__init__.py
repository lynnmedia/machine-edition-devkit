"""Validation module implementing the C1-C7 conformance contract of Machine Edition Specification v0.1."""

from dataclasses import dataclass, field
from pathlib import Path
import json
import hashlib
from typing import List, Dict, Any, Optional, Set
import jsonschema


@dataclass
class ValidationCheckResult:
    check_id: str
    status: str  # "PASS" or "FAIL"
    path: str
    message: str
    record_id: Optional[str] = None


@dataclass
class ValidationReport:
    outcome: str  # "ME_CONFORMANT" or "ME_NONCONFORMANT"
    checks: List[ValidationCheckResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.outcome == "ME_CONFORMANT"

    def render_summary(self) -> str:
        lines = [
            "Machine Edition Specification v0.1 Conformance Report",
            "=" * 54,
        ]
        categories = {
            "C1 (Manifest Presence & Schema)": "PASS",
            "C2 (Required Package Files)": "PASS",
            "C3 (Valid JSON/JSONL Syntax)": "PASS",
            "C4 (Meaning Unit Validation)": "PASS",
            "C5 (Referential & Provenance Integrity)": "PASS",
            "C6 (Human Entrypoint Linkage)": "PASS",
            "C7 (License Alignment & Boundaries)": "PASS",
        }

        for check in self.checks:
            if check.status == "FAIL":
                for cat in categories:
                    if cat.startswith(check.check_id):
                        categories[cat] = "FAIL"

        for cat, status in categories.items():
            lines.append(f"{cat:<40} {status}")

        lines.append("=" * 54)
        lines.append(f"Outcome: {self.outcome}")
        if self.errors:
            lines.append("\nFailures:")
            for err in self.errors:
                lines.append(f"  - {err}")
        return "\n".join(lines)


class MachineEditionValidator:
    """Reference implementation of the Machine Edition Specification v0.1 Conformance Contract."""

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
        checks: List[ValidationCheckResult] = []
        errors: List[str] = []
        warnings: List[str] = []

        if not package_path.exists() or not package_path.is_dir():
            err = f"Package directory does not exist: {package_path}"
            errors.append(err)
            return ValidationReport(outcome="ME_NONCONFORMANT", errors=errors)

        # C1: Manifest Presence & Schema
        manifest_path = package_path / "manifest.json"
        manifest: Optional[Dict[str, Any]] = None
        if not manifest_path.exists():
            msg = "Missing required file: manifest.json"
            errors.append(msg)
            checks.append(ValidationCheckResult(check_id="C1", status="FAIL", path="manifest.json", message=msg))
        else:
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                if "manifest.schema.json" in self._schemas:
                    try:
                        jsonschema.validate(manifest, self._schemas["manifest.schema.json"])
                        checks.append(ValidationCheckResult(check_id="C1", status="PASS", path="manifest.json", message="Manifest conforms to schema"))
                    except jsonschema.ValidationError as ve:
                        msg = f"Manifest schema validation error: {ve.message}"
                        errors.append(msg)
                        checks.append(ValidationCheckResult(check_id="C1", status="FAIL", path="manifest.json", message=msg))
                else:
                    msg = "Manifest schema not found for validation"
                    errors.append(msg)
                    checks.append(ValidationCheckResult(check_id="C1", status="FAIL", path="manifest.json", message=msg))
            except Exception as e:
                msg = f"Malformed JSON in manifest.json: {str(e)}"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C1", status="FAIL", path="manifest.json", message=msg))

        # C2: Required Files
        required_files = [
            ("manifest.json", "manifest.json"),
            ("meaning-units.jsonl", "meaning-units.jsonl"),
            ("provenance.jsonl", manifest.get("provenance_file", "provenance.jsonl") if manifest else "provenance.jsonl"),
            ("full-preview.md", manifest.get("human_readable_entrypoint", "full-preview.md") if manifest else "full-preview.md"),
            ("LICENSE.txt", manifest.get("license", "LICENSE.txt") if manifest else "LICENSE.txt"),
        ]

        for desc, filename in required_files:
            target_path = package_path / filename
            if not target_path.exists():
                msg = f"Missing required file: {filename}"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C2", status="FAIL", path=filename, message=msg))
            else:
                checks.append(ValidationCheckResult(check_id="C2", status="PASS", path=filename, message=f"Required file present: {filename}"))

        # C3 & C5: Load Provenance Records
        provenance_ids: Set[str] = set()
        prov_file = package_path / (manifest.get("provenance_file", "provenance.jsonl") if manifest else "provenance.jsonl")
        if prov_file.exists():
            try:
                with open(prov_file, "r", encoding="utf-8") as f:
                    for line_no, line in enumerate(f, start=1):
                        if not line.strip():
                            continue
                        try:
                            record = json.loads(line)
                            if "provenance.schema.json" in self._schemas:
                                try:
                                    jsonschema.validate(record, self._schemas["provenance.schema.json"])
                                except jsonschema.ValidationError as ve:
                                    msg = f"provenance.jsonl line {line_no} schema error: {ve.message}"
                                    errors.append(msg)
                                    checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"{prov_file.name}:{line_no}", message=msg, record_id=record.get("id")))
                            rec_id = record.get("id")
                            if rec_id:
                                if rec_id in provenance_ids:
                                    msg = f"Duplicate provenance ID: {rec_id}"
                                    errors.append(msg)
                                    checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"{prov_file.name}:{line_no}", message=msg, record_id=rec_id))
                                provenance_ids.add(rec_id)
                        except json.JSONDecodeError as jde:
                            msg = f"Malformed JSON in {prov_file.name} line {line_no}: {str(jde)}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=f"{prov_file.name}:{line_no}", message=msg))
            except Exception as e:
                msg = f"Failed reading {prov_file.name}: {str(e)}"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=prov_file.name, message=msg))

        # C3 & C4 & C5: Meaning Units
        meaning_unit_ids: Set[str] = set()
        mu_file = package_path / "meaning-units.jsonl"
        if mu_file.exists():
            try:
                with open(mu_file, "r", encoding="utf-8") as f:
                    for line_no, line in enumerate(f, start=1):
                        if not line.strip():
                            continue
                        try:
                            record = json.loads(line)
                            rec_id = record.get("id")
                            if "meaning-unit.schema.json" in self._schemas:
                                try:
                                    jsonschema.validate(record, self._schemas["meaning-unit.schema.json"])
                                    checks.append(ValidationCheckResult(check_id="C4", status="PASS", path=f"meaning-units.jsonl:{line_no}", message="Record conforms to schema", record_id=rec_id))
                                except jsonschema.ValidationError as ve:
                                    msg = f"meaning-units.jsonl line {line_no} schema error: {ve.message}"
                                    errors.append(msg)
                                    checks.append(ValidationCheckResult(check_id="C4", status="FAIL", path=f"meaning-units.jsonl:{line_no}", message=msg, record_id=rec_id))

                            if rec_id:
                                if rec_id in meaning_unit_ids:
                                    msg = f"Duplicate meaning_unit ID: {rec_id}"
                                    errors.append(msg)
                                    checks.append(ValidationCheckResult(check_id="C4", status="FAIL", path=f"meaning-units.jsonl:{line_no}", message=msg, record_id=rec_id))
                                meaning_unit_ids.add(rec_id)

                            prov_id = record.get("provenance_id")
                            if prov_id and prov_id not in provenance_ids:
                                msg = f"meaning-units.jsonl line {line_no} references undefined provenance_id: {prov_id}"
                                errors.append(msg)
                                checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"meaning-units.jsonl:{line_no}", message=msg, record_id=rec_id))
                        except json.JSONDecodeError as jde:
                            msg = f"Malformed JSON in meaning-units.jsonl line {line_no}: {str(jde)}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=f"meaning-units.jsonl:{line_no}", message=msg))
            except Exception as e:
                msg = f"Failed reading meaning-units.jsonl: {str(e)}"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path="meaning-units.jsonl", message=msg))

        # Optional Definitions Check
        def_file = package_path / "definitions.jsonl"
        if def_file.exists():
            with open(def_file, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        if "definition.schema.json" in self._schemas:
                            try:
                                jsonschema.validate(record, self._schemas["definition.schema.json"])
                            except jsonschema.ValidationError as ve:
                                msg = f"definitions.jsonl line {line_no} schema error: {ve.message}"
                                errors.append(msg)
                                checks.append(ValidationCheckResult(check_id="C4", status="FAIL", path=f"definitions.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                        prov_id = record.get("provenance_id")
                        if prov_id and prov_id not in provenance_ids:
                            msg = f"definitions.jsonl line {line_no} references undefined provenance_id: {prov_id}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"definitions.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                    except json.JSONDecodeError as jde:
                        msg = f"Malformed JSON in definitions.jsonl line {line_no}: {str(jde)}"
                        errors.append(msg)
                        checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=f"definitions.jsonl:{line_no}", message=msg))

        # Optional Boundaries Check
        bound_file = package_path / "boundaries.jsonl"
        if bound_file.exists():
            with open(bound_file, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        if "boundary.schema.json" in self._schemas:
                            try:
                                jsonschema.validate(record, self._schemas["boundary.schema.json"])
                            except jsonschema.ValidationError as ve:
                                msg = f"boundaries.jsonl line {line_no} schema error: {ve.message}"
                                errors.append(msg)
                                checks.append(ValidationCheckResult(check_id="C4", status="FAIL", path=f"boundaries.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                        prov_id = record.get("provenance_id")
                        if prov_id and prov_id not in provenance_ids:
                            msg = f"boundaries.jsonl line {line_no} references undefined provenance_id: {prov_id}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"boundaries.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                    except json.JSONDecodeError as jde:
                        msg = f"Malformed JSON in boundaries.jsonl line {line_no}: {str(jde)}"
                        errors.append(msg)
                        checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=f"boundaries.jsonl:{line_no}", message=msg))

        # Optional Relationships Check
        rel_file = package_path / "relationships.jsonl"
        if rel_file.exists():
            with open(rel_file, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        if "relationship.schema.json" in self._schemas:
                            try:
                                jsonschema.validate(record, self._schemas["relationship.schema.json"])
                            except jsonschema.ValidationError as ve:
                                msg = f"relationships.jsonl line {line_no} schema error: {ve.message}"
                                errors.append(msg)
                                checks.append(ValidationCheckResult(check_id="C4", status="FAIL", path=f"relationships.jsonl:{line_no}", message=msg, record_id=record.get("id")))

                        sub_id = record.get("subject_id")
                        obj_id = record.get("object_id")
                        if sub_id and sub_id not in meaning_unit_ids:
                            msg = f"relationships.jsonl line {line_no} references undefined subject_id: {sub_id}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"relationships.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                        if obj_id and obj_id not in meaning_unit_ids:
                            msg = f"relationships.jsonl line {line_no} references undefined object_id: {obj_id}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"relationships.jsonl:{line_no}", message=msg, record_id=record.get("id")))

                        prov_id = record.get("provenance_id")
                        if prov_id and prov_id not in provenance_ids:
                            msg = f"relationships.jsonl line {line_no} references undefined provenance_id: {prov_id}"
                            errors.append(msg)
                            checks.append(ValidationCheckResult(check_id="C5", status="FAIL", path=f"relationships.jsonl:{line_no}", message=msg, record_id=record.get("id")))
                    except json.JSONDecodeError as jde:
                        msg = f"Malformed JSON in relationships.jsonl line {line_no}: {str(jde)}"
                        errors.append(msg)
                        checks.append(ValidationCheckResult(check_id="C3", status="FAIL", path=f"relationships.jsonl:{line_no}", message=msg))

        # C6: Human Entrypoint Linkage
        if manifest:
            entrypoint_name = manifest.get("human_readable_entrypoint", "full-preview.md")
            if not (package_path / entrypoint_name).exists():
                msg = f"Declared human_readable_entrypoint '{entrypoint_name}' not found"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C6", status="FAIL", path="manifest.json", message=msg))
            else:
                checks.append(ValidationCheckResult(check_id="C6", status="PASS", path=entrypoint_name, message="Human entrypoint verified"))

        # C7: License Alignment
        if manifest:
            license_name = manifest.get("license", "LICENSE.txt")
            if not (package_path / license_name).exists():
                msg = f"Declared license file '{license_name}' not found"
                errors.append(msg)
                checks.append(ValidationCheckResult(check_id="C7", status="FAIL", path="manifest.json", message=msg))
            else:
                checks.append(ValidationCheckResult(check_id="C7", status="PASS", path=license_name, message="License file verified"))

        outcome = "ME_CONFORMANT" if len(errors) == 0 else "ME_NONCONFORMANT"
        return ValidationReport(outcome=outcome, checks=checks, errors=errors, warnings=warnings)
