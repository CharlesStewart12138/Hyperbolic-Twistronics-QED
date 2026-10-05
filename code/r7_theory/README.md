# R7 executable certificate source

This directory contains the exact-rational R7 operational-margin verifier and its executable tests. Manuscript-oriented theorem specifications and TeX figure sources are excluded from this scientific-computation release.

Run the source-only certificate replay from the repository root:

```bash
python reproduce.py r7-certificate
python reproduce.py test r7
```

Generated certificates are written under `outputs/r7/`, not into the source tree.
