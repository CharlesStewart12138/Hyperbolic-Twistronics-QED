# CM-AUTO-001 bounded Bolza canonical engine

## Result

The exact breadth-first canonical interface is certified through physical
geometric word length 6.  It contains **155,577**
distinct exact SU(1,1) matrices and reproduces the frozen shell and ball counts.

Canonical order is minimum physical-geometric word length followed by
`g0<...<g7`.  Equality uses normalized algebraic matrices, never rounded disk
coordinates.

| Regression | Result |
|---|---|
| `shell_counts_exact` | PASS |
| `ball_counts_exact` | PASS |
| `shortlex_first_discovery_unique_in_certified_domain` | PASS |
| `inverse_pairing_exact` | PASS |
| `registered_surface_relator_exact` | PASS |
| `generator_inverse_products_exact` | PASS |
| `exact_orbit_coordinate_inputs` | PASS |
| `physical_degree_eight` | PASS |
| `C8_action_exact` | PASS |
| `physical_shell_nielsen_transport_exact` | PASS |
| `physical_shell_parity_odd` | PASS |
| `deterministic_repeat_prefix` | PASS |

## Scope boundary

GAP, KBMAG, SageMath and libgap are absent.  This task therefore does **not**
claim a complete automatic/geodesic language beyond depth 6.  It releases the
prefix-sharding infrastructure task, whose own acceptance must preserve
complete generation and exact per-shard accounting.  Deep proof searches and
the m=7 scientific run remain closed until their additional gates pass.

`main.tex` remains unchanged.
