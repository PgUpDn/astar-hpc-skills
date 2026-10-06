#!/bin/bash
# Replace every REPLACE_* value. Create logs/ BEFORE sbatch.
#SBATCH --account=REPLACE_ACCOUNT
#SBATCH --partition=REPLACE_PARTITION
#SBATCH --job-name=research-gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=14
#SBATCH --mem=64G
#SBATCH --time=00:30:00
#SBATCH --gres=gpu:1
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -euo pipefail
: "${SLURM_JOB_ID:?Run within a Slurm allocation}"
cd "${SLURM_SUBMIT_DIR:?Missing submission directory}"
# Set a literal path or export ACRC_PROJECT_DIR before submission.
: "${ACRC_PROJECT_DIR:?Set the approved project storage path}"
[[ -d "$ACRC_PROJECT_DIR" ]] || { echo 'Project storage missing' >&2; exit 2; }
# Inspect the actual project quota; filesystem free space is not a reservation.
df -h "$ACRC_PROJECT_DIR"
umask 077
export TMPDIR
TMPDIR=$(mktemp -d "/tmp/research-${SLURM_JOB_ID}.XXXXXX")
export SRUN_CPUS_PER_TASK="$SLURM_CPUS_PER_TASK"
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export PYTHONUNBUFFERED=1
printf 'job=%s host=%s cpus=%s\n' "$SLURM_JOB_ID" "$(hostname)" "$SLURM_CPUS_PER_TASK"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
# Add verified module/environment setup. Preserve scheduler GPU bindings.
# Save durable outputs in project storage, not TMPDIR.
# Replace with the workload and its arguments; nonzero exits propagate.
exec srun --cpus-per-task="$SLURM_CPUS_PER_TASK" ./REPLACE_EXECUTABLE
