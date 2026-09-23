# Machine Edition Developer Kit v0.1.0

## What this is

A small, public implementation of [Machine Edition Specification v0.1](https://winmedia.com/machine-editions/specification/v0.1). It contains a complete SROW reference specimen derived from the authorized public companion, JSON Schemas, a validator, a parser, and query examples. A Machine Edition makes meaning units, relationships, boundaries, and provenance addressable for software.

The kit runs locally with Python 3.10+ and the declared `jsonschema` dependency. Its [GitHub v0.1.0 release](https://github.com/lynnmedia/machine-edition-devkit/releases/tag/v0.1.0) identifies the published files and checksums.

## When to use it

Use it to inspect a package, check its structural conformance, trace a specimen claim to its public source, or prototype a small query. Start with the three [sample queries](examples/queries.md). The [SROW specimen](specimen/srow/README.md) is synthetic and intentionally small enough to inspect in full.

## What it does not claim

Schema validation does not establish truth, eliminate model error, or grant rights over the governed SROW edition. The specimen is not the manuscript or full SROW meaning-unit database. The comparison describes representation affordances, not universal performance superiority. Research and benchmark materials in this repository are separate follow-on work; they are not required to use the kit.

## Five-minute validation

From a clean checkout, install the package in a local environment, then run the one validation command:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m machine_edition_devkit.validate specimen/srow/package
```

Expected final line: `All schemas and invariants verified successfully (ME_CONFORMANT).` The command exits nonzero for a nonconformant package. Run the test suite with `.venv/bin/python -m pip install -e '.[dev]'` followed by `.venv/bin/python -m pytest -q`. Three persistent malformed fixtures in `tests/fixtures/` demonstrate rejection by the manifest, meaning-unit, and provenance schemas.

For a bounded parser result, run `.venv/bin/python examples/parse.py`. It emits the package ID, version, and at most three meaning-unit IDs with their provenance IDs in stable ID order. The dependency-free TypeScript version is [`examples/parse.ts`](examples/parse.ts); with Node.js 22.18+ run `node examples/parse.ts`.

## Normative specification

[Machine Edition Specification v0.1](https://winmedia.com/machine-editions/specification/v0.1) is the versioned, normative definition. This repository implements it; the [WinMedia reference page](https://winmedia.com/reference/machine-edition) provides canonical context. The kit's local schemas are in [`schemas/`](schemas/), with SHA-256 values in [`schema-manifest.json`](schemas/schema-manifest.json).

## Explore the kit

- [Three example queries](examples/queries.md) show exact lookup, relationship traversal, and provenance resolution. The 20-query pack is in [`queries/sample_queries.json`](queries/sample_queries.json); run it with `.venv/bin/python -m machine_edition_devkit.queries run-all`.
- [PDF, EPUB, RAG chunks, knowledge graphs, and Machine Editions](comparison/pdf-epub-rag-knowledge-graph-machine-edition.md) gives a concise format comparison.
- [SROW source and derivation](specimen/srow/README.md) records the rights-cleared source archive and transformation into the v0.1 specimen.
- [Changelog](CHANGELOG.md), [rights](RIGHTS.md), [MIT code license](LICENSE), and [citation record](CITATION.cff) document release identity and reuse terms.

## Release integrity and citation

The published [v0.1.0 release](https://github.com/lynnmedia/machine-edition-devkit/releases/tag/v0.1.0) includes the SROW specimen ZIP (SHA-256 `ebe193fca0609de8e957d8e88e2a26bddb5fe6490e41a5be44f6bf05cad26151`). The release also contains optional benchmark and research bundles. All three published asset hashes are pinned in [`RELEASE-CHECKSUMS.sha256`](RELEASE-CHECKSUMS.sha256). If those files are downloaded into `dist/`, run `cd dist && shasum -a 256 -c ../RELEASE-CHECKSUMS.sha256` to verify the exact bytes. Changes on `main` after the v0.1.0 tag do not alter that release.

Cite the stable [specification](https://winmedia.com/machine-editions/specification/v0.1) when referring to the format. Cite the [v0.1.0 release](https://github.com/lynnmedia/machine-edition-devkit/releases/tag/v0.1.0) when referring to this implementation or specimen. The machine-readable citation is [`CITATION.cff`](CITATION.cff). No Zenodo DOI is claimed until the exact release has been archived and verified.

The software, schemas, examples, and kit documentation are MIT licensed. The SROW specimen and derived comparison data and benchmark content have the separately documented CC BY 4.0 source scope. See [`RIGHTS.md`](RIGHTS.md) before redistribution.

## Further research

The repository also contains [ME-BENCH](benchmark/README.md), [representation comparison](docs/rag-comparison.md), and the [ME-RES-001](research/me-res-001/report/ME-RES-001-REPORT.md) and [ME-RES-002](research/me-res-002/report/ME-RES-002-REPORT.md) reports. Their methods, limitations, and evidence are documented separately from the five-minute kit path.
