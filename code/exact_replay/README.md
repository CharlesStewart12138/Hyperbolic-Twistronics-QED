# Complete exact-replay source layer

This directory preserves the full retained source required to replay the electronic-physics project's large finite-group and hyperbolic-geometry computations.

Included source families:

- all GAP jobs for exact finite-group, subgroup, quotient, and permutation-representation calculations;
- all Unix shell shard launchers, time/memory limits, retry and recovery orchestration;
- PowerShell launch/build helpers;
- all retained C/C++ enumerators and high-performance geometric/group search programs;
- the associated Python controllers and small configuration sources required by those launchers.

This layer is intentionally isolated from the current import path. Use `../production_code`, `../validation_code`, `../r6_physics`, and `../r7_theory` for current work. Use this directory only when reproducing the original large sharded exact computations.

Many replay scripts retain their original relative layout and machine-oriented launch parameters. Before a new run, set the workspace, GAP executable, compiler, scratch, memory, and scheduler paths for the target machine. Large generated buckets and frozen binary tables are not bundled.
