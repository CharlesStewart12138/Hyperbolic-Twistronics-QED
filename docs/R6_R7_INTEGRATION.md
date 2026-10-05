# R6 and R7 integration

## R6 numerical physics

`code/r6_physics/` contains the current infinite/local operator builders, observables, propagation and spectral routines, campaign orchestration, HPC launch source, frozen small configuration, tests, and a deterministic data-free demonstration.

The source release omits the large Q* generator table and universal-cover archive. Supply them without editing source by setting:

- `R6_QSTAR_TABLE`
- `R6_QSTAR_MANIFEST`
- `R6_UNIVERSAL_COVER`
- `R6_FROZEN_ROOT` (optional common override)
- `R6_SOURCE_CODE_ROOT` (optional code-root override)

The reduced demonstration validates code paths only and sets `production_claim` to `false`.

## R7 theorem/certificate layer

`code/r7_theory/` contains the theorem specifications, exact-rational magic-margin verifier, and source TeX for the R7 explanatory figures. Generated certificates go to `outputs/r7/`.

```bash
python reproduce.py test r6
python reproduce.py r6-demo
python reproduce.py test r7
python reproduce.py r7-certificate
```
