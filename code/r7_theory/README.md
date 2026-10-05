# R7 theory and certificate source

This directory contains the current R7 theorem specifications, the exact-rational operational-margin verifier, and the TeX source for the R7 explanatory figures.

Run the source-only certificate replay from the repository root:

```bash
python reproduce.py r7-certificate
python reproduce.py test r7
```

Generated certificates are written under `outputs/r7/`, not into the source tree. The theorem specifications document the infinite-volume non-Bloch formulation and its certified finite-approximation statements; they are source documents, not generated manuscript output.
