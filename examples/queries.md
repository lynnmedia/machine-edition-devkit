# Three specimen queries (Developer Kit v0.1.0)

The three queries below run against the CC BY 4.0 SROW public reference specimen. They return stored records; they do not infer new claims. First install the kit as shown in the [README](../README.md).

| Question | Command | Deterministic result |
| --- | --- | --- |
| Which unit describes the stable-ID algorithm? | `.venv/bin/python -m machine_edition_devkit.queries run Q005` | `Stable-ID Algorithm Invariant` |
| What relationship leaves that unit? | `.venv/bin/python -m machine_edition_devkit.queries run Q012` | `derives_from` |
| Which public source identifies a specimen unit? | `.venv/bin/python -m machine_edition_devkit.queries run Q015` | `https://winmedia.com/frameworks/srow` |

The complete, bounded query definitions and expected values are in [`queries/sample_queries.json`](../queries/sample_queries.json). The query runner compares actual and expected values and prints `PASS` or `FAIL`; run all 20 with `.venv/bin/python -m machine_edition_devkit.queries run-all`.

Rights: example text and code are MIT; referenced SROW specimen content is CC BY 4.0 within the public companion scope. See [`RIGHTS.md`](../RIGHTS.md).
