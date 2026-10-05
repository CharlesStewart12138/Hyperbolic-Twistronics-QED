# Test matrix

The source-only release is continuously checked with:

| Layer | Command | Source-only expectation |
|---|---|---|
| All Python | `python reproduce.py audit` | Every packaged Python file parses |
| Independent validation | `python reproduce.py test validation` | Data-free tests pass; RUN-002 fixture tests skip until generated fixtures are supplied |
| R6 numerical physics | `python reproduce.py test r6` | Reduced operator tests pass; the exact Q* hash test skips until the large table is supplied |
| R7 theory certificate | `python reproduce.py test r7` | Exact-rational certificate tests pass |
| R6 smoke path | `python reproduce.py r6-demo` | Deterministic 18-dimensional reduced operator run |
| R7 certificate replay | `python reproduce.py r7-certificate` | Writes a PASS certificate with joint margin `1/48` |

The full `production` regression family is retained as source but is not a source-only CI target: many tests intentionally consume generated R4/R5 certificates, group registries, numerical arrays, and other large artifacts excluded from this repository. Restore or regenerate those inputs before running `python reproduce.py test production`.
