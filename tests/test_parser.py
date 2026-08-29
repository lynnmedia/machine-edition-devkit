from pathlib import Path
import pytest
from machine_edition_devkit.parse import (
    MachineEdition,
    MeaningUnit,
    DefinitionRecord,
    BoundaryRecord,
    RelationshipRecord,
    ProvenanceRecord,
    MachineEditionError,
    MachineEditionValidationError,
    RecordNotFoundError,
    ProvenanceResolutionError,
)


@pytest.fixture
def specimen_path():
    return Path(__file__).resolve().parent.parent / "specimen" / "srow" / "package"


def test_machine_edition_load_and_inspect(specimen_path):
    edition = MachineEdition.load(specimen_path, validate=True)
    summary = edition.inspect()

    assert summary["package_id"] == "winmedia.srow.reference-specimen"
    assert summary["version"] == "0.1.0"
    assert summary["status"] == "developer_preview"
    assert summary["record_counts"]["meaning_units"] == 3
    assert summary["record_counts"]["definitions"] == 2
    assert summary["record_counts"]["boundaries"] == 3
    assert summary["record_counts"]["relationships"] == 2
    assert summary["record_counts"]["provenance"] == 2


def test_meaning_units_enumeration_and_lookup(specimen_path):
    edition = MachineEdition.load(specimen_path)

    units = edition.units()
    assert len(units) == 3

    # Exact lookup
    mu = edition.get_unit("srow.ref.mu.001")
    assert mu.title == "SROW Validation Compliance Sample"
    assert mu.resolution_level == "L3"
    assert mu.provenance_id == "prov.srow-public-companion-release"

    # Filter by resolution
    l1_units = edition.find_units(resolution_level="L1")
    assert len(l1_units) == 1
    assert l1_units[0].id == "srow.ref.mu.003"

    # Filter by scope
    sample_units = edition.find_units(scope="public sample")
    assert len(sample_units) == 2

    # Case-insensitive query
    query_units = edition.find_units(query="reader respect")
    assert len(query_units) == 1
    assert query_units[0].id == "srow.ref.mu.003"


def test_definitions_and_boundaries_access(specimen_path):
    edition = MachineEdition.load(specimen_path)

    defs = edition.definitions()
    assert len(defs) == 2
    srow_def = edition.get_definition("srow.ref.def.001")
    assert srow_def.term == "SROW"

    matching_defs = edition.find_definitions("disclosure")
    assert len(matching_defs) == 1
    assert matching_defs[0].term == "Progressive Disclosure"

    boundaries = edition.boundaries()
    assert len(boundaries) == 3
    assert any("expression and structuring protocol" in b.statement for b in boundaries)


def test_relationship_traversal(specimen_path):
    edition = MachineEdition.load(specimen_path)

    all_rels = edition.relationships()
    assert len(all_rels) == 2

    # Filter by predicate
    derives_rels = edition.relationships(predicate="derives_from")
    assert len(derives_rels) == 1
    assert derives_rels[0].subject_id == "srow.ref.mu.002"
    assert derives_rels[0].object_id == "srow.ref.mu.001"

    # Related queries
    outgoing = edition.related("srow.ref.mu.002", direction="outgoing")
    assert len(outgoing) == 1
    assert outgoing[0].object_id == "srow.ref.mu.001"

    incoming = edition.related("srow.ref.mu.001", direction="incoming")
    assert len(incoming) == 1
    assert incoming[0].subject_id == "srow.ref.mu.002"


def test_provenance_resolution(specimen_path):
    edition = MachineEdition.load(specimen_path)

    prov_records = edition.provenance_records()
    assert len(prov_records) == 2

    # Resolve by unit instance
    mu = edition.get_unit("srow.ref.mu.001")
    prov = edition.provenance(mu)
    assert prov.id == "prov.srow-public-companion-release"
    assert prov.source_title == "SROW Machine Edition — Public Companion v0.1"

    # Resolve by unit ID string
    prov2 = edition.provenance("srow.ref.mu.003")
    assert prov2.id == "prov.public-srow-framework"
    assert prov2.source_url == "https://winmedia.com/frameworks/srow"


def test_capabilities_declaration(specimen_path):
    edition = MachineEdition.load(specimen_path)
    caps = edition.capabilities()
    assert "formats" in caps
    assert "resolution_levels" in caps
    assert "markdown" in caps["formats"]
    assert "L0" in caps["resolution_levels"]


def test_load_validation_failure_behavior(tmp_path):
    bad_pkg = tmp_path / "bad_pkg"
    bad_pkg.mkdir()
    # Missing manifest
    with pytest.raises(MachineEditionValidationError):
        MachineEdition.load(bad_pkg, validate=True)


def test_record_not_found_error(specimen_path):
    edition = MachineEdition.load(specimen_path)
    with pytest.raises(RecordNotFoundError):
        edition.get_unit("nonexistent.unit.id")
