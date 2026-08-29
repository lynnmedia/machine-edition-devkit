import hashlib
from pathlib import Path
import json
import jsonschema


def test_srow_reference_specimen_authority_and_integrity():
    specimen_dir = Path(__file__).resolve().parent.parent / "specimen" / "srow"
    package_dir = specimen_dir / "package"
    schemas_dir = Path(__file__).resolve().parent.parent / "schemas"

    # 1. Verify SOURCE.json metadata
    source_json = json.loads((specimen_dir / "SOURCE.json").read_text(encoding="utf-8"))
    assert source_json["source_archive_sha256"] == "0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181"
    assert source_json["source_tag"] == "v0.1-srow-rc4"

    # 2. Check required files presence
    required_files = [
        "manifest.json",
        "meaning-units.jsonl",
        "provenance.jsonl",
        "definitions.jsonl",
        "boundaries.jsonl",
        "relationships.jsonl",
        "full-preview.md",
        "LICENSE.txt",
    ]
    for rf in required_files:
        assert (package_dir / rf).exists(), f"Required file missing: {rf}"

    # 3. Validate manifest schema
    manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest_schema = json.loads((schemas_dir / "manifest.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(manifest, manifest_schema)
    assert manifest["package_id"] == "winmedia.srow.reference-specimen"
    assert manifest["version"] == "0.1.0"
    assert manifest["status"] == "developer_preview"

    # 4. Validate meaning units and referential integrity
    mu_schema = json.loads((schemas_dir / "meaning-unit.schema.json").read_text(encoding="utf-8"))
    prov_schema = json.loads((schemas_dir / "provenance.schema.json").read_text(encoding="utf-8"))
    def_schema = json.loads((schemas_dir / "definition.schema.json").read_text(encoding="utf-8"))
    bound_schema = json.loads((schemas_dir / "boundary.schema.json").read_text(encoding="utf-8"))
    rel_schema = json.loads((schemas_dir / "relationship.schema.json").read_text(encoding="utf-8"))

    # Load and validate provenance
    provenance_ids = set()
    for line in (package_dir / "provenance.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jsonschema.validate(record, prov_schema)
        provenance_ids.add(record["id"])

    # Load and validate meaning units
    meaning_unit_ids = set()
    for line in (package_dir / "meaning-units.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jsonschema.validate(record, mu_schema)
        assert record["id"] not in meaning_unit_ids, f"Duplicate MU id: {record['id']}"
        meaning_unit_ids.add(record["id"])
        assert record["provenance_id"] in provenance_ids, f"Unresolved prov ID: {record['provenance_id']}"

    # Load and validate definitions
    for line in (package_dir / "definitions.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jsonschema.validate(record, def_schema)
        assert record["provenance_id"] in provenance_ids

    # Load and validate boundaries
    for line in (package_dir / "boundaries.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jsonschema.validate(record, bound_schema)
        assert record["provenance_id"] in provenance_ids

    # Load and validate relationships
    for line in (package_dir / "relationships.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jsonschema.validate(record, rel_schema)
        assert record["subject_id"] in meaning_unit_ids, f"Subject {record['subject_id']} not in MUs"
        assert record["object_id"] in meaning_unit_ids, f"Object {record['object_id']} not in MUs"
        assert record["provenance_id"] in provenance_ids
