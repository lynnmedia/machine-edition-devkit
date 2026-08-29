# SROW Machine Edition — Developer Preview v0.1

This is a limited developer preview of a possible Machine Edition package format. It is not the complete SROW publication, a replacement for the human edition, or a complete specification.

## Contents

- `full-preview.md` — a short, human-readable companion.
- `meaning-units.jsonl` — five compact units, one for each public SROW resolution level.
- `definitions.jsonl`, `boundaries.jsonl`, and `examples.jsonl` — distinct record types rather than a single undifferentiated corpus.
- `relationships.jsonl` — limited relations among preview records.
- `provenance.jsonl` — source and scope records for every included artifact.
- `schemas/` — JSON Schemas for the manifest and meaning-unit records.
- `tests/` — a valid example and an intentionally invalid example for schema-validation exercises.

## Ingestion guidance

Treat every JSONL file as newline-delimited JSON: parse one object per non-empty line. Preserve `id`, `version`, `provenance_id`, `source_url`, and `scope` when indexing or transforming a record. Keep definitions, examples, and boundaries in separate collections or retain their `record_type` distinction.

The five `resolution_level` values are `L0` through `L4`. They identify an intended depth of explanation; they do not rank truth, assign confidence, or replace source review.

Do not infer omitted claims, permissions, or relationships. This preview supports format evaluation only. Refer to `LICENSE.txt` before any use.
