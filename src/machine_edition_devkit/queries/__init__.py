"""Query Runner module for executing the deterministic sample query pack."""

from dataclasses import dataclass
from pathlib import Path
import json
from typing import List, Dict, Any, Optional
from machine_edition_devkit.parse import MachineEdition
from machine_edition_devkit.validate import MachineEditionValidator


@dataclass
class QueryExecutionResult:
    query_id: str
    category: str
    question: str
    operation: str
    status: str  # "PASS" or "FAIL"
    actual: Any
    expected: Any
    error_message: Optional[str] = None


class SampleQueryRunner:
    """Executes deterministic reference queries over a Machine Edition instance."""

    def __init__(self, queries_path: Optional[Path] = None):
        if queries_path is None:
            queries_path = Path(__file__).resolve().parent.parent.parent.parent / "queries" / "sample_queries.json"
        self.queries_path = queries_path
        self._query_defs = self._load_query_defs()

    def _load_query_defs(self) -> List[Dict[str, Any]]:
        with open(self.queries_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_queries(self) -> List[Dict[str, str]]:
        return [
            {
                "query_id": q["query_id"],
                "category": q["category"],
                "question": q["question"],
                "capability": q["capability_demonstrated"],
            }
            for q in self._query_defs
        ]

    def run_query(self, edition: MachineEdition, query_id: str) -> QueryExecutionResult:
        q = next((item for item in self._query_defs if item["query_id"] == query_id), None)
        if not q:
            raise KeyError(f"Query {query_id} not found")

        expected = q["expected_result"]
        actual = None
        status = "FAIL"
        err_msg = None

        try:
            # Deterministic execution dispatcher
            if query_id == "Q001":
                actual = edition.manifest.get("package_id")
            elif query_id == "Q002":
                actual = edition.manifest.get("version")
            elif query_id == "Q003":
                actual = edition.capabilities().get("formats")
            elif query_id == "Q004":
                actual = edition.capabilities().get("resolution_levels")
            elif query_id == "Q005":
                actual = edition.get_unit(q["arguments"]["unit_id"]).title
            elif query_id == "Q006":
                actual = len(edition.find_units(scope=q["arguments"]["scope"]))
            elif query_id == "Q007":
                actual = edition.find_units(query=q["arguments"]["query"])[0].id
            elif query_id == "Q008":
                actual = edition.get_definition(q["arguments"]["def_id"]).term
            elif query_id == "Q009":
                actual = edition.find_definitions(q["arguments"]["term"])[0].term
            elif query_id == "Q010":
                actual = len(edition.boundaries())
            elif query_id == "Q011":
                actual = edition._boundaries[q["arguments"]["bound_id"]].statement
            elif query_id == "Q012":
                actual = edition.related(q["arguments"]["unit_id"], direction=q["arguments"]["direction"])[0].predicate
            elif query_id == "Q013":
                actual = edition.related(q["arguments"]["unit_id"], direction=q["arguments"]["direction"])[0].subject_id
            elif query_id == "Q014":
                actual = edition.relationships(predicate=q["arguments"]["predicate"])[0].object_id
            elif query_id == "Q015":
                actual = edition.provenance(q["arguments"]["unit_id"]).source_url
            elif query_id == "Q016":
                actual = edition.provenance(q["arguments"]["unit_id"]).source_title
            elif query_id == "Q017":
                actual = edition.find_units(resolution_level=q["arguments"]["resolution_level"])[0].id
            elif query_id == "Q018":
                actual = edition.find_units(resolution_level=q["arguments"]["resolution_level"])[0].id
            elif query_id == "Q019":
                actual = MachineEditionValidator().validate_package(edition.package_path).outcome
            elif query_id == "Q020":
                actual = edition.provenance(edition.get_definition(q["arguments"]["def_id"])).id
            else:
                err_msg = f"No execution mapping for query {query_id}"

            if actual == expected:
                status = "PASS"
            else:
                status = "FAIL"
                err_msg = f"Actual ({actual}) != Expected ({expected})"
        except Exception as e:
            status = "FAIL"
            err_msg = str(e)

        return QueryExecutionResult(
            query_id=query_id,
            category=q["category"],
            question=q["question"],
            operation=q["operation"],
            status=status,
            actual=actual,
            expected=expected,
            error_message=err_msg,
        )

    def run_all(self, edition: MachineEdition) -> List[QueryExecutionResult]:
        return [self.run_query(edition, q["query_id"]) for q in self._query_defs]

    def render_matrix(self, results: List[QueryExecutionResult]) -> str:
        lines = [
            f"{'ID':<6} {'Category':<16} {'Status':<8} {'Question'}",
            "-" * 78,
        ]
        for r in results:
            lines.append(f"{r.query_id:<6} {r.category:<16} {r.status:<8} {r.question[:46]}")
        lines.append("-" * 78)
        passed = sum(1 for r in results if r.status == "PASS")
        total = len(results)
        lines.append(f"Result: {passed}/{total} Passed")
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    specimen = Path(__file__).resolve().parent.parent.parent.parent / "specimen" / "srow" / "package"
    ed = MachineEdition.load(specimen)
    runner = SampleQueryRunner()

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        for q in runner.list_queries():
            print(f"{q['query_id']}: [{q['category']}] {q['question']}")
    elif len(sys.argv) > 2 and sys.argv[1] == "run":
        res = runner.run_query(ed, sys.argv[2])
        print(f"{res.query_id} [{res.status}]: {res.question} -> {res.actual}")
    else:
        results = runner.run_all(ed)
        print(runner.render_matrix(results))
