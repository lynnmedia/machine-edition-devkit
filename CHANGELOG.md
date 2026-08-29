# Changelog - Machine Edition Developer Kit

All notable changes to the Machine Edition Developer Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-29

### Added
- Initial Developer Kit v0.1 reference implementation architecture.
- Five core modules established:
  - `inspect`: Metadata and layout summary inspection without full parse overhead.
  - `validate`: Schema validation (Draft 2020-12) and referential integrity checking.
  - `parse`: Typed object mapping from newline-delimited JSON (`.jsonl`) streams.
  - `query`: Multi-tier resolution filtering and provenance traversal engine.
  - `compare`: Structural and capability comparison matrix against PDF, EPUB, and naive RAG chunks.
- Bound directly to `Machine Edition Specification v0.1`.
- Bundled public schemas and preview specimen (`srow-machine-edition-preview-v0.1`).
- End-to-end integration test suite.
