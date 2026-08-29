# SROW Machine Edition — Public Reference Specimen (v0.1)

## Overview

This is the human-readable entrypoint for the **SROW Public Reference Specimen**, conforming to **Machine Edition Specification v0.1**.

It illustrates how structured meaning units, progressive disclosure resolution levels (`L0` to `L4`), negative boundaries, definitions, and provenance records fit together in a verified, computable publication package.

## Core Meaning Units

* **`srow.ref.mu.003` (Resolution: L1)**: *Structure is a form of reader respect.* Explicit structural hierarchy reduces cognitive friction for both human readers and automated inference agents.
* **`srow.ref.mu.002` (Resolution: L2)**: *Stable-ID Algorithm Invariant.* The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters over the canonical lexically sorted source-block binding key.
* **`srow.ref.mu.001` (Resolution: L3)**: *SROW Validation Compliance Sample.* Structured Resolution-Oriented Writing (SROW) establishes explicit structural compliance for software and AI validation.

## Provenance

All assertions in this specimen bind to authorized public records documented in `provenance.jsonl`:
1. `prov.srow-public-companion-release`: Authoritative release archive of the SROW Public Companion (SHA-256: `0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181`).
2. `prov.public-srow-framework`: Public framework documentation on WinMedia.
