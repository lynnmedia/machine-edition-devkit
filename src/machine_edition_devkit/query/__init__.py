"""Query interface for filtering and traversing Machine Edition graphs and resolution levels."""

from typing import List, Optional, Dict
from machine_edition_devkit.parse import MachineEditionParser, MeaningUnit, ProvenanceRecord


class MachineEditionQueryEngine:
    """Executes structured queries across resolution levels and provenance graphs."""

    def __init__(self, parser: MachineEditionParser):
        self.parser = parser
        self._meaning_units = list(parser.iter_meaning_units())
        self._provenance_map = parser.load_provenance()

    def filter_by_resolution(self, level: str) -> List[MeaningUnit]:
        """Returns all meaning units matching the specified resolution tier (L0-L4)."""
        return [mu for mu in self._meaning_units if mu.resolution_level == level]

    def search_claims(self, keyword: str) -> List[MeaningUnit]:
        """Searches claims and titles for a substring match."""
        kw = keyword.lower()
        return [mu for mu in self._meaning_units if kw in mu.claim.lower() or kw in mu.title.lower()]

    def trace_provenance(self, meaning_unit_id: str) -> Optional[ProvenanceRecord]:
        """Resolves the provenance record for a given meaning unit."""
        for mu in self._meaning_units:
            if mu.id == meaning_unit_id:
                return self._provenance_map.get(mu.provenance_id)
        return None
