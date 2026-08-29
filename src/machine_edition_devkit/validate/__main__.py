"""CLI entrypoint for Machine Edition validator."""

import sys
from pathlib import Path
from machine_edition_devkit.validate import MachineEditionValidator


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m machine_edition_devkit.validate <path/to/package>")
        sys.exit(1)

    target_dir = Path(sys.argv[1])
    validator = MachineEditionValidator()
    report = validator.validate_package(target_dir)

    print(f"Validation outcome: {report.outcome}")
    if report.errors:
        print(f"Errors ({len(report.errors)}):")
        for err in report.errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("All schemas and invariants verified successfully (ME_CONFORMANT).")
        sys.exit(0)


if __name__ == "__main__":
    main()
