# Reproducibility workflow

## Environment

Use Python 3.11 and install `requirements.txt` or `environment.yml`.

```bash
python reproduce.py doctor
python reproduce.py audit
python tools/audit_release.py
```

The current Python import root is `code/`; `code/exact_replay/` is deliberately excluded from imports so frozen replay modules cannot shadow current R4--R7 code.

## Source-only checks

```bash
python reproduce.py test validation
python reproduce.py test r6
python reproduce.py r6-demo
python reproduce.py test r7
python reproduce.py r7-certificate
```

The R6 demonstration uses a deterministic nine-site patch and explicitly reports `production_claim: false`. The R7 certificate uses exact rational arithmetic and writes generated JSON under `outputs/r7/`.

## Frozen production configuration

Begin with:

```text
code/production_code/config/model.yaml
code/production_code/config/production_reference.yaml
code/r6_physics/00_FROZEN_INPUTS/config/
```

For an exact current R6 replay, provide the large external inputs using:

```text
R6_QSTAR_TABLE
R6_QSTAR_MANIFEST
R6_UNIVERSAL_COVER
R6_FROZEN_ROOT       (optional common root)
R6_SOURCE_CODE_ROOT  (optional code root)
```

## Complete GAP/shell/C++ replay layer

The full retained exact-replay source is under `code/exact_replay/`. It contains every retained GAP shard, `.sh` launcher, PowerShell helper, C/C++ enumerator, Python recovery controller, and associated small configuration file. This layer is included for exhaustive reconstruction and is not imported by the current Python package.

Replay order is encoded by the launcher families themselves. Before execution, configure the target machine's GAP packages, compiler/GMP/MPFR paths, scheduler, scratch directories, memory limits, and workspace root. Generated buckets and large binary registries must be recreated or restored externally.

## Exact and reduced runs

A reduced run may lower search depth, shard count, candidate range, or plot resolution. It tests implementation and qualitative behavior but is not an exact frozen certificate.

An exact production run must use the frozen configuration, exhaust every registered shard/search range, preserve exact arithmetic, and pass production validation gates. The source package intentionally contains no precomputed scientific result.
