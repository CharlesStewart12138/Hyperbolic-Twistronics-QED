# R6 numerical physics

This directory contains the current R6 non-Bloch numerical implementation.

Included:

- sparse local and periodic operator builders;
- KPM, Lanczos, Green-function and time-evolution routines;
- current R6 campaign and figure builders;
- convergence and control calculations;
- a deterministic reduced demo and unit tests;
- current YAML/JSON parameter definitions and the small R5 certificate.

Excluded from the source repository:

- checkpoints and pre-repair copies;
- HDF5/JSON numerical outputs;
- rendered figures and captions;
- logs, reports and machine-specific execution records;
- the large universal-cover archive and Q* binary tables.

Run the source-only path with:

```bash
python reproduce.py r6-demo
python reproduce.py test r6
```

For an exact production campaign, provide the external inputs under
`code/r6_physics/00_FROZEN_INPUTS/` or set `R6_UNIVERSAL_COVER`,
`R6_QSTAR_TABLE`, `R6_QSTAR_MANIFEST`, and `R6_R5_CERTIFICATE`.
The production code root defaults to the repository's `code/` directory and
can be overridden with `R6_SOURCE_CODE_ROOT`.
