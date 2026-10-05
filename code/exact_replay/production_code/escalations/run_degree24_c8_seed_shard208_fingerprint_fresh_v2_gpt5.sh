#!/usr/bin/env bash
set -euo pipefail
ulimit -v 50331648
exec /usr/bin/time -v gap -q /mnt/d/work/revise/production_code/escalations/gap_audit_degree24_c8_seed_shard208_fresh_v2_gpt5.g
