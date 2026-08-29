from pathlib import Path
import json
import hashlib
import pytest
from machine_edition_devkit.validate import MachineEditionValidator


@pytest.fixture
def schemas_dir():
    return Path(__file__).resolve().parent.parent / "schemas"


@pytest.fixture
def base_valid_package(tmp_path):
    pkg = tmp_path / "valid_pkg"
    pkg.mkdir()
    (pkg / "manifest.json").write_text(
        json.dumps({
            "package_id": "winmedia.test.package",
            "title": "Test Package",
            "version": "0.1.0",
            "status": "developer_preview",
            "scope": "Test Scope",
            "formats": ["markdown", "jsonl"],
            "resolution_levels": ["L0", "L1", "L2", "L3", "L4"],
            "license": "LICENSE.txt",
            "human_readable_entrypoint": "full-preview.md",
            "provenance_file": "provenance.jsonl",
        }),
        encoding="utf-8"
    )
    (pkg / "provenance.jsonl").write_text(
        json.dumps({
            "id": "prov.1",
            "record_type": "provenance",
            "source_title": "Test Source",
            "source_url": "https://winmedia.com/test",
            "source_scope": "test",
        }) + "\n",
        encoding="utf-8"
    )
    (pkg / "meaning-units.jsonl").write_text(
        json.dumps({
            "id": "mu.1",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L1",
            "title": "Test Title",
            "claim": "Test Claim Assertion",
            "provenance_id": "prov.1",
            "scope": "test",
        }) + "\n",
        encoding="utf-8"
    )
    (pkg / "full-preview.md").write_text("# Preview\n", encoding="utf-8")
    (pkg / "LICENSE.txt").write_text("MIT License\n", encoding="utf-8")
    return pkg


def test_schema_source_manifest_drift(schemas_dir):
    manifest_path = schemas_dir / "schema-manifest.json"
    assert manifest_path.exists(), "schema-manifest.json must exist"
    meta = json.loads(manifest_path.read_text(encoding="utf-8"))

    for item in meta["schemas"]:
        schema_file = schemas_dir / item["name"]
        assert schema_file.exists(), f"Schema {item['name']} missing"
        computed_sha = hashlib.sha256(schema_file.read_bytes()).hexdigest()
        assert computed_sha == item["sha256"], f"Schema drift detected in {item['name']}"


def test_positive_srow_reference_specimen():
    specimen_path = Path(__file__).resolve().parent.parent / "specimen" / "srow" / "package"
    validator = MachineEditionValidator()
    report = validator.validate_package(specimen_path)
    print(report.render_summary())
    assert report.outcome == "ME_CONFORMANT"
    assert len(report.errors) == 0


def test_negative_fixture_missing_required_file(base_valid_package):
    (base_valid_package / "meaning-units.jsonl").unlink()
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("Missing required file: meaning-units.jsonl" in e for e in report.errors)


def test_negative_fixture_malformed_manifest(base_valid_package):
    (base_valid_package / "manifest.json").write_text("{ invalid json", encoding="utf-8")
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("Malformed JSON in manifest.json" in e for e in report.errors)


def test_negative_fixture_invalid_meaning_unit(base_valid_package):
    (base_valid_package / "meaning-units.jsonl").write_text(
        json.dumps({"id": "mu.1", "record_type": "meaning_unit"}) + "\n",
        encoding="utf-8"
    )
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("schema error" in e for e in report.errors)


def test_negative_fixture_duplicate_id(base_valid_package):
    mu_text = json.dumps({
        "id": "mu.duplicate",
        "record_type": "meaning_unit",
        "version": "0.1.0",
        "resolution_level": "L1",
        "title": "Test Title",
        "claim": "Test Claim",
        "provenance_id": "prov.1",
        "scope": "test",
    }) + "\n"
    (base_valid_package / "meaning-units.jsonl").write_text(mu_text + mu_text, encoding="utf-8")
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("Duplicate meaning_unit ID" in e for e in report.errors)


def test_negative_fixture_invalid_resolution(base_valid_package):
    (base_valid_package / "meaning-units.jsonl").write_text(
        json.dumps({
            "id": "mu.1",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "INVALID_LEVEL",
            "title": "Test Title",
            "claim": "Test Claim",
            "provenance_id": "prov.1",
            "scope": "test",
        }) + "\n",
        encoding="utf-8"
    )
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("schema error" in e for e in report.errors)


def test_negative_fixture_unresolved_provenance(base_valid_package):
    (base_valid_package / "meaning-units.jsonl").write_text(
        json.dumps({
            "id": "mu.1",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L1",
            "title": "Test Title",
            "claim": "Test Claim",
            "provenance_id": "prov.nonexistent",
            "scope": "test",
        }) + "\n",
        encoding="utf-8"
    )
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("references undefined provenance_id: prov.nonexistent" in e for e in report.errors)


def test_negative_fixture_dangling_relationship(base_valid_package):
    (base_valid_package / "relationships.jsonl").write_text(
        json.dumps({
            "id": "rel.1",
            "record_type": "relationship",
            "subject_id": "mu.1",
            "predicate": "clarifies",
            "object_id": "mu.nonexistent",
            "provenance_id": "prov.1",
            "scope": "test",
        }) + "\n",
        encoding="utf-8"
    )
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("references undefined object_id: mu.nonexistent" in e for e in report.errors)


def test_negative_fixture_malformed_jsonl(base_valid_package):
    (base_valid_package / "meaning-units.jsonl").write_text("{ not valid json\n", encoding="utf-8")
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("Malformed JSON" in e for e in report.errors)


def test_negative_fixture_missing_license(base_valid_package):
    (base_valid_package / "LICENSE.txt").unlink()
    validator = MachineEditionValidator()
    report = validator.validate_package(base_valid_package)
    assert report.outcome == "ME_NONCONFORMANT"
    assert any("Declared license file 'LICENSE.txt' not found" in e for e in report.errors)
