"""Machine Edition Developer Kit (v0.1)

Reference implementation architecture for the Machine Edition Specification v0.1.
Responsibilities: inspect, validate, parse, query, compare.
"""

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
from machine_edition_devkit.validate import MachineEditionValidator, ValidationReport
from machine_edition_devkit.inspect import inspect_package, PackageSummary
from machine_edition_devkit.comparison import ComparisonHarness, TaskEvaluationResult
from machine_edition_devkit.compare import RepresentationComparator, RepresentationMetrics

__version__ = "0.1.0"
__spec_version__ = "0.1.0"

__all__ = [
    "MachineEdition",
    "MeaningUnit",
    "DefinitionRecord",
    "BoundaryRecord",
    "RelationshipRecord",
    "ProvenanceRecord",
    "MachineEditionValidator",
    "ValidationReport",
    "inspect_package",
    "PackageSummary",
    "ComparisonHarness",
    "TaskEvaluationResult",
    "RepresentationComparator",
    "RepresentationMetrics",
    "MachineEditionError",
    "MachineEditionValidationError",
    "RecordNotFoundError",
    "ProvenanceResolutionError",
]
