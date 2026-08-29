from pathlib import Path
from machine_edition_devkit.inspect import inspect_package
from machine_edition_devkit.validate import MachineEditionValidator
from machine_edition_devkit.parse import MachineEditionParser
from machine_edition_devkit.query import MachineEditionQueryEngine
from machine_edition_devkit.compare import RepresentationComparator


def test_devkit_inspect_validate_parse_query_compare_flow():
    specimen_path = Path(__file__).resolve().parent.parent / "specimen" / "srow" / "package"
    assert specimen_path.exists()

    # 1. Inspect
    summary = inspect_package(specimen_path)
    assert summary.package_id == "winmedia.srow.reference-specimen"
    assert summary.version == "0.1.0"
    assert summary.meaning_units_count > 0
    assert summary.provenance_count > 0

    # 2. Validate
    validator = MachineEditionValidator()
    report = validator.validate_package(specimen_path)
    assert report.is_valid, f"Validation errors: {report.errors}"

    # 3. Parse
    parser = MachineEditionParser(specimen_path)
    meaning_units = list(parser.iter_meaning_units())
    provenance_map = parser.load_provenance()
    assert len(meaning_units) == summary.meaning_units_count
    assert len(provenance_map) == summary.provenance_count

    # 4. Query
    query_engine = MachineEditionQueryEngine(parser)
    l1_units = query_engine.filter_by_resolution("L1")
    assert len(l1_units) > 0
    prov = query_engine.trace_provenance(meaning_units[0].id)
    assert prov is not None
    assert prov.id == meaning_units[0].provenance_id

    # 5. Compare
    matrix = RepresentationComparator.get_standard_matrix()
    assert "Machine_Edition_v0.1" in matrix
    assert matrix["Machine_Edition_v0.1"].has_explicit_boundaries is True
    assert matrix["PDF"].has_explicit_boundaries is False
