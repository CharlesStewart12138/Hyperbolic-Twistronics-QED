#!/bin/bash
#SBATCH --job-name=5203-r6
#SBATCH --array=1-9
#SBATCH --cpus-per-task=16
#SBATCH --mem=120G
#SBATCH --time=24:00:00
set -euo pipefail
JOB=$(awk -v n=$((SLURM_ARRAY_TASK_ID+1)) 'NR==n {print $0}' jobs.tsv)
echo "$JOB"
# Site-specific launcher intentionally left explicit: map JOB fields to the
# local_operator/KPM entry point after copying the frozen input manifest.
