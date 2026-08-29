# Zenodo Archival & DOI Citation Handoff (v0.1.0)

* **Repository**: [`lynnmedia/machine-edition-devkit`](https://github.com/lynnmedia/machine-edition-devkit)
* **Release Tag**: `v0.1.0` ([GitHub Release URL](https://github.com/lynnmedia/machine-edition-devkit/releases/tag/v0.1.0))
* **Effective Metadata Authority**: `.zenodo.json` (takes precedence over `CITATION.cff` for automated archiving)

---

## 1. Audited Metadata Summary (`.zenodo.json`)

```json
{
  "title": "Machine Edition Developer Kit (v0.1.0)",
  "version": "0.1.0",
  "description": "Reference developer kit, validation engine, parser, query suite, benchmark (ME-BENCH-001), and research trial packages (ME-RES-001 reference-harness qualification and ME-RES-002 real generative model trial) implementing the Machine Edition Specification v0.1.",
  "creators": [
    {
      "name": "Lynn Media",
      "affiliation": "Lynn Media / WinMedia",
      "orcid": ""
    }
  ],
  "upload_type": "software",
  "access_right": "open",
  "license": "MIT",
  "keywords": [
    "Machine Edition",
    "structured publishing",
    "machine-readable publication",
    "RAG",
    "knowledge representation",
    "provenance",
    "LLM evaluation",
    "digital publishing"
  ],
  "related_identifiers": [
    {
      "identifier": "https://winmedia.com/machine-editions/specification/v0.1",
      "relation": "isDocumentedBy",
      "scheme": "url"
    },
    {
      "identifier": "https://github.com/lynnmedia/machine-edition-devkit",
      "relation": "isSupplementTo",
      "scheme": "url"
    }
  ]
}
```

---

## 2. Human Execution Routes

### Route A: Manual Archival of Existing v0.1.0 Release (Recommended)
Because GitHub `v0.1.0` was tagged before Zenodo integration was activated, manual upload ensures `v0.1.0` is permanently archived with an exact DOI without minting a premature patch release tag:
1. Sign in to [Zenodo](https://zenodo.org).
2. Click **New Upload** (`https://zenodo.org/deposit/new`).
3. Under **Files**, upload the release assets or source archive:
   * Source ZIP from `https://github.com/lynnmedia/machine-edition-devkit/archive/refs/tags/v0.1.0.zip`
   * Release assets: `srow-public-reference-specimen-v0.1.0.zip`, `me-bench-v0.1.0-bundle.zip`, `me-res-002-evidence-bundle.zip`
4. Fill metadata fields directly matching `.zenodo.json` above:
   * **Resource Type**: Software
   * **Title**: `Machine Edition Developer Kit (v0.1.0)`
   * **Creator**: Lynn Media (Affiliation: Lynn Media / WinMedia)
   * **Version**: `0.1.0`
   * **License**: MIT License
   * **Related Identifiers**:
     * URL `https://winmedia.com/machine-editions/specification/v0.1` (isDocumentedBy)
     * URL `https://github.com/lynnmedia/machine-edition-devkit` (isSupplementTo)
5. Click **Publish** to mint the version DOI and concept DOI.

### Route B: Enable GitHub Integration for Automated Future Archival
1. In Zenodo, navigate to **Profile → GitHub** (`https://zenodo.org/account/settings/github/`).
2. Sync GitHub repositories.
3. Locate `lynnmedia/machine-edition-devkit` and toggle the switch to **ON**.
4. Future release tags published on GitHub will automatically trigger Zenodo archival ingestion.

---

## 3. Post-Archival Recording
Once published, record the public Zenodo record URL, concept DOI, and version DOI to ratify `ME_DIST_ZENODO_CITATION_SURFACE_VERIFIED`.
