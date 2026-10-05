# Hyperbolic Bilayer — complete electronic-physics source release

This GitHub-ready, source-only repository contains the complete retained code for the electronic-physics hyperbolic-bilayer project. It combines the current R4--R7 implementation with the full frozen exact-replay source needed for the large finite-group and hyperbolic-geometry computations.

Generated scientific results, rendered figures, PDFs, workbooks, caches, checkpoints, large binary registries, and Node.js files are excluded.

## Repository layout

- `code/production_code/`: current production geometry, group, kernel, Hodge, and streaming modules.
- `code/validation_code/`: independent validation implementations.
- `code/CONSTRUCTIVE_EXECUTION_R4/`: current exact quotient and construction code.
- `code/OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/`: current R5 constructive and proof-support checks.
- `code/r6_physics/`: current non-Bloch numerical operators, campaigns, convergence tools, and reduced tests.
- `code/r7_theory/`: exact magic-margin certificate, R7 figure sources, and theorem specifications.
- `code/exact_replay/`: complete frozen GAP jobs, shell shard launchers, recovery controllers, C/C++ enumerators, and their supporting source/configuration files.
- `code/manuscript_tools/`: newest paper and scientific-figure builders.
- `reproduce.py`: portable current-code command dispatcher.

The exact-replay layer is isolated so it cannot shadow the current R4--R7 Python modules. Its original script names and path conventions are retained because they encode the large sharded computations; see `code/exact_replay/README.md`.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python reproduce.py doctor
python reproduce.py audit
python reproduce.py test validation
python reproduce.py test r6
python reproduce.py test r7
python reproduce.py r6-demo
python reproduce.py r7-certificate
python tools/audit_release.py
```

The reduced R6 demo and R7 certificate do not require the excluded large registries. Exact production and replay runs require regenerating or externally supplying their declared group tables and universal-cover data; see `docs/REPRODUCIBILITY.md`.

## External tools

Exact stages additionally require GAP and its named packages, a C++20 compiler with GMP/MPFR where indicated, and a LaTeX/Poppler toolchain for source figure builds.

## Release policy

The three per-file TSV inventories (`ENTRYPOINTS.tsv`, `SOURCE_MANIFEST.tsv`, and `PACKAGE_MANIFEST.tsv`) are intentionally not distributed. Release integrity is provided by the SHA-256 sidecar for the final ZIP. `RELEASE_AUDIT.json` contains only aggregate content checks and no per-file inventory.

## License

No license has been selected automatically. Choose and add a public license before publishing; see `LICENSE_PENDING.md`.
