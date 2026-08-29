"""Representation adapters for the ME-BENCH-001 evaluation benchmark."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import json
import zipfile
import re
from typing import List, Dict, Any, Optional
from xml.etree import ElementTree as ET

from machine_edition_devkit.parse import MachineEdition


@dataclass(frozen=True)
class BenchmarkSearchMatch:
    location: str
    matched_text: str
    context: str
    metadata: Dict[str, Any]


class BaseBenchmarkAdapter(ABC):
    @abstractmethod
    def representation_name(self) -> str:
        pass

    @abstractmethod
    def get_full_text(self) -> str:
        pass

    @abstractmethod
    def search_text(self, query: str) -> List[BenchmarkSearchMatch]:
        pass


class BenchmarkPDFAdapter(BaseBenchmarkAdapter):
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self._cached_text = self._extract_text()

    def representation_name(self) -> str:
        return "PDF"

    def _extract_text(self) -> str:
        if not self.pdf_path.exists():
            return ""
        content = self.pdf_path.read_bytes().decode("latin-1", errors="ignore")
        matches = re.findall(r"\((.*?)\)\s*Tj", content)
        cleaned = [m.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\") for m in matches]
        return "\n".join(cleaned)

    def get_full_text(self) -> str:
        return self._cached_text

    def search_text(self, query: str) -> List[BenchmarkSearchMatch]:
        results = []
        q = query.lower()
        lines = self._cached_text.splitlines()
        for idx, line in enumerate(lines):
            if q in line.lower():
                results.append(
                    BenchmarkSearchMatch(
                        location=f"PDF Line {idx + 1}",
                        matched_text=line,
                        context=line,
                        metadata={"format": "PDF", "line": idx + 1},
                    )
                )
        return results


class BenchmarkEPUBAdapter(BaseBenchmarkAdapter):
    def __init__(self, epub_path: Path):
        self.epub_path = epub_path
        self._sections: Dict[str, str] = {}
        self._load_epub()

    def representation_name(self) -> str:
        return "EPUB"

    def _load_epub(self):
        if not self.epub_path.exists():
            return
        with zipfile.ZipFile(self.epub_path, "r") as z:
            for name in z.namelist():
                if name.endswith(".xhtml") or name.endswith(".html"):
                    raw = z.read(name).decode("utf-8")
                    try:
                        root = ET.fromstring(raw)
                        text = "".join(root.itertext())
                        self._sections[name] = text
                    except Exception:
                        text = re.sub(r"<[^>]+>", "", raw)
                        self._sections[name] = text

    def get_full_text(self) -> str:
        return "\n".join(self._sections.values())

    def search_text(self, query: str) -> List[BenchmarkSearchMatch]:
        results = []
        q = query.lower()
        for sec_name, text in self._sections.items():
            for line_no, line in enumerate(text.splitlines(), start=1):
                if q in line.lower():
                    results.append(
                        BenchmarkSearchMatch(
                            location=f"EPUB Section: {sec_name}:{line_no}",
                            matched_text=line.strip(),
                            context=line.strip(),
                            metadata={"format": "EPUB", "section": sec_name, "line": line_no},
                        )
                    )
        return results


class BenchmarkNaiveRAGAdapter(BaseBenchmarkAdapter):
    def __init__(self, rag_json_path: Path):
        self.rag_json_path = rag_json_path
        self.config: Dict[str, Any] = {}
        self.chunks: List[Dict[str, Any]] = []
        self._load_rag()

    def representation_name(self) -> str:
        return "Naive_RAG"

    def _load_rag(self):
        if not self.rag_json_path.exists():
            return
        data = json.loads(self.rag_json_path.read_text(encoding="utf-8"))
        self.config = data
        self.chunks = data.get("chunks", [])

    def get_full_text(self) -> str:
        return "\n".join(c["text"] for c in self.chunks)

    def search_text(self, query: str) -> List[BenchmarkSearchMatch]:
        q_terms = set(re.findall(r"\w+", query.lower()))
        scored_chunks = []
        for c in self.chunks:
            chunk_terms = re.findall(r"\w+", c["text"].lower())
            overlap = sum(1 for t in chunk_terms if t in q_terms)
            if overlap > 0:
                scored_chunks.append((overlap, c))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, c in scored_chunks:
            results.append(
                BenchmarkSearchMatch(
                    location=f"RAG {c['chunk_id']} (pos {c['position']})",
                    matched_text=c["text"],
                    context=c["text"],
                    metadata={
                        "format": "Naive_RAG",
                        "chunk_id": c["chunk_id"],
                        "score": score,
                        "position": c["position"],
                    },
                )
            )
        return results


class BenchmarkMachineEditionAdapter(BaseBenchmarkAdapter):
    def __init__(self, package_path: Path):
        self.package_path = package_path
        self.edition = MachineEdition.load(package_path, validate=True)

    def representation_name(self) -> str:
        return "Machine_Edition"

    def get_full_text(self) -> str:
        claims = [u.claim for u in self.edition.units()]
        defs = [d.definition for d in self.edition.definitions()]
        bounds = [b.statement for b in self.edition.boundaries()]
        return "\n".join(claims + defs + bounds)

    def search_text(self, query: str) -> List[BenchmarkSearchMatch]:
        results = []
        q = query.lower()
        for u in self.edition.units():
            if q in u.claim.lower() or q in u.title.lower():
                results.append(
                    BenchmarkSearchMatch(
                        location=f"MeaningUnit {u.id} [L{u.resolution_level}]",
                        matched_text=u.claim,
                        context=f"Title: {u.title} | Claim: {u.claim}",
                        metadata={
                            "format": "Machine_Edition",
                            "record_type": "meaning_unit",
                            "id": u.id,
                            "resolution_level": u.resolution_level,
                            "provenance_id": u.provenance_id,
                        },
                    )
                )
        for d in self.edition.definitions():
            if q in d.term.lower() or q in d.definition.lower():
                results.append(
                    BenchmarkSearchMatch(
                        location=f"Definition {d.id} ({d.term})",
                        matched_text=d.definition,
                        context=f"Term: {d.term} = {d.definition}",
                        metadata={"format": "Machine_Edition", "record_type": "definition", "id": d.id},
                    )
                )
        for b in self.edition.boundaries():
            if q in b.statement.lower():
                results.append(
                    BenchmarkSearchMatch(
                        location=f"Boundary {b.id}",
                        matched_text=b.statement,
                        context=b.statement,
                        metadata={"format": "Machine_Edition", "record_type": "boundary", "id": b.id},
                    )
                )
        return results
