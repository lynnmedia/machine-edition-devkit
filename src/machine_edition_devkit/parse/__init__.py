"""Parser module implementing typed domain objects and MachineEdition entity loader."""

from dataclasses import dataclass
from pathlib import Path
import json
from typing import List, Dict, Any, Optional, Iterator
from machine_edition_devkit.validate import MachineEditionValidator, ValidationReport


class MachineEditionError(Exception):
    """Base exception for Machine Edition consumption failures."""
    pass


class MachineEditionValidationError(MachineEditionError):
    """Raised when a package fails validation during load."""
    def __init__(self, message: str, report: ValidationReport):
        super().__init__(message)
        self.report = report


class RecordNotFoundError(MachineEditionError):
    """Raised when an exact record ID cannot be located."""
    pass


class ProvenanceResolutionError(MachineEditionError):
    """Raised when a required provenance reference cannot be resolved."""
    pass


@dataclass(frozen=True)
class MeaningUnit:
    id: str
    record_type: str
    version: str
    resolution_level: str
    title: str
    claim: str
    provenance_id: str
    scope: str


@dataclass(frozen=True)
class DefinitionRecord:
    id: str
    record_type: str
    term: str
    definition: str
    provenance_id: str
    scope: str


@dataclass(frozen=True)
class BoundaryRecord:
    id: str
    record_type: str
    statement: str
    provenance_id: str
    scope: str


@dataclass(frozen=True)
class RelationshipRecord:
    id: str
    record_type: str
    subject_id: str
    predicate: str
    object_id: str
    provenance_id: str
    scope: str


@dataclass(frozen=True)
class ProvenanceRecord:
    id: str
    record_type: str
    source_title: str
    source_url: Optional[str]
    source_scope: str
    retrieved_for_preview: Optional[str]


class MachineEdition:
    """Represents a loaded, validated, conformant Machine Edition package."""

    def __init__(
        self,
        package_path: Path,
        manifest: Dict[str, Any],
        meaning_units: Dict[str, MeaningUnit],
        definitions: Dict[str, DefinitionRecord],
        boundaries: Dict[str, BoundaryRecord],
        relationships: List[RelationshipRecord],
        provenance_records: Dict[str, ProvenanceRecord],
    ):
        self.package_path = package_path
        self.manifest = manifest
        self._units = meaning_units
        self._definitions = definitions
        self._boundaries = boundaries
        self._relationships = relationships
        self._provenance = provenance_records

    @classmethod
    def load(cls, package_path: str | Path, validate: bool = True) -> "MachineEdition":
        """Loads a Machine Edition from directory, verifying conformance if validate=True."""
        path = Path(package_path).resolve()
        if not path.exists() or not path.is_dir():
            raise MachineEditionError(f"Package path does not exist or is not a directory: {path}")

        if validate:
            validator = MachineEditionValidator()
            report = validator.validate_package(path)
            if not report.is_valid:
                raise MachineEditionValidationError(
                    f"Machine Edition validation failed with outcome {report.outcome}: {'; '.join(report.errors)}",
                    report=report,
                )

        manifest_file = path / "manifest.json"
        if not manifest_file.exists():
            raise MachineEditionError("Missing required manifest.json")

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Load Provenance
        prov_file = path / manifest.get("provenance_file", "provenance.jsonl")
        provenance_map: Dict[str, ProvenanceRecord] = {}
        if prov_file.exists():
            with open(prov_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    provenance_map[d["id"]] = ProvenanceRecord(
                        id=d["id"],
                        record_type=d["record_type"],
                        source_title=d.get("source_title", ""),
                        source_url=d.get("source_url"),
                        source_scope=d.get("source_scope", ""),
                        retrieved_for_preview=d.get("retrieved_for_preview"),
                    )

        # Load Meaning Units
        mu_file = path / "meaning-units.jsonl"
        units_map: Dict[str, MeaningUnit] = {}
        if mu_file.exists():
            with open(mu_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    units_map[d["id"]] = MeaningUnit(
                        id=d["id"],
                        record_type=d["record_type"],
                        version=d["version"],
                        resolution_level=d["resolution_level"],
                        title=d["title"],
                        claim=d["claim"],
                        provenance_id=d["provenance_id"],
                        scope=d["scope"],
                    )

        # Load Definitions
        def_file = path / "definitions.jsonl"
        definitions_map: Dict[str, DefinitionRecord] = {}
        if def_file.exists():
            with open(def_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    definitions_map[d["id"]] = DefinitionRecord(
                        id=d["id"],
                        record_type=d["record_type"],
                        term=d["term"],
                        definition=d["definition"],
                        provenance_id=d["provenance_id"],
                        scope=d["scope"],
                    )

        # Load Boundaries
        bound_file = path / "boundaries.jsonl"
        boundaries_map: Dict[str, BoundaryRecord] = {}
        if bound_file.exists():
            with open(bound_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    boundaries_map[d["id"]] = BoundaryRecord(
                        id=d["id"],
                        record_type=d["record_type"],
                        statement=d["statement"],
                        provenance_id=d["provenance_id"],
                        scope=d["scope"],
                    )

        # Load Relationships
        rel_file = path / "relationships.jsonl"
        relationships_list: List[RelationshipRecord] = []
        if rel_file.exists():
            with open(rel_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    d = json.loads(line)
                    relationships_list.append(
                        RelationshipRecord(
                            id=d["id"],
                            record_type=d["record_type"],
                            subject_id=d["subject_id"],
                            predicate=d["predicate"],
                            object_id=d["object_id"],
                            provenance_id=d["provenance_id"],
                            scope=d["scope"],
                        )
                    )

        return cls(
            package_path=path,
            manifest=manifest,
            meaning_units=units_map,
            definitions=definitions_map,
            boundaries=boundaries_map,
            relationships=relationships_list,
            provenance_records=provenance_map,
        )

    def units(self) -> List[MeaningUnit]:
        """Returns all meaning units."""
        return list(self._units.values())

    def get_unit(self, unit_id: str) -> MeaningUnit:
        """Retrieves a meaning unit by exact ID."""
        if unit_id not in self._units:
            raise RecordNotFoundError(f"Meaning unit not found: {unit_id}")
        return self._units[unit_id]

    def find_units(
        self,
        resolution_level: Optional[str] = None,
        scope: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[MeaningUnit]:
        """Deterministic filtering over meaning unit fields."""
        results = list(self._units.values())
        if resolution_level:
            results = [u for u in results if u.resolution_level == resolution_level]
        if scope:
            results = [u for u in results if u.scope.lower() == scope.lower()]
        if query:
            q = query.lower()
            results = [u for u in results if q in u.claim.lower() or q in u.title.lower()]
        return results

    def definitions(self) -> List[DefinitionRecord]:
        """Returns all domain definitions."""
        return list(self._definitions.values())

    def get_definition(self, def_id: str) -> DefinitionRecord:
        """Retrieves a definition by exact ID."""
        if def_id not in self._definitions:
            raise RecordNotFoundError(f"Definition not found: {def_id}")
        return self._definitions[def_id]

    def find_definitions(self, term: Optional[str] = None) -> List[DefinitionRecord]:
        """Finds definitions matching term."""
        if not term:
            return self.definitions()
        t = term.lower()
        return [d for d in self._definitions.values() if t in d.term.lower()]

    def boundaries(self) -> List[BoundaryRecord]:
        """Returns all scope boundaries."""
        return list(self._boundaries.values())

    def relationships(self, predicate: Optional[str] = None) -> List[RelationshipRecord]:
        """Returns all relationships, optionally filtered by predicate."""
        if not predicate:
            return list(self._relationships)
        return [r for r in self._relationships if r.predicate == predicate]

    def related(
        self,
        unit_id: str,
        direction: str = "both",
        predicate: Optional[str] = None,
    ) -> List[RelationshipRecord]:
        """Traverses relationships connecting to unit_id ('outgoing', 'incoming', or 'both')."""
        results = []
        for r in self._relationships:
            if predicate and r.predicate != predicate:
                continue
            if direction in ("outgoing", "both") and r.subject_id == unit_id:
                results.append(r)
            elif direction in ("incoming", "both") and r.object_id == unit_id:
                results.append(r)
        return results

    def provenance_records(self) -> List[ProvenanceRecord]:
        """Returns all provenance records."""
        return list(self._provenance.values())

    def provenance(self, unit_or_id: str | MeaningUnit | DefinitionRecord | BoundaryRecord | RelationshipRecord) -> ProvenanceRecord:
        """Resolves the authoritative source provenance record for a unit or ID."""
        if isinstance(unit_or_id, (MeaningUnit, DefinitionRecord, BoundaryRecord, RelationshipRecord)):
            prov_id = unit_or_id.provenance_id
        elif unit_or_id in self._units:
            prov_id = self._units[unit_or_id].provenance_id
        elif unit_or_id in self._definitions:
            prov_id = self._definitions[unit_or_id].provenance_id
        elif unit_or_id in self._boundaries:
            prov_id = self._boundaries[unit_or_id].provenance_id
        elif unit_or_id in self._provenance:
            return self._provenance[unit_or_id]
        else:
            # Check if any relationship has this ID
            rel = next((r for r in self._relationships if r.id == unit_or_id), None)
            if rel:
                prov_id = rel.provenance_id
            else:
                raise RecordNotFoundError(f"Record with ID '{unit_or_id}' not found")

        if prov_id not in self._provenance:
            raise ProvenanceResolutionError(f"Provenance ID '{prov_id}' could not be resolved")
        return self._provenance[prov_id]

    def capabilities(self) -> Dict[str, Any]:
        """Returns explicitly declared format and resolution capabilities."""
        return {
            "formats": self.manifest.get("formats", []),
            "resolution_levels": self.manifest.get("resolution_levels", []),
        }

    def inspect(self) -> Dict[str, Any]:
        """Returns a deterministic structured summary of the package."""
        return {
            "package_id": self.manifest.get("package_id", ""),
            "title": self.manifest.get("title", ""),
            "version": self.manifest.get("version", ""),
            "status": self.manifest.get("status", ""),
            "scope": self.manifest.get("scope", ""),
            "formats": self.manifest.get("formats", []),
            "resolution_levels": self.manifest.get("resolution_levels", []),
            "license": self.manifest.get("license", ""),
            "human_readable_entrypoint": self.manifest.get("human_readable_entrypoint", ""),
            "provenance_file": self.manifest.get("provenance_file", ""),
            "record_counts": {
                "meaning_units": len(self._units),
                "definitions": len(self._definitions),
                "boundaries": len(self._boundaries),
                "relationships": len(self._relationships),
                "provenance": len(self._provenance),
            },
        }


class MachineEditionParser:
    """Backward-compatible parser wrapper around MachineEdition entity loader."""

    def __init__(self, package_path: Path):
        self.package_path = package_path
        self._edition = MachineEdition.load(package_path, validate=False)

    def iter_meaning_units(self) -> Iterator[MeaningUnit]:
        return iter(self._edition.units())

    def load_provenance(self) -> Dict[str, ProvenanceRecord]:
        return dict(self._edition._provenance)
