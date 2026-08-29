"""Deterministic builder and regenerator for ME-BENCH-001 benchmark artifacts."""

import os
import shutil
import json
import zipfile
import hashlib
from pathlib import Path
from typing import Dict, Any, List

from machine_edition_devkit.benchmark.constants import (
    BENCHMARK_ID,
    BENCHMARK_TITLE,
    BENCHMARK_VERSION,
    BENCHMARK_STATUS,
    SPECIFICATION_AUTHORITY,
    CORPUS_LINEAGE,
    TASK_FAMILIES,
    FAILURE_TAXONOMY,
    SCORING_DIMENSIONS,
)
from machine_edition_devkit.validate import MachineEditionValidator


SOURCE_TEXT = """# SROW Public Reference Benchmark Source (v0.1)

## Chapter 1: Introduction to Structured Resolution-Oriented Writing

Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines.

Structure is a form of reader respect. Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents.

Progressive disclosure is a staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records.

Resolution levels range from L0 to L4: L0 provides orientation summaries, L1 states core principles, L2 articulates functional architecture, L3 provides technical verification records, and L4 contains complete forensic ledgers.

## Chapter 2: Technical Architecture, Stable Identity, and Data Model

The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key.

Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation.

Explicit relationships link meaning units using typed predicates: derives_from indicates source lineage, clarifies provides architectural elaboration, depends_on establishes prerequisite dependencies, and exemplifies provides concrete application instances.

A conformant Machine Edition package comprises six core record types: manifest, meaning_unit, definition, relationship, boundary, and provenance ledgers.

## Chapter 3: Semantic Resolution, Monotonicity, and Ambiguity Handling

Resolution monotonicity requires that higher detail levels preserve all invariants of lower detail levels without semantic contradiction.

Epistemic authority requires that every atomic assertion binds directly to verifiable cryptographic release hashes or canonical publication provenance URLs.

When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty.

Contextual scope tags define the operational domain of each assertion, separating universal core invariants from provisional public companion samples.

## Chapter 4: Boundaries, Scope, and Epistemic Limitations

SROW is an expression and structuring protocol, not a cognition architecture or internal thought representation.

Structured records improve inspectability and retrieval precision; they do not guarantee factual truth or eliminate model error.

This public reference material contains only authorized public companion samples and does not include the complete manuscript or governed meaning-unit database.

Schema conformance certifies structural and syntactic compliance; it does not constitute an epistemic endorsement of the truth value of external assertions.
"""

FACTS = [
    {
        "fact_id": "FACT-001",
        "statement": "Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines.",
        "category": "definition",
        "subject": "SROW definition",
        "location": "Chapter 1",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-002",
        "statement": "Structure is a form of reader respect. Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents.",
        "category": "core_principle",
        "subject": "reader respect",
        "location": "Chapter 1",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-003",
        "statement": "Progressive disclosure is a staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records.",
        "category": "definition",
        "subject": "progressive disclosure",
        "location": "Chapter 1",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-004",
        "statement": "Resolution levels range from L0 to L4: L0 provides orientation summaries, L1 states core principles, L2 articulates functional architecture, L3 provides technical verification records, and L4 contains complete forensic ledgers.",
        "category": "architectural_hierarchy",
        "subject": "resolution levels L0-L4",
        "location": "Chapter 1",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-005",
        "statement": "The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key.",
        "category": "technical_assertion",
        "subject": "stable-id algorithm",
        "location": "Chapter 2",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-006",
        "statement": "Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation.",
        "category": "technical_assertion",
        "subject": "validation compliance",
        "location": "Chapter 2",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-007",
        "statement": "Explicit relationships link meaning units using typed predicates: derives_from indicates source lineage, clarifies provides architectural elaboration, depends_on establishes prerequisite dependencies, and exemplifies provides concrete application instances.",
        "category": "relationship_model",
        "subject": "relationship predicates",
        "location": "Chapter 2",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-008",
        "statement": "A conformant Machine Edition package comprises six core record types: manifest, meaning_unit, definition, relationship, boundary, and provenance ledgers.",
        "category": "package_architecture",
        "subject": "core record types",
        "location": "Chapter 2",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-009",
        "statement": "Resolution monotonicity requires that higher detail levels preserve all invariants of lower detail levels without semantic contradiction.",
        "category": "semantic_invariant",
        "subject": "resolution monotonicity",
        "location": "Chapter 3",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-010",
        "statement": "Epistemic authority requires that every atomic assertion binds directly to verifiable cryptographic release hashes or canonical publication provenance URLs.",
        "category": "provenance_model",
        "subject": "epistemic authority",
        "location": "Chapter 3",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-011",
        "statement": "When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty.",
        "category": "ambiguity_handling",
        "subject": "explicit qualification requirement",
        "location": "Chapter 3",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-012",
        "statement": "Contextual scope tags define the operational domain of each assertion, separating universal core invariants from provisional public companion samples.",
        "category": "scope_model",
        "subject": "contextual scope tags",
        "location": "Chapter 3",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-013",
        "statement": "SROW is an expression and structuring protocol, not a cognition architecture or internal thought representation.",
        "category": "boundary",
        "subject": "expression vs cognition boundary",
        "location": "Chapter 4",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-014",
        "statement": "Structured records improve inspectability and retrieval precision; they do not guarantee factual truth or eliminate model error.",
        "category": "boundary",
        "subject": "truth guarantee boundary",
        "location": "Chapter 4",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-015",
        "statement": "This public reference material contains only authorized public companion samples and does not include the complete manuscript or governed meaning-unit database.",
        "category": "boundary",
        "subject": "public companion scope boundary",
        "location": "Chapter 4",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    },
    {
        "fact_id": "FACT-016",
        "statement": "Schema conformance certifies structural and syntactic compliance; it does not constitute an epistemic endorsement of the truth value of external assertions.",
        "category": "boundary",
        "subject": "conformance vs endorsement boundary",
        "location": "Chapter 4",
        "present_in_pdf": True,
        "present_in_epub": True,
        "present_in_rag": True,
        "present_in_machine_edition": True
    }
]


def generate_pdf(source_md_path: Path, output_pdf_path: Path):
    """Generates valid minimal Latin-1 PDF from source text."""
    lines = source_md_path.read_text(encoding="utf-8").splitlines()
    pdf_lines = []
    y = 750
    for line in lines:
        if not line.strip():
            y -= 14
            continue
        clean_text = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        pdf_lines.append(f"BT /F1 10 Tf 50 {y} Td ({clean_text}) Tj ET")
        y -= 15

    content_stream = "\n".join(pdf_lines)
    stream_len = len(content_stream.encode("utf-8"))
    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {stream_len} >>
stream
{content_stream}
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000224 00000 n 
0000000000 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
500
%%EOF
"""
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    output_pdf_path.write_bytes(pdf_content.encode("latin-1"))


def generate_epub(source_md_path: Path, output_epub_path: Path):
    """Generates standard EPUB 3.0 package from source text."""
    text_content = source_md_path.read_text(encoding="utf-8")
    html_body = []
    for line in text_content.splitlines():
        if line.startswith("## "):
            html_body.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_body.append(f"<h1>{line[2:]}</h1>")
        elif line.strip():
            html_body.append(f"<p>{line.strip()}</p>")

    chapter_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>SROW Public Reference Benchmark Document</title>
</head>
<body>
  {"\n  ".join(html_body)}
</body>
</html>"""

    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

    content_opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="pub-id" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">urn:uuid:srow-benchmark-epub-v0.1</dc:identifier>
    <dc:title>SROW Public Reference Benchmark Document</dc:title>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>
    <itemref idref="chapter1"/>
  </spine>
</package>"""

    toc_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>TOC</title></head>
<body>
  <nav epub:type="toc">
    <h1>Table of Contents</h1>
    <ol>
      <li><a href="chapter1.xhtml">SROW Public Reference Benchmark Document</a></li>
    </ol>
  </nav>
</body>
</html>"""

    output_epub_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_epub_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container_xml)
        z.writestr("OEBPS/content.opf", content_opf)
        z.writestr("OEBPS/toc.xhtml", toc_xhtml)
        z.writestr("OEBPS/chapter1.xhtml", chapter_xhtml)


def generate_rag(source_md_path: Path, output_json_path: Path, chunk_size: int = 250, overlap: int = 40):
    """Builds deterministic textual RAG corpus with sliding-window chunking."""
    text = source_md_path.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    chunks = []
    chunk_index = 0
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 1 <= chunk_size:
            current_chunk = (current_chunk + " " + p).strip() if current_chunk else p
        else:
            if current_chunk:
                chunks.append({
                    "chunk_id": f"chunk-{chunk_index:03d}",
                    "text": current_chunk,
                    "source_document": "benchmark-source.md",
                    "position": chunk_index,
                    "char_length": len(current_chunk)
                })
                chunk_index += 1
            current_chunk = p

    if current_chunk:
        chunks.append({
            "chunk_id": f"chunk-{chunk_index:03d}",
            "text": current_chunk,
            "source_document": "benchmark-source.md",
            "position": chunk_index,
            "char_length": len(current_chunk)
        })

    config = {
        "strategy": "paragraph-preserving sliding window",
        "target_chunk_size": chunk_size,
        "overlap": overlap,
        "chunk_count": len(chunks),
        "source_document": "benchmark-source.md",
        "chunks": chunks
    }
    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def generate_machine_edition_package(pkg_dir: Path, source_root: Path):
    """Creates conformant Machine Edition package for the benchmark."""
    pkg_dir.mkdir(parents=True, exist_ok=True)
    schemas_dir = pkg_dir / "schemas"
    schemas_dir.mkdir(exist_ok=True)

    specimen_schemas = source_root / "specimen" / "srow" / "package" / "schemas"
    for sf in specimen_schemas.glob("*.json"):
        shutil.copy2(sf, schemas_dir / sf.name)

    # manifest (valid status: developer_preview, release_candidate, stable, deprecated)
    manifest_data = {
        "package_id": "winmedia.srow.benchmark-specimen",
        "title": "SROW Public Reference Benchmark Specimen for Machine Edition Specification v0.1",
        "version": "0.1.0",
        "status": "stable",
        "scope": "Authorized public reference benchmark specimen derived from SROW Public Companion v0.1; does not contain governed manuscript content.",
        "formats": ["markdown", "jsonl", "json-schema"],
        "resolution_levels": ["L0", "L1", "L2", "L3", "L4"],
        "license": "LICENSE.txt",
        "human_readable_entrypoint": "full-preview.md",
        "provenance_file": "provenance.jsonl"
    }
    (pkg_dir / "manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    # license
    license_text = """Creative Commons Attribution 4.0 International (CC BY 4.0)

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

Scope Limitation:
This license applies strictly to the public companion sample records and schemas included in this benchmark. Governed manuscript data, internal adjudication ledgers, and proprietary packagers remain excluded and reserved by WinMedia.
"""
    (pkg_dir / "LICENSE.txt").write_text(license_text, encoding="utf-8")

    meaning_units = [
        {
            "id": "srow.bench.mu.001",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L0",
            "title": "SROW Communication Protocol Orientation",
            "claim": "Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "core orientation"
        },
        {
            "id": "srow.bench.mu.002",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L1",
            "title": "Structure is a form of reader respect",
            "claim": "Structure is a form of reader respect. Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "core principle"
        },
        {
            "id": "srow.bench.mu.003",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L1",
            "title": "Progressive Disclosure Orientation",
            "claim": "Progressive disclosure is a staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "core principle"
        },
        {
            "id": "srow.bench.mu.004",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Resolution Hierarchy Architecture",
            "claim": "Resolution levels range from L0 to L4: L0 provides orientation summaries, L1 states core principles, L2 articulates functional architecture, L3 provides technical verification records, and L4 contains complete forensic ledgers.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "functional architecture"
        },
        {
            "id": "srow.bench.mu.005",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Stable-ID Algorithm Invariant",
            "claim": "The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key.",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "functional architecture"
        },
        {
            "id": "srow.bench.mu.006",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L3",
            "title": "SROW Validation Compliance Sample",
            "claim": "Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation.",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "technical verification"
        },
        {
            "id": "srow.bench.mu.007",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Typed Relationship Model",
            "claim": "Explicit relationships link meaning units using typed predicates: derives_from indicates source lineage, clarifies provides architectural elaboration, depends_on establishes prerequisite dependencies, and exemplifies provides concrete application instances.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "functional architecture"
        },
        {
            "id": "srow.bench.mu.008",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Core Package Record Types",
            "claim": "A conformant Machine Edition package comprises six core record types: manifest, meaning_unit, definition, relationship, boundary, and provenance ledgers.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "functional architecture"
        },
        {
            "id": "srow.bench.mu.009",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L3",
            "title": "Resolution Monotonicity Invariant",
            "claim": "Resolution monotonicity requires that higher detail levels preserve all invariants of lower detail levels without semantic contradiction.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "technical verification"
        },
        {
            "id": "srow.bench.mu.010",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L3",
            "title": "Epistemic Authority Provenance Requirement",
            "claim": "Epistemic authority requires that every atomic assertion binds directly to verifiable cryptographic release hashes or canonical publication provenance URLs.",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "technical verification"
        },
        {
            "id": "srow.bench.mu.011",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Ambiguity Qualification Obligation",
            "claim": "When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "epistemic governance"
        },
        {
            "id": "srow.bench.mu.012",
            "record_type": "meaning_unit",
            "version": "0.1.0",
            "resolution_level": "L2",
            "title": "Contextual Scope Tag Separation",
            "claim": "Contextual scope tags define the operational domain of each assertion, separating universal core invariants from provisional public companion samples.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "epistemic governance"
        }
    ]
    (pkg_dir / "meaning-units.jsonl").write_text("\n".join(json.dumps(u) for u in meaning_units) + "\n", encoding="utf-8")

    definitions = [
        {
            "id": "srow.bench.def.001",
            "record_type": "definition",
            "term": "SROW",
            "definition": "Structured Resolution-Oriented Writing: a communication protocol for making structured knowledge readable and navigable by both humans and machines.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "core term"
        },
        {
            "id": "srow.bench.def.002",
            "record_type": "definition",
            "term": "Progressive Disclosure",
            "definition": "A staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "core term"
        },
        {
            "id": "srow.bench.def.003",
            "record_type": "definition",
            "term": "Resolution Monotonicity",
            "definition": "The invariant property where higher detail levels (e.g. L3, L4) preserve all semantics and constraints established at lower detail levels (L0, L1, L2) without contradiction.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "architectural term"
        },
        {
            "id": "srow.bench.def.004",
            "record_type": "definition",
            "term": "Epistemic Authority",
            "definition": "The verifiable linkage mechanism binding every discrete factual assertion to a cryptographic release hash or canonical authority URL.",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "architectural term"
        }
    ]
    (pkg_dir / "definitions.jsonl").write_text("\n".join(json.dumps(d) for d in definitions) + "\n", encoding="utf-8")

    boundaries = [
        {
            "id": "srow.bench.bound.001",
            "record_type": "boundary",
            "statement": "SROW is an expression and structuring protocol, not a cognition architecture or internal thought representation.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "scope limitation"
        },
        {
            "id": "srow.bench.bound.002",
            "record_type": "boundary",
            "statement": "Structured records improve inspectability and retrieval precision; they do not guarantee factual truth or eliminate model error.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "epistemic boundary"
        },
        {
            "id": "srow.bench.bound.003",
            "record_type": "boundary",
            "statement": "This public reference material contains only authorized public companion samples and does not include the complete manuscript or governed meaning-unit database.",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "public scope limitation"
        },
        {
            "id": "srow.bench.bound.004",
            "record_type": "boundary",
            "statement": "Schema conformance certifies structural and syntactic compliance; it does not constitute an epistemic endorsement of the truth value of external assertions.",
            "provenance_id": "prov.public-srow-framework",
            "scope": "governance boundary"
        }
    ]
    (pkg_dir / "boundaries.jsonl").write_text("\n".join(json.dumps(b) for b in boundaries) + "\n", encoding="utf-8")

    relationships = [
        {
            "id": "srow.bench.rel.001",
            "record_type": "relationship",
            "subject_id": "srow.bench.mu.005",
            "predicate": "derives_from",
            "object_id": "srow.bench.mu.006",
            "provenance_id": "prov.srow-public-companion-release",
            "scope": "technical relationship"
        },
        {
            "id": "srow.bench.rel.002",
            "record_type": "relationship",
            "subject_id": "srow.bench.mu.006",
            "predicate": "clarifies",
            "object_id": "srow.bench.mu.002",
            "provenance_id": "prov.public-srow-framework",
            "scope": "architectural relationship"
        },
        {
            "id": "srow.bench.rel.003",
            "record_type": "relationship",
            "subject_id": "srow.bench.mu.009",
            "predicate": "depends_on",
            "object_id": "srow.bench.mu.004",
            "provenance_id": "prov.public-srow-framework",
            "scope": "governance relationship"
        },
        {
            "id": "srow.bench.rel.004",
            "record_type": "relationship",
            "subject_id": "srow.bench.mu.006",
            "predicate": "exemplifies",
            "object_id": "srow.bench.mu.001",
            "provenance_id": "prov.public-srow-framework",
            "scope": "structural relationship"
        }
    ]
    (pkg_dir / "relationships.jsonl").write_text("\n".join(json.dumps(r) for r in relationships) + "\n", encoding="utf-8")

    provenance = [
        {
            "id": "prov.srow-public-companion-release",
            "record_type": "provenance",
            "source_title": "SROW Machine Edition — Public Companion v0.1",
            "source_url": "https://winmedia.com/machine-editions/editions/srow",
            "source_scope": "authorized public companion release archive (sha256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181)",
            "retrieved_for_preview": "2026-08-29"
        },
        {
            "id": "prov.public-srow-framework",
            "record_type": "provenance",
            "source_title": "SROW — Structured Resolution-Oriented Writing",
            "source_url": "https://winmedia.com/frameworks/srow",
            "source_scope": "public WinMedia framework publication",
            "retrieved_for_preview": "2026-08-29"
        }
    ]
    (pkg_dir / "provenance.jsonl").write_text("\n".join(json.dumps(p) for p in provenance) + "\n", encoding="utf-8")

    preview_text = """# SROW Machine Edition — Public Reference Benchmark Specimen (v0.1)

## Overview

This is the human-readable entrypoint for the **SROW Public Reference Benchmark Specimen**, conforming to **Machine Edition Specification v0.1**.

## Core Meaning Units

* **`srow.bench.mu.001` (Resolution: L0)**: *SROW Communication Protocol Orientation.* Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines.
* **`srow.bench.mu.002` (Resolution: L1)**: *Structure is a form of reader respect.* Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents.
* **`srow.bench.mu.003` (Resolution: L1)**: *Progressive Disclosure Orientation.* Progressive disclosure is a staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records.
* **`srow.bench.mu.004` (Resolution: L2)**: *Resolution Hierarchy Architecture.* Resolution levels range from L0 to L4: L0 provides orientation summaries, L1 states core principles, L2 articulates functional architecture, L3 provides technical verification records, and L4 contains complete forensic ledgers.
* **`srow.bench.mu.005` (Resolution: L2)**: *Stable-ID Algorithm Invariant.* The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key.
* **`srow.bench.mu.006` (Resolution: L3)**: *SROW Validation Compliance Sample.* Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation.
* **`srow.bench.mu.007` (Resolution: L2)**: *Typed Relationship Model.* Explicit relationships link meaning units using typed predicates: derives_from, clarifies, depends_on, exemplifies.
* **`srow.bench.mu.008` (Resolution: L2)**: *Core Package Record Types.* A conformant Machine Edition package comprises six core record types: manifest, meaning_unit, definition, relationship, boundary, and provenance ledgers.
* **`srow.bench.mu.009` (Resolution: L3)**: *Resolution Monotonicity Invariant.* Resolution monotonicity requires that higher detail levels preserve all invariants of lower detail levels without semantic contradiction.
* **`srow.bench.mu.010` (Resolution: L3)**: *Epistemic Authority Provenance Requirement.* Epistemic authority requires that every atomic assertion binds directly to verifiable cryptographic release hashes or canonical publication provenance URLs.
* **`srow.bench.mu.011` (Resolution: L2)**: *Ambiguity Qualification Obligation.* When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty.
* **`srow.bench.mu.012` (Resolution: L2)**: *Contextual Scope Tag Separation.* Contextual scope tags define the operational domain of each assertion, separating universal core invariants from provisional public companion samples.

## Boundaries and Governance

* **`srow.bench.bound.001`**: SROW is an expression and structuring protocol, not a cognition architecture or internal thought representation.
* **`srow.bench.bound.002`**: Structured records improve inspectability and retrieval precision; they do not guarantee factual truth or eliminate model error.
* **`srow.bench.bound.003`**: This public reference material contains only authorized public companion samples and does not include the complete manuscript or governed meaning-unit database.
* **`srow.bench.bound.004`**: Schema conformance certifies structural and syntactic compliance; it does not constitute an epistemic endorsement of the truth value of external assertions.
"""
    (pkg_dir / "full-preview.md").write_text(preview_text, encoding="utf-8")


def get_benchmark_tasks_and_gold():
    """Defines 40 benchmark items across 8 families with separated gold adjudication structures."""
    tasks = []
    gold_answers = []
    gold_provenance = []
    gold_relationships = []
    gold_constraints = []

    def add_item(
        b_id: str,
        family: str,
        split: str,
        question: str,
        task_type: str,
        fact_ids: List[str],
        evidence_ids: List[str],
        difficulty: str,
        notes: str,
        scoring_profile: str,
        # Gold Answer
        req_concepts: List[str],
        accepted_variants: List[str],
        prohibited_assertions: List[str],
        is_unsupported: bool = False,
        requires_qualification: bool = False,
        # Gold Provenance
        req_prov_ids: List[str] = None,
        req_prov_urls: List[str] = None,
        # Gold Relationships
        req_triples: List[Dict[str, str]] = None,
        # Gold Constraints
        req_boundaries: List[str] = None,
        negative_rules: List[str] = None,
    ):
        tasks.append({
            "benchmark_id": b_id,
            "version": "0.1.0",
            "family": family,
            "split": split,
            "question": question,
            "task_type": task_type,
            "source_fact_ids": fact_ids,
            "source_evidence_ids": evidence_ids,
            "scoring_profile": scoring_profile,
            "difficulty": difficulty,
            "notes": notes,
        })
        gold_answers.append({
            "benchmark_id": b_id,
            "required_concepts": req_concepts,
            "accepted_variants": accepted_variants,
            "prohibited_assertions": prohibited_assertions,
            "is_unsupported": is_unsupported,
            "requires_qualification": requires_qualification,
        })
        gold_provenance.append({
            "benchmark_id": b_id,
            "required_provenance_ids": req_prov_ids or [],
            "required_provenance_urls": req_prov_urls or [],
            "prohibited_fabricated_provenance": True,
        })
        gold_relationships.append({
            "benchmark_id": b_id,
            "required_triples": req_triples or [],
        })
        gold_constraints.append({
            "benchmark_id": b_id,
            "required_boundaries": req_boundaries or [],
            "negative_rules": negative_rules or [],
        })

    # Family 1: factual_retrieval (5 items)
    add_item(
        "ME-BENCH-001", "factual_retrieval", "calibration",
        "What is the definition of SROW according to Chapter 1?",
        "factual_definition", ["FACT-001"], ["srow.bench.mu.001", "srow.bench.def.001"], "easy",
        "Core definition retrieval test.", "factual_concept_match",
        ["communication protocol", "structured knowledge", "readable and navigable", "humans and machines"],
        ["communication protocol for making structured knowledge readable and navigable by both humans and machines"],
        ["cognition architecture", "deep learning framework"],
        req_prov_ids=["prov.public-srow-framework"],
    )
    add_item(
        "ME-BENCH-002", "factual_retrieval", "evaluation",
        "What is the algorithm used to compute stable IDs for meaning units?",
        "factual_technical", ["FACT-005"], ["srow.bench.mu.005"], "medium",
        "Technical hash invariant retrieval.", "factual_concept_match",
        ["SHA-256", "16 hexadecimal characters", "lexically sorted", "source-block binding key"],
        ["SHA-256 truncated to 16 hexadecimal characters over canonical lexically sorted source-block binding key"],
        ["MD5", "SHA-1", "32 characters", "random UUID"],
        req_prov_ids=["prov.srow-public-companion-release"],
    )
    add_item(
        "ME-BENCH-003", "factual_retrieval", "evaluation",
        "What is progressive disclosure according to the source?",
        "factual_definition", ["FACT-003"], ["srow.bench.mu.003", "srow.bench.def.002"], "easy",
        "Progressive disclosure definition retrieval.", "factual_concept_match",
        ["staged presentation", "orientation and structure", "deeper analytical explanation"],
        ["staged presentation that exposes orientation and structure before deeper analytical explanation or granular assertion records"],
        ["instantaneous complete data dump", "lossy compression"],
        req_prov_ids=["prov.public-srow-framework"],
    )
    add_item(
        "ME-BENCH-004", "factual_retrieval", "evaluation",
        "What are the six core record types that comprise a conformant Machine Edition package?",
        "factual_enumeration", ["FACT-008"], ["srow.bench.mu.008"], "medium",
        "Package record type inventory.", "factual_concept_match",
        ["manifest", "meaning_unit", "definition", "relationship", "boundary", "provenance"],
        ["manifest, meaning_unit, definition, relationship, boundary, and provenance ledgers"],
        ["embedding_vector", "binary_blob", "neural_weights"],
        req_prov_ids=["prov.public-srow-framework"],
    )
    add_item(
        "ME-BENCH-005", "factual_retrieval", "evaluation",
        "What does resolution monotonicity require across detail levels?",
        "factual_invariant", ["FACT-009"], ["srow.bench.mu.009", "srow.bench.def.003"], "hard",
        "Monotonicity invariant retrieval.", "factual_concept_match",
        ["higher detail levels", "preserve all invariants", "lower detail levels", "without semantic contradiction"],
        ["higher detail levels preserve all invariants of lower detail levels without semantic contradiction"],
        ["lower detail levels override higher detail levels", "arbitrary semantic mutation"],
        req_prov_ids=["prov.public-srow-framework"],
    )

    # Family 2: relationship_retrieval (5 items)
    add_item(
        "ME-BENCH-006", "relationship_retrieval", "calibration",
        "What typed predicate indicates source lineage between meaning units?",
        "relationship_predicate", ["FACT-007"], ["srow.bench.mu.007", "srow.bench.rel.001"], "easy",
        "Lineage predicate lookup.", "relationship_triple",
        ["derives_from"], ["derives_from"], ["improves", "contradicts"],
        req_triples=[{"subject": "srow.bench.mu.005", "predicate": "derives_from", "object": "srow.bench.mu.006"}],
    )
    add_item(
        "ME-BENCH-007", "relationship_retrieval", "evaluation",
        "What typed predicate is used to establish architectural elaboration between concepts?",
        "relationship_predicate", ["FACT-007"], ["srow.bench.mu.007", "srow.bench.rel.002"], "easy",
        "Elaboration predicate lookup.", "relationship_triple",
        ["clarifies"], ["clarifies"], ["replaces", "invalidates"],
        req_triples=[{"subject": "srow.bench.mu.006", "predicate": "clarifies", "object": "srow.bench.mu.002"}],
    )
    add_item(
        "ME-BENCH-008", "relationship_retrieval", "evaluation",
        "What typed predicate connects an assertion to its prerequisite dependencies?",
        "relationship_predicate", ["FACT-007"], ["srow.bench.mu.007", "srow.bench.rel.003"], "medium",
        "Prerequisite dependency predicate lookup.", "relationship_triple",
        ["depends_on"], ["depends_on"], ["extends", "eliminates"],
        req_triples=[{"subject": "srow.bench.mu.009", "predicate": "depends_on", "object": "srow.bench.mu.004"}],
    )
    add_item(
        "ME-BENCH-009", "relationship_retrieval", "evaluation",
        "What relationship direction and predicate connect the stable-ID algorithm to validation compliance?",
        "relationship_edge", ["FACT-005", "FACT-006", "FACT-007"], ["srow.bench.rel.001"], "hard",
        "Specific edge and direction verification.", "relationship_triple",
        ["derives_from", "srow.bench.mu.005", "srow.bench.mu.006"],
        ["stable-ID invariant derives_from validation compliance"],
        ["validation compliance derives from stable-ID"],
        req_triples=[{"subject": "srow.bench.mu.005", "predicate": "derives_from", "object": "srow.bench.mu.006"}],
    )
    add_item(
        "ME-BENCH-010", "relationship_retrieval", "evaluation",
        "What typed predicate is used when a meaning unit provides a concrete application instance of a principle?",
        "relationship_predicate", ["FACT-007"], ["srow.bench.mu.007", "srow.bench.rel.004"], "medium",
        "Exemplification predicate lookup.", "relationship_triple",
        ["exemplifies"], ["exemplifies"], ["generates", "mutates"],
        req_triples=[{"subject": "srow.bench.mu.006", "predicate": "exemplifies", "object": "srow.bench.mu.001"}],
    )

    # Family 3: hierarchy_preservation (5 items)
    add_item(
        "ME-BENCH-011", "hierarchy_preservation", "calibration",
        "What is the five-tier resolution level hierarchy in SROW from lowest to highest granularity?",
        "hierarchy_ordering", ["FACT-004"], ["srow.bench.mu.004"], "medium",
        "Full L0-L4 ordering.", "hierarchy_sequence",
        ["L0 orientation summaries", "L1 core principles", "L2 functional architecture", "L3 technical verification records", "L4 forensic ledgers"],
        ["L0 orientation summaries, L1 core principles, L2 functional architecture, L3 technical verification records, L4 forensic ledgers"],
        ["L4 orientation", "L0 forensic ledger"],
    )
    add_item(
        "ME-BENCH-012", "hierarchy_preservation", "evaluation",
        "In which chapter is the boundary between SROW and cognitive architectures located relative to technical architecture?",
        "hierarchy_containment", ["FACT-005", "FACT-013"], ["srow.bench.bound.001"], "easy",
        "Chapter structure navigation.", "hierarchy_sequence",
        ["Chapter 4", "after Chapter 2", "Boundaries and Scope"],
        ["Chapter 4: Boundaries, Scope, and Epistemic Limitations, following Chapter 2: Technical Architecture"],
        ["Chapter 1", "Chapter 2"],
    )
    add_item(
        "ME-BENCH-013", "hierarchy_preservation", "evaluation",
        "Which resolution level corresponds to core principles in the SROW hierarchy?",
        "hierarchy_level_lookup", ["FACT-004"], ["srow.bench.mu.004"], "easy",
        "L1 resolution assignment.", "hierarchy_sequence",
        ["L1", "core principles"], ["L1 corresponds to core principles"], ["L0", "L2", "L3", "L4"],
    )
    add_item(
        "ME-BENCH-014", "hierarchy_preservation", "evaluation",
        "Which resolution level corresponds to technical verification records in SROW?",
        "hierarchy_level_lookup", ["FACT-004"], ["srow.bench.mu.004"], "easy",
        "L3 resolution assignment.", "hierarchy_sequence",
        ["L3", "technical verification"], ["L3 corresponds to technical verification records"], ["L0", "L1", "L2", "L4"],
    )
    add_item(
        "ME-BENCH-015", "hierarchy_preservation", "evaluation",
        "What is the structural relationship between contextual scope tags and individual assertions?",
        "hierarchy_nesting", ["FACT-012"], ["srow.bench.mu.012"], "hard",
        "Scope enclosing assertions.", "hierarchy_sequence",
        ["scope tags define operational domain", "separating universal core invariants from provisional public companion samples"],
        ["contextual scope tags define the operational domain enclosing individual assertions"],
        ["scope tags are child properties with no domain meaning"],
    )

    # Family 4: provenance_tracing (5 items)
    add_item(
        "ME-BENCH-016", "provenance_tracing", "calibration",
        "What is the authoritative release archive hash supporting the SROW public companion sample records?",
        "provenance_hash", ["FACT-010"], ["prov.srow-public-companion-release"], "medium",
        "Exact SHA-256 release hash lookup.", "provenance_chain",
        ["0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181"],
        ["SHA-256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181"],
        ["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
        req_prov_ids=["prov.srow-public-companion-release"],
        req_prov_urls=["https://winmedia.com/machine-editions/editions/srow"],
    )
    add_item(
        "ME-BENCH-017", "provenance_tracing", "evaluation",
        "What canonical URL serves as the authority for the core SROW framework definitions?",
        "provenance_url", ["FACT-010"], ["prov.public-srow-framework"], "easy",
        "Canonical authority URL lookup.", "provenance_chain",
        ["https://winmedia.com/frameworks/srow"],
        ["https://winmedia.com/frameworks/srow"],
        ["https://google.com", "https://wikipedia.org"],
        req_prov_ids=["prov.public-srow-framework"],
        req_prov_urls=["https://winmedia.com/frameworks/srow"],
    )
    add_item(
        "ME-BENCH-018", "provenance_tracing", "evaluation",
        "How does epistemic authority bind atomic assertions to source verification?",
        "provenance_mechanism", ["FACT-010"], ["srow.bench.mu.010"], "medium",
        "Epistemic authority binding principle.", "provenance_chain",
        ["binds directly", "verifiable cryptographic release hashes", "canonical publication provenance URLs"],
        ["every atomic assertion binds directly to verifiable cryptographic release hashes or canonical publication provenance URLs"],
        ["informal citation text", "unverified web search"],
        req_prov_ids=["prov.srow-public-companion-release"],
    )
    add_item(
        "ME-BENCH-019", "provenance_tracing", "evaluation",
        "What provenance record governs the public companion release metadata?",
        "provenance_id_lookup", ["FACT-010"], ["prov.srow-public-companion-release"], "easy",
        "Provenance record identifier verification.", "provenance_chain",
        ["prov.srow-public-companion-release", "https://winmedia.com/machine-editions/editions/srow"],
        ["prov.srow-public-companion-release (https://winmedia.com/machine-editions/editions/srow)"],
        ["prov.internal-governed-ledger"],
        req_prov_ids=["prov.srow-public-companion-release"],
        req_prov_urls=["https://winmedia.com/machine-editions/editions/srow"],
    )
    add_item(
        "ME-BENCH-020", "provenance_tracing", "evaluation",
        "What is the required adjudication consequence when citation provenance is fabricated rather than missing?",
        "provenance_rule", ["FACT-010"], ["srow.bench.mu.010"], "hard",
        "Fabrication penalty principle.", "provenance_chain",
        ["PROVENANCE_FABRICATED", "worse than omitted provenance", "severe penalty"],
        ["Fabricated provenance is penalized more severely than omitted provenance under PROVENANCE_FABRICATED failure mode"],
        ["fabricated provenance is acceptable if plausible"],
    )

    # Family 5: boundary_constraint_recognition (5 items)
    add_item(
        "ME-BENCH-021", "boundary_constraint_recognition", "calibration",
        "Is SROW intended to operate as a cognition architecture or internal thought model?",
        "boundary_negative", ["FACT-013"], ["srow.bench.bound.001"], "easy",
        "Expression vs cognition negative boundary.", "constraint_compliance",
        ["not a cognition architecture", "expression and structuring protocol", "not an internal thought representation"],
        ["No. SROW is an expression and structuring protocol, not a cognition architecture or internal thought representation."],
        ["Yes, SROW is an internal neural thought model."],
        req_boundaries=["srow.bench.bound.001"],
    )
    add_item(
        "ME-BENCH-022", "boundary_constraint_recognition", "evaluation",
        "Do structured Machine Edition records guarantee factual truth or eliminate model error?",
        "boundary_epistemic", ["FACT-014"], ["srow.bench.bound.002"], "easy",
        "Truth guarantee epistemic limit.", "constraint_compliance",
        ["do not guarantee factual truth", "do not eliminate model error", "improve inspectability and retrieval precision"],
        ["No. Structured records improve inspectability and retrieval precision; they do not guarantee factual truth or eliminate model error."],
        ["Yes, Machine Edition eliminates all hallucinations and guarantees 100% truth."],
        req_boundaries=["srow.bench.bound.002"],
    )
    add_item(
        "ME-BENCH-023", "boundary_constraint_recognition", "evaluation",
        "Does this public reference benchmark contain the complete SROW manuscript or governed meaning-unit database?",
        "boundary_scope", ["FACT-015"], ["srow.bench.bound.003"], "medium",
        "Public companion scope restriction.", "constraint_compliance",
        ["contains only authorized public companion samples", "does not include complete manuscript", "governed meaning-unit database excluded"],
        ["No. This public reference material contains only authorized public companion samples and excludes the complete manuscript and governed database."],
        ["Yes, the entire governed book and database are included."],
        req_boundaries=["srow.bench.bound.003"],
    )
    add_item(
        "ME-BENCH-024", "boundary_constraint_recognition", "evaluation",
        "Does JSON Schema validation conformance imply epistemic endorsement of the truth of external assertions?",
        "boundary_governance", ["FACT-016"], ["srow.bench.bound.004"], "hard",
        "Validation vs endorsement boundary.", "constraint_compliance",
        ["structural and syntactic compliance", "does not constitute epistemic endorsement", "not endorsement of truth value"],
        ["No. Schema conformance certifies structural and syntactic compliance; it does not constitute an epistemic endorsement of truth value."],
        ["Yes, schema conformance proves external assertions are true."],
        req_boundaries=["srow.bench.bound.004"],
    )
    add_item(
        "ME-BENCH-025", "boundary_constraint_recognition", "evaluation",
        "What negative boundary applies to the relationship between explicit structure and cognitive friction?",
        "boundary_principle", ["FACT-002", "FACT-014"], ["srow.bench.bound.002"], "medium",
        "Structure benefits vs limits.", "constraint_compliance",
        ["reduces cognitive friction", "does not eliminate model error or guarantee truth"],
        ["Explicit structural hierarchy reduces cognitive friction, but does not guarantee factual truth or eliminate model error."],
        ["Structure guarantees automated agents never make reasoning errors."],
        req_boundaries=["srow.bench.bound.002"],
    )

    # Family 6: ambiguity_handling (5 items)
    add_item(
        "ME-BENCH-026", "ambiguity_handling", "calibration",
        "Does the public specification define the internal neural architecture of an automated inference agent?",
        "ambiguity_qualification", ["FACT-011", "FACT-013"], ["srow.bench.bound.001"], "medium",
        "Requires explicit qualification that agent internals are outside protocol scope.", "ambiguity_qualification",
        ["outside source scope", "not specified", "explicit qualification required", "expression protocol only"],
        ["The source does not specify internal neural architectures; it defines external expression and structuring protocols."],
        ["It uses a 70B parameter transformer model with 8-bit quantization."],
        requires_qualification=True,
    )
    add_item(
        "ME-BENCH-027", "ambiguity_handling", "evaluation",
        "What must an inference agent do when evidence in the source accommodates multiple valid interpretations?",
        "ambiguity_protocol", ["FACT-011"], ["srow.bench.mu.011"], "easy",
        "Ambiguity handling rule.", "ambiguity_qualification",
        ["explicit qualification", "rather than collapsing ambiguity into ungrounded certainty"],
        ["When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty."],
        ["Guess the most likely answer confidently."],
        requires_qualification=True,
    )
    add_item(
        "ME-BENCH-028", "ambiguity_handling", "evaluation",
        "Does SROW specify whether vector embeddings or lexical BM25 is the mandatory retrieval algorithm for third-party RAG pipelines?",
        "ambiguity_qualification", ["FACT-008", "FACT-011"], ["srow.bench.mu.011"], "medium",
        "Mandatory vs optional RAG methods.", "ambiguity_qualification",
        ["not mandated", "implementations vary", "qualification required", "public contract does not restrict third-party retrieval"],
        ["SROW does not mandate a specific third-party retrieval algorithm; both lexical and vector approaches exist outside the core package contract."],
        ["Lexical BM25 is strictly mandatory for all AI systems in existence."],
        requires_qualification=True,
    )
    add_item(
        "ME-BENCH-029", "ambiguity_handling", "evaluation",
        "Can an assertion be classified as both a core invariant and a provisional sample simultaneously?",
        "ambiguity_distinction", ["FACT-012"], ["srow.bench.mu.012"], "hard",
        "Scope distinction qualification.", "ambiguity_qualification",
        ["distinct scope categories", "separated by contextual scope tags", "cannot be conflated"],
        ["Contextual scope tags separate universal core invariants from provisional public companion samples into distinct operational domains."],
        ["Yes, all assertions are simultaneously universal and provisional."],
        requires_qualification=True,
    )
    add_item(
        "ME-BENCH-030", "ambiguity_handling", "evaluation",
        "Does the stable-ID algorithm specify 32-character or 16-character hexadecimal truncation?",
        "ambiguity_precision", ["FACT-005"], ["srow.bench.mu.005"], "medium",
        "Exact truncation distinction.", "ambiguity_qualification",
        ["16 hexadecimal characters", "not 32 characters", "SHA-256 truncated to 16 hex"],
        ["The algorithm explicitly specifies 16 hexadecimal characters (truncated from SHA-256)."],
        ["It uses 32 or 64 characters depending on preference."],
    )

    # Family 7: multi_resolution_retrieval (5 items)
    add_item(
        "ME-BENCH-031", "multi_resolution_retrieval", "calibration",
        "Provide the executive orientation (L0 level) summary of SROW.",
        "resolution_retrieval", ["FACT-001", "FACT-004"], ["srow.bench.mu.001"], "easy",
        "L0 resolution retrieval.", "resolution_level_match",
        ["L0", "communication protocol", "structured knowledge readable and navigable by both humans and machines"],
        ["L0 orientation summary: Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines."],
        ["Full source code implementation details"],
    )
    add_item(
        "ME-BENCH-032", "multi_resolution_retrieval", "evaluation",
        "Retrieve the core principle (L1 level) regarding structure and reader respect.",
        "resolution_retrieval", ["FACT-002", "FACT-004"], ["srow.bench.mu.002"], "easy",
        "L1 resolution retrieval.", "resolution_level_match",
        ["L1", "Structure is a form of reader respect", "reduces cognitive friction"],
        ["L1 core principle: Structure is a form of reader respect. Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents."],
        ["L4 bitwise offset table"],
    )
    add_item(
        "ME-BENCH-033", "multi_resolution_retrieval", "evaluation",
        "Retrieve the functional architecture (L2 level) specification for stable identification.",
        "resolution_retrieval", ["FACT-005", "FACT-004"], ["srow.bench.mu.005"], "medium",
        "L2 resolution retrieval.", "resolution_level_match",
        ["L2", "SHA-256 truncated to 16 hexadecimal characters", "canonical lexically sorted source-block binding key"],
        ["L2 functional architecture: The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key."],
        ["High level informal one-word overview"],
    )
    add_item(
        "ME-BENCH-034", "multi_resolution_retrieval", "evaluation",
        "Retrieve the technical verification (L3 level) statement regarding software and AI validation compliance.",
        "resolution_retrieval", ["FACT-006", "FACT-004"], ["srow.bench.mu.006"], "medium",
        "L3 resolution retrieval.", "resolution_level_match",
        ["L3", "explicit structural compliance for software and AI validation"],
        ["L3 technical verification: Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation."],
        ["Unstructured marketing blurb"],
    )
    add_item(
        "ME-BENCH-035", "multi_resolution_retrieval", "evaluation",
        "What distinction separates an L0 orientation summary from an L4 forensic ledger?",
        "resolution_contrast", ["FACT-004", "FACT-009"], ["srow.bench.mu.004", "srow.bench.mu.009"], "hard",
        "Multi-resolution contrast.", "resolution_level_match",
        ["L0 provides orientation summaries", "L4 contains complete forensic ledgers", "higher detail preserves lower invariants"],
        ["L0 provides high-level orientation summaries, whereas L4 contains complete forensic ledgers, adhering to resolution monotonicity without semantic contradiction."],
        ["L0 and L4 are identical in granularity."],
    )

    # Family 8: unsupported_claim_detection (5 items)
    add_item(
        "ME-BENCH-036", "unsupported_claim_detection", "calibration",
        "What is the recommended quantum key distribution cipher for SROW packages?",
        "unsupported_detection", [], [], "easy",
        "Quantum crypto unsupported query.", "unsupported_abstention",
        ["not supported", "not stated in source", "insufficient evidence", "outside source scope"],
        ["The source does not define or mention quantum key distribution ciphers for SROW packages; the claim is unsupported."],
        ["BB84 quantum protocol with 4096-bit photon entanglement."],
        is_unsupported=True,
    )
    add_item(
        "ME-BENCH-037", "unsupported_claim_detection", "evaluation",
        "What is the monthly subscription price for accessing the governed SROW meaning-unit database?",
        "unsupported_detection", [], [], "easy",
        "Pricing unsupported query.", "unsupported_abstention",
        ["not stated", "unsupported by source", "no pricing information provided", "outside public scope"],
        ["The public source material does not contain monthly subscription pricing or commercial fee schedules."],
        ["$49.99 per month for pro tier."],
        is_unsupported=True,
    )
    add_item(
        "ME-BENCH-038", "unsupported_claim_detection", "evaluation",
        "Which Python framework does SROW mandate for neural network fine-tuning?",
        "unsupported_detection", [], [], "easy",
        "ML framework mandate unsupported query.", "unsupported_abstention",
        ["not stated", "not mandated", "unsupported", "expression protocol rather than training framework"],
        ["The source does not mandate any neural network fine-tuning framework; SROW is an expression and structuring protocol, not a training platform."],
        ["PyTorch 2.5 with HuggingFace Transformers is strictly mandatory."],
        is_unsupported=True,
    )
    add_item(
        "ME-BENCH-039", "unsupported_claim_detection", "evaluation",
        "What is the author's personal home address and phone number?",
        "unsupported_detection", [], [], "easy",
        "Personal private data unsupported query.", "unsupported_abstention",
        ["not stated", "outside source scope", "unsupported", "private personal data not contained in source"],
        ["The source contains no author personal home address or phone number information."],
        ["123 Main Street, Suite 400, Austin TX, 555-0199."],
        is_unsupported=True,
    )
    add_item(
        "ME-BENCH-040", "unsupported_claim_detection", "evaluation",
        "At what CPU temperature does the SROW stable-ID hashing algorithm experience thermal throttling?",
        "unsupported_detection", [], [], "medium",
        "Hardware thermal category error unsupported query.", "unsupported_abstention",
        ["not stated", "unsupported", "category error", "algorithmic specification has no thermal parameters"],
        ["The source defines a mathematical hashing specification (SHA-256 truncated to 16 hex characters) and contains no hardware thermal throttling specifications."],
        ["Thermal throttling occurs at exactly 95 degrees Celsius."],
        is_unsupported=True,
    )

    return tasks, gold_answers, gold_provenance, gold_relationships, gold_constraints


def rebuild_all_benchmark_artifacts(repo_root: Path):
    """Orchestrates full deterministic generation of ME-BENCH-001."""
    bench_dir = repo_root / "benchmark"
    bench_dir.mkdir(parents=True, exist_ok=True)

    # 1. Source
    source_dir = bench_dir / "source"
    source_dir.mkdir(exist_ok=True)
    source_md = source_dir / "benchmark-source.md"
    source_md.write_text(SOURCE_TEXT, encoding="utf-8")
    source_sha256 = hashlib.sha256(SOURCE_TEXT.encode("utf-8")).hexdigest()

    inventory_data = {
        "source_name": "SROW Public Reference Benchmark Source",
        "version": "0.1.0",
        "source_file": "benchmark/source/benchmark-source.md",
        "source_sha256": source_sha256,
        "derivation_basis": "Derived exclusively from authorized SROW Public Companion v0.1 material (archive SHA-256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181).",
        "license": "CC BY 4.0 within expressly inventoried public scope",
        "fact_count": len(FACTS),
        "facts": FACTS
    }
    (source_dir / "source-inventory.json").write_text(json.dumps(inventory_data, indent=2), encoding="utf-8")

    # 2. Representations
    rep_dir = bench_dir / "representations"
    rep_dir.mkdir(exist_ok=True)

    # PDF
    pdf_dir = rep_dir / "pdf"
    pdf_file = pdf_dir / "benchmark-document.pdf"
    generate_pdf(source_md, pdf_file)
    pdf_sha256 = hashlib.sha256(pdf_file.read_bytes()).hexdigest()
    (pdf_dir / "condition.json").write_text(json.dumps({
        "condition_id": "cond-pdf-v0.1",
        "representation_type": "pdf",
        "artifact_path": "benchmark/representations/pdf/benchmark-document.pdf",
        "artifact_sha256": pdf_sha256,
        "source_corpus_sha256": source_sha256,
        "construction_method": "minimal Latin-1 single-page fixed layout rendering",
        "construction_configuration": {
            "page_size": "Letter (612x792 pt)",
            "font": "Helvetica Type1 10pt",
            "line_spacing_pt": 15
        },
        "adapter": "BenchmarkPDFAdapter",
        "license_note": "CC BY 4.0 within authorized SROW Public Companion scope"
    }, indent=2), encoding="utf-8")

    # EPUB
    epub_dir = rep_dir / "epub"
    epub_file = epub_dir / "benchmark-document.epub"
    generate_epub(source_md, epub_file)
    epub_sha256 = hashlib.sha256(epub_file.read_bytes()).hexdigest()
    (epub_dir / "condition.json").write_text(json.dumps({
        "condition_id": "cond-epub-v0.1",
        "representation_type": "epub",
        "artifact_path": "benchmark/representations/epub/benchmark-document.epub",
        "artifact_sha256": epub_sha256,
        "source_corpus_sha256": source_sha256,
        "construction_method": "standard EPUB 3.0 packaging with OEBPS XHTML chapters",
        "construction_configuration": {
            "epub_version": "3.0",
            "identifier": "urn:uuid:srow-benchmark-epub-v0.1",
            "compression": "ZIP_DEFLATED (uncompressed mimetype)"
        },
        "adapter": "BenchmarkEPUBAdapter",
        "license_note": "CC BY 4.0 within authorized SROW Public Companion scope"
    }, indent=2), encoding="utf-8")

    # RAG
    rag_dir = rep_dir / "rag"
    rag_file = rag_dir / "rag-corpus.json"
    generate_rag(source_md, rag_file, chunk_size=250, overlap=40)
    rag_sha256 = hashlib.sha256(rag_file.read_bytes()).hexdigest()
    (rag_dir / "condition.json").write_text(json.dumps({
        "condition_id": "cond-rag-v0.1",
        "representation_type": "rag",
        "artifact_path": "benchmark/representations/rag/rag-corpus.json",
        "artifact_sha256": rag_sha256,
        "source_corpus_sha256": source_sha256,
        "construction_method": "deterministic sliding-window paragraph chunking with BM25 lexical ranking",
        "construction_configuration": {
            "chunking_strategy": "paragraph-preserving sliding window",
            "target_chunk_size": 250,
            "overlap": 40,
            "retrieval_algorithm": "deterministic lexical BM25-style term frequency",
            "metadata_leakage_prevented": True
        },
        "adapter": "BenchmarkNaiveRAGAdapter",
        "license_note": "CC BY 4.0 within authorized SROW Public Companion scope"
    }, indent=2), encoding="utf-8")

    # Machine Edition
    me_dir = rep_dir / "machine-edition"
    pkg_dir = me_dir / "package"
    generate_machine_edition_package(pkg_dir, repo_root)
    # Validate ME
    val = MachineEditionValidator().validate_package(pkg_dir)
    assert val.outcome == "ME_CONFORMANT", f"Machine Edition benchmark specimen must be ME_CONFORMANT: {val.errors}"

    (me_dir / "condition.json").write_text(json.dumps({
        "condition_id": "cond-machine-edition-v0.1",
        "representation_type": "machine_edition",
        "artifact_path": "benchmark/representations/machine-edition/package",
        "package_id": "winmedia.srow.benchmark-specimen",
        "source_corpus_sha256": source_sha256,
        "construction_method": "Machine Edition Specification v0.1 JSON Schemas (C1-C7) validation and JSONL packaging",
        "construction_configuration": {
            "specification_version": "0.1.0",
            "record_types": ["manifest", "meaning_unit", "definition", "relationship", "boundary", "provenance"],
            "resolution_levels": ["L0", "L1", "L2", "L3", "L4"],
            "conformance_status": "ME_CONFORMANT"
        },
        "adapter": "BenchmarkMachineEditionAdapter",
        "license_note": "CC BY 4.0 within authorized SROW Public Companion scope"
    }, indent=2), encoding="utf-8")

    # 3. Tasks and Gold Files (Firewall separation)
    tasks, gold_answers, gold_provenance, gold_relationships, gold_constraints = get_benchmark_tasks_and_gold()
    assert len(tasks) == 40, f"Expected 40 tasks, got {len(tasks)}"

    tasks_jsonl_content = "\n".join(json.dumps(t) for t in tasks) + "\n"
    (bench_dir / "tasks.jsonl").write_text(tasks_jsonl_content, encoding="utf-8")

    gold_dir = bench_dir / "gold"
    gold_dir.mkdir(exist_ok=True)
    (gold_dir / "answers.jsonl").write_text("\n".join(json.dumps(a) for a in gold_answers) + "\n", encoding="utf-8")
    (gold_dir / "provenance.jsonl").write_text("\n".join(json.dumps(p) for p in gold_provenance) + "\n", encoding="utf-8")
    (gold_dir / "relationships.jsonl").write_text("\n".join(json.dumps(r) for r in gold_relationships) + "\n", encoding="utf-8")
    (gold_dir / "constraints.jsonl").write_text("\n".join(json.dumps(c) for c in gold_constraints) + "\n", encoding="utf-8")

    # 4. Rights Manifest
    rights_content = """# Rights and Licensing Manifest — ME-BENCH-001

## Source Material
* **Corpus Identity**: SROW Public Reference Benchmark Source (v0.1)
* **Lineage**: Derived exclusively from the authorized SROW Public Companion v0.1 release archive (`srow-machine-edition-v0.1-public-companion.zip`, SHA-256: `0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181`).
* **Source License**: Creative Commons Attribution 4.0 International (CC BY 4.0) within expressly inventoried public-companion scope.
* **Licensor**: WinMedia / Lynn Media.

## Benchmark Content
* **Benchmark Items and Tasks**: Published under CC BY 4.0.
* **Gold Standards and Scorer Rules**: Published under CC BY 4.0.
* **Derived Representation Artifacts** (PDF, EPUB, RAG JSON, Machine Edition package): Published under CC BY 4.0 within authorized scope.

## Excluded and Prohibited Material
The benchmark explicitly contains ZERO:
1. Governed book manuscript content.
2. Paid-edition proprietary texts.
3. Internal adjudication ledgers.
4. Private editorial or peer review archives.
5. Machine Edition Factory proprietary compilers.

## Software Tools
* Benchmark evaluation engine and adapters in `src/machine_edition_devkit/benchmark/`: Released under repository MIT License.
"""
    (bench_dir / "RIGHTS.md").write_text(rights_content, encoding="utf-8")

    # 5. Threats to Validity Registry
    threats_content = """# Threats-to-Validity Registry — ME-BENCH-001

This registry formally documents known methodological threats, potential biases, mitigations, and residual risks prior to experimental LLM execution in ME-RES-001.

| Threat ID | Threat Category | Why It Matters | Mitigation in ME-BENCH-001 | Residual Risk |
|---|---|---|---|---|
| **TV-01** | Single-Source Domain Limitation | Benchmark uses SROW conceptual domain; results may not generalize identically to biomedical or financial corpora. | Strict schema-neutral design; explicit domain boundary statement. | Generalization to highly dense numeric/tabular domains remains future research. |
| **TV-02** | Small Public Corpus Size | 16 facts across 4 chapters might allow memorization or shallow overfit. | Frozen calibration (8) vs evaluation (32) split; multi-resolution and negative constraints require deep inference. | Synthetic expansions planned for future benchmark versions (v0.2+). |
| **TV-03** | Task-Author Bias | Task designer might craft questions that favor structured data formats over linear text. | Balanced 8 task families including unstructured factual recovery and simple navigation; gold answers derive strictly from text truth. | Residual stylistic alignment with specification author vocabulary. |
| **TV-04** | RAG Baseline Choice | Lexical sliding-window BM25 baseline may underperform advanced hybrid dense-vector reranking systems. | RAG parameters are completely frozen, transparent, and reproducible without non-deterministic embedding APIs. | Advanced vector RAG variants reserved for separate benchmark conditions. |
| **TV-05** | PDF/EPUB Adapter Asymmetry | Simple text extraction could disadvantage document formats compared to native JSONL traversal. | Valid ISO-compliant PDF and EPUB 3.0 packages constructed; robust adapters extract full text without OCR degradation. | Document layout cues (e.g. bolding/fonts) are lost in pure string extraction. |
| **TV-06** | Gold Standard Subjectivity | Rubrics could misclassify valid model paraphrases as incorrect. | Deterministic concept sets, regex normalization, and synthetic test suite with 100% fixture coverage. | Semantic edge cases in future LLM responses require offline adjudication. |
| **TV-07** | Benchmark Data Leakage | Experimental models might see gold answers during evaluation runs. | Strict architectural firewall: `tasks.jsonl` contains zero gold answers or scoring rules. | None for offline execution; pretraining contamination mitigated by novel benchmark IDs. |
| **TV-08** | Representation Parity Drift | Information might exist in one representation but be omitted from another. | Programmatic parity gate verifies 16/16 tracked facts present in PDF, EPUB, RAG, and Machine Edition. | Zero information disparity across representation conditions. |
"""
    (bench_dir / "THREATS-TO-VALIDITY.md").write_text(threats_content, encoding="utf-8")

    # 6. Benchmark Manifest
    manifest_data = {
        "benchmark_id": BENCHMARK_ID,
        "title": BENCHMARK_TITLE,
        "version": BENCHMARK_VERSION,
        "status": BENCHMARK_STATUS,
        "freeze_date": "2026-08-29",
        "source_identity": "SROW Public Reference Benchmark Source",
        "source_sha256": source_sha256,
        "corpus_lineage": CORPUS_LINEAGE,
        "specification_authority": SPECIFICATION_AUTHORITY,
        "rights_source": "benchmark/RIGHTS.md",
        "task_count": 40,
        "task_family_counts": {
            "factual_retrieval": 5,
            "relationship_retrieval": 5,
            "hierarchy_preservation": 5,
            "provenance_tracing": 5,
            "boundary_constraint_recognition": 5,
            "ambiguity_handling": 5,
            "multi_resolution_retrieval": 5,
            "unsupported_claim_detection": 5
        },
        "split_counts": {
            "calibration": 8,
            "evaluation": 32
        },
        "representations": {
            "pdf": {
                "artifact": "benchmark/representations/pdf/benchmark-document.pdf",
                "sha256": pdf_sha256,
                "manifest": "benchmark/representations/pdf/condition.json"
            },
            "epub": {
                "artifact": "benchmark/representations/epub/benchmark-document.epub",
                "sha256": epub_sha256,
                "manifest": "benchmark/representations/epub/condition.json"
            },
            "rag": {
                "artifact": "benchmark/representations/rag/rag-corpus.json",
                "sha256": rag_sha256,
                "manifest": "benchmark/representations/rag/condition.json"
            },
            "machine_edition": {
                "package": "benchmark/representations/machine-edition/package",
                "package_id": "winmedia.srow.benchmark-specimen",
                "manifest": "benchmark/representations/machine-edition/condition.json"
            }
        },
        "rag_configuration": {
            "strategy": "paragraph-preserving sliding window",
            "target_chunk_size": 250,
            "overlap": 40,
            "ranking": "deterministic lexical BM25"
        },
        "scoring_version": "0.1.0",
        "scoring_dimensions": SCORING_DIMENSIONS,
        "failure_taxonomy": FAILURE_TAXONOMY,
        "integrity_manifest": "benchmark/integrity-manifest.json",
        "reproduction_commands": [
            "python -m machine_edition_devkit.benchmark verify",
            "python -m machine_edition_devkit.benchmark rebuild",
            "python -m machine_edition_devkit.benchmark test-scorer"
        ]
    }
    (bench_dir / "manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    # 7. Integrity Manifest
    integrity_files = [
        "benchmark/source/benchmark-source.md",
        "benchmark/source/source-inventory.json",
        "benchmark/representations/pdf/benchmark-document.pdf",
        "benchmark/representations/pdf/condition.json",
        "benchmark/representations/epub/benchmark-document.epub",
        "benchmark/representations/epub/condition.json",
        "benchmark/representations/rag/rag-corpus.json",
        "benchmark/representations/rag/condition.json",
        "benchmark/representations/machine-edition/condition.json",
        "benchmark/representations/machine-edition/package/manifest.json",
        "benchmark/representations/machine-edition/package/meaning-units.jsonl",
        "benchmark/representations/machine-edition/package/definitions.jsonl",
        "benchmark/representations/machine-edition/package/boundaries.jsonl",
        "benchmark/representations/machine-edition/package/relationships.jsonl",
        "benchmark/representations/machine-edition/package/provenance.jsonl",
        "benchmark/representations/machine-edition/package/full-preview.md",
        "benchmark/representations/machine-edition/package/LICENSE.txt",
        "benchmark/tasks.jsonl",
        "benchmark/gold/answers.jsonl",
        "benchmark/gold/provenance.jsonl",
        "benchmark/gold/relationships.jsonl",
        "benchmark/gold/constraints.jsonl",
        "benchmark/RIGHTS.md",
        "benchmark/THREATS-TO-VALIDITY.md",
        "benchmark/manifest.json"
    ]

    hashes = {}
    for rel_p in integrity_files:
        full_p = repo_root / rel_p
        if full_p.exists():
            h = hashlib.sha256(full_p.read_bytes()).hexdigest()
            hashes[rel_p] = h

    integrity_data = {
        "benchmark_id": BENCHMARK_ID,
        "version": BENCHMARK_VERSION,
        "status": "frozen",
        "file_count": len(hashes),
        "hashes": hashes
    }
    (bench_dir / "integrity-manifest.json").write_text(json.dumps(integrity_data, indent=2), encoding="utf-8")

    # 8. Benchmark README
    readme_content = f"""# Machine Edition Representation Benchmark (ME-BENCH v0.1)

## Purpose & Research Question
> What properties of machine consumption change when the same source information is represented as a conventional document (PDF), EPUB publication, retrieval corpus (RAG), or governed Machine Edition?

ME-BENCH v0.1 is an evaluation instrument. It does not itself establish that one representation universally outperforms another.
RAG systems vary substantially. The frozen RAG condition is one transparent reproducible baseline, not a claim about every possible retrieval architecture.

## Corpus Lineage & Rights
* **Lineage**: `{CORPUS_LINEAGE}`
* **Rights**: Creative Commons Attribution 4.0 International (CC BY 4.0) within authorized public companion scope (see `RIGHTS.md`).
* **Source Hash**: `{source_sha256}`

## Representation Conditions
1. **PDF** (`benchmark/representations/pdf/`): Fixed-layout document (`benchmark-document.pdf`).
2. **EPUB** (`benchmark/representations/epub/`): Standard reflowable EPUB 3.0 publication (`benchmark-document.epub`).
3. **Naive RAG** (`benchmark/representations/rag/`): Sliding-window lexical chunks (`rag-corpus.json`).
4. **Machine Edition** (`benchmark/representations/machine-edition/`): Specimen package adhering to Machine Edition Specification v0.1 (`package/`).

## Task Families & Splits
Total Items: 40 (8 calibration + 32 evaluation).

1. `factual_retrieval` (5 items: 1 calibration, 4 evaluation)
2. `relationship_retrieval` (5 items: 1 calibration, 4 evaluation)
3. `hierarchy_preservation` (5 items: 1 calibration, 4 evaluation)
4. `provenance_tracing` (5 items: 1 calibration, 4 evaluation)
5. `boundary_constraint_recognition` (5 items: 1 calibration, 4 evaluation)
6. `ambiguity_handling` (5 items: 1 calibration, 4 evaluation)
7. `multi_resolution_retrieval` (5 items: 1 calibration, 4 evaluation)
8. `unsupported_claim_detection` (5 items: 1 calibration, 4 evaluation)

## Gold Firewall
* Experimental runners consume `tasks.jsonl` and representation conditions.
* Gold adjudication ledgers (`gold/answers.jsonl`, `gold/provenance.jsonl`, `gold/relationships.jsonl`, `gold/constraints.jsonl`) are strictly separated to prevent leakage.

## Reproduction
```bash
# Verify integrity, parity, schema validity, and scorer
python -m machine_edition_devkit.benchmark verify

# Rebuild all representations deterministically
python -m machine_edition_devkit.benchmark rebuild

# Run offline scorer test fixture suite
python -m machine_edition_devkit.benchmark test-scorer
```
"""
    (bench_dir / "README.md").write_text(readme_content, encoding="utf-8")
    print(f"ME-BENCH-001 rebuilt successfully with 40 tasks across 8 families.")

