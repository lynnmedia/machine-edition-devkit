"""Developer Kit v0.1.0: print a bounded, deterministic SROW specimen summary."""

from pathlib import Path
import json

from machine_edition_devkit.parse import MachineEdition


def main() -> None:
    package = Path(__file__).resolve().parents[1] / "specimen" / "srow" / "package"
    edition = MachineEdition.load(package, validate=True)
    units = sorted(edition.units(), key=lambda unit: unit.id)[:3]
    result = {
        "package_id": edition.manifest["package_id"],
        "version": edition.manifest["version"],
        "meaning_units": [
            {"id": unit.id, "provenance_id": unit.provenance_id}
            for unit in units
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
