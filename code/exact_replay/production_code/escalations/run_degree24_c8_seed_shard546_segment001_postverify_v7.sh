#!/usr/bin/env bash
set -euo pipefail
ulimit -v 50331648
exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q /mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard546_segment001_unit1_915_postverify_v7_gpt56sol.g
