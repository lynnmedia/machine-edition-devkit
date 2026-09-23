# Five representations of publication content (Developer Kit v0.1.0)

These are common affordances, not accuracy or speed rankings. Any of these representations can be enriched with IDs, links, and provenance. The SROW specimen shows one concrete Machine Edition implementation under [Specification v0.1](https://winmedia.com/machine-editions/specification/v0.1).

| Representation | Natural unit | Strong fit | What the publisher must add for claim-level inspection |
| --- | --- | --- | --- |
| PDF | Page and visual span | Fixed layout and citation by page | Stable claim IDs, machine-readable relationships, and source bindings |
| EPUB | Document, section, and XHTML element | Reflowable human reading and navigable structure | Stable semantic units, explicit boundaries, and claim provenance |
| RAG chunks | Retrieved text segment | Search over an existing corpus with low conversion effort | Meaning-preserving segment boundaries and traceable assertions; retrieval alone does not supply them |
| Knowledge graph | Node and edge | Entity and relationship traversal across sources | Publication scope, source authority, text-level evidence, and a governed package boundary |
| Machine Edition v0.1 | Typed meaning unit and related records | Inspection of a governed publication package with explicit provenance and validation | The editorial work of producing and reviewing those records |

A knowledge graph can be part of a Machine Edition, and RAG can index one. The differences above describe what each representation carries by default in this comparison. They do not show that one format produces more truthful answers. For the controlled four-format trial and its limits, see the [representation comparison](../docs/rag-comparison.md).

Rights: this comparison text is MIT licensed. The referenced SROW specimen is CC BY 4.0 within the public companion scope. See [`RIGHTS.md`](../RIGHTS.md).
