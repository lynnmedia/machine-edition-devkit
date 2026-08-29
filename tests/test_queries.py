from pathlib import Path
import json
import pytest
from machine_edition_devkit.parse import MachineEdition
from machine_edition_devkit.queries import SampleQueryRunner


@pytest.fixture
def specimen_edition():
    specimen_path = Path(__file__).resolve().parent.parent / "specimen" / "srow" / "package"
    return MachineEdition.load(specimen_path, validate=True)


@pytest.fixture
def query_runner():
    return SampleQueryRunner()


def test_query_definitions_integrity(query_runner):
    queries = query_runner._query_defs
    assert len(queries) == 20, "Must contain exactly 20 sample queries"

    query_ids = [q["query_id"] for q in queries]
    assert len(set(query_ids)) == 20, "All query IDs must be unique"

    categories = {q["category"] for q in queries}
    expected_categories = {
        "Identity",
        "Capability",
        "Retrieval",
        "Definitions",
        "Boundaries",
        "Relationships",
        "Provenance",
        "Resolution",
        "Verification",
    }
    assert expected_categories.issubset(categories)


def test_run_all_sample_queries_pass(specimen_edition, query_runner):
    results = query_runner.run_all(specimen_edition)
    print("\n" + query_runner.render_matrix(results))

    failures = [r for r in results if r.status != "PASS"]
    assert len(failures) == 0, f"Queries failed: {[(f.query_id, f.error_message) for f in failures]}"


@pytest.mark.parametrize("query_id", [f"Q{i:03d}" for i in range(1, 21)])
def test_individual_sample_query_execution(specimen_edition, query_runner, query_id):
    result = query_runner.run_query(specimen_edition, query_id)
    assert result.status == "PASS", f"Query {query_id} failed: {result.error_message}"
