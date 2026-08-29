"""Integrity verification for ME-BENCH-001 frozen benchmark artifacts."""

from pathlib import Path
import json
import hashlib
from typing import Dict, Any, List


def verify_benchmark_integrity(repo_root: Path) -> Dict[str, Any]:
    """Verifies SHA-256 hashes of all benchmark files against integrity-manifest.json."""
    integrity_manifest_path = repo_root / "benchmark" / "integrity-manifest.json"
    if not integrity_manifest_path.exists():
        return {
            "all_passed": False,
            "error": "integrity-manifest.json not found",
            "mismatches": [],
        }

    manifest = json.loads(integrity_manifest_path.read_text(encoding="utf-8"))
    expected_hashes = manifest.get("hashes", {})

    mismatches = []
    checked_files = []

    for rel_path, expected_hash in expected_hashes.items():
        full_path = repo_root / rel_path
        if not full_path.exists():
            mismatches.append({
                "file": rel_path,
                "error": "FILE_MISSING",
                "expected": expected_hash,
                "actual": None,
            })
            continue

        actual_hash = hashlib.sha256(full_path.read_bytes()).hexdigest()
        checked_files.append(rel_path)
        if actual_hash != expected_hash:
            mismatches.append({
                "file": rel_path,
                "error": "HASH_MISMATCH",
                "expected": expected_hash,
                "actual": actual_hash,
            })

    return {
        "benchmark_id": manifest.get("benchmark_id"),
        "version": manifest.get("version"),
        "status": manifest.get("status"),
        "file_count": len(expected_hashes),
        "checked_count": len(checked_files),
        "mismatches": mismatches,
        "all_passed": len(mismatches) == 0,
    }
