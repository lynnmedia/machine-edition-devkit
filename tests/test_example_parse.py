"""The public parser example should be stable and bounded."""

from pathlib import Path
import json
import subprocess
import sys


def test_example_parser_is_bounded_and_deterministic():
    root = Path(__file__).resolve().parents[1]
    command = [sys.executable, str(root / "examples" / "parse.py")]
    first = subprocess.run(command, check=True, capture_output=True, text=True, cwd=root)
    second = subprocess.run(command, check=True, capture_output=True, text=True, cwd=root)

    assert first.stdout == second.stdout
    result = json.loads(first.stdout)
    assert result["package_id"] == "winmedia.srow.reference-specimen"
    assert result["version"] == "0.1.0"
    units = result["meaning_units"]
    assert len(units) <= 3
    assert [unit["id"] for unit in units] == sorted(unit["id"] for unit in units)
    assert all(unit["provenance_id"] for unit in units)


def test_documented_query_commands():
    root = Path(__file__).resolve().parents[1]
    for query_id in ("Q005", "Q012", "Q015"):
        result = subprocess.run(
            [sys.executable, "-m", "machine_edition_devkit.queries", "run", query_id],
            check=True,
            capture_output=True,
            text=True,
            cwd=root,
        )
        assert f"{query_id} [PASS]" in result.stdout

    all_queries = subprocess.run(
        [sys.executable, "-m", "machine_edition_devkit.queries", "run-all"],
        check=True,
        capture_output=True,
        text=True,
        cwd=root,
    )
    assert "Result: 20/20 Passed" in all_queries.stdout
